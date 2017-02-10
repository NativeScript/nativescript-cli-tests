"""
Test for device command in context of iOS
"""
import unittest

from time import sleep

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH
from core.tns.tns import Tns
from core.settings.strings import *


class DeviceiOSTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        Device.ensure_available(platform="ios")

    @unittest.skip("Ignored because of https://github.com/NativeScript/nativescript-cli/issues/2154")
    def test_001_device_log_list_applications_and_run_ios(self):
        device_id = Device.get_id(platform="ios")
        device_ids = Device.get_ids("ios")

        # Deploy TNS_App on device
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })

        output = Tns.deploy_ios(attributes={"--path": self.app_name,
                                            "--justlaunch": ""
                                            },
                                timeout=180)

        # This is the first time we build the project -> we need a prepare
        assert successfully_prepared in output

        for device_id in device_ids:
            assert device_id in output
        sleep(10)

        # Verify list-applications command list org.nativescript.TNSApp
        for device_id in device_ids:
            output = Tns.run_tns_command("device list-applications", attributes={"--device": device_id})
            assert "org.nativescript.TNSApp" in output

        # Get logs
        output = Tns.run_tns_command("device log", attributes={"--device": device_id}, timeout=30)
        assert ("<Notice>:" in output) or ("<Error>:" in output) or ("com.apple." in output)
