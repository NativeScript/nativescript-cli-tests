import os.path
from core.osutils.command import run
from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TEST_RUN_HOME
from core.tns.tns import Tns
from nose.tools import timed
from  core.settings.strings import *


class UnittestsEmulator(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
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

        # Hack to workaround https://github.com/NativeScript/nativescript-cli/issues/2212
        Folder.navigate_to(self.app_name)
        run("npm install --save-dev mocha")
        run("npm install --save-dev chai")

        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)

        output = Tns.run_tns_command("test android", attributes={"--emulator": "",
                                                                 "--justlaunch": "",
                                                                 "--path": self.app_name,
                                                                 "--timeout": "120"})

        assert installed_plugin + " " + nativescript_unit_test_runner in output
        assert successfully_prepared in output
        assert server_started in output
        assert starting_ut_runner in output

        assert executed_tests in output
