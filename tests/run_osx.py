'''
Tests for run command in context of iOS
'''
import os, unittest

from helpers._os_lib import cleanup_folder, run_aut, is_running_process
from helpers._tns_lib import create_project, create_project_add_platform, \
    IOS_RUNTIME_SYMLINK_PATH, TNSPATH
from helpers.device import given_real_device, stop_simulators

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class RuniOS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        given_real_device(platform="ios")

        cleanup_folder('./TNS App')
        cleanup_folder('./TNS_App')
        cleanup_folder('./TNSAppNoPlatform')
        create_project_add_platform(
            proj_name="\"TNS App\"",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
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

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cleanup_folder('./TNS App')
        cleanup_folder('./TNS_App')
        cleanup_folder('./TNSAppNoPlatform')
        stop_simulators()

    def test_001_run_ios(self):
        output = run_aut(TNSPATH + " run ios --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_run_ios_release(self):
        output = run_aut(
            TNSPATH +
            " run ios --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_003_run_ios_simulator(self):
        output = run_aut(TNSPATH + " run ios --emulator --path \"TNS App\" --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output

        # Simulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
            assert "Session started without errors" in output
            assert is_running_process("Simulator")

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_004_run_ios_release_simulator(self):
        output = run_aut(TNSPATH + " run ios --emulator --release --path \"TNS App\" --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output

        # Simulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
            assert "Session started without errors" in output
            assert is_running_process("Simulator")

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_005_run_ios_default(self):
        output = run_aut(TNSPATH + " run ios --path TNS_App", 60)
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        assert "Mounting" in output
        assert "Successfully run application" in output

    def test_200_run_ios_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(
            os.path.join(
                "..",
                TNSPATH) +
            " run ios --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output

    def test_300_run_ios_platform_not_added(self):
        create_project(proj_name="TNSAppNoPlatform")
        output = run_aut(
            TNSPATH +
            " run ios --path TNSAppNoPlatform --justlaunch")

        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
