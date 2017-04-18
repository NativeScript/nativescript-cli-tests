"""
Test for `tns emulate android` command
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID
from core.settings.strings import *
from core.tns.tns import Tns


class EmulateAndroidTests(BaseClass):
    """
    Important Notes:
    Emulator will be always started in advance due to following issues:
    https://github.com/NativeScript/nativescript-cli/issues/2525
    https://github.com/NativeScript/nativescript-cli/issues/2526
    Please write tests that ensure `tns emulate android --device <avd name>` works after issues are fixes.
    """
    app_name_noplatform = "Test_AppNoPlatform"

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Folder.cleanup('./' + cls.app_name)
        Tns.create_app(cls.app_name, update_modules=True)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup('./' + self.app_name_noplatform)
        Folder.cleanup('./' + self.app_name + '/platforms/android/build/outputs')

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup('./' + cls.app_name)

    def test_001_emulate_android_in_running_emulator(self):
        output = Tns.run_tns_command("emulate android", attributes={"--path": self.app_name,
                                                                    "--timeout": "240",
                                                                    "--justlaunch": ""
                                                                    }, timeout=300)
        assert successfully_prepared in output
        assert successfully_built in output
        assert installed_on_device.format(EMULATOR_ID) in output
        assert "Starting Android emulator with image" not in output
        Device.is_running(app_id=app_identifier, device_id=EMULATOR_ID), \
        "Application is not running on {0}".format(EMULATOR_ID)

    def test_002_emulate_android_release(self):
        output = Tns.run_tns_command("emulate android", attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                                                    "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                                                    "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                                                    "--keyStoreAliasPassword":
                                                                        ANDROID_KEYSTORE_ALIAS_PASS,
                                                                    "--release": "",
                                                                    "--path": self.app_name,
                                                                    "--timeout": "240",
                                                                    "--justlaunch": ""
                                                                    }, timeout=300)
        assert successfully_prepared in output
        assert successfully_built in output
        assert "Starting Android emulator with image" not in output
        assert installed_on_device.format(EMULATOR_ID) in output
        assert started_on_device in output

    def test_200_emulate_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_tns_command("emulate android", attributes={"--timeout": "240", "--justlaunch": ""},
                                     tns_path=os.path.join("..", TNS_PATH), timeout=300)
        os.chdir(current_dir)
        assert successfully_prepared in output
        assert successfully_built in output
        assert "Starting Android emulator with image" not in output
        assert installed_on_device.format(EMULATOR_ID) in output
        assert started_on_device in output

    def test_300_emulate_android_platform_not_added(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.run_tns_command("emulate android", attributes={"--timeout": "240", "--justlaunch": "",
                                                                    "--path": self.app_name_noplatform}, timeout=300)
        assert copy_template_files in output
        assert successfully_created in output
        assert successfully_prepared in output
        assert successfully_built in output
        assert "Starting Android emulator with image" not in output
        assert installed_on_device.format(EMULATOR_ID) in output
        assert started_on_device in output

    def test_400_emulate_invalid_platform(self):
        output = Tns.run_tns_command("emulate invalidPlatform", attributes={"--path": self.app_name, "--timeout": "30",
                                                                            "--justlaunch": ""})
        assert invalid_input.format("emulate") in output
        assert "Usage" in output

    def test_401_emulate_invalid_avd(self):
        output = Tns.run_tns_command("emulate android",
                                     attributes={"--path": self.app_name, "--device": invalid, "--timeout": "30",
                                                 "--justlaunch": ""})
        assert 'Cannot resolve the specified connected device by the provided index or identifier' or \
               'Cannot find device with name' in output
        assert "Usage" in output
