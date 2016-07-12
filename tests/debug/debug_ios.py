import time
import unittest

from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH
from core.tns.tns import Tns


class DebugiOS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Emulator.stop_emulators()
        Simulator.stop_simulators()
        Folder.cleanup('./TNS_App')
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH)

    def setUp(self):
        Device.ensure_available(platform="ios")
        Process.kill("Safari")
        Process.kill("Inspector")
        Device.uninstall_app(app_prefix="org.nativescript.", platform="ios", fail=False)

    def tearDown(self):
        Process.kill("Safari")
        Process.kill("Inspector")

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./TNS_App')

    def test_001_debug_ios_device_debug_brk(self):
        File.cat("TNS_App/package.json")
        output = run(TNS_PATH + " debug ios --path TNS_App --device " + Device.get_id("ios") + " --timeout 180", 200)

        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Frontend client connected" in output
        assert "Backend socket created" in output
        assert "NativeScript debugger attached" in output

        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output

    def test_002_debug_ios_device_start(self):
        File.cat("TNS_App/package.json")
        output = run(TNS_PATH + " run ios --path TNS_App --justlaunch --device " + Device.get_id("ios"))
        assert "Project successfully built" in output
        assert "Successfully run application " in output
        time.sleep(5)

        output = run(TNS_PATH + " debug ios --start --path TNS_App --timeout 120", 120)

        assert "Frontend client connected" in output
        assert "Backend socket created" in output

        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output
