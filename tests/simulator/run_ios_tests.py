"""
Test for `tns run ios` command.

Run should sync all the changes correctly:
 - Valid changes in CSS, JS, XML should be applied.
 - Invalid changes in XML should be logged in the console and lives-sync should continue when XML is fixed.
 - Hidden files should not be synced at all.
 - --syncAllFiles should sync changes in node_modules
 - --justlaunch should release the console.

If simulator is not started and device is not connected `tns run ios` should start simulator.
"""

import os
import time
import unittest

import nose

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE, SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class RunIOSSimulatorTests(BaseClass):
    SIMULATOR_ID = ''
    one_hundred_symbols_string = "123456789012345678901234567890123456789012345678901234567890" \
                                 "1234567890123456789012345678901234567890"
    very_long_string = ''
    for x in range(0, 30):
        very_long_string = very_long_string + one_hundred_symbols_string

    max_long_string = ''
    for x in range(0, 9):
        max_long_string = max_long_string + one_hundred_symbols_string
    max_long_string = max_long_string + "12345678901234567890123456789012345678901234567890123456789012345678901"
                                        
    plugin_path = os.path.join(TEST_RUN_HOME, 'data', 'plugins', 'sample-plugin', 'src')

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Folder.cleanup(cls.app_name)
        Tns.create_app(cls.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name, TEST_RUN_HOME + "/data/TestApp")

    def setUp(self):
        BaseClass.setUp(self)
        self.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Folder.cleanup(self.app_name)
        Folder.copy(TEST_RUN_HOME + "/data/TestApp", TEST_RUN_HOME + "/TestApp")

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")

    def test_180_tns_run_ios_console_log(self):
        """
         Test console info, warn, error, assert, trace, time and logging of different objects.
        """

        # Change main-page.js so it contains console logging
        source_js = os.path.join('data', 'console-log', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        john_obj = "{\n" \
                   "\"name\": \"John\",\n" \
                   "\"age\": 34\n" \
                   "}"

        john_obj2 = "[\n" + "1,\n" \
                            "5,\n" \
                            "12.5,\n" \
                            "{\n" \
                            "\"name\": \"John\",\n" \
                            "\"age\": 34\n" \
                            "},\n" \
                            "\"text\",\n" \
                            "42\n" \
                            "]"

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', self.SIMULATOR_ID,
                   "CONSOLE LOG file:///app/main-page.js",
                   "true",
                   "false",
                   "null",
                   "undefined",
                   "-1",
                   "text",
                   john_obj,
                   "number: -1",
                   "string: text",
                   "text -1",
                   "CONSOLE INFO",
                   "info",
                   "CONSOLE WARN",
                   "warn",
                   "CONSOLE ERROR",
                   "error",
                   "false == true",
                   "empty string evaluates to 'false'",
                   "CONSOLE TRACE file:///app/main-page.js",
                   "console.trace() called",
                   "pageLoaded",
                   "Button(8)",
                   "-1 text {",
                   john_obj2,
                   self.max_long_string,
                   "CONSOLE INFO Time:",
                   "### TEST END ###"
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=150, check_interval=10)
        assert self.very_long_string not in log

    def test_181_tns_run_ios_console_dir(self):
        """
         Test console.dir() of different objects.
        """

        # Change main-page.js so it contains console logging
        source_js = os.path.join('data', 'console-dir', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        john_obj = "==== object dump start ====\n" \
                   "name: John\n" \
                   "age: 34\n" \
                   "==== object dump end ===="

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', self.SIMULATOR_ID,
                   "true",
                   "false",
                   "null",
                   "undefined",
                   "-1",
                   "text",
                   self.max_long_string,
                   john_obj
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=150, check_interval=10)
        assert self.very_long_string not in log