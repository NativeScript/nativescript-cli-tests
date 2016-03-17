import time
import unittest

from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH
from core.tns.tns import Tns


class DebugSimulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Folder.cleanup('./TNS_App')
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH)

    def setUp(self):
        Simulator.stop_simulators()
        Process.kill("Safari")
        Process.kill("Inspector")

    def tearDown(self):
        Simulator.stop_simulators()
        Process.kill("Safari")
        Process.kill("Inspector")

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./TNS_App')

    def test_001_debug_ios_simulator_debug_brk(self):
        File.cat("TNS_App/package.json")
        output = run(TNS_PATH + " debug ios --debug-brk --emulator --path TNS_App --frameworkPath " +
                     IOS_RUNTIME_SYMLINK_PATH + " --timeout 180", 200)

        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Setting up proxy" in output
        assert "Starting iOS Simulator" in output
        assert "Frontend client connected" in output
        assert "Backend socket created" in output
        assert "NativeScript debugger attached" in output

        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output

    def test_002_debug_ios_simulator_start(self):
        File.cat("TNS_App/package.json")
        output = run(TNS_PATH + " emulate ios --path TNS_App --justlaunch")
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output
        time.sleep(10)

        output = run(TNS_PATH + " debug ios --start --emulator --path TNS_App --frameworkPath " +
                     IOS_RUNTIME_SYMLINK_PATH + " --timeout 120", 120)

        assert "Frontend client connected" in output
        assert "Backend socket created" in output

        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output
