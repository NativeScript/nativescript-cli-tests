"""
Run jasmine tests on iOS Simulator.
"""

from nose.tools import timed

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
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
