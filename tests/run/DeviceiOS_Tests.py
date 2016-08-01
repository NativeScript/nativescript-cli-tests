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
    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')
        Device.ensure_available(platform="ios")

    def tearDown(self):
        pass

    def test_001_device_log_list_applications_and_run_ios(self):
        device_id = Device.get_id(platform="ios")
        device_ids = Device.get_ids("ios")

        # Deploy TNS_App on device
        Tns.create_app_platform_add(app_name="TNS_App",
                                    platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH,
                                    symlink=True)

        output = run(TNS_PATH + " deploy ios --path TNS_App  --justlaunch", timeout=180)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        for id in device_ids:
            assert id in output
        sleep(10)

        # Verify list-applications command list org.nativescript.TNSApp
        for id in device_ids:
            output = run(TNS_PATH + " device list-applications --device " + id)
            assert "org.nativescript.TNSApp" in output

        # Get logs
        output = run(TNS_PATH + " device log --device " + device_id, timeout=30)
        assert ("<Notice>:" in output) or ("<Error>:" in output) or ("com.apple." in output)