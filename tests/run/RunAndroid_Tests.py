"""
Tests for run command in context of Android
"""

import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns
from core.settings.strings import *


class RuniOSTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

    def setUp(self):
        BaseClass.setUp(self)
        Emulator.ensure_available()
        Device.ensure_available(platform="android")
        Folder.cleanup(self.app_name + '/platforms/android/build/outputs')

    @classmethod
    def tearDownClass(cls):
        Emulator.stop_emulators()
        Folder.cleanup(cls.app_name_appTest)
        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_noplatform)

    def test_001_run_android_release(self):
        output = Tns.run_android(attributes={"--path": self.app_name,
                                             "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                             "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                             "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                             "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                             "--release": "",
                                             "--justlaunch": ""
                                             },
                                 assert_success=False)

        # This is the first time we build the project -> we need a prepare
        assert successfully_prepared in output

        device_ids = Device.get_ids("android")
        for device_id in device_ids:
            assert device_id in output
            assert Device.is_running(app_id="org.nativescript.TNSApp", device_id=device_id)

    def test_002_run_android_debug(self):
        output = Tns.run_android(attributes={"--path": self.app_name,
                                             "--justlaunch": ""
                                             },
                                 assert_success=False)

        # This is the first time we build in debug -> we need a prepare
        assert successfully_prepared in output

        device_ids = Device.get_ids("android")
        for device_id in device_ids:
            assert device_id in output
            assert Device.is_running(app_id="org.nativescript.TNSApp", device_id=device_id)

    def test_003_run_android_default(self):
        output = Tns.run_android(attributes={"--path": self.app_name}, timeout=60)
        # When previously build in debug and now we build in debug we do not need a prepare
        assert successfully_prepared not in output
         # We do not show full adb logs (only those from app)
        assert "I/ActivityManager" not in output

    def test_200_run_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_android(attributes={"--path": self.app_name,
                                             "--justlaunch": ""
                                             },
                                 tns_path=os.path.join("..", TNS_PATH), assert_success=False)
        os.chdir(current_dir)

        # We should not prepare because previous test already prepared in debug mode
        assert successfully_prepared not in output
        assert successfully_built in output
        assert installed_on_device.format() in output

    def test_201_run_android_device_id_renamed_proj_dir(self):
        run("mv " + self.app_name + " " + self.app_name_appTest)
        output = Tns.run_android(attributes={"--path": self.app_name_appTest,
                                             "--device": "emulator-5554",
                                             "--justlaunch": ""
                                             },
                                 assert_success=False)

        # We should not prepare because previous test already prepared in debug mode
        assert successfully_prepared not in output

        assert successfully_built in output
        assert installed_on_device.format(emulator) in output

    def test_301_run_android_patform_not_added(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.run_android(attributes={"--path": self.app_name_noplatform,
                                             "--justlaunch": "",
                                             })
        assert copy_template_files in output
        assert "Installing tns-android" in output

        # This is the first time we build the project -> we need a prepare
        assert successfully_prepared in output

    def test_302_run_android_device_not_connected(self):
        output = Tns.run_android(attributes={"--path": self.app_name_noplatform,
                                             "--device": "xxxxx",
                                             "--justlaunch": ""
                                             },
                                 assert_success=False)
        assert cannot_resolve_device in output
        assert successfully_prepared not in output
        assert successfully_built not in output
        assert deployed_on_device not in output
