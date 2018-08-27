"""
Test for `tns run android` command.

Run should sync all the changes correctly:
 - Valid changes in CSS, JS, XML should be applied.
 - Invalid changes in XML should be logged in the console and lives-sync should continue when XML is fixed.
 - Hidden files should not be synced at all.
 - --syncAllFiles should sync changes in node_modules
 - --justlaunch should release the console.

If emulator is not started and device is not connected `tns run android` should start emulator.
"""

import datetime
import os
import re
import time
import unittest

import nose
import pytz

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_PACKAGE, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, EMULATOR_NAME, CURRENT_OS, TEST_RUN_HOME
from tests.helpers.livesync_helper import LivesyncHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunAndroidEmulatorTests(BaseClass):
    source_app = os.path.join(TEST_RUN_HOME, BaseClass.app_name)
    temp_app = os.path.join(TEST_RUN_HOME, 'data', BaseClass.app_name)
    one_hundred_symbols_string = "123456789012345678901234567890123456789012345678901234567890" \
                                 "1234567890123456789012345678901234567890"
    very_long_string = ''
    for x in range(0, 30):
        very_long_string = very_long_string + one_hundred_symbols_string

    max_long_string = ''
    for x in range(0, 10):
        max_long_string = max_long_string + one_hundred_symbols_string
    max_long_string = max_long_string + "123456789012345678901234"

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.kill()
        Emulator.stop()
        Emulator.ensure_available()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_PACKAGE})

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)
        Folder.cleanup('TestApp')
        Folder.cleanup('TestApp2')

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()  # We need this because of test_400_tns_run_android_respect_adb_errors
        Folder.cleanup(cls.temp_app)

    def test_001_tns_run_android_js_css_xml_manifest(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Change JS and wait until app is synced
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=20)
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Change XML and wait until app is synced
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
        assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js-js-css-xml')

        # Rollback all the changes
        LivesyncHelper.rollback(self.app_name, LivesyncHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        LivesyncHelper.rollback(self.app_name, LivesyncHelper.CHANGE_CSS, sleep=10)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180)

        LivesyncHelper.rollback(self.app_name, LivesyncHelper.CHANGE_XML, sleep=10)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Changes in App_Resources should rebuild native project
        res_path = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'src', 'main', 'AndroidManifest.xml')
        File.replace(res_path, '17', '19')
        strings = ['Preparing project', 'Building project', 'Gradle build', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=60)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    def test_100_tns_run_android_release(self):
        """Make valid changes in JS,CSS and HTML"""

        # `tns run android --release` and wait until app is deployed
        # IMPORTANT NOTE: `tns run android --release` Do NOT livesync by design!
        copy = os.path.join(TEST_RUN_HOME,'data', 'folders', 'main-page.js')
        paste = os.path.join(self.app_name, 'app')
        Folder.copy(copy, paste)
        Device.uninstall_app(app_prefix="org.nativescript", platform=Platform.ANDROID)
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          '--device': EMULATOR_ID,
                                          '--keyStorePath': ANDROID_KEYSTORE_PATH,
                                          '--keyStorePassword': ANDROID_KEYSTORE_PASS,
                                          '--keyStoreAlias': ANDROID_KEYSTORE_ALIAS,
                                          '--keyStoreAliasPassword': ANDROID_KEYSTORE_ALIAS_PASS,
                                          '--release': ''}, wait=False, assert_success=False)

        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=150, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='hello-world-js')

        # Kills `tns run android --release`
        Tns.kill()

        # Replace files
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_JS)
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_CSS)
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_XML)

        # Run `tns run android --release` again and make sure changes above are applied
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          '--device': EMULATOR_ID,
                                          '--keyStorePath': ANDROID_KEYSTORE_PATH,
                                          '--keyStorePassword': ANDROID_KEYSTORE_PASS,
                                          '--keyStoreAlias': ANDROID_KEYSTORE_ALIAS,
                                          '--keyStoreAliasPassword': ANDROID_KEYSTORE_ALIAS_PASS,
                                          '--release': ''}, wait=False, assert_success=False)

        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier',
                   'Successfully started on device with identifier', EMULATOR_ID]

        # https://github.com/NativeScript/android-runtime/issues/1024
        not_existing_log = ['JS:']
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_log, timeout=120,
                         clean_log=False)

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js-js-css-xml')

    def test_180_tns_run_android_console_logging(self):
        """
         Test console info, warn, error, assert, trace, time and logging of different objects.
        """

        # Change main-page.js so it contains console logging
        source_js = os.path.join('data', 'console-log', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application',
                   "true",
                   "false",
                   "null",
                   "undefined",
                   "-1",
                   "text",
                   "\"name\": \"John\",",
                   "\"age\": 34",
                   "number: -1",
                   "string: text",
                   "text -1",
                   "info",
                   "warn",
                   "error",
                   "Assertion failed:  false == true",
                   "Assertion failed:  empty string evaluates to 'false'",
                   "Trace: console.trace() called",
                   "Button(",
                   "-1 text {",
                   "[1, 5, 12.5, {", "\"name\": \"John\",",
                   "\"age\": 34",
                   "}, text, 42]",
                   "Time:",
                   self.max_long_string,
                   "### TEST END ###"
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        assert "1 equals 1" not in log
        assert self.very_long_string not in log

    def test_181_tns_run_android_console_dir(self):
        """
         Test console.dir() of different objects.
        """

        # Change main-page.js so it contains console logging
        source_js = os.path.join('data', 'console-dir', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application',
                   "true",
                   "false",
                   "null",
                   "undefined",
                   "-1",
                   "text",
                   "==== object dump start ====",
                   "name: \"John\"",
                   "age: \"34\"",
                   "==== object dump end ====",
                   self.max_long_string
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        assert self.very_long_string not in log

    @unittest.skip("Problems with CI")
    def test_182_tns_run_android_new_date_work_as_expected_when_changing_timezone(self):
        """
         Test new date is working as expected. Test in different timezones
        """
        output = Adb.run("shell settings put global auto_time_zone 0", EMULATOR_ID)
        assert '' in output, "Failed to change auto timezone!"

        output = Adb.run("shell settings put system time_12_24 24", EMULATOR_ID)
        assert '' in output, "Failed to change system format to 24!"

        output = Adb.run("shell settings put global time_zone UTC", EMULATOR_ID)
        assert '' in output, "Failed to change timezone!"
        output = Adb.run("shell setprop persist.sys.timezone UTC", EMULATOR_ID)
        assert '' in output, "Failed to change timezone!"

        # Change main-page.js so it contains only logging information
        source_js = os.path.join('data', "issues", 'android-runtime-961', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)
        # Change main-view-model.js so it contains the new date logging functionality
        source_js = os.path.join('data', "issues", 'android-runtime-961', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)
        # Change app package.json so it contains the options for remove V8 date cache
        source_js = os.path.join('data', "issues", 'android-runtime-961', 'package.json')
        target_js = os.path.join(self.app_name, 'app', 'package.json')

        File.copy(src=source_js, dest=target_js)

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)

        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application',
                   "### TEST END ###"
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        # Get UTC date and time
        time_utc = datetime.datetime.utcnow()

        # Generate regex for asserting date and time
        date_to_find_gmt = time_utc.strftime('%a %b %d %Y %H:.{2}:.{2}') + " GMT\+0000 \(UTC\)"

        Device.click(device_id=EMULATOR_ID, text="TAP", timeout=30)
        Tns.wait_for_log(log_file=log, string_list=["GMT+0000 (UTC)"], timeout=180, check_interval=10, clean_log=False)

        # Assert date time is correct
        if re.search(date_to_find_gmt, str(file.read(file(log)))):
            print "Date was correct!"
        else:
            assert 1 == 2, 'Date {0} was not found! \n Log: \n {1}'.format(date_to_find_gmt, file.read(file(log)))

        # Get Los Angeles date and time
        los_angeles_time = time_utc.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("America/Los_Angeles"))

        # Open Date and time settings to change the timezone
        output = Adb.run("shell am start -a android.settings.DATE_SETTINGS", EMULATOR_ID)
        assert 'Starting: Intent { act=android.settings.DATE_SETTINGS }' in output, \
            "Failed to start Date and Time settings activity!"

        # Change TimeZone
        time.sleep(20)
        Device.click(device_id=EMULATOR_ID, text="Select time zone", timeout=15)
        time.sleep(25)
        Device.click(device_id=EMULATOR_ID, text="Pacific Daylight Time", timeout=60)
        time.sleep(10)

        # Open the test app again
        output = Adb.run("shell am start -n org.nativescript.TestApp/com.tns.NativeScriptActivity", EMULATOR_ID)
        assert 'Starting: Intent { cmp=org.nativescript.TestApp/com.tns.NativeScriptActivity }' in output, \
            "Failed to start Nativescript test app activity!"

        time.sleep(15)

        Device.click(device_id=EMULATOR_ID, text="TAP", timeout=30)
        Tns.wait_for_log(log_file=log, string_list=["GMT-0700 (PDT)"], timeout=180, check_interval=10,
                         clean_log=False)
        # Generate regex for asserting date and time
        date_to_find_los_angeles = los_angeles_time.strftime('%a %b %d %Y %H:.{2}:.{2}') + " GMT\-0700 \(PDT\)"

        # Assert date time is correct
        if re.search(date_to_find_los_angeles, str(file.read(file(log)))):
            print "Date was correct!"
        else:
            assert 1 == 2, 'Date {0} was not found! \n Log: \n {1}'.format(date_to_find_los_angeles,
                                                                           file.read(file(log)))

    def test_200_tns_run_android_break_and_fix_app(self):
        """
        Make changes in xml that break the app and then changes that fix the app.
        Add/remove js files that break the app and then fix it.
        """
        copy = os.path.join(TEST_RUN_HOME, 'data', 'folders', 'main-page.js')
        paste = os.path.join(self.app_name, 'app')
        Folder.copy(copy, paste)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Break the app with invalid xml changes
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_XML_INVALID_SYNTAX)

        # Verify console notify user for broken xml
        strings = ['main-page.xml has syntax errors', 'unclosed xml attribute',
                   'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)
        assert Adb.wait_for_text(device_id=EMULATOR_ID, text="Exception", timeout=30), "Error activity not found!"

        # Revert changes
        LivesyncHelper.rollback(self.app_name, LivesyncHelper.CHANGE_XML_INVALID_SYNTAX)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Delete app.js and verify app crash with error activiry dialog
        app_js_original_path = os.path.join(self.app_name, 'app', 'app.js')
        app_js_new_path = os.path.join(TEST_RUN_HOME, 'app.js')
        File.copy(src=app_js_original_path, dest=app_js_new_path)
        File.remove(file_path=app_js_original_path)
        strings = ['Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=30, check_interval=10)
        assert Adb.wait_for_text(device_id=EMULATOR_ID, text="Exception", timeout=30), "Error activity not found!"

        # Restore js file and verify app
        File.copy(src=app_js_new_path, dest=app_js_original_path)
        verify_app_loaded = 'JS: Page loaded'
        strings = ['Successfully synced application', 'app.js', EMULATOR_ID, verify_app_loaded]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=30, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    def test_210_run_android_add_remove_files_and_folders(self):
        """
        New files and folders should be synced properly.
        """

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Add new files
        new_file_name = 'main-page2.xml'
        source_file = os.path.join(self.app_name, 'app', 'main-page.xml')
        destination_file = os.path.join(self.app_name, 'app', new_file_name)
        File.copy(source_file, destination_file)
        strings = ['Successfully transferred main-page2.xml', 'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new file is synced and available on device.
        error_message = 'Newly created file {0} not found on {1}'.format(new_file_name, EMULATOR_ID)
        app_id = Tns.get_app_id(app_name=self.app_name)
        path = 'app/{0}'.format(new_file_name)
        assert Adb.path_exists(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Revert changes(rename file and delete file)
        File.copy(destination_file, source_file)
        File.remove(destination_file)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new file is synced and available on device.
        error_message = '{0} was deleted, but still available on {1}'.format(new_file_name, EMULATOR_ID)
        assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Add folder
        new_folder_name = 'test2'
        source_file = os.path.join(TEST_RUN_HOME, 'data', 'folders', 'test')
        destination_file = os.path.join(self.app_name, 'app', new_folder_name)
        Folder.copy(source_file, destination_file)
        strings = ['Successfully transferred test.txt', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is synced and available on device.
        error_message = 'Newly created folder {0} not found on {1}'.format(new_folder_name, EMULATOR_ID)
        path = 'app/{0}'.format(new_folder_name)
        assert Adb.path_exists(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Delete folder
        if CURRENT_OS == OSType.OSX:
            # Due to unknown reason this fails on Linux and Windows
            # It might be related to https://github.com/NativeScript/nativescript-cli/issues/2657.
            Folder.cleanup(destination_file)
            strings = ['Successfully synced application', EMULATOR_ID]
            Tns.wait_for_log(log_file=log, string_list=strings)

            # Verify new folder is synced and available on device.
            error_message = 'Deleted folder {0} is still available on {1}'.format(new_folder_name, EMULATOR_ID)
            assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_290_tns_run_android_should_refresh_images(self):
        """Test for https://github.com/NativeScript/nativescript-cli/issues/2981"""

        # Ensure app with image
        run("cp -R data/issues/nativescript-cli-2981/* " + self.app_name + "/app/")
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image='issue_2981_logo_image',
                            tolerance=3.0, timeout=30)

        # Change the image
        old_image = os.path.join(self.app_name, 'app', 'img', 'logo.png')
        new_image = os.path.join(self.app_name, 'app', 'img', 'icon.png')
        File.copy(src=new_image, dest=old_image)
        Tns.wait_for_log(log_file=log, string_list=['Successfully transferred', 'Successfully synced application'])

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image='issue_2981_icon_image',
                            tolerance=3.0, timeout=30)

    def test_300_tns_run_android_just_launch_and_incremental_builds(self):
        """
        This test verify following things:
        1. `--justlaunch` option release the console.
        2. Prepare is not triggered if no changed are done.
        3. Incremental prepare is triggered if js, xml and css files are changed.
        """

        # Execute `tns run android --path TNS_App --justlaunch` and verify app looks correct on emulator
        Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''})
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Execute `tns run android --path TNS_App --justlaunch` again
        # without any changes on app under test and verify incremental prepare works
        output = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''},
                                 assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.SKIP)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Replace JS, XML and CSS files
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_JS)
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_CSS)
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_XML)

        # Run `tns run android` after file changes (this should trigger incremental prepare).
        output = Tns.run_android(attributes={'--path': self.app_name, '--justlaunch': ''}, assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.ANDROID, output=output,
                            prepare=Prepare.INCREMENTAL)

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js-js-css-xml')

    def test_310_tns_run_android_clean_builds(self):
        """
        * --clean - If set, forces rebuilding the native application.
        """

        Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''})

        # Verify `--clean` without any changes skip prepare and rebuild native project (and runs properly)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID,
                                          '--justlaunch': '', '--clean': ''})
        assert 'Skipping prepare' in log, "Prepare NOT skipped when no files are changed and `tns run android --clean`"
        assert 'Building project...' in log, "Full rebuild not triggered when --clean is used"
        assert 'Gradle build' in log, "Full rebuild not triggered when --clean is used"

        Device.wait_for_text(device_id=EMULATOR_ID, text='42 taps left')

        # Verify if changes are applied and then build with `--clean` it will apply changes on attached device
        LivesyncHelper.replace(self.app_name, LivesyncHelper.CHANGE_JS)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID,
                                          '--justlaunch': '', '--clean': ''})
        assert 'Skipping prepare' not in log, "Prepare skipped when change files and run `tns run android --clean`"
        assert 'Gradle build' in log, "Full rebuild not triggered when --clean is used"

        Device.wait_for_text(device_id=EMULATOR_ID, text='52 taps left')

        # Verify if changes are applied and then build with `--clean` it will apply changes on attached device
        LivesyncHelper.rollback(self.app_name, LivesyncHelper.CHANGE_JS)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID,
                                          '--justlaunch': '', '--clean': ''})
        assert 'Skipping prepare' not in log
        assert 'Gradle build' in log, "Full rebuild not triggered when --clean is used"

        Device.wait_for_text(device_id=EMULATOR_ID, text='42 taps left')

    def test_315_tns_run_android_change_appResources_check_per_platform(self):
        # https://github.com/NativeScript/nativescript-cli/pull/3619
        output = Tns.run_android(attributes={'--path': self.app_name}, wait=False, assert_success=False)
        strings = ['Successfully installed on device with identifier',
                   'Successfully synced application', EMULATOR_ID, ]
        Tns.wait_for_log(log_file=output, string_list=strings, timeout=120, check_interval=10)

        source = os.path.join('data', 'issues', 'nativescript-cli-3619', 'hello.png')
        target = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'drawable-hdpi')
        File.copy(source, target)
        strings = ['Gradle build']
        Tns.wait_for_log(log_file=output, string_list=strings, clean_log=False)
        assert "Xcode build" not in output

    def test_320_tns_run_android_no_watch(self):
        """
         * --no-watch - If set, changes in your code will not be reflected during the execution of this command.
        """

        # `tns run android --no-watch` and wait until app is deployed
        copy = os.path.join(TEST_RUN_HOME, 'data', 'folders', 'main-page.js')
        paste = os.path.join(self.app_name, 'app')
        Folder.copy(copy, paste)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--no-watch': ''},
                              wait=False, assert_success=False)
        strings = ['Successfully installed on device with identifier',
                   'Successfully synced application',
                   EMULATOR_ID,  # Verify device id
                   'JS:']  # Verify console log messages are shown.
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Add new files
        new_file_name = 'main-page3.xml'
        old_file_name = 'main-page.xml'
        source_file = os.path.join(self.app_name, 'app', old_file_name)
        destination_file = os.path.join(self.app_name, 'app', new_file_name)
        File.copy(source_file, destination_file)
        time.sleep(20)  # Give it some time to sync the changes

        # Verify new file is synced and available on device.
        error_message = 'Newly created file {0} found on {1}'.format(new_file_name, EMULATOR_ID)
        app_id = Tns.get_app_id(app_name=self.app_name)
        new_file_path = 'app/{0}'.format(new_file_name)
        old_file_path = 'app/{0}'.format(old_file_name)
        assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=new_file_path), error_message
        assert not Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=old_file_path)
        # Last line is just to be very sure we have no bug in Adb.path_does_not_exist()

    def test_330_tns_run_android_sync_all_files(self):
        """
        Verify '--syncAllFiles' option will sync all files, including node modules.
        """
        copy = os.path.join(TEST_RUN_HOME, 'data', 'folders', 'main-page.js')
        paste = os.path.join(self.app_name, 'app')
        Folder.copy(copy, paste)
        Tns.build_android(attributes={'--path': self.app_name})
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--syncAllFiles': ''},
                              wait=False, assert_success=False)
        strings = ['Successfully synced application', EMULATOR_ID, 'JS:']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=60, check_interval=10)

        LivesyncHelper.replace(app_name=self.app_name, file_change=LivesyncHelper.CHANGE_TNS_MODULES)

        strings = ['Successfully transferred application-common.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Delete log during livesync not possible on Windows.")
    def test_340_tns_run_should_not_sync_hidden_files(self):
        """
        Adding hidden files should not break run and they should not be transferred.
        """

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        # Clean log (this will not work on windows since file is locked)
        File.write(file_path=log, text="")

        # Add some hidden files
        source_file = os.path.join(self.app_name, 'app', 'main-page.xml')
        destination_file = os.path.join(self.app_name, 'app', '.tempfile')
        File.copy(source_file, destination_file)

        # Give it 5 sec and check no messages are available in log files
        time.sleep(5)
        output = File.read(log)

        print ""
        print "LOG AFTER HIDDEN FILE ADDED:"
        print ""
        print output
        print ""

        assert 'Successfully' not in output, 'Sync is triggered after adding hidden file.'
        assert 'synced' not in output, 'Sync is triggered after adding hidden file.'
        assert 'tempfile' not in output, 'Sync is triggered after adding hidden file.'
        assert EMULATOR_ID not in output, 'Sync is triggered after adding hidden file.'

        # Verify hidden file does not exists on mobile device.
        path = 'app/{0}'.format('.tempfile')
        app_id = Tns.get_app_id(self.app_name)
        error_message = 'Hidden file {0} is transferred to {1}'.format(path, EMULATOR_ID)
        assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    def test_350_tns_run_android_should_start_emulator(self):
        """
        `tns run android` should start emulator if device is not connected.
        """
        count = Device.get_count(platform=Platform.ANDROID)
        if count == 0:
            Emulator.stop()
            Tns.build_android(attributes={'--path': self.app_name})
            log = Tns.run_android(attributes={'--path': self.app_name}, wait=False, assert_success=False)
            strings = ['Starting Android emulator with image']
            Tns.wait_for_log(log_file=log, string_list=strings, timeout=120)
            Emulator.stop()
            Emulator.ensure_available()
        else:
            raise nose.SkipTest('This test is not valid when devices are connected.')
    #
    def test_355_tns_run_android_changes_in_app_resources_rebuild_app(self):
        """
        https://github.com/NativeScript/nativescript-cli/issues/3658
        In case when some change occurs in App_Resources/iOS and tns run android command is executed,
        the application is fully rebuild when it should not.
        """

        # Run app twice and check the second time it's not rebuild
        log1 = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                               assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log1, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        log2 = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                               assert_success=False)
        strings_skipping_prepare = ['Skipping prepare', 'Refreshing application',
                                    'Successfully synced application']
        Tns.wait_for_log(log_file=log2, string_list=strings_skipping_prepare, timeout=180, check_interval=10,
                         clean_log=False)

        # Make change in App_Resources/iOS folder
        app_resources_file = os.path.join(self.app_name, "app", "App_Resources", "iOS", "Assets.xcassets",
                                          "Contents.json")
        file_to_change = os.path.join("data", "issues", "nativescript-cli-3658", "Contents.json")
        File.copy(file_to_change, app_resources_file)

        # Run again the app and ensure it's not rebuild
        log3 = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                               assert_success=False)
        Tns.wait_for_log(log_file=log3, string_list=strings_skipping_prepare, timeout=180, check_interval=10,
                         clean_log=False)
        assert 'Building project' not in log3, "Project is rebuilt when it should not."

    def test_360_tns_run_android_with_jar_file_in_plugin(self):
        """
        App should not crash when reference .jar file in some plugin
        https://github.com/NativeScript/android-runtime/pull/905
        """

        # Add .jar file in plugin and modify the app to reference it
        custom_jar_file = os.path.join('data', 'issues', 'android-runtime-pr-905', 'customLib.jar')
        modules_widgets = os.path.join(self.app_name, 'node_modules', 'tns-core-modules-widgets', 'platforms',
                                       'android')
        File.copy(src=custom_jar_file, dest=modules_widgets)

        source = os.path.join('data', 'issues', 'android-runtime-pr-905', 'app.js')
        target = os.path.join(self.app_name, 'app', 'app.js')
        File.copy(src=source, dest=target)

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    def test_370_tns_run_android_with_jar_and_aar_files_in_app_res(self):
        """
        App should not crash when reference .jar or/and .aar file in App_Resources/Android/libs
        https://github.com/NativeScript/android-runtime/issues/899
        """

        # Create libs/ in app/App_resources/, add .jar and .aar files in it and modify the app to reference them
        curr_folder = os.getcwd()
        Folder.navigate_to(os.path.join(self.app_name, 'app', 'App_Resources', 'Android'))
        Folder.create("libs")
        app_res_libs = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'libs')
        Folder.navigate_to(curr_folder)

        custom_jar_file = os.path.join('data', 'issues', 'android-runtime-pr-905', 'customLib.jar')
        custom_aar_file = os.path.join('data', 'issues', 'android-runtime-899', 'mylibrary.aar')

        File.copy(src=custom_jar_file, dest=app_res_libs)
        File.copy(src=custom_aar_file, dest=app_res_libs)

        source = os.path.join('data', 'issues', 'android-runtime-899', 'app.js')
        target = os.path.join(self.app_name, 'app', 'app.js')
        File.copy(src=source, dest=target)

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    def test_380_tns_run_android_livesync_aar_file_changes(self):
        """
        App should not crash when reference .jar or/and .aar file in App_Resources/Android/libs
        https://github.com/NativeScript/nativescript-cli/issues/3610
        """
        Tns.plugin_add("nativescript-camera", attributes={"--path": self.app_name})
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--syncAllFiles': ''},
                              wait=False,
                              assert_success=False)

        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

        copy_aar = os.path.join(TEST_RUN_HOME, 'data', 'plugins', 'TNSListView-release.aar')
        paste_aar = os.path.join(self.app_name, 'node_modules', 'nativescript-camera', 'platforms', 'android')

        File.copy(src=copy_aar, dest=paste_aar)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')

    @unittest.skip("Skip because of https://github.com/NativeScript/nativescript-cli/issues/2825")
    def test_390_tns_run_android_should_warn_if_package_ids_do_not_match(self):
        """
        If bundle identifiers in package.json and app.gradle do not match CLI should warn the user.
        """
        app_gradle = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'app.gradle')
        File.replace(file_path=app_gradle, str1='org.nativescript.' + self.app_name, str2='org.nativescript.MyApp')
        # File.replace(file_path=app_gradle, str1='__PACKAGE__', str2='org.nativescript.MyApp')
        assert "org.nativescript.MyApp" in File.read(app_gradle), "Failed to replace bundle identifier."

        output = Tns.run_android(attributes={'--path': self.app_name, '--justlaunch': ''})
        assert "The Application identifier is different from the one inside 'package.json' file." in output
        assert "NativeScript CLI might not work properly." in output
        assert "Project successfully built" in output

    @unittest.skipIf(CURRENT_OS == OSType.LINUX, "`shell cp -r` fails for some reason on emulators on Linux.")
    def test_400_tns_run_android_respect_adb_errors(self):
        """
        If disk is full adb error is thrown durring deploy, CLI should respect it
        """

        # Run the app to make sure we have something at /data/data/org.nativescript.TestApp
        Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''})

        # Use all the disk space on emulator
        for index in range(1, 1000):
            command = "shell cp -r /data/data/org.nativescript.TestApp /data/data/org.nativescript.TestApp" + str(index)
            output = Adb.run(device_id=EMULATOR_ID, command=command, log_level=CommandLogLevel.FULL)
            if "No space left on device" in output:
                break

        # Create new app
        Tns.create_app(app_name='TestApp2', update_modules=True)
        Tns.platform_add_android(attributes={'--path': 'TestApp2', '--frameworkPath': ANDROID_PACKAGE})

        # Run the app and verify there is appropriate error
        output = Tns.run_android(attributes={'--path': 'TestApp2', '--device': EMULATOR_ID, '--justlaunch': ''},
                                 assert_success=False)
        # Test for CLI issue 2170
        assert 'No space left on device' in output or "didn't have enough storage space" in output

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Delete log during livesync not possible on Windows.")
    def test_401_tns_run_android_should_not_continue_on_build_failure(self):
        """
        `tns run android` should start emulator if device is not connected.
        """
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_PACKAGE})
        File.replace(file_path=self.app_name + "/app/App_Resources/Android/app.gradle", str1="applicationId", str2="x")
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['FAILURE', 'Build failed with an exception', 'gradlew failed with exit code 1']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        time.sleep(10)
        output = File.read(file_path=log)
        assert "successfully built" not in output
        assert "Installing..." not in output
        assert "installed on device" not in output
        assert "synced" not in output

    def test_404_run_on_invalid_device_id(self):
        output = Tns.run_android(attributes={'--path': self.app_name, '--device': 'fakeId', '--justlaunch': ''},
                                 assert_success=False)
        TnsAsserts.invalid_device(output=output)
