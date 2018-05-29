"""
Tests for `tns debug ios` executed on iOS Simulator with different nsconfig setup.
"""
import unittest
from time import sleep

from enum import Enum
from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.chrome.chrome import Chrome
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


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

        if File.exists(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS"):
            assert "ChangeAppLocationLS" in TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS"
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS", TEST_RUN_HOME + "/ChangeAppLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLS",
                        TEST_RUN_HOME + "/ChangeAppLocationAndNameLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationLS",
                        TEST_RUN_HOME + "/ChangeAppResLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootLS",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRootLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppLS", TEST_RUN_HOME + "/RenameAppLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppResLS", TEST_RUN_HOME + "/RenameAppResLS")
        else:
            CreateNSConfigApps.createAppsLiveSync()

        if not File.exists(TEST_RUN_HOME + "/ChangeAppLocationLS"):
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationLS", TEST_RUN_HOME + "/ChangeAppLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameLS",
                        TEST_RUN_HOME + "/ChangeAppLocationAndNameLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationLS",
                        TEST_RUN_HOME + "/ChangeAppResLocationLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootLS",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRootLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppLS", TEST_RUN_HOME + "/RenameAppLS")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppResLS", TEST_RUN_HOME + "/RenameAppResLS")
        else:
            assert File.exists(TEST_RUN_HOME + "/ChangeAppLocationLS")

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

        Folder.cleanup("ChangeAppLocationLS")
        Folder.cleanup("ChangeAppLocationAndNameLS")
        Folder.cleanup("ChangeAppResLocationLS")
        Folder.cleanup("ChangeAppResLocationInRootLS")
        Folder.cleanup("RenameAppLS")
        Folder.cleanup("RenameAppResLS")
        Folder.cleanup("ChangeAppLocationLS.app")
        File.remove("ChangeAppLocationLS.ipa")
        Folder.cleanup("ChangeAppLocationAndNameLS.app")
        File.remove("ChangeAppLocationAndNameLS.ipa")
        Folder.cleanup("ChangeAppResLocationLS.app")
        File.remove("ChangeAppResLocationLS.ipa")
        Folder.cleanup("ChangeAppResLocationInRootLS.app")
        File.remove("ChangeAppResLocationInRootLS.ipa")
        Folder.cleanup("RenameAppLS.app")
        File.remove("RenameAppLS.ipa")
        Folder.cleanup("RenameAppResLS.app")
        File.remove("RenameAppResLS.ipa")

    @staticmethod
    def attach_chrome(log, mode=DebugMode.DEFAULT, port="41000"):
        """
        Attach chrome dev tools and verify logs
        :param log: log file with tns output.
        :param mode: DebugMode enum value (START or DEFAULT).
        :param port: debugger port
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

    @parameterized.expand([
        'ChangeAppLocationLS',
        'ChangeAppLocationAndNameLS',
        'ChangeAppResLocationLS',
        'ChangeAppResLocationInRootLS',
        'RenameAppLS',
        'RenameAppResLS'
    ])
    def test_001_debug_ios_simulator(self, app_name):
        """
        Default `tns debug ios` starts debugger (do not stop at the first code statement)
        """
        log = Tns.debug_ios(attributes={'--path': app_name, '--emulator': ''})
        self.attach_chrome(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Verify debugger not detached
        self.assert_not_detached(log)

        # Uninstall the app so that to avoid "Address already in use" when trying to debug on the same simulator
        Simulator.uninstall("org.nativescript." + app_name)

    @parameterized.expand([
        'ChangeAppLocationLS',
        'ChangeAppLocationAndNameLS',
        'ChangeAppResLocationLS',
        'ChangeAppResLocationInRootLS',
        'RenameAppLS',
        'RenameAppResLS'
    ])
    def test_002_debug_ios_simulator_debug_brk(self, app_name):
        """
        Starts debugger and stop at the first code statement.
        """
        log = Tns.debug_ios(attributes={'--path': app_name, '--emulator': '', '--debug-brk': ''})

        # Verify app starts and stops on the first line of code
        Device.screen_match(device_name=SIMULATOR_NAME, tolerance=3.0, device_id=self.SIMULATOR_ID,
                            timeout=180, expected_image='livesync-hello-world_debug_brk')

        self.attach_chrome(log)

        # Verify app is still on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME, tolerance=3.0, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_debug_brk')

        # Verify debugger not detached
        self.assert_not_detached(log)

        # Uninstall the app so that to avoid "Address already in use" when trying to debug on the same simulator
        Simulator.uninstall("org.nativescript." + app_name)

    @parameterized.expand([
        'ChangeAppLocationLS',
        'ChangeAppLocationAndNameLS',
        'ChangeAppResLocationLS',
        'ChangeAppResLocationInRootLS',
        'RenameAppLS',
        'RenameAppResLS'
    ])
    def test_003_debug_ios_simulator_start(self, app_name):
        """
        Attach the debug tools to a running app in the iOS Simulator
        """
        # Run the app and ensure it works
        log = Tns.run_ios(attributes={'--path': app_name, '--emulator': '', '--justlaunch': ''},
                          assert_success=False, timeout=120)
        TnsAsserts.prepared(app_name=app_name, platform=Platform.IOS, output=log, prepare=Prepare.SKIP)
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Attach debugger
        log = Tns.debug_ios(attributes={'--path': app_name, '--emulator': '', '--start': ''})
        self.attach_chrome(log, mode=DebugMode.START)

        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')
        self.assert_not_detached(log)

        # Attach debugger once again
        Tns.kill()
        log = Tns.debug_ios(attributes={'--path': app_name, '--emulator': '', '--start': ''})
        self.attach_chrome(log, mode=DebugMode.START)

        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')
        self.assert_not_detached(log)

        # Uninstall the app so that to avoid "Address already in use" when trying to debug on the same simulator
        Simulator.uninstall("org.nativescript." + app_name)

    @parameterized.expand([
        ('ChangeAppLocationLS',
         ['new_folder/app/main-view-model.js', 'taps', 'clicks'],
         ['new_folder/app/main-page.xml', 'TAP', 'TEST'],
         ['new_folder/app/app.css', '42', '99']),
        ('ChangeAppLocationAndNameLS',
         ['my folder/my app/main-view-model.js', 'taps', 'clicks'],
         ['my folder/my app/main-page.xml', 'TAP', 'TEST'],
         ['my folder/my app/app.css', '42', '99']),
        ('ChangeAppResLocationLS',
         ReplaceHelper.CHANGE_JS,
         ReplaceHelper.CHANGE_XML,
         ReplaceHelper.CHANGE_CSS),
        ('ChangeAppResLocationInRootLS',
         ReplaceHelper.CHANGE_JS,
         ReplaceHelper.CHANGE_XML,
         ReplaceHelper.CHANGE_CSS),
        ('RenameAppLS',
         ['renamed_app/main-view-model.js', 'taps', 'clicks'],
         ['renamed_app/main-page.xml', 'TAP', 'TEST'],
         ['renamed_app/app.css', '42', '99']),
        ('RenameAppResLS',
         ReplaceHelper.CHANGE_JS,
         ReplaceHelper.CHANGE_XML,
         ReplaceHelper.CHANGE_CSS)
    ])
    @unittest.skip("Problems when running parameterized test")
    def test_100_debug_ios_simulator_with_livesync(self, app_name, change_js, change_xml, change_css):
        """
        `tns debug ios` should be able to run with livesync
        """
        log = Tns.debug_ios(attributes={'--path': app_name, '--emulator': ''}, log_trace=True)
        self.attach_chrome(log)
        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, timeout=180, expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(app_name, change_js, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'open the following URL in Chrome',
                   'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(app_name, change_xml, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml', 'open the following URL in Chrome', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(app_name, change_css, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'open the following URL in Chrome', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)

        # Verify application looks correct
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID, timeout=180,
                            expected_image='livesync-hello-world_js_css_xml')
        # Enable next lines after https://github.com/NativeScript/nativescript-cli/issues/3085 is implemented.
        # Verify debugger not detached
        # self.assert_not_detached(log)

        # Uninstall the app so that to avoid "Address already in use" when trying to debug on the same simulator
        Simulator.uninstall("org.nativescript." + app_name)
