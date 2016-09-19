"""
Tests for run command in context of Android
"""

import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns


class RuniOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass()
        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

    def setUp(self):
        BaseClass.setUp()
        Emulator.ensure_available()
        Device.ensure_available(platform="android")
        Folder.cleanup(self.app_name + '/platforms/android/build/outputs')

    @classmethod
    def tearDownClass(cls):
        Emulator.stop_emulators()
        Folder.cleanup(cls.app_name_appTest)
        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_noplatform)

    def test_001_run_android_justlaunch(self):
        output = Tns.run_android(attributes={"--path": self.app_name,
                                             "--justlaunch": ""
                                             },
                                 assert_success=False)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        device_ids = Device.get_ids("android")
        for device_id in device_ids:
            assert device_id in output
            assert Device.is_running(app_id="org.nativescript.TNSApp", device_id=device_id)

    def test_002_run_android_release(self):
        output = Tns.run_android(attributes={"--path": self.app_name,
                                             "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                             "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                             "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                             "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                             "--release": "",
                                             "--justlaunch": ""
                                             },
                                 assert_success=False)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        device_ids = Device.get_ids("android")
        for device_id in device_ids:
            assert device_id in output
            assert Device.is_running(app_id="org.nativescript.TNSApp", device_id=device_id)

    def test_003_run_android_default(self):
        output = Tns.run_android(attributes={"--path": self.app_name}, timeout=60)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        assert "I/ActivityManager" not in output  # We do not show full adb logs (only those from app)

    def test_200_run_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_tns_command("run android", attributes={"--path": self.app_name,
                                                                "--justlaunch": ""
                                                                },
                                     tns_path=os.path.join("..", TNS_PATH))
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_201_run_android_device_id_renamed_proj_dir(self):
        run("mv " + self.app_name + " " + self.app_name_appTest)
        output = Tns.run_android(attributes={"--path": self.app_name_appTest,
                                             "--device": "emulator-5554",
                                             "--justlaunch": ""
                                             },
                                 assert_success=False)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output

    def test_301_run_android_patform_not_added(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.run_android(attributes={"--path": self.app_name_noplatform,
                                             "--justlaunch": "",
                                             })
        assert "Copying template files..." in output
        assert "Installing tns-android" in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output

    def test_302_run_android_device_not_connected(self):
        output = Tns.run_android(attributes={"--path": self.app_name_noplatform,
                                             "--device": "xxxxx",
                                             "--justlaunch": ""
                                             },
                                 assert_success=False)
        assert "Cannot resolve the specified connected device" in output
        assert "Project successfully prepared" not in output
        assert "Project successfully built" not in output
        assert "Successfully deployed on device" not in output
