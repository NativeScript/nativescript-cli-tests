import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.chrome.chrome import Chrome
from core.osutils.file import File
from core.settings.settings import ANDROID_PACKAGE, IOS_PACKAGE
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.osutils.command import run
from time import sleep
from enum import Enum
from core.osutils.process import Process

class DebugMode(Enum):
    DEFAULT = 0
    START = 1

class DebugBothPlatformsTests(BaseClass):
    ANDROID_DEVICES = Device.get_ids(platform=Platform.ANDROID, include_emulators=True)
    IOS_DEVICES = Device.get_ids(platform=Platform.IOS)
    DEVICE_ID = Device.get_id(platform=Platform.ANDROID)

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Device.ensure_available(platform=Platform.ANDROID)
        Device.ensure_available(platform=Platform.IOS)
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.IOS)

        Tns.create_app(cls.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_android(attributes={'--path': cls.app_name, '--frameworkPath': ANDROID_PACKAGE})
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})

    def setUp(self):
        BaseClass.setUp(self)
        Tns.kill()

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

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

    def __verify_debugger_start(self, log):
        strings = ['NativeScript Debugger started', 'To start debugging, open the following URL in Chrome',
                   'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output

    def __verify_debugger_attach(self, log):
        strings = ['To start debugging', 'Chrome', 'chrome-devtools', 'localhost:4000']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        output = File.read(file_path=log, print_content=True)
        assert "closed" not in output
        assert "detached" not in output
        assert "did not start in time" not in output
        assert "NativeScript Debugger started" not in output

    def test_001_tns_run_android(self):
        log = Tns.debug_android(attributes={'--path': self.app_name})
        strings = ['Successfully installed on device with identifier']
        for android_device_id in self.ANDROID_DEVICES:
            strings.append(android_device_id)
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)
        self.__verify_debugger_start(log)

        # Get Chrome URL and open it
        url = run(command="grep chrome-devtools " + log)
        Chrome.start(url)

    def test_002_tns_run_ios(self):
        log = Tns.debug_ios(attributes={'--path': self.app_name})
        self.attach_chrome(log)
        strings = ['Successfully started on device with identifier']
        Tns.wait_for_log(log_file=log, string_list= strings, clean_log=False)
        self.assert_not_detached(log)
