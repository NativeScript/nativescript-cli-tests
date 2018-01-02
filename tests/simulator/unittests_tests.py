"""
Run jasmine tests on iOS Simulator.
"""
import os
from nose.tools import timed

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.settings.strings import *
from core.tns.tns import Tns


class UnittestsSimulator(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        Simulator.ensure_available(simulator_name=SIMULATOR_NAME)

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        Simulator.stop()

    @timed(360)
    def test_100_test_jasmine_ios_simulator(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.run_tns_command("test init", attributes={"--framework": "jasmine", "--path": self.app_name})

        output = Tns.run_tns_command("test ios", attributes={"--emulator": "",
                                                             "--justlaunch": "",
                                                             "--path": self.app_name}, timeout=180)

        assert successfully_prepared in output
        assert server_started in output
        assert starting_ut_runner in output
        assert executed_tests in output

        assert "Disconnectedundefined" not in output

    @timed(360)
    def test_200_test_mocha_ios_simulator(self):
        Tns.create_app(self.app_name, update_modules=True)
        Npm.install(package='mocha', folder=self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.run_tns_command("test init", attributes={"--framework": "mocha", "--path": self.app_name})

        output = Tns.run_tns_command("test ios", attributes={"--emulator": "",
                                                             "--justlaunch": "",
                                                             "--path": self.app_name}, timeout=180)

        assert successfully_prepared in output
        assert server_started in output
        assert starting_ut_runner in output
        assert executed_tests in output

        assert "Disconnectedundefined" not in output

    def test_201_test_init_mocha_js_stacktrace(self):
        # https://github.com/NativeScript/ios-runtime/issues/565
        Tns.create_app(app_name=self.app_name)
        Npm.install(package='mocha', folder=self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.run_tns_command("test init", attributes={"--framework": "mocha", "--path": self.app_name})

        copy = os.path.join('data', 'issues', 'ios-runtime-565', 'example.js')
        paste = os.path.join(self.app_name, 'app', 'tests')
        Folder.copy(copy, paste)

        output = File.read(self.app_name + "/app/tests/example.js")
        assert "Mocha test" in output
        assert "Test" in output
        assert not "Array" in output

        output = Tns.run_tns_command("test ios", attributes={"--emulator": "", "--path": self.app_name},
                                     log_trace=True, wait=False)
        strings = ['JavaScript stack trace', 'assert@undefined']
        Tns.wait_for_log(log_file=output, string_list=strings, timeout=90)
