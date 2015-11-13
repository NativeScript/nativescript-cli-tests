'''
Test for deploy command
'''
import unittest

from helpers._os_lib import cleanup_folder, run_aut
from helpers._tns_lib import create_project, create_project_add_platform, \
    IOS_RUNTIME_SYMLINK_PATH, TNSPATH
from helpers.device import given_real_device


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class DeployiOS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        given_real_device(platform="ios")

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')

    def tearDown(self):
        cleanup_folder('./TNS_App')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_001_deploy_ios_device(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)
        output = run_aut(TNSPATH + " deploy ios --path TNS_App  --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_300_deploy_ios_platform_not_added(self):
        create_project(proj_name="TNS_App")
        output = run_aut(TNSPATH + " deploy ios --path TNS_App --justlaunch")
        assert "Copying template files..." in output
        assert "Project successfully created." in output

        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device
