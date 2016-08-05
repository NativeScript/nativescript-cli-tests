"""
Test for emulate command in context of iOS
"""

import unittest

from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH, SIMULATOR_NAME
from core.tns.tns import Tns


class EmulateiOS_Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        Simulator.stop_simulators()

        Simulator.delete(SIMULATOR_NAME)
        Simulator.create(SIMULATOR_NAME, 'iPhone 6', '9.1')

        Folder.cleanup('./TNS_App')
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

        Folder.cleanup('./TNS_AppNoPlatform')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./TNS_App')

    def test_001_emulate_list_devices(self):
        output = run(TNS_PATH + " emulate ios --availableDevices --path TNS_App --justlaunch")
        assert SIMULATOR_NAME in output

    def test_002_emulate_ios(self):
        output = run(TNS_PATH + " emulate ios --device '" + SIMULATOR_NAME + "' --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output
        assert Process.is_running("Simulator")

    def test_003_emulate_ios_release(self):
        Folder.cleanup('TNS_App/platforms')
        output = run(TNS_PATH + " emulate ios --device '" + SIMULATOR_NAME + "' --path TNS_App --release --justlaunch")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output
        assert Process.is_running("Simulator")

    def test_210_emulate_ios_patform_not_added(self):
        Tns.create_app(app_name="TNS_AppNoPlatform")
        output = run(TNS_PATH + " emulate ios --device '" + SIMULATOR_NAME + "' --path TNS_AppNoPlatform --justlaunch")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting iOS Simulator" in output
        assert Process.is_running("Simulator")

    def test_400_emulate_invalid_device(self):
        output = run(TNS_PATH + " emulate ios --device invalidDevice --path TNS_App --justlaunch")
        assert "Cannot find device with name: invalidDevice." in output
