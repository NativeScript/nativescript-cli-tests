import unittest

from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, ANDROID_RUNTIME_PATH, EMULATOR_NAME
from core.tns.tns import Tns
from nose.tools import timed

class UnittestsEmulator_Tests(unittest.TestCase):
    app_name = "TNS_App"

    @classmethod
    def setUpClass(cls):
        Emulator.stop_emulators()
        Emulator.create(EMULATOR_NAME, api="19")

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
        Emulator.stop_emulators()

    @timed(360)
    def test_010_test_mocha_android_emulator(self):
        Tns.create_app_platform_add(app_name=self.app_name, platform="android", framework_path=ANDROID_RUNTIME_PATH)
        run(TNS_PATH + " test init --framework mocha --path " + self.app_name)

        # Next lines are required because of https://github.com/NativeScript/nativescript-cli/issues/1636
        run(TNS_PATH + " test android --emulator --justlaunch --path " + self.app_name, timeout=90, output=False)

        output = run(TNS_PATH + " test android --emulator --justlaunch --path " + self.app_name, timeout=60)
        assert "Successfully prepared plugin nativescript-unit-test-runner for android." in output
        assert "Project successfully prepared" in output
        assert "server started" in output
        assert "Starting browser NativeScript Unit Test Runner" in output

        assert "Executed 1 of 1 SUCCESS" in output