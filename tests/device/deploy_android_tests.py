"""
Tests for deploy command
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class DeployAndroidTests(BaseClass):
    app_name_noplatform = "Test_AppNoPlatform"

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Device.ensure_available(platform=Platform.ANDROID)
        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name_noplatform)
        Emulator.ensure_available()
        Device.uninstall_app(app_prefix="org.nativescript", platform=Platform.ANDROID)
        Folder.cleanup(self.app_name + '/platforms/android/build/outputs')

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup(cls.app_name)

    def test_001_deploy_android(self):
        output = Tns.run_tns_command("deploy android", attributes={"--path": self.app_name,
                                                                   "--justlaunch": ""}, timeout=180)

        # This is the first time we build the project -> we need a prepare
        assert successfully_prepared in output

        device_ids = Device.get_ids(platform=Platform.ANDROID)
        for device_id in device_ids:
            print device_id
            assert device_id in output

    def test_002_deploy_android_release(self):
        output = Tns.deploy_android(attributes={"--path": self.app_name,
                                                "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                                "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                                "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                                "--keyStoreAliasPassword":
                                                    ANDROID_KEYSTORE_ALIAS_PASS,
                                                "--release": "",
                                                "--justlaunch": ""
                                                }, timeout=180)

        # We executed build once, but this is first time we call build --release -> we need a prepare
        assert successfully_prepared in output
        device_ids = Device.get_ids(platform=Platform.ANDROID)
        for device_id in device_ids:
            assert device_id in output

    def test_200_deploy_android_deviceid(self):
        output = Tns.deploy_android(attributes={"--path": self.app_name, "--device": EMULATOR_ID, "--justlaunch": ""},
                                    timeout=180)

        # We executed build once, but this is first time we call build --release -> we need a prepare
        assert successfully_prepared in output
        assert installed_on_device.format(EMULATOR_ID) in output
        device_ids = Device.get_ids(platform=Platform.ANDROID)
        for device_id in device_ids:
            if "emulator" not in device_id:
                assert device_id not in output

    def test_201_deploy_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.deploy_android(attributes={"--path": self.app_name, "--justlaunch": ""},
                                    tns_path=os.path.join("..", TNS_PATH), timeout=180, assert_success=False)
        os.chdir(current_dir)

        # Now we do not need prepare, because previous test also did build in debug mode
        assert successfully_prepared not in output

        device_ids = Device.get_ids(platform=Platform.ANDROID)
        for device_id in device_ids:
            assert device_id in output

    def test_300_deploy_android_platform_not_added(self):
        Tns.create_app(app_name=self.app_name_noplatform)
        output = Tns.deploy_android(attributes={"--path": self.app_name_noplatform, "--justlaunch": ""}, timeout=180)

        # It is brand new project and we need a prepare for first run
        assert copy_template_files in output
        assert "Installing tns-android" in output
        assert successfully_prepared in output

        device_ids = Device.get_ids(platform=Platform.ANDROID)
        for device_id in device_ids:
            assert device_id in output

    def test_401_deploy_invalid_platform(self):
        output = Tns.run_tns_command("deploy " + invalid.lower(), attributes={"--path": self.app_name,
                                                                              "--justlaunch": ""
                                                                              })
        assert "Invalid platform {0}. Valid platforms are ios or android.".format(invalid.lower()) in output

    def test_402_deploy_invalid_device(self):
        output = Tns.run_tns_command("deploy android", attributes={"--path": self.app_name,
                                                                   "--justlaunch": "",
                                                                   "--device": "invaliddevice_id"
                                                                   })
        assert "Could not find device by specified identifier" in output
        assert "To list currently connected devices and verify that the specified identifier exists, run" in output
        assert "tns device" in output
