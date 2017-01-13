"""
Tests for run command in context of iOS
"""

import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_PATH, TNS_PATH
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class RuniOS(BaseClass):
    @classmethod
    def setUpClass(cls):
        Xcode.cleanup_cache()
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Xcode.cleanup_cache()
        Device.ensure_available(platform="ios")
        Device.uninstall_app(app_prefix="org.nativescript.", platform="ios", fail=False)
        Simulator.stop_simulators()

        Tns.create_app(cls.app_name_space)
        Tns.platform_add_ios(attributes={"--path": "\"" + cls.app_name_space + "\"",
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        Tns.create_app(cls.app_name)
        Tns.platform_add_ios(attributes={"--path": cls.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./' + cls.app_name_space)
        Folder.cleanup('./' + cls.app_name)
        Folder.cleanup('./' + cls.app_name_noplatform)
        Simulator.stop_simulators()

    def test_001_run_ios_release(self):
        output = Tns.run_ios(attributes={"--path": self.app_name,
                                         "--justlaunch": "",
                                         "--release": ""
                                         },
                             timeout=180)

        # First build in release require prepare
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output

        assert "Successfully run application org.nativescript." in output
        assert "Successfully started on device with identifier" in output

        device_ids = Device.get_ids("ios")
        for device_id in device_ids:
            assert device_id in output

    def test_002_run_ios_debug(self):
        output = Tns.run_ios(attributes={"--path": self.app_name,
                                         "--justlaunch": ""},
                             timeout=180)

        # First build in debug require prepare
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output

        assert "Successfully transferred all files." in output
        assert "Successfully synced application org.nativescript." in output

        device_ids = Device.get_ids("ios")
        for device_id in device_ids:
            assert device_id in output

    def test_003_run_ios_debug_simulator_same_app(self):
        output = Tns.run_ios(attributes={"--path": self.app_name,
                                         "--justlaunch": "",
                                         "--emulator": ""
                                         },
                             timeout=180)

        assert "Skipping prepare." in output  # As it is prepared from test_002
        assert "CONFIGURATION Debug" in output  # New build for emulator, as previously built only for device

        assert "Successfully transferred all files." in output
        assert "Successfully synced application org.nativescript." in output

        assert Process.wait_until_running("Simulator", 60)

    def test_004_run_ios_debug_simulator(self):
        output = Tns.run_ios(attributes={"--path": "\"" + self.app_name_space + "\"",
                                         "--justlaunch": "",
                                         "--emulator": ""
                                         },
                             timeout=180)

        # Prepare because this is new project
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Debug" in output

        assert "Successfully transferred all files." in output
        assert "Successfully synced application org.nativescript." in output

        assert Process.wait_until_running("Simulator", 60)

    def test_005_run_ios_release_simulator(self):
        output = Tns.run_ios(attributes={"--path": "\"" + self.app_name_space + "\"",
                                         "--emulator": "",
                                         "--release": "",
                                         "--justlaunch": ""
                                         },
                             timeout=180)

        # First build for simulator in release for first time, so require prepare
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output

        assert "Successfully started on device with identifier" in output

        assert Process.wait_until_running("Simulator", 60)
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_006_run_ios_default(self):
        output = Tns.run_ios(attributes={"--path": self.app_name},
                             assert_success=False,
                             timeout=60)

        # Dimitar: Hm....not sure this is ok, but no prepare in this case.
        # Vasil: It's ok as there are no changes in this app since test_002
        # and we build again in debug configuration.
        assert "Skipping prepare." in output
        assert "Searching for devices..." in output
        assert "Skipping package build." in output
        assert "Skipping install." in output
        assert "Refreshing application..." in output
        assert "Successfully synced application org.nativescript." in output

        assert "Project successfully prepared" not in output

    def test_200_run_ios_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_ios(attributes={"--path": self.app_name,
                                         "--justlaunch": ""},
                             tns_path=os.path.join("..", TNS_PATH),
                             assert_success=False,
                             timeout=60)
        os.chdir(current_dir)

        # Second build in debug should not prepare
        assert "Skipping prepare." in output
        assert "Searching for devices..." in output
        assert "Skipping package build." in output
        assert "Skipping install." in output
        assert "Refreshing application..." in output
        assert "Successfully synced application org.nativescript." in output

        assert "Project successfully prepared" not in output

    def test_301_run_ios_platform_not_added(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.run_ios(attributes={"--path": self.app_name_noplatform,
                                         "--justlaunch": ""},
                             assert_success=False,
                             timeout=180)
        assert "Copying template files..." in output
        assert "Installing tns-ios" in output
        assert "Project successfully created." in output

        assert "Project successfully prepared" in output
        assert "Project successfully built." in output
        assert "Successfully installed on device with identifier" in output
        assert "Successfully synced application org.nativescript." in output

    def test_302_run_ios_device_not_connected(self):
        output = Tns.run_ios(attributes={"--path": self.app_name_noplatform,
                                         "--device": "xxxxx",
                                         "--justlaunch": ""},
                             assert_success=False,
                             timeout=60)
        assert "Skipping prepare." in output
        assert "Cannot resolve the specified connected device" in output

        assert "Project successfully prepared" not in output
        assert "Project successfully built" not in output
        assert "Successfully deployed on device" not in output
