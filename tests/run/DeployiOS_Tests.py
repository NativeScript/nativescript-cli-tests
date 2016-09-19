"""
Tests for deploy command
"""
from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH
from core.tns.tns import Tns


class DeployiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass()
        Device.ensure_available(platform="ios")

    def setUp(self):
        BaseClass.setUp()
        Folder.cleanup('./' + self.app_name)
        Device.uninstall_app("org.nativescript.", platform="ios", fail=False)

    def tearDown(self):
        BaseClass.tearDown()
        Folder.cleanup('./' + self.app_name)

    def test_001_deploy_ios_device(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.run_tns_command("deploy ios", attributes={"--path": self.app_name,
                                                               "--justlaunch": ""
                                                               },
                                     timeout=180)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output

        device_ids = Device.get_ids(platform="ios")
        for device_id in device_ids:
            assert device_id in output

    def test_300_deploy_ios_platform_not_added(self):
        Tns.create_app(app_name=self.app_name)
        output = Tns.run_tns_command("deploy ios", attributes={"--path": self.app_name,
                                                               "--justlaunch": ""
                                                               },
                                     timeout=180)
        assert "Copying template files..." in output
        assert "Installing tns-ios" in output
        assert "Project successfully created." in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
