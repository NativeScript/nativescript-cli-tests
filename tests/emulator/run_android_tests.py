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

import os
import time
import unittest

import nose

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_RUNTIME_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, EMULATOR_NAME, CURRENT_OS, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunAndroidEmulatorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.create_app(self.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)
        Folder.cleanup('TestApp2')

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()  # We need this because of test_400_tns_run_android_respect_adb_errors

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
                            expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=20)
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
        assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml')

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Changes in App_Resources should rebuild native project
        res_path = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'AndroidManifest.xml')
        File.replace(res_path, '17', '19')
        strings = ['Preparing project', 'Building project', 'Gradle build', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=60)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    def test_100_tns_run_android_release(self):
        """Make valid changes in JS,CSS and HTML"""

        # `tns run android --release` and wait until app is deployed
        # IMPORTANT NOTE: `tns run android --release` Do NOT livesync by design!
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
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

        # Kills `tns run android --release`
        Tns.kill()

        # Replace files
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML)

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
                   'Successfully started on device with identifier',
                   'JS:', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120)

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml')

    def test_200_tns_run_android_break_and_fix_app(self):
        """
        Make changes in xml that break the app and then changes that fix the app.
        Add/remove js files that break the app and then fix it.
        """

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Break the app with invalid xml changes
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML_INVALID_SYNTAX)

        # Verify console notify user for broken xml
        strings = ['main-page.xml has syntax errors', 'unclosed xml attribute',
                   'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Revert changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML_INVALID_SYNTAX)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

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
                            expected_image='livesync-hello-world_home')

    def test_210_tns_run_android_add_remove_files_and_folders(self):
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
                            expected_image='livesync-hello-world_home')

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
        source_file = os.path.join(self.app_name, 'app', 'test')
        destination_file = os.path.join(self.app_name, 'app', new_folder_name)
        Folder.copy(source_file, destination_file)
        strings = ['Successfully transferred test2', 'Successfully transferred test.txt', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is synced and available on device.
        error_message = 'Newly created folder {0} not found on {1}'.format(new_folder_name, EMULATOR_ID)
        path = 'app/{0}'.format(new_folder_name)
        assert Adb.path_exists(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Delete folder
        Folder.cleanup(destination_file)
        strings = ['Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Uncomment following lines after https://github.com/NativeScript/nativescript-cli/issues/2657 is fixed.

        # Verify new folder is synced and available on device.
        # error_message = 'Deleted folder {0} is still available on {1}'.format(new_folder_name, EMULATOR_ID)
        # assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    @unittest.skipIf(CURRENT_OS == OSType.LINUX, "Run only on macOS.")
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
                            expected_image='livesync-hello-world_home')

        # Execute `tns run android --path TNS_App --justlaunch` again
        # without any changes on app under test and verify incremental prepare works
        output = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''},
                                 assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.SKIP)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Replace JS, XML and CSS files
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML)

        # Run `tns run android` after file changes (this should trigger incremental prepare).
        output = Tns.run_android(attributes={'--path': self.app_name, '--justlaunch': ''}, assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.ANDROID, output=output,
                            prepare=Prepare.INCREMENTAL)

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml')

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
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID,
                                          '--justlaunch': '', '--clean': ''})
        assert 'Skipping prepare' not in log, "Prepare skipped when change files and run `tns run android --clean`"
        assert 'Gradle build' in log, "Full rebuild not triggered when --clean is used"

        Device.wait_for_text(device_id=EMULATOR_ID, text='52 taps left')

        # Verify if changes are applied and then build with `--clean` it will apply changes on attached device
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID,
                                          '--justlaunch': '', '--clean': ''})
        assert 'Skipping prepare' not in log
        assert 'Gradle build' in log, "Full rebuild not triggered when --clean is used"

        Device.wait_for_text(device_id=EMULATOR_ID, text='42 taps left')

    def test_320_tns_run_android_no_watch(self):
        """
         * --no-watch - If set, changes in your code will not be reflected during the execution of this command.
        """

        # `tns run android --no-watch` and wait until app is deployed
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
        Tns.build_android(attributes={'--path': self.app_name})
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--syncAllFiles': ''},
                              wait=False, assert_success=False)
        strings = ['Successfully synced application', EMULATOR_ID, 'JS:']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=60, check_interval=10)

        ReplaceHelper.replace(app_name=self.app_name, file_change=ReplaceHelper.CHANGE_TNS_MODULES)

        strings = ['Successfully transferred application-common.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

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
                            expected_image='livesync-hello-world_home')

        # Clean log (this will not work on windows since file is locked)
        if CURRENT_OS != OSType.WINDOWS:
            File.write(file_path=log, text="")
            time.sleep(1)

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
                            expected_image='livesync-hello-world_home')

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

    def test_360_tns_run_android_with_jar_file_in_plugin(self):
        """
        App should not crash when reference .jar file in some plugin
        https://github.com/NativeScript/android-runtime/pull/905
        """

        # Add .jar file in plugin and modify the app to reference it
        custom_jar_file = os.path.join('data', 'issues', 'android-runtime-pr-905', 'customLib.jar')
        modules_widgets = os.path.join(self.app_name, 'node_modules', 'tns-core-modules-widgets', 'platforms', 'android')
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
                            expected_image='livesync-hello-world_home')

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
        for index in range(1, 500):
            command = "shell cp -r /data/data/org.nativescript.TestApp /data/data/org.nativescript.TestApp" + str(index)
            output = Adb.run(device_id=EMULATOR_ID, command=command, log_level=CommandLogLevel.FULL)
            if "No space left on device" in output:
                break

        # Create new app
        Tns.create_app(app_name='TestApp2', update_modules=True)
        Tns.platform_add_android(attributes={'--path': 'TestApp2', '--frameworkPath': ANDROID_RUNTIME_PATH})

        # Run the app and verify there is appropriate error
        output = Tns.run_android(attributes={'--path': 'TestApp2', '--device': EMULATOR_ID, '--justlaunch': ''},
                                 assert_success=False)
        # Test for CLI issue 2170
        assert 'No space left on device' in output or "didn't have enough storage space" in output

    def test_401_tns_run_android_should_not_continue_on_build_failure(self):
        """
        `tns run android` should start emulator if device is not connected.
        """
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})
        File.replace(file_path=self.app_name + "/app/App_Resources/Android/app.gradle", str1="applicationId", str2="x")
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['FAILURE', 'Build failed with an exception', 'gradlew failed with exit code 1']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        time.sleep(10)
        output = File.read(file_path=log)
        assert "successfully built" not in output
        assert "installed" not in output
        assert "synced" not in output

    def test_404_run_on_invalid_device_id(self):
        output = Tns.run_android(attributes={'--path': self.app_name, '--device': 'fakeId', '--justlaunch': ''},
                                 assert_success=False)
        TnsAsserts.invalid_device(output=output)
