"""
Run mocha tests on Android emulator.
"""

from nose.tools import timed

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.npm.npm import Npm
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH
from  core.settings.strings import *
from core.tns.tns import Tns


class UnittestsEmulator(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

    def setUp(self):
        BaseClass.setUp(self)
        Tns.kill()
        Folder.cleanup(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        Emulator.stop()
        Tns.kill()

    @timed(420)
    def test_100_test_mocha_android_emulator(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.build_android(attributes={'--path': self.app_name})
        Tns.run_tns_command("test init", attributes={"--framework": "mocha", "--path": self.app_name})

        # Hack to workaround https://github.com/NativeScript/nativescript-cli/issues/2283
        Npm.install(package='mocha', folder=self.app_name, option='--save-dev')

        output = Tns.run_tns_command("test android", attributes={"--emulator": "",
                                                                 "--justlaunch": "",
                                                                 "--path": self.app_name}, timeout=120)

        assert successfully_prepared in output
        assert server_started in output
        assert starting_ut_runner in output
        assert executed_tests in output

        assert "Disconnectedundefined" not in output
