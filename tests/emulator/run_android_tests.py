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

import nose

from core.base_class.BaseClass import BaseClass
from core.device.adb import Adb
from core.device.device import Device
from core.device.device_type import DeviceType
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import ANDROID_RUNTIME_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, EMULATOR_NAME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunAndroidEmulatorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.create_app(self.app_name, attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world')},
                       update_modules=True)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

    def tearDown(self):
        Process.kill('node')  # Stop 'node' to kill the livesync after each test method.
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def test_001_tns_run_android_js_css_xml_manifest(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Adb.wait_for_text(device_id=EMULATOR_ID, text='clicks', timeout=20)
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Adb.wait_for_text(device_id=EMULATOR_ID, text='TEST')
        assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_js_css_xml')

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
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

        # Changes in App_Resources should rebuild native project
        res_path = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'AndroidManifest.xml')
        File.replace(res_path, '17', '19')
        strings = ['Preparing project', 'Building project', 'BUILD SUCCESSFUL', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=60)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_100_tns_run_android_release(self):
        """Make valid changes in JS,CSS and HTML"""

        # `tns run android --release` and wait until app is deployed
        # IMPORTANT NOTE: `tns run android --release` Do NOT livesync by design!

        log = Tns.run_android(attributes={'--path': self.app_name,
                                          '--device': EMULATOR_ID,
                                          '--keyStorePath': ANDROID_KEYSTORE_PATH,
                                          '--keyStorePassword': ANDROID_KEYSTORE_PASS,
                                          '--keyStoreAlias': ANDROID_KEYSTORE_ALIAS,
                                          '--keyStoreAliasPassword': ANDROID_KEYSTORE_ALIAS_PASS,
                                          '--release': ''}, wait=False, assert_success=False)

        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

        # Kills `tns run android --release`
        Process.kill('node')

        # Replace files
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML)

        # Run `tns run android --release` again and make sure changes above are applied
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          '--keyStorePath': ANDROID_KEYSTORE_PATH,
                                          '--keyStorePassword': ANDROID_KEYSTORE_PASS,
                                          '--keyStoreAlias': ANDROID_KEYSTORE_ALIAS,
                                          '--keyStoreAliasPassword': ANDROID_KEYSTORE_ALIAS_PASS,
                                          '--release': ''}, wait=False, assert_success=False)

        strings = ['Project successfully prepared']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_js_css_xml')

    def test_200_tns_run_android_break_and_fix_app(self):
        """
        Make changes in xml that break the app and then changes that fix the app.
        """

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

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
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

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
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

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

        # Un=comment following lines after https://github.com/NativeScript/nativescript-cli/issues/2657 is fixed.

        # Verify new folder is synced and available on device.
        # error_message = 'Deleted folder {0} is still available on {1}'.format(new_folder_name, EMULATOR_ID)
        # assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_300_tns_run_android_just_launch_and_incremental_builds(self):
        """
        This test verify following things:
        1. `--justlaunch` option release the console.
        2. Prepare is not triggered if no changed are done.
        3. Incremental prepare is triggered if js, xml and css files are changed.
        """

        # Execute `tns run android --path TNS_App --justlaunch` and verify app looks correct on emulator
        Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''})
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

        # Execute `tns run android --path TNS_App --justlaunch` again
        # without any changes on app under test and verify incremental prepare works
        output = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''},
                                 assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.ANDROID, output=output,
                            prepare=Prepare.SKIP)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

        # Replace JS, XML and CSS files
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML)

        # Run `tns run android` after file changes (this should trigger incremental prepare).
        output = Tns.run_android(attributes={'--path': self.app_name, '--justlaunch': ''}, assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.ANDROID, output=output,
                            prepare=Prepare.INCREMENTAL)

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_js_css_xml')

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
        assert 'BUILD SUCCESSFUL' in log, "Full rebuild not triggered when --clean is used"

        Adb.wait_for_text(device_id=EMULATOR_ID, text='42 taps left')

        # Verify if changes are applied and then build with `--clean` it will apply changes on attached device
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID,
                                          '--justlaunch': '', '--clean': ''})
        assert 'Skipping prepare' not in log, "Prepare skipped when change files and run `tns run android --clean`"
        assert 'Building project...' in log, "Full rebuild not triggered when --clean is used"
        assert 'BUILD SUCCESSFUL' in log, "Full rebuild not triggered when --clean is used"

        Adb.wait_for_text(device_id=EMULATOR_ID, text='52 taps left')

        # Verify if changes are applied and then build with `--clean` it will apply changes on attached device
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS)
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID,
                                          '--justlaunch': '', '--clean': ''})
        assert 'Skipping prepare' not in log
        assert 'Building project...' in log
        assert 'BUILD SUCCESSFUL' in log

        Adb.wait_for_text(device_id=EMULATOR_ID, text='42 taps left')

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
        source_file = os.path.join(self.app_name, 'app', 'main-page.xml')
        destination_file = os.path.join(self.app_name, 'app', new_file_name)
        File.copy(source_file, destination_file)
        time.sleep(20)  # Give it some time to sync the changes

        # Verify new file is synced and available on device.
        error_message = 'Newly created file {0} found on {1}'.format(new_file_name, EMULATOR_ID)
        app_id = Tns.get_app_id(app_name=self.app_name)
        path = 'app/{0}'.format(new_file_name)
        assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

    def test_330_tns_run_android_sync_all_files(self):
        """
        Verify '--syncAllFiles' option will sync all files, including node modules.
        """
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--syncAllFiles': ''},
                              wait=False, assert_success=False)
        strings = ['Successfully installed on device with identifier',
                   'Successfully synced application',
                   EMULATOR_ID,  # Verify device id
                   'JS:']  # Verify console log messages are shown.
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        ReplaceHelper.replace(app_name=self.app_name, file_change=ReplaceHelper.CHANGE_TNS_MODULES)

        strings = ['Successfully transferred application-common.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_340_tns_run_should_not_sync_hidden_files(self):
        """
        Adding hidden files should not break run and they should not be transferred.
        """

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

        # Add some hidden files
        source_file = os.path.join(self.app_name, 'app', 'main-page.xml')
        destination_file = os.path.join(self.app_name, 'app', '.tempfile')
        File.copy(source_file, destination_file)

        # Give it 10 sec and check no messages are available in log files
        time.sleep(10)
        output = File.read(log)
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
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_350_tns_run_android_should_start_emulator(self):
        """
        `tns run android` should start emulator if device is not connected.
        """
        count = Device.get_count(platform=Platform.ANDROID)
        if count == 0:
            Emulator.stop()
            output = Tns.run_android(attributes={'--path': self.app_name, '--justlaunch': ''})
            assert 'Starting Android emulator with image' in output
            assert Emulator.is_running(device_id=EMULATOR_ID), 'Emulator not started by `tns run android`!'
        else:
            raise nose.SkipTest('This test is not valid when devices are connected.')
