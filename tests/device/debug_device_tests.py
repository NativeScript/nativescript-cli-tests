import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.chrome.chrome import Chrome
from core.osutils.file import File
from core.settings.settings import ANDROID_PACKAGE, IOS_PACKAGE
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.osutils.command import run

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

        # Verify app is deployed and running on all available android devices
        for device_id in self.ANDROID_DEVICES:
            Device.wait_until_app_is_running(app_id=Tns.get_app_id(self.app_name), device_id=device_id, timeout=30)

        log = Tns.debug_android(attributes={'--path': self.app_name})
        self.__verify_debugger_start(log)

        # Get Chrome URL and open it
        url = run(command="grep chrome-devtools " + log)
        Chrome.start(url)

    def test_002_tns_run_ios(self):
        log = Tns.debug_ios(attributes={'--path': self.app_name})
        strings = ['Successfully installed on device with identifier']
        for ios_device_id in self.IOS_DEVICES:
            strings.append(ios_device_id)
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)

        log = Tns.debug_ios(attributes={'--path': self.app_name})
        self.__verify_debugger_start(log)

        # Get Chrome URL and open it
        url = run(command="grep chrome-devtools " + log)
        Chrome.start(url)
