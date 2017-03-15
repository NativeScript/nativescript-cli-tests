"""
Test for emulate command in context of iOS
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME, SIMULATOR_TYPE, SIMULATOR_SDK
from core.tns.tns import Tns
from core.settings.strings import *


class EmulateiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)

        Tns.create_app(cls.app_name)
        Tns.platform_add_ios(attributes={"--path": cls.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup('./' + self.app_name_noplatform)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup('./' + cls.app_name)

    def test_001_emulate_list_devices(self):
        """
        `tns emulate ios --availableDevices` should list all available iOS Simulators.
        """
        output = Tns.run_tns_command("emulate ios", attributes={"--availableDevices": "",
                                                                "--path": self.app_name,
                                                                "--justlaunch": ""
                                                                })
        assert "Available emulators" in output
        assert SIMULATOR_NAME in output

    def test_002_emulate_ios(self):
        """
        `tns emulate ios` should build the project and run it in simulator.
        If simulator is not running `tns` should start it.
        """
        output = Tns.run_tns_command("emulate ios", attributes={"--path": self.app_name,
                                                                "--device": SIMULATOR_NAME,
                                                                "--justlaunch": ""
                                                                })
        assert successfully_prepared in output
        assert successfully_built in output
        assert started_on_device in output
        assert Process.is_running("Simulator")

    def test_003_emulate_ios_release(self):
        output = Tns.run_tns_command("emulate ios", attributes={"--device": SIMULATOR_NAME,
                                                                "--path": self.app_name,
                                                                "--justlaunch": "",
                                                                "--release": ""
                                                                })
        assert successfully_prepared in output
        assert config_release in output
        assert successfully_built in output
        assert started_on_device in output
        assert Process.is_running("Simulator")

    def test_210_emulate_ios_patform_not_added(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.run_tns_command("emulate ios", attributes={"--device": SIMULATOR_NAME,
                                                                "--path": self.app_name_noplatform,
                                                                "--justlaunch": ""
                                                                })
        assert copy_template_files in output
        assert successfully_created in output
        assert successfully_prepared in output
        assert successfully_built in output
        assert started_on_device in output
        assert Process.is_running("Simulator")

    def test_400_emulate_invalid_device(self):
        output = Tns.run_tns_command("emulate ios", attributes={"--device": invalid,
                                                                "--path": self.app_name,
                                                                "--justlaunch": ""
                                                                })
        assert "Cannot resolve the specified connected device by the provided index or identifier." in output
