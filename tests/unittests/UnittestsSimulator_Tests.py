import os.path

from nose.tools import timed

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.tns import Tns


class UnittestsSimulator(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.stop_emulators()
        Simulator.stop_simulators()
        Simulator.start(SIMULATOR_NAME, '9.1')

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        Simulator.uninstall_app(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        Simulator.stop_simulators()

    @timed(360)
    def test_010_test_jasmine_ios_simulator(self):
        Tns.create_app(self.app_name, attributes={})
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        Tns.run_tns_command("test init", attributes={"--framework": "jasmine",
                                                     "--path": self.app_name
                                                     })

        Tns.run_tns_command("test ios", attributes={"--emulator": "",
                                                    "--justlaunch": "",
                                                    "--path": self.app_name,
                                                    "--timeout": "180"})

        output = Tns.run_tns_command("test ios", attributes={"--emulator": "",
                                                             "--justlaunch": "",
                                                             "--path": self.app_name,
                                                             "--timeout": "60"})

        assert "Project successfully prepared" in output
        assert "server started" in output
        assert "Starting browser NativeScript Unit Test Runner" in output

        assert "Executed 1 of 1 SUCCESS" in output
