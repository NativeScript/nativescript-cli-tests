"""
Tests for `tns debug ios` executed on iOS Simulator.
"""
import os
import time

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import IOS_RUNTIME_PATH, IOS_INSPECTOR_PACKAGE, SIMULATOR_NAME
from core.tns.tns import Tns
from core.settings.strings import *


class DebugSimulatorTests(BaseClass):

    INSPECTOR_GLOBAL_PATH = os.path.join(os.path.expanduser('~'), '.npm/tns-ios-inspector')

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')
        Emulator.stop()
        Simulator.stop()
        Simulator.start(name=SIMULATOR_NAME)
        Folder.cleanup(cls.INSPECTOR_GLOBAL_PATH)
        Tns.create_app(cls.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_RUNTIME_PATH})
        Npm.install(package=IOS_INSPECTOR_PACKAGE, option='--save-dev', folder=cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')

    def tearDown(self):
        BaseClass.tearDown(self)
        Process.kill('Safari')
        Process.kill('NativeScript Inspector')

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

    def test_001_debug_ios_simulator_debug_brk(self):
        print File.read(self.app_name + '/package.json')
        output = Tns.run_tns_command('debug ios', attributes={'--debug-brk': '',
                                                              '--emulator': '',
                                                              '--path': self.app_name,
                                                              '--frameworkPath': IOS_INSPECTOR_PACKAGE,
                                                              '--timeout': '200'
                                                              }, timeout=200)

        assert successfully_prepared in output
        assert successfully_built in output
        assert 'Setting up proxy' in output
        assert starting_simulator in output
        assert frontend_connected in output

        assert 'closed' not in output
        assert 'detached' not in output
        assert 'disconnected' not in output

    def test_002_debug_ios_simulator_start(self):
        print File.read(self.app_name + '/package.json')
        output = Tns.run_tns_command('emulate ios', attributes={'--path': self.app_name,
                                                                '--justlaunch': ''})
        assert 'started on device' in output
        time.sleep(15)

        output = Tns.run_tns_command('debug ios', attributes={'--start': '',
                                                              '--emulator': '',
                                                              '--path': self.app_name,
                                                              '--frameworkPath': IOS_INSPECTOR_PACKAGE,
                                                              '--timeout': '150'
                                                              }, timeout=150)
        assert frontend_connected in output
        assert 'closed' not in output
        assert 'detached' not in output
        assert 'disconnected' not in output
