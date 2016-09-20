import unittest
import os.path
from time import sleep

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH
from core.tns.tns import Tns
from nose.tools import timed


class UnittestsSimulator(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.stop_emulators()
        Simulator.stop_simulators()
        Device.ensure_available(platform="ios")
        Device.uninstall_app(app_prefix="org.nativescript", platform="ios", fail=False)

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        Simulator.stop_simulators()

    @unittest.skip("Unit testing is not very stable on iOS")
    @timed(360)
    def test_010_test_jasmine_ios_simulator(self):
        Tns.create_app(self.app_name, attributes={})
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        Tns.run_tns_command("test init", attributes={"--framework": "jasmine",
                                                     "--path": self.app_name
                                                     })
        # run(TNS_PATH + " test init --framework jasmine --path " + self.app_name, timeout=60)

        # Next lines are required because of https://github.com/NativeScript/nativescript-cli/issues/1636
        Tns.run_tns_command("test ios", attributes={"--justlaunch": "",
                                                    "--path": self.app_name})
        # run(TNS_PATH + " test ios --justlaunch --path " + self.app_name, timeout=90)
        sleep(10)

        output = Tns.run_tns_command("test ios", attributes={"--justlaunch": "",
                                                             "--path": self.app_name})
        # output = run(TNS_PATH + " test ios --justlaunch --path " + self.app_name, timeout=60)
        assert "Project successfully prepared" in output
        assert "server started" in output
        assert "Starting browser NativeScript Unit Test Runner" in output

        assert "Executed 1 of 1 SUCCESS" in output
