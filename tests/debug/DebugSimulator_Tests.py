import time
import os.path

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH
from core.tns.tns import Tns


class DebugSimulatorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.stop_emulators()
        Tns.create_app(cls.app_name)
        Tns.platform_add_ios(attributes={"--path": cls.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH
                                         })

    def setUp(self):
        BaseClass.setUp(self)
        Simulator.stop_simulators()
        Process.kill("Safari")
        Process.kill("Inspector")

    def tearDown(self):
        BaseClass.tearDown(self)
        Simulator.stop_simulators()
        Process.kill("Safari")
        Process.kill("Inspector")

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup('./' + cls.app_name)

    def test_001_debug_ios_simulator_debug_brk(self):
        File.cat(self.app_name + "/package.json")
        output = Tns.run_tns_command("debug ios", attributes={"--debug-brk": "",
                                                              "--emulator": "",
                                                              "--path": self.app_name,
                                                              "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                                              "--timeout": "200"
                                                              },
                                     timeout=200)

        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Setting up proxy" in output
        assert "Starting iOS Simulator" in output
        assert "Frontend client connected" in output

        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output

    def test_002_debug_ios_simulator_start(self):
        File.cat(self.app_name + "/package.json")
        output = Tns.run_tns_command("emulate ios", attributes={"--path": self.app_name,
                                                                "--justlaunch": ""})
        assert "Project successfully built" in output
        time.sleep(5)

        output = Tns.run_tns_command("debug ios", attributes={"--start": "",
                                                              "--emulator": "",
                                                              "--path": self.app_name,
                                                              "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                                              "--timeout": "150"
                                                              },
                                     timeout=150)
        assert "Frontend client connected" in output
        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output
