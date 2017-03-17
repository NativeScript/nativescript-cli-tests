"""
Run mocha tests on Android emulator.
"""
import os.path

from nose.tools import timed

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.npm.npm import Npm
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TEST_RUN_HOME
from  core.settings.strings import *
from core.tns.tns import Tns


class UnittestsEmulator(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        Emulator.stop()

    @timed(360)
    def test_010_test_mocha_android_emulator(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.run_tns_command("test init", attributes={"--framework": "mocha", "--path": self.app_name})

        # Hack to workaround https://github.com/NativeScript/nativescript-cli/issues/2212
        Npm.install(package='mocha', folder=self.app_name, option='--save-dev')
        Npm.install(package='chai', folder=self.app_name, option='--save-dev')

        # --timeout is hack to workaround https://github.com/NativeScript/karma-nativescript-launcher/issues/26
        # Please remove --timeout after issue is fixed.
        output = Tns.run_tns_command("test android", attributes={"--emulator": "",
                                                                 "--justlaunch": "",
                                                                 "--path": self.app_name,
                                                                 "--timeout": "120"}, timeout=130)

        assert successfully_prepared in output
        assert server_started in output
        assert starting_ut_runner in output

        assert executed_tests in output
