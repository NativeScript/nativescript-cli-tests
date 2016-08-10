import unittest
from time import sleep

from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, IOS_RUNTIME_PATH
from core.tns.tns import Tns
from nose.tools import timed


class UnittestsSimulator(unittest.TestCase):
    app_name = "TNS_App"

    @classmethod
    def setUpClass(cls):
        Emulator.stop_emulators()
        Simulator.stop_simulators()
        Device.ensure_available(platform="ios")
        Device.uninstall_app(app_prefix="org.nativescript", platform="ios", fail=False)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup(self.app_name)

    def tearDown(self):
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        Simulator.stop_simulators()

    @unittest.skip("Unit testing is not very stable on iOS")
    @timed(360)
    def test_010_test_jasmine_ios_simulator(self):
        Tns.create_app_platform_add(app_name=self.app_name, platform="ios", framework_path=IOS_RUNTIME_PATH)
        run(TNS_PATH + " test init --framework jasmine --path " + self.app_name, timeout=60)

        # Next lines are required because of https://github.com/NativeScript/nativescript-cli/issues/1636
        run(TNS_PATH + " test ios --justlaunch --path " + self.app_name, timeout=90)
        sleep(10)

        output = run(TNS_PATH + " test ios --justlaunch --path " + self.app_name, timeout=60)
        assert "Project successfully prepared" in output
        assert "server started" in output
        assert "Starting browser NativeScript Unit Test Runner" in output

        assert "Executed 1 of 1 SUCCESS" in output
