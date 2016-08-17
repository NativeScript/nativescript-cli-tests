"""
Test for device command in context of iOS
"""

import unittest
from time import sleep

from core.device.device import Device
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, ANDROID_RUNTIME_PATH, IOS_RUNTIME_SYMLINK_PATH
from core.tns.tns import Tns


class DeviceiOS_Tests(unittest.TestCase):
    app_name = "TNS_App"

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./' + self.app_name)
        Device.ensure_available(platform="ios")

    def tearDown(self):
        pass

    def test_001_device_log_list_applications_and_run_ios(self):
        device_id = Device.get_id(platform="ios")
        device_ids = Device.get_ids("ios")

        # Deploy TNS_App on device
        Tns.create_app_platform_add(app_name=self.app_name,
                                    platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH,
                                    symlink=True)

        output = run(TNS_PATH + " deploy ios --path " + self.app_name + "  --justlaunch", timeout=180)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        for device_id in device_ids:
            assert device_id in output
        sleep(10)

        # Verify list-applications command list org.nativescript.TNSApp
        for device_id in device_ids:
            output = run(TNS_PATH + " device list-applications --device " + device_id)
            assert "org.nativescript.TNSApp" in output

        # Get logs
        output = run(TNS_PATH + " device log --device " + device_id, timeout=30)
        assert ("<Notice>:" in output) or ("<Error>:" in output) or ("com.apple." in output)
