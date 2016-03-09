import unittest

from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH
from core.tns.tns import Tns


class UnitTestsEmulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Emulator.ensure_available()

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
        Emulator.stop_emulators()

    def test_010_test_mocha_android_emulator(self):
        Tns.create_app(app_name="TNS_App")
        run(TNS_PATH + " test init --framework mocha --path TNS_App")

        output = run(TNS_PATH + " test android --device emulator-5554 --justlaunch --path TNS_App")
        assert "Successfully prepared plugin nativescript-unit-test-runner for android." in output
        assert "Project successfully prepared" in output
        assert "server started" in output
        assert "Starting browser NativeScript Unit Test Runner" in output

        assert "Connected on socket" in output
        assert "Executed 1 of 1 SUCCESS" in output
        # assert "server disconnect" in output
