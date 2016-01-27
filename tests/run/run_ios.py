"""
Tests for run command in context of iOS
"""

import os
import unittest

from core.device.device import Device
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH
from core.tns.tns import Tns


class RuniOS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        Device.ensure_available(platform="ios")

        Folder.cleanup('./TNS App')
        Folder.cleanup('./TNS_App')
        Folder.cleanup('./TNSAppNoPlatform')
        Tns.create_app_platform_add(
                app_name="\"TNS App\"",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        Tns.create_app_platform_add(
                app_name="TNS_App",
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
        Folder.cleanup('./TNS App')
        Folder.cleanup('./TNS_App')
        Folder.cleanup('./TNSAppNoPlatform')
        Simulator.stop_simulators()

    def test_001_run_ios_justlaunch(self):
        output = run(TNS_PATH + " run ios --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "Project successfully built" in output

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_run_ios_release(self):
        output = run(
                TNS_PATH +
                " run ios --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_003_run_ios_simulator(self):
        output = run(TNS_PATH + " run ios --emulator --path \"TNS App\" --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output

        # Simulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
            assert Process.is_running("Simulator")

            # TODO: Get device id and verify files are deployed and process is
            # running on this device

    def test_004_run_ios_release_simulator(self):
        output = run(TNS_PATH + " run ios --emulator --release --path \"TNS App\" --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output

        # Simulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
            assert Process.is_running("Simulator")

            # TODO: Get device id and verify files are deployed and process is
            # running on this device

    def test_005_run_ios_default(self):
        output = run(TNS_PATH + " run ios --path TNS_App", 60)
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        assert "Successfully run application" in output

    def test_200_run_ios_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(
                os.path.join(
                        "..",
                        TNS_PATH) +
                " run ios --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output

    def test_301_run_ios_platform_not_added(self):
        Tns.create_app(app_name="TNSAppNoPlatform")
        output = run(
                TNS_PATH + " run ios --path TNSAppNoPlatform --justlaunch")
        assert "Copying template files..." in output
        assert "Installing tns-ios" in output
        assert "Project successfully created." in output
        # Note:
        # Do not assert that project runs because it adds latest official platform from npm,
        # it might not work with latest CLI and modules.

    def test_302_run_ios_device_not_connected(self):
        output = run(TNS_PATH + " run ios --device xxxxx --path TNSAppNoPlatform  --justlaunch")
        assert "Cannot resolve the specified connected device" in output
        assert "Project successfully prepared" not in output
        assert "Project successfully built" not in output
        assert "Successfully deployed on device" not in output
