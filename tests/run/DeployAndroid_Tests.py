"""
Tests for deploy command
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns


class DeployAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass()
        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

    def setUp(self):
        BaseClass.setUp()

        Folder.cleanup(self.app_name_noplatform)
        Emulator.ensure_available()
        Device.ensure_available(platform="android")
        Device.uninstall_app(app_prefix="org.nativescript", platform="android", fail=False)
        Folder.cleanup(self.app_name + '/platforms/android/build/outputs')

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./' + cls.app_name)

    def test_001_deploy_android(self):
        output = Tns.run_tns_command("deploy android", attributes={"--path": self.app_name,
                                                                   "--justlaunch": ""},
                                     timeout=180)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

        device_ids = Device.get_ids(platform="android")
        for device_id in device_ids:
            print device_id
            assert device_id in output

    def test_002_deploy_android_release(self):
        output = Tns.run_tns_command("deploy android", attributes={"--path": self.app_name,
                                                                   "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                                                   "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                                                   "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                                                   "--keyStoreAliasPassword":
                                                                       ANDROID_KEYSTORE_ALIAS_PASS,
                                                                   "--release": "",
                                                                   "--justlaunch": ""
                                                                   },
                                     timeout=180)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

        device_ids = Device.get_ids("android")
        for device_id in device_ids:
            assert device_id in output

    def test_200_deploy_android_deviceid(self):
        output = Tns.run_tns_command("deploy android", attributes={"--path": self.app_name,
                                                                   "--device": "emulator-5554",
                                                                   "--justlaunch": ""
                                                                   },
                                     timeout=180)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output
        device_ids = Device.get_ids("android")
        for device_id in device_ids:
            if "emulator" not in device_id:
                assert device_id not in output

    def test_201_deploy_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_tns_command("deploy android", attributes={"--path": self.app_name,
                                                                   "--justlaunch": ""
                                                                   },
                                     tns_path=os.path.join("..", TNS_PATH), timeout=180)
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

        device_ids = Device.get_ids("android")
        for device_id in device_ids:
            assert device_id in output

    def test_300_deploy_android_platform_not_added(self):
        Tns.create_app(app_name=self.app_name_noplatform)
        output = Tns.run_tns_command("deploy android", attributes={"--path": self.app_name_noplatform,
                                                                   "--justlaunch": ""
                                                                   },
                                     timeout=180)
        assert "Copying template files..." in output
        assert "Installing tns-android" in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

        device_ids = Device.get_ids("android")
        for device_id in device_ids:
            assert device_id in output

    def test_401_deploy_invalid_platform(self):
        output = Tns.run_tns_command("deploy invalidPlatform", attributes={"--path": self.app_name,
                                                                           "--justlaunch": ""
                                                                           })
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output

    def test_402_deploy_invalid_device(self):
        output = Tns.run_tns_command("deploy android", attributes={"--path": self.app_name,
                                                                   "--justlaunch": "",
                                                                   "--device": "invaliddevice_id"
                                                                   })
        assert "Project successfully prepared" not in output
        assert "Cannot resolve the specified connected device" in output
        assert "To list currently connected devices" in output
        assert "tns device" in output
