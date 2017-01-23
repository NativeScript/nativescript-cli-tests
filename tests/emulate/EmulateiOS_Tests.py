"""
Test for emulate command in context of iOS
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.tns import Tns


class EmulateiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Simulator.stop_simulators()
        Simulator.delete(SIMULATOR_NAME)
        Simulator.create(SIMULATOR_NAME, 'iPhone 6', '9.1')

        Tns.create_app(cls.app_name)
        Tns.platform_add_ios(attributes={"--path": cls.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup('./' + self.app_name_noplatform)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup('./' + cls.app_name)

    def test_001_emulate_list_devices(self):
        output = Tns.run_tns_command("emulate ios", attributes={"--availableDevices": "",
                                                                "--path": self.app_name,
                                                                "--justlaunch": ""
                                                                })
        assert SIMULATOR_NAME in output

    def test_002_emulate_ios(self):
        output = Tns.run_tns_command("emulate ios", attributes={"--path": self.app_name,
                                                                "--device": SIMULATOR_NAME,
                                                                "--justlaunch": ""
                                                                })
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully started on device with identifier" in output
        assert Process.is_running("Simulator")

    def test_003_emulate_ios_release(self):
        Folder.cleanup(self.app_name + '/platforms')
        output = Tns.run_tns_command("emulate ios", attributes={"--device": SIMULATOR_NAME,
                                                                "--path": self.app_name,
                                                                "--justlaunch": "",
                                                                "--release": ""
                                                                })
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "Project successfully built" in output
        assert "Successfully started on device with identifier" in output
        assert Process.is_running("Simulator")

    def test_210_emulate_ios_patform_not_added(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.run_tns_command("emulate ios", attributes={"--device": SIMULATOR_NAME,
                                                                "--path": self.app_name_noplatform,
                                                                "--justlaunch": ""
                                                                })
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully started on device with identifier" in output
        assert Process.is_running("Simulator")

    def test_400_emulate_invalid_device(self):
        output = Tns.run_tns_command("emulate ios", attributes={"--device": "invalidDevice",
                                                                "--path": self.app_name,
                                                                "--justlaunch": ""
                                                                })
        assert "Cannot find device with name: invalidDevice." in output
