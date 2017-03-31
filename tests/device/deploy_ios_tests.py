"""
Tests for deploy command
"""
import os.path

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH
from core.tns.tns import Tns
from core.settings.strings import *


class DeployiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Device.ensure_available(platform="ios")
        Simulator.stop()

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup('./' + self.app_name)
        Device.uninstall_app("org.nativescript.", platform="ios", fail=False)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup('./' + self.app_name)

    def test_001_deploy_ios_device(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        output = Tns.deploy_ios(attributes={"--path": self.app_name, "--justlaunch": ""}, timeout=180)

        # This is the first time we build the project -> we need a prepare
        assert successfully_prepared in output

        device_ids = Device.get_ids(platform="ios")
        for device_id in device_ids:
            assert device_id in output

    def test_300_deploy_ios_platform_not_added(self):
        Tns.create_app(app_name=self.app_name)
        output = Tns.deploy_ios(attributes={"--path": self.app_name, "--justlaunch": ""}, timeout=180)
        assert copy_template_files in output
        assert "Installing tns-ios" in output
        # This is the first time we build the project -> we need a prepare
        assert successfully_prepared in output
