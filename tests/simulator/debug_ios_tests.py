"""
Tests for `tns debug ios` executed on iOS Simulator.
"""
import os
import time

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.device_type import DeviceType
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_PATH, IOS_INSPECTOR_PACKAGE, SIMULATOR_NAME
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class DebugiOSSimulatorTests(BaseClass):
    SIMULATOR_ID = ''
    INSPECTOR_GLOBAL_PATH = os.path.join(os.path.expanduser('~'), '.npm/tns-ios-inspector')

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.start(name=SIMULATOR_NAME)
        Folder.cleanup(cls.INSPECTOR_GLOBAL_PATH)
        Tns.create_app(cls.app_name, attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_RUNTIME_PATH})
        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev', folder=cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')
        Process.kill('node')

    def tearDown(self):
        BaseClass.tearDown(self)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')
        Process.kill('node')

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    """
    Spec:

    | Usage                                                                             | Synopsis                                                                  |
    | Deploy on device, run the app, start Safari Web Inspector and attach the debugger | $ tns debug ios                                                           |
    | Deploy on device, run the app and stop at the first code statement                | $ tns debug ios --debug-brk [--device <Device ID>] [--no-client]          |
    |    Deploy in the iOS Simulator, run the app and stop at the first code statement  | $ tns debug ios --debug-brk --emulator [<Emulator Options>] [--no-client] |
    | Attach the debug tools to a running app on device                                 | $ tns debug ios --start [--device <Device ID>] [--no-client]              |
    | Attach the debug tools to a running app in the iOS Simulator                      | $ tns debug ios --start --emulator [<Emulator Options>] [--no-client]     |

    Prepares, builds and deploys the project when necessary. Debugs your project on a connected device or in the iOS Simulator.
    While debugging, prints the output from the application in the console and watches for changes in your code. Once a change is detected, it synchronizes the change with all selected devices and restarts/refreshes the application.

    IMPORTANT: Before building for iOS device, verify that you have configured a valid pair of certificate and provisioning profile on your OS X system.

    ### Options

        * --device - Specifies a connected device on which to run the app.
        * --emulator - Indicates that you want to debug your app in the iOS simulator.
        * --debug-brk - Prepares, builds and deploys the application package on a device or in an emulator, runs the app, launches the developer tools of your Safari browser and stops at the first code statement.
        * --start - Attaches the debug tools to a deployed and running app and launches the developer tools of your Safari browser.
        * --no-client - If set, the NativeScript CLI attaches the debug tools but does not launch the developer tools in Safari.
        * --timeout - Sets the number of seconds that NativeScript CLI will wait for the debugger to boot. If not set, the default timeout is 90 seconds.
        * --no-watch - If set, changes in your code will not be reflected during the execution of this command.
        * --clean - If set, forces rebuilding the native application.

    ### Attributes

        * <Device ID> is the index or name of the target device as listed by $ tns device
        * <Emulator Options> is any valid combination of options as listed by $ tns help emulate ios

    """

    def __verify_debugger_start(self, log):
        strings = [self.SIMULATOR_ID, "Frontend client connected", "Backend socket created",
                   "NativeScript debugger attached"]
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
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

    def test_002_debug_ios_simulator_debug_brk(self):
        """
        Starts debugger and stop at the first code statement.
        """

        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': '', '--debug-brk': ''})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME, tolerance=3.0,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_debug_brk')

    def test_003_debug_ios_simulator_start(self):
        """
        Attach the debug tools to a running app in the iOS Simulator
        """

        # Run the app and ensure it works
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--justlaunch': ''},
                          assert_success=False, timeout=30)
        TnsAsserts.prepared(app_name=self.app_name, platform=Platform.IOS, output=log, prepare=Prepare.SKIP)
        Device.screen_match(device_type=DeviceType.SIMULATOR, device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='livesync-hello-world_home')

        # Attach debugger
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--emulator': '', '--start': ''})
        self.__verify_debugger_attach(log=log)
