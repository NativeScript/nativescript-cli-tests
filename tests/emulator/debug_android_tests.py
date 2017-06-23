"""
Tests for `tns debug android` executed on Android Emulator.
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import EMULATOR_NAME, EMULATOR_ID, ANDROID_RUNTIME_PATH
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class DebugAndroidEmulatorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.create_app(self.app_name, attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world')},
                       update_modules=True)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    """
    Spec:

    Usage                                                                           Synopsis                                                                                          
    Deploy on device, run the app start Chrome DevTools, and attach the debugger    $ tns debug android                                                                               
    Deploy on device, run the app and stop at the first code statement              $ tns debug android --debug-brk [--device <Device ID>] [--debug-port <port>] [--timeout <timeout>]
    Deploy in the native emulator, run the app and stop at the first code statement $ tns debug android --debug-brk --emulator [<Emulator Options>] [--timeout <timeout>]             
    Attach the debug tools to a running app on device                               $ tns debug android --start [--device <Device ID>] [--debug-port <port>] [--timeout <timeout>]    
    Attach the debug tools to a running app in the native emulator                  $ tns debug android --start --emulator [<Emulator Options>] [--timeout <timeout>]                 
    Detach the debug tools                                                          $ tns debug android --stop                                                                        


    Prepares, builds and deploys the project when necessary. Debugs your project on a connected device or emulator.
    While debugging, prints the output from the application in the console and watches for changes in your code. Once a change is detected, it synchronizes the change with all selected devices and restarts/refreshes the application.

    ### Options

        * --device - Specifies a connected device on which to debug the app.
        * --emulator - Specifies that you want to debug the app in the native Android emulator from the Android SDK.
        * --debug-brk - Prepares, builds and deploys the application package on a device or in an emulator, launches the Chrome DevTools of your Chrome browser and stops at the first code statement.
        * --start - Attaches the debug tools to a deployed and running app.
        * --stop - Detaches the debug tools.
        * --debug-port - Sets a new port on which to attach the debug tools.
        * --timeout - Sets the number of seconds that the NativeScript CLI will wait for the debugger to boot. If not set, the default timeout is 90 seconds.
        * --no-watch - If set, changes in your code will not be reflected during the execution of this command.
        * --clean - If set, forces rebuilding the native application.

    ### Attributes

        * <Device ID> is the index or name of the target device as listed by $ tns device
        * <Port> is an accessible port on the device to which you want to attach the debugging tools.
        * <Emulator Options> is any valid combination of options as listed by $ tns help emulate android
    """

    def __verify_debugger_start(self, log):
        strings = [EMULATOR_ID, 'NativeScript Debugger started', 'To start debugging, open the following URL in Chrome',
                   'chrome-devtools', 'localhost:40000']
        if Device.get_count(platform=Platform.ANDROID) > 0:
            strings.append("Multiple devices found! Starting debugger on emulator")
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output

    def __verify_debugger_attach(self, log):
        strings = [EMULATOR_ID, 'To start debugging', 'Chrome', 'chrome-devtools', 'localhost:40000']
        if Device.get_count(platform=Platform.ANDROID) > 0:
            strings.append("Multiple devices found! Starting debugger on emulator")
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output
        assert "NativeScript Debugger started" not in output

    def test_001_debug_android(self):
        """
        Default `tns debug android` starts debugger (do not stop at the first code statement)
        """
        log = Tns.debug_android(attributes={'--path': self.app_name})
        self.__verify_debugger_start(log)

        # Verify app starts and do not stop on first line of code
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    def test_002_debug_android_emulator_debug_brk(self):
        """
        Starts debugger and stop at the first code statement.
        """

        log = Tns.debug_android(attributes={'--path': self.app_name, '--debug-brk': ''})
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
        log = Tns.debug_android(attributes={'--path': self.app_name, '--start': ''})
        self.__verify_debugger_attach(log=log)
