"""
Test for deploy command
"""

import unittest

from core.device.device import Device
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH
from core.tns.tns import Tns


class DeployiOS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Device.ensure_available(platform="ios")

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        Folder.cleanup('./TNS_App')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_001_deploy_ios_device(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        output = run(TNS_PATH + " deploy ios --path TNS_App  --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_300_deploy_ios_platform_not_added(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " deploy ios --path TNS_App --justlaunch")
        assert "Copying template files..." in output
        assert "Installing tns-ios" in output
        assert "Project successfully created." in output
        # Note:
        # Do not assert that project runs because it adds latest official platform from npm,
        # it might not work with latest CLI and modules.
