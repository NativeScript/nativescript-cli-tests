import unittest

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, SIMULATOR_NAME
from core.tns.tns import Tns


class UnittestsSimulator_Tests(unittest.TestCase):
    app_name = "TNS_App"

    @classmethod
    def setUpClass(cls):
        Emulator.stop_emulators()
        Simulator.stop_simulators()

        Simulator.delete(SIMULATOR_NAME)
        Simulator.create(SIMULATOR_NAME, 'iPhone 6', '9.1')
        Simulator.start(SIMULATOR_NAME, '9.1')

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

    def test_010_test_jasmine_ios_simulator(self):
        Tns.create_app(app_name=self.app_name)
        run(TNS_PATH + " test init --framework jasmine --path " + self.app_name, timeout=30)

        # Next 3 lines are required because of https://github.com/NativeScript/nativescript-cli/issues/1636
        output = run(TNS_PATH + " test ios --emulator --justlaunch --path " + self.app_name, timeout=60, output=False)

        output = run(TNS_PATH + " test ios --emulator --justlaunch --path " + self.app_name, timeout=180)
        assert "Project successfully prepared" in output
        assert "server started" in output
        assert "Starting browser NativeScript Unit Test Runner" in output

        assert "Executed 1 of 1 SUCCESS" in output
