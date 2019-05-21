"""
Test for `tns run android` command.

Run should sync all the changes correctly:
 - Valid changes in CSS, JS, XML should be applied.
 - Invalid changes in XML should be logged in the console and lives-sync should continue when XML is fixed.
 - Hidden files should not be synced at all.
 - --syncAllFiles should sync changes in node_modules
 - --justlaunch should release the console.

If emulator is not started and device is not connected `tns run android` should start emulator.
"""

import datetime
import os
import re
import time
import unittest

import nose
import pytz

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_PACKAGE, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, EMULATOR_NAME, CURRENT_OS, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunAndroidEmulatorTests(BaseClass):
    source_app = os.path.join(TEST_RUN_HOME, BaseClass.app_name)
    temp_app = os.path.join(TEST_RUN_HOME, 'data', BaseClass.app_name)
    one_hundred_symbols_string = "123456789012345678901234567890123456789012345678901234567890" \
                                 "1234567890123456789012345678901234567890"
    very_long_string = ''
    for x in range(0, 30):
        very_long_string = very_long_string + one_hundred_symbols_string

    max_long_string = ''
    for x in range(0, 10):
        max_long_string = max_long_string + one_hundred_symbols_string
    max_long_string = max_long_string + "123456789012345678901234"

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.kill()
        Emulator.stop()
        Emulator.ensure_available()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        if CURRENT_OS != OSType.WINDOWS:
            Tns.create_app(cls.app_name,
                           attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                           update_modules=True)
            Tns.platform_add_android(attributes={'--path': cls.app_name, '--frameworkPath': ANDROID_PACKAGE})
            Folder.cleanup(cls.temp_app)
            Folder.copy(cls.source_app, cls.temp_app)

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.source_app)
        if CURRENT_OS != OSType.WINDOWS:
            Folder.copy(self.temp_app, self.source_app)
        else:
            Tns.create_app(self.app_name,
                           attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                           update_modules=True)
            Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_PACKAGE})
            Emulator.ensure_available()

    def tearDown(self):
        Tns.kill()
        if CURRENT_OS == OSType.WINDOWS:
            Emulator.stop()
        BaseClass.tearDown(self)
        Folder.cleanup('TestApp2')

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()  # We need this because of test_400_tns_run_android_respect_adb_errors
        Folder.cleanup(cls.temp_app)


    def test_180_tns_run_android_console_logging(self):
        """
         Test console info, warn, error, assert, trace, time and logging of different objects.
        """

        # Change main-page.js so it contains console logging
        source_js = os.path.join('data', 'console-log', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application',
                   "true",
                   "false",
                   "null",
                   "undefined",
                   "-1",
                   "text",
                   "\"name\": \"John\",",
                   "\"age\": 34",
                   "number: -1",
                   "string: text",
                   "text -1",
                   "info",
                   "warn",
                   "error",
                   "Assertion failed:  false == true",
                   "Assertion failed:  empty string evaluates to 'false'",
                   "Trace: console.trace() called",
                   "at pageLoaded",
                   "Button(8)",
                   "-1 text {",
                   "[1, 5, 12.5, {", "\"name\": \"John\",",
                   "\"age\": 34",
                   "}, text, 42]",
                   "Time:",
                   self.max_long_string,
                   "### TEST END ###"
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        assert "1 equals 1" not in log
        assert self.very_long_string not in log

    def test_181_tns_run_android_console_dir(self):
        """
         Test console.dir() of different objects.
        """

        # Change main-page.js so it contains console logging
        source_js = os.path.join('data', 'console-dir', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application',
                   "true",
                   "false",
                   "null",
                   "undefined",
                   "-1",
                   "text",
                   "==== object dump start ====",
                   "name: \"John\"",
                   "age: \"34\"",
                   "==== object dump end ====",
                   self.max_long_string
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)
        assert self.very_long_string not in log


    def test_360_tns_run_android_with_jar_file_in_plugin(self):
        """
        App should not crash when reference .jar file in some plugin
        https://github.com/NativeScript/android-runtime/pull/905
        """

        # Add .jar file in plugin and modify the app to reference it
        custom_jar_file = os.path.join('data', 'issues', 'android-runtime-pr-905', 'customLib.jar')
        modules_widgets = os.path.join(self.app_name, 'node_modules', 'tns-core-modules-widgets', 'platforms',
                                       'android')
        File.copy(src=custom_jar_file, dest=modules_widgets)

        source = os.path.join('data', 'issues', 'android-runtime-pr-905', 'app.js')
        target = os.path.join(self.app_name, 'app', 'app.js')
        File.copy(src=source, dest=target)

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    def test_370_tns_run_android_with_jar_and_aar_files_in_app_res(self):
        """
        App should not crash when reference .jar or/and .aar file in App_Resources/Android/libs
        https://github.com/NativeScript/android-runtime/issues/899
        """

        # Create libs/ in app/App_resources/, add .jar and .aar files in it and modify the app to reference them
        curr_folder = os.getcwd()
        Folder.navigate_to(os.path.join(self.app_name, 'app', 'App_Resources', 'Android'))
        Folder.create("libs")
        app_res_libs = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'libs')
        Folder.navigate_to(curr_folder)

        custom_jar_file = os.path.join('data', 'issues', 'android-runtime-pr-905', 'customLib.jar')
        custom_aar_file = os.path.join('data', 'issues', 'android-runtime-899', 'mylibrary.aar')

        File.copy(src=custom_jar_file, dest=app_res_libs)
        File.copy(src=custom_aar_file, dest=app_res_libs)

        source = os.path.join('data', 'issues', 'android-runtime-899', 'app.js')
        target = os.path.join(self.app_name, 'app', 'app.js')
        File.copy(src=source, dest=target)

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')
