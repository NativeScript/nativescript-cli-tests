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
import time

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunIOSDeviceTests(BaseClass):
    SIMULATOR_ID = ''
    DEVICES = Device.get_ids(platform=Platform.IOS)
    DEVICE_ID = Device.get_id(platform=Platform.IOS)

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Simulator.stop()
        Device.ensure_available(platform=Platform.IOS)

        Folder.cleanup(cls.app_name)
        Tns.create_app(cls.app_name, attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)
        Process.kill(proc_name='node', proc_cmdline='tns')  # Stop 'node' to kill the livesync after each test method.

    def tearDown(self):
        Process.kill(proc_name='node', proc_cmdline='tns')  # Stop 'node' to kill the livesync after each test method.
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Simulator.stop()

    def test_001_tns_run_ios_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--syncAllFiles': ''}, log_trace=True, wait=False,
                          assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', self.DEVICE_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)

        # Verify app is deployed and running on all available ios devices
        output = File.read(log)
        for device_id in self.DEVICES:
            assert device_id in output, 'Application is not deployed on {0}'.format(device_id)

        # Verify Simulator is not started
        assert not Simulator.is_running()[0], 'Device is attached, but emulator is also started after `tns run ios`!'

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Successfully synced application', self.DEVICE_ID]
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Rollback all the changes and verify files are synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Refreshing application']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'Refreshing application']
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

    def test_300_tns_run_ios_emulator_should_start_emulator_even_if_device_is_connected(self):
        """
        `tns run ios --emulator` should start emulator even if physical device is connected
        """
        Simulator.stop()
        Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''}, assert_success=False)
        assert Simulator.is_running()[0], 'iOS Simulator not started by `tns run ios`!'

    def test_310_tns_run_ios_emulator_should_run_only_on_emulator(self):
        """
        `tns run ios --emulator` should start emulator even if physical device is connected
        """
        self.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        output = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                             assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, output=output, platform=Platform.IOS, prepare=Prepare.SKIP)
        assert self.SIMULATOR_ID in output
        for device_id in self.DEVICES:
            assert device_id not in output, 'Application is deployed on {0} device.'.format(device_id)

    def test_320_tns_run_ios_specific_device(self):
        """
        `tns run ios --device` should run only on specified device
        """
        self.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        output = Tns.run_ios(attributes={'--path': self.app_name, '--device': self.DEVICE_ID, '--justlaunch': ''},
                             assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, output=output, platform=Platform.IOS, prepare=Prepare.SKIP)
        assert self.SIMULATOR_ID not in output, 'Application is also deployed on iOS Simulator!'
        for device_id in self.DEVICES:
            if device_id != self.DEVICE_ID:
                assert device_id not in output, \
                    'Application is deployed on {0} while it should be only on {1}'.format(device_id, self.DEVICES)

        output = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                             assert_success=False)
        TnsAsserts.prepared(app_name=self.app_name, output=output, platform=Platform.IOS, prepare=Prepare.SKIP)
        assert self.SIMULATOR_ID in output, 'Application is NOT deployed on emulator specified by --device option!'
        for device_id in self.DEVICES:
            assert device_id not in output, \
                'Application is deployed on {0} while it should be only on {1}'.format(device_id, self.SIMULATOR_ID)
