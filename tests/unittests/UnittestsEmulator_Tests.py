from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH
from core.tns.tns import Tns
from nose.tools import timed


class UnittestsEmulator(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass()
        # It is important to auto start emulator, because otherwise it start random.
        # Latest SDK 23 emulators show some error dialogs on startup and tests fail.
        Emulator.stop_emulators()
        Emulator.ensure_available()

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        Emulator.stop_emulators()

    @timed(360)
    def test_010_test_mocha_android_emulator(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.run_tns_command("test init", attributes={"--framework": "mocha",
                                                     "--path": self.app_name})

        # Next lines are required because of https://github.com/NativeScript/nativescript-cli/issues/1636
        Tns.run_tns_command("test android", attributes={"--emulator": "",
                                                        "--justlaunch": "",
                                                        "--path": self.app_name},
                            timeout=90)

        output = Tns.run_tns_command("test android", attributes={"--emulator": "",
                                                                 "--justlaunch": "",
                                                                 "--path": self.app_name,
                                                                 "--timeout": "90"})
        assert "Successfully prepared plugin nativescript-unit-test-runner for android." in output
        assert "Project successfully prepared" in output
        assert "server started" in output
        assert "Starting browser NativeScript Unit Test Runner" in output

        assert "Executed 1 of 1 SUCCESS" in output
