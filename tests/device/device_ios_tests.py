"""
Test for device command in context of iOS
"""
from time import sleep

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class DeviceIOSTests(BaseClass):
    SIMULATOR_ID = ''
    DEVICE_ID = Device.get_id(platform=Platform.IOS)
    DEVICE_IDS = Device.get_ids(platform=Platform.IOS)

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        Device.ensure_available(platform=Platform.IOS)

    def test_001_device_list(self):
        # Ensure both simulator and real device are listed
        self.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        output = Tns.run_tns_command("device ios")
        assert self.SIMULATOR_ID in output
        for device_id in self.DEVICE_IDS:
            assert device_id in output

        # Ensure when simulator is stopped real device are listed
        Simulator.stop()
        sleep(10)
        output = Tns.run_tns_command("device ios")
        assert self.SIMULATOR_ID not in output
        for device_id in self.DEVICE_IDS:
            assert device_id in output

    def test_100_device_log_list_applications_and_run_ios(self):
        """
        Verify following command work
        - tns device list-applications
        - tns device log
        """

        # Deploy TNS_App on device
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        output = Tns.deploy_ios(attributes={"--path": self.app_name, "--justlaunch": ""}, timeout=180)

        for device_id in self.DEVICE_IDS:
            assert device_id in output
        sleep(10)

        # Verify list-applications command list org.nativescript.TestApp
        for device_id in self.DEVICE_IDS:
            output = Tns.run_tns_command("device list-applications", attributes={"--device": self.DEVICE_ID})
            assert Tns.get_app_id(self.app_name) in output

        # Get logs
        log = Tns.run_tns_command("device log", attributes={"--device": self.DEVICE_ID}, wait=False)
        strings = ['iP', 'message', '<Notice>:']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=30, clean_log=False)
