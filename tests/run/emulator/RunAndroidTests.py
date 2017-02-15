"""
Test for `tns run android` command
"""

import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.devide_type import DeviceType
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import ANDROID_RUNTIME_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, EMULATOR_NAME
from core.tns.tns import Tns
from tests.run.ReplaceHelper import ReplaceHelper


class RunAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.stop_emulators()
        Emulator.ensure_available()

    def setUp(self):
        BaseClass.setUp(self)
        Tns.create_app(self.app_name, attributes={"--template": os.path.join("data", "apps", "livesync-hello-world")})
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

    def tearDown(self):
        Process.kill('node')  # Stop 'node' to kill the livesync after each test method.
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        # Emulator.stop_emulators()

    def test_001_tns_run_android_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={"--path": self.app_name}, wait=False, assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_home")

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_JS)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_CSS)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_XML)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_js_css_xml")

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.FILE_CHANGE_JS)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.FILE_CHANGE_CSS)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.FILE_CHANGE_XML)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_home")

    @unittest.skip("Ignored because of https://github.com/NativeScript/nativescript-cli/issues/2511")
    def test_100_tns_run_android_release(self):
        """Make valid changes in JS,CSS and HTML"""

        # `tns run android --release` and wait until app is deployed
        # IMPORTANT NOTE: `tns run android --release` Do NOT livesync by design!

        log = Tns.run_android(attributes={"--path": self.app_name,
                                          "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                          "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                          "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                          "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                          "--release": ""}, wait=False, assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_home")

        # Kills `tns run android --release`
        Process.kill('node')

        # Replace files
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_JS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_CSS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_XML)

        # Run `tns run android --release` again and make sure changes above are applied
        log = Tns.run_android(attributes={"--path": self.app_name,
                                          "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                          "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                          "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                          "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                          "--release": ""}, wait=False, assert_success=False)

        strings = ['Project successfully prepared']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_js_css_xml")

    def test_200_tns_run_android_break_and_fix_app(self):
        """Make changes that break the app and then changes that fix the app."""

        log = Tns.run_android(attributes={"--path": self.app_name}, wait=False, assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_home")

    def test_210_tns_run_android_add_remove_files_and_folders(self):
        """Add and remove files and folders"""

        log = Tns.run_android(attributes={"--path": self.app_name}, wait=False, assert_success=False)
        strings = ['Project successfully prepared', 'Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_home")

    def test_300_tns_run_android_justlaunch_and_incremental_builds(self):
        """ This test verify following things:
        1. `--justlaunch` option release the console.
        2. Prepare and build are incremental.
        3. `tns run android` deploy on all attached Android emulators and devices.
        """

        # Execute `tns run android --path TNS_App --justlaunch` and verify project is prepared (this is first run)
        output = Tns.run_android(attributes={"--path": self.app_name, "--justlaunch": ""})
        assert "Project successfully prepared" in output

        # Verify app is deployed and running on all available android devices
        device_ids = Device.get_ids(platform="android")
        for device_id in device_ids:
            assert device_id in output, "Application is not deployes on {0}".format(device_id)
            assert Device.is_running(app_id="org.nativescript.TNSApp", device_id=device_id), \
                "Application is not running on {0}".format(device_id)

        # Verify app looks correct inside emulator
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_home")

        # Execute `tns run android --path TNS_App --justlaunch` again
        # without any changes on app under test and verify incremental prepare works
        output = Tns.run_android(attributes={"--path": self.app_name, "--justlaunch": ""}, assert_success=False)
        assert "Skipping prepare." in output
        assert "Skipping package build. No changes detected on the native side. This will be fast!" in output
        assert "Refreshing application..." in output
        assert "Project successfully prepared" not in output

        # Verify app is deployed and running on all available android devices
        device_ids = Device.get_ids(platform="android")
        for device_id in device_ids:
            assert device_id in output, "Application is not deployes on {0}".format(device_id)
            assert Device.is_running(app_id="org.nativescript.TNSApp", device_id=device_id), \
                "Application is not running on {0}".format(device_id)

        # Repalce files and run `tns run android --release` again.
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_JS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_CSS)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.FILE_CHANGE_XML)
        output = Tns.run_android(attributes={"--path": self.app_name, "--justlaunch": ""}, assert_success=False)
        assert "Project successfully prepared" in output

        # Verify app looks is update after changes in js, css and xml
        Device.screen_match(device_type=DeviceType.EMULATOR, device_name=EMULATOR_NAME,
                            device_id=EMULATOR_ID, expected_image="livesync-hello-world_js_css_xml")

    def test_310_tns_run_android_clean_builds(self):
        pass

    def test_320_tns_run_android_no_watch(self):
        pass

    def test_330_tns_run_android_syncAllFiles(self):
        """Verify '--syncAllFiles' option will sync all files, including node modules."""
        pass

    @unittest.skip("Ignored because of https://github.com/NativeScript/nativescript-cli/issues/2512")
    def test_400_tns_run_should_not_sync_hidden_files(self):
        # TODO: Please write test after issue is fixed!
        pass
