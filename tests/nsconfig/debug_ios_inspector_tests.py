"""
Tests for `tns debug ios` executed on iOS Simulator with different nsconfig setup.
"""
import os
import time
import unittest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_INSPECTOR_PACKAGE, SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class DebugiOSInspectorSimulatorTests(BaseClass):
    SIMULATOR_ID = ''
    INSPECTOR_GLOBAL_PATH = os.path.join(os.path.expanduser('~'), '.npm', 'tns-ios-inspector')

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Folder.cleanup(cls.INSPECTOR_GLOBAL_PATH)

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

        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev',
                    folder=CreateNSConfigApps.app_name_change_app_location_ls)
        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev',
                    folder=CreateNSConfigApps.app_name_change_app_location_and_name_ls)
        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev',
                    folder=CreateNSConfigApps.app_name_change_app_res_location_ls)
        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev',
                    folder=CreateNSConfigApps.app_name_change_app_res_location_in_root_ls)
        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev',
                    folder=CreateNSConfigApps.app_name_rename_app_ls)
        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev',
                    folder=CreateNSConfigApps.app_name_rename_app_res_ls)

    def setUp(self):
        BaseClass.setUp(self)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')
        Tns.kill()

    def tearDown(self):
        BaseClass.tearDown(self)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')
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
    def __verify_debugger_start(log):
        strings = ["Frontend client connected", "Backend socket created", "NativeScript debugger attached"]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        time.sleep(10)
        output = File.read(log)
        assert "Frontend socket closed" not in output
        assert "Backend socket closed" not in output
        assert "NativeScript debugger detached" not in output
        assert Process.is_running('NativeScript Inspector')

    @staticmethod
    def __verify_debugger_attach(log):
        strings = ["Frontend client connected", "Backend socket created"]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        time.sleep(10)
        output = File.read(log)
        assert "NativeScript debugger attached" not in output  # This is not in output when you attach to running app
        assert "Frontend socket closed" not in output
        assert "Backend socket closed" not in output
        assert "NativeScript debugger detached" not in output
        assert Process.is_running('NativeScript Inspector')

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
        log = Tns.debug_ios(attributes={'--path': app_name, '--emulator': '', '--inspector': ''})
        DebugiOSInspectorSimulatorTests.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

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

        log = Tns.debug_ios(
            attributes={'--path': app_name, '--emulator': '', '--debug-brk': '', '--inspector': ''})
        DebugiOSInspectorSimulatorTests.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME, tolerance=3.0, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_debug_brk')

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
        log = Tns.run_ios(attributes={'--path': app_name, '--emulator': '', '--justlaunch': '', '--inspector': ''},
                          assert_success=False, timeout=30)
        TnsAsserts.prepared(app_name=app_name, platform=Platform.IOS, output=log, prepare=Prepare.SKIP)
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Attach debugger
        log = Tns.debug_ios(attributes={'--path': app_name, '--emulator': '', '--start': '', '--inspector': ''})
        DebugiOSInspectorSimulatorTests.__verify_debugger_attach(log=log)

        # Uninstall the app so that to avoid "Address already in use" when trying to debug on the same simulator
        Simulator.stop_application("org.nativescript." + app_name)

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
        log = Tns.debug_ios(attributes={'--path': app_name, '--emulator': '', '--inspector': ''})
        DebugiOSInspectorSimulatorTests.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(app_name, change_js, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'CONSOLE LOG',
                   'Backend socket closed', 'Frontend socket closed',
                   'Frontend client connected', 'Backend socket created', 'NativeScript debugger attached']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(app_name, change_xml, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml',
                   'Backend socket created', 'NativeScript debugger attached', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(app_name, change_css, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Backend socket created',
                   'NativeScript debugger attached', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml', tolerance=0.26)

        assert Process.is_running('NativeScript Inspector')

        # Uninstall the app so that to avoid "Address already in use" when trying to debug on the same simulator
        Simulator.uninstall("org.nativescript." + app_name)
