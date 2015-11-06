import os
import unittest

from helpers._os_lib import cleanup_folder, run_aut, is_running_process
from helpers._tns_lib import create_project, create_project_add_platform, \
    IOS_RUNTIME_SYMLINK_PATH, TNSPATH

# pylint: disable=R0201, C0111


class EmulateiOS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cleanup_folder('./TNS_App')
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_AppNoPlatform')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cleanup_folder('./TNS_App')

    def test_001_Emulate_ListDevices(self):
        output = run_aut(
            TNSPATH +
            " emulate ios --availableDevices --path TNS_App --justlaunch")
        assert "iPhone 6 81" in output

    def test_002_Emulate_iOS(self):
        output = run_aut(
            TNSPATH +
            " emulate ios --device 'iPhone 6 81' --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output

        # Simulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
            assert is_running_process("Simulator")

    def test_003_Emulate_iOS_Release(self):
        output = run_aut(
            TNSPATH +
            " emulate ios --device 'iPhone 6 81' --path TNS_App --release --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output

        # Simulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
            assert is_running_process("Simulator")

    def test_210_Emulate_iOS_PlatformNotAdded(self):
        create_project(proj_name="TNS_AppNoPlatform")
        output = run_aut(
            TNSPATH +
            " emulate ios --device 'iPhone 6 81' --path TNS_AppNoPlatform --justlaunch")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output

        # Simulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
            assert is_running_process("Simulator")

    def test_400_Emulate_InvalidDevice(self):
        output = run_aut(
            TNSPATH +
            " emulate ios --device invalidDevice --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Unable to find device invalidDevice" in output
