"""
Tests for `tns debug ios` executed on iOS Simulator.
"""
import os
import unittest
from time import sleep

from enum import Enum

from core.base_class.BaseClass import BaseClass
from core.chrome.chrome import Chrome
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class DebugMode(Enum):
    DEFAULT = 0
    START = 1


class DebugiOSChromeSimulatorTests(BaseClass):
    SIMULATOR_ID = ''

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Chrome.stop()
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Tns.create_app(cls.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)
        Chrome.stop()
        Tns.kill()

    def tearDown(self):
        assert not Process.is_running('NativeScript Inspector')
        BaseClass.tearDown(self)
        Chrome.stop()
        Tns.kill()

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    @staticmethod
    def attach_chrome(log, mode=DebugMode.DEFAULT, port="41000"):
        """
        Attach chrome dev tools and verify logs
        :type log: Log file of `tns debug ios` command.
        """

        # Check initial logs
        strings = ["Setting up debugger proxy...", "Press Ctrl + C to terminate, or disconnect.",
                   "Opened localhost", "To start debugging, open the following URL in Chrome"]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)

        # Attach Chrome DevTools
        url = run(command="grep chrome-devtools " + log)
        text_log = File.read(log)
        assert "chrome-devtools://devtools/remote" in text_log, "Debug url not printed in output of 'tns debug ios'."
        assert "localhost:" + port in text_log, "Wrong port of debug url:" + url
        Chrome.start(url)

        # Verify debugger attached
        strings = ["Frontend client connected", "Backend socket created"]
        if mode != DebugMode.START:
            strings.extend(["Loading inspector modules",
                            "Finished loading inspector modules",
                            "NativeScript debugger attached"])
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)

        # Verify debugger not disconnected
        sleep(10)
        output = File.read(log)
        assert "socket closed" not in output, "Debugger disconnected."
        assert "detached" not in output, "Debugger disconnected."
        assert not Process.is_running('NativeScript Inspector'), "iOS Inspector running instead of ChromeDev Tools."

    @staticmethod
    def assert_not_detached(log):
        output = File.read(log)
        assert "socket created" in output, "Debugger not attached at all.\n Log:\n" + output
        assert "socket closed" not in output, "Debugger disconnected.\n Log:\n" + output
        assert "detached" not in output, "Debugger disconnected.\n Log:\n" + output

    def test_001_debug_ios_simulator(self):
        """
        Default `tns debug ios` starts debugger (do not stop at the first code statement)
        """
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': ''})
        self.attach_chrome(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Verify debugger not detached
        self.assert_not_detached(log)

    @unittest.skip("Skip the test because of https://github.com/NativeScript/nativescript-cli/issues/3338")
    def test_002_debug_ios_simulator_debug_brk(self):
        """
        Starts debugger and stop at the first code statement.
        """
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': '', '--debug-brk': ''})

        # Verify app starts and stops on the first line of code
        Device.screen_match(device_name=SIMULATOR_NAME, tolerance=3.0, device_id=self.SIMULATOR_ID,
                            timeout=90, expected_image='livesync-hello-world_debug_brk')

        self.attach_chrome(log)

        # Verify app is still on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME, tolerance=3.0, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_debug_brk')

        # Verify debugger not detached
        self.assert_not_detached(log)

    def test_003_debug_ios_simulator_start(self):
        """
        Attach the debug tools to a running app in the iOS Simulator
        """

        # Run the app and ensure it works
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                          assert_success=False, timeout=60)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.IOS, output=log, prepare=Prepare.SKIP)
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Attach debugger
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': '', '--start': ''})
        self.attach_chrome(log, mode=DebugMode.START)

        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')
        self.assert_not_detached(log)

        # Attach debugger once again
        Tns.kill()
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': '', '--start': ''})
        self.attach_chrome(log, mode=DebugMode.START)

        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')
        self.assert_not_detached(log)

    def test_100_debug_ios_simulator_with_livesync(self):
        """
        `tns debug ios` should be able to run with livesync
        """
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': ''})
        self.attach_chrome(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'open the following URL in Chrome', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'open the following URL in Chrome', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'open the following URL in Chrome', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        # Verify application looks correct
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml')

        # Enable next lines after https://github.com/NativeScript/nativescript-cli/issues/3085 is implemented.
        # Verify debugger not detached
        # self.assert_not_detached(log)
