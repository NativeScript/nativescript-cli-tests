"""
Tests for `tns debug ios` executed on iOS Simulator.
"""
import os
import time

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_PACKAGE, IOS_INSPECTOR_PACKAGE, SIMULATOR_NAME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


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
        Tns.create_app(cls.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})
        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev', folder=cls.app_name)

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
        Folder.cleanup(cls.app_name)

    def __verify_debugger_start(self, log):
        strings = ["Frontend client connected", "Backend socket created", "NativeScript debugger attached"]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        time.sleep(10)
        output = File.read(log)
        assert "Frontend socket closed" not in output
        assert "Backend socket closed" not in output
        assert "NativeScript debugger detached" not in output
        assert Process.is_running('NativeScript Inspector')

    def __verify_debugger_attach(self, log):
        strings = ["Frontend client connected", "Backend socket created"]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        time.sleep(10)
        output = File.read(log)
        assert "NativeScript debugger attached" not in output  # This is not in output when you attach to running app
        assert "Frontend socket closed" not in output
        assert "Backend socket closed" not in output
        assert "NativeScript debugger detached" not in output
        assert Process.is_running('NativeScript Inspector')

    def test_001_debug_ios_simulator(self):
        """
        Default `tns debug ios` starts debugger (do not stop at the first code statement)
        """
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': '', '--inspector': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_002_debug_ios_simulator_debug_brk(self):
        """
        Starts debugger and stop at the first code statement.
        """

        log = Tns.debug_ios(
            attributes={'--path': self.app_name, '--emulator': '', '--debug-brk': '', '--inspector': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME, tolerance=3.0, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_debug_brk')

    def test_003_debug_ios_simulator_start(self):
        """
        Attach the debug tools to a running app in the iOS Simulator
        """

        # Run the app and ensure it works
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': '', '--inspector': ''},
                          assert_success=False, timeout=30)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.IOS, output=log, prepare=Prepare.SKIP)
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Attach debugger
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': '', '--start': '', '--inspector': ''})
        self.__verify_debugger_attach(log=log)

    def test_100_debug_ios_simulator_with_livesync(self):
        """
        `tns debug ios` should be able to run with livesync
        """
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': '', '--inspector': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred', 'main-view-model.js', 'CONSOLE LOG',
                   'Backend socket closed', 'Frontend socket closed',
                   'Frontend client connected', 'Backend socket created', 'NativeScript debugger attached']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred', 'main-page.xml',
                   'Backend socket created', 'NativeScript debugger attached', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred', 'app.css', 'Backend socket created',
                   'NativeScript debugger attached', 'CONSOLE LOG']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml')

        assert Process.is_running('NativeScript Inspector')
