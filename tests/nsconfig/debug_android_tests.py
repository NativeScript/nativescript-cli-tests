"""
Tests for `tns debug android` executed on Android Emulator with different nsconfig setup.
"""
from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.chrome.chrome import Chrome
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import EMULATOR_NAME, EMULATOR_ID, TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class DebugAndroidEmulatorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Emulator.ensure_available()

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
        Tns.kill()

    def tearDown(self):
        Tns.kill()
        Chrome.stop()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

        Folder.cleanup("ChangeAppLocationLS")
        Folder.cleanup("ChangeAppLocationAndNameLS")
        Folder.cleanup("ChangeAppResLocationLS")
        Folder.cleanup("ChangeAppResLocationInRootLS")
        Folder.cleanup("RenameAppLS")
        Folder.cleanup("RenameAppResLS")

    @staticmethod
    def __verify_debugger_start(log):
        strings = [EMULATOR_ID, 'NativeScript Debugger started', 'To start debugging, open the following URL in Chrome',
                   'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output

    @staticmethod
    def __verify_debugger_attach(log):
        strings = [EMULATOR_ID, 'To start debugging', 'Chrome', 'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output
        assert "NativeScript Debugger started" not in output

    @parameterized.expand([
        'ChangeAppLocationLS',
        'ChangeAppLocationAndNameLS',
        'ChangeAppResLocationLS',
        'ChangeAppResLocationInRootLS',
        'RenameAppLS',
        'RenameAppResLS'
    ])
    def test_001_debug_android(self, app_name):
        """
        Default `tns debug android` starts debugger (do not stop at the first code statement)
        """
        log = Tns.debug_android(attributes={'--path': app_name, '--emulator': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    @parameterized.expand([
        'ChangeAppLocationLS',
        'ChangeAppLocationAndNameLS',
        'ChangeAppResLocationLS',
        'ChangeAppResLocationInRootLS',
        'RenameAppLS',
        'RenameAppResLS'
    ])
    def test_002_debug_android_emulator_debug_brk(self, app_name):
        """
        Starts debugger and stop at the first code statement.
        """

        log = Tns.debug_android(attributes={'--path': app_name, '--debug-brk': '', '--emulator': ''})
        DebugAndroidEmulatorTests.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=EMULATOR_NAME, tolerance=3.0, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_debug_brk')

    @parameterized.expand([
        'ChangeAppLocationLS',
        'ChangeAppLocationAndNameLS',
        'ChangeAppResLocationLS',
        'ChangeAppResLocationInRootLS',
        'RenameAppLS',
        'RenameAppResLS'
    ])
    def test_003_debug_android_emulator_start(self, app_name):
        """
        Attach the debug tools to a running app in the Android Emulator
        """

        # Run the app and ensure it works
        Tns.run_android(attributes={'--path': app_name, '--emulator': '', '--justlaunch': ''},
                        assert_success=False, timeout=90)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Attach debugger
        log = Tns.debug_android(attributes={'--path': app_name, '--start': '', '--emulator': ''})
        DebugAndroidEmulatorTests.__verify_debugger_attach(log=log)

    @parameterized.expand([
        'ChangeAppLocationLS',
        'ChangeAppLocationAndNameLS',
        'ChangeAppResLocationLS',
        'ChangeAppResLocationInRootLS',
        'RenameAppLS',
        'RenameAppResLS'
    ])
    def test_100_debug_android_should_start_emulator_if_there_is_no_device(self, app_name):
        """
        Debug android should start emulator if emulator is not running
        """

        Emulator.stop()
        Tns.build_android(attributes={'--path': app_name})
        log = Tns.debug_android(attributes={'--path': app_name, '--emulator': '', '--timeout': '180'})
        strings = ['Starting Android emulator with image']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120)

        # Reset the usage of the predefined emulator in settings.py so the next tests reuse its images
        Emulator.stop()
        Emulator.ensure_available()
