"""
Tests for `tns debug android` executed on Android Emulator.
"""
import os

from core.base_class.BaseClass import BaseClass
from core.chrome.chrome import Chrome
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import EMULATOR_NAME, EMULATOR_ID, ANDROID_RUNTIME_PATH
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class DebugAndroidEmulatorTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.create_app(self.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def __verify_debugger_start(self, log):
        strings = [EMULATOR_ID, 'NativeScript Debugger started', 'To start debugging, open the following URL in Chrome',
                   'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output

    def __verify_debugger_attach(self, log):
        strings = [EMULATOR_ID, 'To start debugging', 'Chrome', 'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output
        assert "NativeScript Debugger started" not in output

    def test_001_debug_android(self):
        """
        Default `tns debug android` starts debugger (do not stop at the first code statement)
        """
        log = Tns.debug_android(attributes={'--path': self.app_name, '--emulator': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    def test_002_debug_android_emulator_debug_brk(self):
        """
        Starts debugger and stop at the first code statement.
        """

        log = Tns.debug_android(attributes={'--path': self.app_name, '--debug-brk': '', '--emulator': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=EMULATOR_NAME, tolerance=3.0, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_debug_brk')

    def test_003_debug_android_emulator_start(self):
        """
        Attach the debug tools to a running app in the Android Emulator
        """

        # Run the app and ensure it works
        Tns.run_android(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                        assert_success=False, timeout=90)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Attach debugger
        log = Tns.debug_android(attributes={'--path': self.app_name, '--start': '', '--emulator': ''})
        self.__verify_debugger_attach(log=log)

    def test_100_debug_android_should_start_emulator_if_there_is_no_device(self):
        """
        Debug android should start emulator if emulator is not running
        """

        Emulator.stop()
        Tns.build_android(attributes={'--path': self.app_name})
        log = Tns.debug_android(attributes={'--path': self.app_name, '--emulator': '', '--timeout': '180'})
        strings = ['Starting Android emulator with image']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120)

        # Reset the usage of the predefined emulator in settings.py so the next tests reuse its images
        Emulator.stop()
        Emulator.ensure_available()

    def test_200_debug_android_with_response_from_server(self):
        """
        Checks that when `tns debug android` app doesn't crash when there is a response from server (https://github.com/NativeScript/nativescript-cli/issues/3187)
        """

        source = os.path.join('data', 'issues', 'nativescript-cli-3187', 'main-view-model.js')
        target = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source, dest=target)

        log = Tns.debug_android(attributes={'--path': self.app_name, '--emulator': ''})
        self.__verify_debugger_start(log)

        # Verify app is running
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Get Chrome URL and open it
        url = run(command="grep chrome-devtools " + log)
        Chrome.start(url)

        # Tap on the button and verify the app still works
        Device.click(device_id=EMULATOR_ID, text="TAP", timeout=15)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home_after_tap', timeout=15)
