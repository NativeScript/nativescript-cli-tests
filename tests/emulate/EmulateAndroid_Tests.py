"""
Test for emulate command in context of Android
"""
import os
import unittest

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
from time import sleep

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_NAME
from core.tns.tns import Tns


class EmulateAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

    def setUp(self):
        BaseClass.setUp(self)
        Emulator.stop_emulators()
        Folder.cleanup('./' + self.app_name_noplatform)
        Folder.cleanup('./' + self.app_name + '/platforms/android/build/outputs')

    def tearDown(self):
        BaseClass.tearDown(self)
        Emulator.stop_emulators()
        sleep(1)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup('./' + cls.app_name)

    def test_001_emulate_android_in_running_emulator(self):
        Emulator.ensure_available()
        sleep(30)
        output = Tns.run_tns_command("emulate android", attributes={"--path": self.app_name,
                                                                    "--timeout": "600",
                                                                    "--justlaunch": ""
                                                                    },
                                     timeout=660)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully installed on device with identifier 'emulator-5554'" in output
        assert "Starting Android emulator with image" not in output

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_emulate_android_release(self):
        output = Tns.run_tns_command("emulate android", attributes={"--device": EMULATOR_NAME,
                                                                    "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                                                    "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                                                    "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                                                    "--keyStoreAliasPassword":
                                                                        ANDROID_KEYSTORE_ALIAS_PASS,
                                                                    "--release": "",
                                                                    "--path": self.app_name,
                                                                    "--timeout": "600",
                                                                    "--justlaunch": ""
                                                                    },
                                     timeout=660)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting Android emulator with image" in output
        assert "Successfully installed on device with identifier" in output
        assert "Successfully started on device with identifier" in output

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    # TODO: Implement this test
    @unittest.skip("Not implemented.")
    def test_014_emulate_android_genymotion(self):
        pass

    def test_200_emulate_android_inside_project_and_specify_emulator_name(self):

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_tns_command("emulate android", attributes={"--device": EMULATOR_NAME,
                                                                    "--timeout": "600",
                                                                    "--justlaunch": ""
                                                                    },
                                     tns_path=os.path.join("..", TNS_PATH), timeout=660)
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting Android emulator with image " + EMULATOR_NAME in output
        assert "Successfully installed on device with identifier" in output
        assert "Successfully started on device with identifier" in output

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_300_emulate_android_platform_not_added(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.run_tns_command("emulate android", attributes={"--device": EMULATOR_NAME,
                                                                    "--timeout": "720",
                                                                    "--justlaunch": "",
                                                                    "--path": self.app_name_noplatform
                                                                    },
                                     timeout=750)
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting Android emulator with image " + EMULATOR_NAME in output
        assert "Successfully installed on device with identifier" in output
        assert "Successfully started on device with identifier" in output

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_400_emulate_invalid_platform(self):
        output = Tns.run_tns_command("emulate invalidPlatform", attributes={"--path": self.app_name,
                                                                            "--timeout": "600",
                                                                            "--justlaunch": ""
                                                                            },
                                     timeout=660)
        assert "The input is not valid sub-command for 'emulate' command" in output
        assert "Usage" in output

    def test_401_emulate_invalid_avd(self):
        output = Tns.run_tns_command("emulate android", attributes={"--path": self.app_name,
                                                                    "--device": "invaliddevice_id",
                                                                    "--timeout": "600",
                                                                    "--justlaunch": ""
                                                                    },
                                     timeout=660)
        assert "Option --avd is no longer supported. Please use --device isntead!" not in output
        assert "Cannot find device with name: invaliddevice_id" in output
        assert "Usage" in output

