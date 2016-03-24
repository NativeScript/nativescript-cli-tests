import unittest

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, SIMULATOR_NAME
from core.tns.tns import Tns


class UnitTestsSimulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Emulator.stop_emulators()
        Simulator.stop_simulators()
        Simulator.delete(SIMULATOR_NAME)
        Simulator.create(SIMULATOR_NAME, 'iPhone 6s', '9.0')
        Simulator.start(SIMULATOR_NAME)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('TNS_App')

    def tearDown(self):
        Folder.cleanup('TNS_App')

    @classmethod
    def tearDownClass(cls):
        Simulator.stop_simulators()

    def test_010_test_jasmine_ios_simulator(self):
        Tns.create_app(app_name="TNS_App")
        run(TNS_PATH + " test init --framework jasmine --path TNS_App")

        output = run(TNS_PATH + " test ios --emulator --justlaunch --path TNS_App", 60)
        assert "Successfully prepared plugin nativescript-unit-test-runner for ios." in output
        assert "Project successfully prepared" in output
        assert "server started" in output
        assert "Starting browser NativeScript Unit Test Runner" in output

        assert "Connected on socket" in output
        assert "Executed 1 of 1 SUCCESS" in output
        # assert "server disconnect" in output
