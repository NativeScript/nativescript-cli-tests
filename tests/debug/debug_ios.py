"""
Test for iOS debugger
"""
from time import sleep
import unittest


# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=R0201, C0103, C0111, R0904
from core.device.device import Device
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
        Folder.cleanup('./TNS_App')
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH)

    def setUp(self):
        Device.ensure_available(platform="ios")
        Simulator.stop_simulators()
        Process.kill("Safari")
        Process.kill("Inspector")
        # Device.uninstall_app(app_prefix="org.nativescript.", platform="ios", fail=False)

    def tearDown(self):
        Simulator.stop_simulators()
        Process.kill("Safari")
        Process.kill("Inspector")

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./TNS_App')

    def test_001_debug_ios_simulator_debugbrk(self):
        File.cat("TNS_APP/package.json")
        output = run(TNS_PATH + " debug ios --debug-brk --emulator --path TNS_App --frameworkPath " +
                     IOS_RUNTIME_SYMLINK_PATH + " --timeout 180", 200, True)
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Starting iOS Simulator" in output
        assert "Frontend client connected" in output
        assert "Session started without errors" in output
        assert "Backend socket created" in output
        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output

    def test_002_debug_ios_simulator_start(self):
        File.cat("TNS_APP/package.json")
        output = run(TNS_PATH + " emulate ios --path TNS_App --justlaunch")
        assert "** BUILD SUCCEEDED **" in output
        assert "Starting iOS Simulator" in output
        assert "Session started without errors" in output
        sleep(10)

        output = run(TNS_PATH + " debug ios --start --emulator --path TNS_App --frameworkPath " +
                     IOS_RUNTIME_SYMLINK_PATH + " --timeout 120", 2 * 60, True)
        assert "Frontend client connected" in output
        assert "Backend socket created" in output
        assert "Backend socket closed" not in output
        assert "Frontend socket closed" not in output
        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output

    def test_003_debug_ios_device_debugbrk(self):
        File.cat("TNS_APP/package.json")
        output = run(TNS_PATH + " debug ios --debug-brk --path TNS_App --frameworkPath " +
                     IOS_RUNTIME_SYMLINK_PATH + " --timeout 120", 2 * 60 + 30, True)
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Successfully deployed on device " in output
        assert "Successfully emulate application org.nativescript.TNSApp on device with ID" in output
        assert "NativeScript waiting for debugger" in output

        assert "Frontend client connected" in output
        assert "Backend socket created" in output
        assert "NativeScript debugger attached" in output
        assert "detached" not in output
        assert "disconnected" not in output

    def test_004_debug_ios_device_start(self):
        File.cat("TNS_APP/package.json")
        output = run(TNS_PATH + " emulate ios --path TNS_App --justlaunch")
        assert "** BUILD SUCCEEDED **" in output
        assert "Successfully deployed on device " in output
        sleep(10)

        output = run(TNS_PATH + " debug ios --start --path TNS_App --frameworkPath " +
                     IOS_RUNTIME_SYMLINK_PATH + " --timeout 120", 2 * 60, True)
        assert "Frontend client connected" in output
        assert "Backend socket created" in output
        assert "closed" not in output
        assert "detached" not in output
        assert "disconnected" not in output
