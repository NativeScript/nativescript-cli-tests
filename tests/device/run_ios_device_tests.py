"""
Test for `tns run ios` command (on real devices).

Verify `tns run ios`
- Run on all available devices
- Changes are synced on physical devices
- Emulator is not started if physical device is attached
- `tns run ios --emulator` starts emulator even if device is connected
- `tns run ios --emulator` should deploy only on emulator
- `tns run ios --device` should deploy only on specified device

TODO: Add tests for:
`tns run ios --device <avd-name>` -> Should be able to start avd image
`tns run ios --device --emulator` -> We should throw nice error
`--available-devices` and `-timeout` options
"""

import os
import unittest
from datetime import datetime
from time import sleep

from flaky import flaky

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE, SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunIOSDeviceTests(BaseClass):
    SIMULATOR_ID = ''
    DEVICES = Device.get_ids(platform=Platform.IOS)
    DEVICE_ID = Device.get_id(platform=Platform.IOS)
    TEMP_FOLDER = os.path.join(TEST_RUN_HOME, 'out',
                               'livesync-hello-world_app_' + datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        Device.ensure_available(platform=Platform.IOS)
        Device.uninstall_app(app_prefix='org.nativescript.', platform=Platform.IOS)

        Folder.cleanup(cls.app_name)
        Tns.create_app(cls.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Folder.copy(src=os.path.join(cls.app_name, 'app'), dst=cls.TEMP_FOLDER)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})

    def setUp(self):
        BaseClass.setUp(self)
        Tns.kill()

        # Replace app folder between tests.
        app_folder = os.path.join(self.app_name, 'app')
        Folder.cleanup(app_folder)
        Folder.copy(src=self.TEMP_FOLDER, dst=app_folder)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Simulator.stop()

    @flaky(max_runs=2)
    def test_001_tns_run_ios_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name}, wait=False, assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', self.DEVICE_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=150, check_interval=10, clean_log=False)

        # Verify app is deployed and running on all available ios devices
        output = File.read(log)
        for device_id in self.DEVICES:
            assert device_id in output, 'Application is not deployed on {0}'.format(device_id)

        # Verify app is running
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="taps left"), "App failed to load!"
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="TAP"), "App failed to load!"

        # Verify Simulator is not started
        assert not Simulator.is_running()[0], 'Device is attached, but emulator is also started after `tns run ios`!'

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=3)
        strings = ['Successfully transferred', 'main-view-model.js', 'Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="clicks"), "JS changes not synced on device!"

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="TEST"), "XML changes not synced on device!"

        # Change CSS and wait until app is synced
        css_change_1 = ['app/app.css', '42', '1']
        ReplaceHelper.replace(self.app_name, css_change_1, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        sleep(15)
        assert "TEST" not in Device.get_screen_text(device_id=self.DEVICE_ID), "Sync of CSS files failed!"

        css_change_2 = ['app/app.css', '1', '42']
        ReplaceHelper.replace(self.app_name, css_change_2, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="TEST"), "Sync of CSS files failed!"

        # Rollback JS changes and verify files are synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="taps left"), "JS changes not synced on device!"

        # Change XML again
        file_change = ReplaceHelper.CHANGE_XML
        File.replace(self.app_name + '/' + file_change[0], "TEST", "MyTest")
        File.copy(src=self.app_name + '/' + file_change[0], dest=self.app_name + '/' + file_change[0] + ".bak")
        File.remove(self.app_name + '/' + file_change[0])
        File.copy(src=self.app_name + '/' + file_change[0] + ".bak", dest=self.app_name + '/' + file_change[0])
        strings = ['Successfully transferred', 'main-page.xml', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="MyTest"), "XML changes not synced on device!"

        # Rollback CSS changes and verify files are synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify Simulator is not started
        assert not Simulator.is_running()[0], 'Device is attached, but emulator is also started after `tns run ios`!'

    def test_210_tns_run_ios_add_remove_files_and_folders(self):
        """
        New files and folders should be synced properly.
        """

        log = Tns.run_ios(attributes={'--path': self.app_name, '--device': self.DEVICE_ID}, wait=False,
                          assert_success=False)
        strings = ['Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Add new files
        new_file_name = 'app2.css'
        source_file = os.path.join(self.app_name, 'app', 'app.css')
        destination_file = os.path.join(self.app_name, 'app', new_file_name)
        File.copy(source_file, destination_file)
        strings = ['Successfully transferred', new_file_name, 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Revert changes(rename file and delete file)
        # File.copy(destination_file, source_file)
        # File.remove(destination_file)
        # strings = ['Successfully transferred', new_file_name, 'Refreshing application']
        # Tns.wait_for_log(log_file=log, string_list=strings)

        # Add folder
        new_folder_name = 'test2'
        source_file = os.path.join(self.app_name, 'app', 'test')
        destination_file = os.path.join(self.app_name, 'app', new_folder_name)
        Folder.copy(source_file, destination_file)
        strings = ['Successfully transferred test2', 'Successfully transferred test.txt']
        Tns.wait_for_log(log_file=log, string_list=strings)

    @flaky(max_runs=2)
    def test_300_tns_run_ios_emulator_should_start_emulator_even_if_device_is_connected(self):
        """
        `tns run ios --emulator` should start emulator even if physical device is connected
        """
        Simulator.stop()
        Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''}, assert_success=False)
        assert Simulator.wait_for_simulator()[0], 'iOS Simulator not started by `tns run ios`!'

    def test_310_tns_run_ios_emulator_should_run_only_on_emulator(self):
        """
        `tns run ios --emulator` should start emulator even if physical device is connected
        """
        self.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        output = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                             assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, output=output, platform=Platform.IOS, prepare=Prepare.INCREMENTAL)
        app_id = Tns.get_app_id(self.app_name)
        assert app_id + " on device " + self.SIMULATOR_ID in output, "App not deployed on iOS Simulator!"
        for device_id in self.DEVICES:
            assert app_id + " on device " + device_id not in output, 'App is deployed on {0} device.'.format(device_id)

    def test_320_tns_run_ios_specific_device(self):
        """
        `tns run ios --device` should run only on specified device
        """
        self.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        output = Tns.run_ios(attributes={'--path': self.app_name, '--device': self.DEVICE_ID, '--justlaunch': ''},
                             assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, output=output, platform=Platform.IOS, prepare=Prepare.INCREMENTAL)
        app_id = Tns.get_app_id(self.app_name)
        assert app_id + " on device " + self.DEVICE_ID in output, "App not deployed on specified device!"
        assert app_id + " on device " + self.SIMULATOR_ID not in output, 'App is also deployed on iOS Simulator!'
        for device_id in self.DEVICES:
            if device_id != self.DEVICE_ID:
                assert app_id + " on device " + device_id not in output, \
                    'App is deployed on {0} while it should be only on {1}'.format(device_id, self.DEVICES)

        # Second prepare should be skipped, since there are no changes in the project.
        output = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                             assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, output=output, platform=Platform.IOS, prepare=Prepare.SKIP)
        assert self.SIMULATOR_ID in output, 'Application is NOT deployed on emulator specified by --device option!'
        for device_id in self.DEVICES:
            assert device_id not in output, \
                'Application is deployed on {0} while it should be only on {1}'.format(device_id, self.SIMULATOR_ID)

    def test_330_tns_run_ios_after_rebuild_of_native_project(self):
        """
        `tns run ios` should work properly after rebuild of native project (test for issue #2860)
        """

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--device': self.DEVICE_ID}, wait=False,
                          assert_success=False, log_trace=True)
        strings = [self.DEVICE_ID, 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app is running
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="Tap the button"), "App failed to load!"

        # Update native project
        config_path = os.path.join(self.app_name, 'app', 'App_Resources', 'iOS', 'build.xcconfig')
        File.replace(file_path=config_path, str1='More info', str2='If you need more info')
        strings = ['BUILD SUCCEEDED', 'Successfully synced application', self.DEVICE_ID, 'CONSOLE LOG']
        not_existing_strings = ['Unable to sync files', 'Multiple errors were thrown']
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings, timeout=120)

        # Verify app is running
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="Tap the button"), "App failed to load!"

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="clicks"), "JS changes not synced on device!"

        # Rollback all the changes and verify files are synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="taps left"), "JS changes not synced on device!"

    @unittest.skipIf('f5ae7a' in Device.get_id(platform=Platform.IOS), "Can not run on this device!")
    def test_400_tns_run_ios_should_not_crash_when_uninstall_app(self):
        """
        `tns run ios` should work properly even if I manually uninstall the app (test for issue #3007)
        """

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, "--device": self.DEVICE_ID}, wait=False,
                          assert_success=False)
        strings = [self.DEVICE_ID, 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app is running
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="taps left"), "App failed to load!"
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="TAP"), "App failed to load!"

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=3)
        strings = ['Successfully transferred', 'main-view-model.js', 'Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="clicks"), "JS changes not synced on device!"

        # Uninstall app while `tns run` is running
        Device.uninstall_app(app_prefix='org.nativescript.', platform=Platform.IOS)
        sleep(5)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully installed', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="TEST"), "XML changes not synced on device!"

    def test_404_tns_run_ios_on_not_existing_device_should_not_start_simualtor(self):
        """
        `tns run ios --device fakeID` should show error and emulator should not be started (test for issue #2728)
        """
        Simulator.stop()
        output = Tns.run_ios(attributes={'--path': self.app_name, '--device': 'fakeID', '--justlaunch': ''},
                             assert_success=False)
        TnsAsserts.invalid_device(output=output)
        sleep(10)
        assert not Simulator.is_running()[0], 'iOS Simulator started by `tns run ios --device fakeID`!'
