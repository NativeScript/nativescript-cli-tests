import os.path

from nose.tools import timed

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME, TEST_RUN_HOME
from core.settings.strings import *
from core.tns.tns import Tns


class UnittestsSimulator(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Simulator.stop()
        Simulator.start(name=SIMULATOR_NAME)

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        Simulator.uninstall_app(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        Simulator.stop()

    @timed(360)
    def test_010_test_jasmine_ios_simulator(self):
        Tns.create_app(self.app_name, attributes={})
        Tns.platform_add_ios(attributes={"--path": self.app_name,"--frameworkPath": IOS_RUNTIME_PATH})
        Tns.run_tns_command("test init", attributes={"--framework": "jasmine","--path": self.app_name})

        # Hack to workaround https://github.com/NativeScript/nativescript-cli/issues/2212
        Folder.navigate_to(self.app_name)
        run("npm install --save-dev jasmine-core")

        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)

        Tns.run_tns_command("test ios", attributes={"--emulator": "",
                                                    "--justlaunch": "",
                                                    "--path": self.app_name,
                                                    "--timeout": "180"})

        output = Tns.run_tns_command("test ios", attributes={"--emulator": "",
                                                             "--justlaunch": "",
                                                             "--path": self.app_name,
                                                             "--timeout": "60"})

        assert successfully_prepared in output
        assert server_started in output
        assert starting_ut_runner in output

        assert executed_tests in output
