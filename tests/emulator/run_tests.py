"""
Test for `tns run android` command.

`tns run android` should:
- Re-use emulator if already running
- Start new emulator if emulator is not runnign and device is not conntected.
- Run on device if device is connected (do not start emulator).

Run should sync all the changes correctly:
 - Valid changes in CSS, JS, XML should be applied.
 - Invalid changes in XML should be logged in the console and lives-sycn should continue when XML is fixed.
 - Hidden files should not be synced at all.
"""

import os
import time
import unittest

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


class RunAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.create_app(self.app_name, attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world')})
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

    def tearDown(self):
        Process.kill('node')  # Stop 'node' to kill the livesync after each test method.
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def test_001_tns_run_android_js_css_xml(self):
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

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
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

    @unittest.skip('Ignored because of https://github.com/NativeScript/nativescript-cli/issues/2511')
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
                   'Successfully installed on device with identifier', EMULATOR_ID]
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

        # Verify new file is sysched and available on device.
        error_message = 'Newly created file {0} not found on {1}'.format(new_file_name, EMULATOR_ID)
        app_id = Tns.get_app_id(app_name=self.app_name)
        path = 'app/{0}'.format(new_file_name)
        assert Adb.file_exists(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Revert changes(rename file and delete file)
        File.copy(destination_file, source_file)
        File.remove(destination_file)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new file is sysched and available on device.
        error_message = '{0} was deleted, but still available on {1}'.format(new_file_name, EMULATOR_ID)
        assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Add folder
        new_folder_name = 'test2'
        source_file = os.path.join(self.app_name, 'app', 'test')
        destination_file = os.path.join(self.app_name, 'app', new_folder_name)
        Folder.copy(source_file, destination_file)
        strings = ['Successfully transferred test2', 'Successfully transferred test.txt', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is sysched and available on device.
        error_message = 'Newly created folder {0} not found on {1}'.format(new_folder_name, EMULATOR_ID)
        path = 'app/{0}'.format(new_folder_name)
        assert Adb.file_exists(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Delete folder
        Folder.cleanup(destination_file)
        strings = ['Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify new folder is sysched and available on device.
        error_message = 'Deleted folder {0} is still available on {1}'.format(new_folder_name, EMULATOR_ID)
        assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_300_tns_run_android_justlaunch_and_incremental_builds(self):
        """ This test verify following things:
        1. `--justlaunch` option release the console.
        2. Prepare and build are incremental.
        3. `tns run android` deploy on all attached Android emulators and devices.
        """

        # Execute `tns run android --path TNS_App --justlaunch` and verify project is prepared (this is first run)
        output = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''})
        assert 'Project successfully prepared' in output

        # Verify app is deployed and running on all available android devices
        device_ids = Device.get_ids(platform='android')
        for device_id in device_ids:
            assert device_id in output, 'Application is not deployes on {0}'.format(device_id)
            assert Device.is_running(app_id='org.nativescript.TNSApp', device_id=device_id), \
                'Application is not running on {0}'.format(device_id)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')

        # Execute `tns run android --path TNS_App --justlaunch` again
        # without any changes on app under test and verify incremental prepare works
        output = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--justlaunch': ''},
                                 assert_success=False)
        assert 'Skipping prepare.' in output
        assert 'Skipping package build. No changes detected on the native side. This will be fast!' in output
        assert 'Refreshing application...' in output
        assert 'Project successfully prepared' not in output

        # Verify app is deployed and running on all available android devices
        device_ids = Device.get_ids(platform='android')
        for device_id in device_ids:
            assert device_id in output, 'Application is not deployes on {0}'.format(device_id)
            assert Device.is_running(app_id='org.nativescript.TNSApp', device_id=device_id), \
                'Application is not running on {0}'.format(device_id)

        # Replace JS, XML and CSS files
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML)

        # Run `tns run android --release` again.
        output = Tns.run_android(attributes={'--path': self.app_name, '--justlaunch': ''}, assert_success=False)
        assert 'Project successfully prepared' in output

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_js_css_xml')

    def test_310_tns_run_android_clean_builds(self):
        pass

    def test_320_tns_run_android_no_watch(self):
        pass

    def test_330_tns_run_android_syncAllFiles(self):
        """
        Verify '--syncAllFiles' option will sync all files, including node modules.
        """
        pass

    def test_400_tns_run_should_not_sync_hidden_files(self):
        """
        Adding hidden files should not break livesync and they should not be transferred.
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
        time.sleep(10)
        strings = ['Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify hidden file does not exists on mobile device.
        path = 'app/{0}'.format('.tempfile')
        app_id = Tns.get_app_id(self.app_name)
        error_message = 'Hidden file {0} is transferred to {1}'.format(path, EMULATOR_ID)
        assert Adb.path_does_not_exist(device_id=EMULATOR_ID, package_id=app_id, path=path), error_message

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image='livesync-hello-world_home')
