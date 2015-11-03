from time import sleep
import unittest

from helpers._os_lib import CleanupFolder, runAUT, KillProcess, uninstall_app
from helpers._tns_lib import CreateProjectAndAddPlatform, iosRuntimeSymlinkPath, \
    tnsPath
from helpers.device import GivenRealDeviceRunning, StopSimulators

# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=R0201, C0103, C0111, R0904
class DebugiOS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanupFolder('./TNS_App')
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath)

    def setUp(self):

        print ""

        GivenRealDeviceRunning(platform="ios")

        StopSimulators()
        KillProcess("Safari")
        KillProcess("Inspector")
        uninstall_app("TNSApp", platform="ios", fail=False)

    def tearDown(self):
        StopSimulators()
        KillProcess("Safari")
        KillProcess("Inspector")

    @classmethod
    def tearDownClass(cls):
        CleanupFolder('./TNS_App')

    def test_001_debug_ios_simulator_debugbrk(self):

        output = runAUT(
            tnsPath +
            " debug ios --debug-brk --emulator --path TNS_App --frameworkPath " +
            iosRuntimeSymlinkPath,
            2 *
            60,
            True)
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Starting iOS Simulator" in output
        assert "Frontend client connected" in output
        assert "Session started without errors" in output
        assert "Backend socket created" in output
        assert not "closed" in output
        assert not "detached" in output
        assert not "disconnected" in output

    def test_002_Debug_iOS_Simulator_Start(self):

        output = runAUT(tnsPath + " emulate ios --path TNS_App --justlaunch")
        assert "** BUILD SUCCEEDED **" in output
        assert "Starting iOS Simulator" in output
        assert "Session started without errors" in output
        sleep(10)
        output = runAUT(
            tnsPath +
            " debug ios --start --emulator --path TNS_App --frameworkPath " +
            iosRuntimeSymlinkPath,
            2 *
            60,
            True)
        assert "Setting up debugger proxy..." in output
        assert "Frontend client connected" in output
        assert "Backend socket created" in output
        assert not "Backend socket closed" in output
        assert not "Frontend socket closed" in output
        assert not "closed" in output
        assert not "detached" in output
        assert not "disconnected" in output

    def test_003_Debug_iOS_Device_DebugBrk(self):

        output = runAUT(
            tnsPath +
            " debug ios --debug-brk --path TNS_App --timeout 120 --frameworkPath " +
            iosRuntimeSymlinkPath,
            2 *
            60 +
            30,
            True)
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Successfully deployed on device " in output
        assert "Successfully run application org.nativescript.TNSApp on device with ID" in output
        assert "NativeScript waiting for debugger" in output

        assert "Setting up debugger proxy..." in output
        assert "Frontend client connected" in output
        assert "Backend socket created" in output
        assert "NativeScript debugger attached" in output
        assert not "detached" in output
        assert not "disconnected" in output

    def test_004_Debug_iOS_Device_Start(self):

        output = runAUT(tnsPath + " run ios --path TNS_App --justlaunch")
        assert "** BUILD SUCCEEDED **" in output
        assert "Successfully deployed on device " in output
        sleep(10)
        output = runAUT(
            tnsPath +
            " debug ios --start --path TNS_App --timeout 120 --frameworkPath " +
            iosRuntimeSymlinkPath,
            2 *
            60,
            True)

        assert "Setting up debugger proxy..." in output
        assert "Frontend client connected" in output
        assert "Backend socket created" in output
        assert not "closed" in output
        assert not "detached" in output
        assert not "disconnected" in output
