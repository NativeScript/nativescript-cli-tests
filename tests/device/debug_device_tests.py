import os

from core.base_class.BaseClass import BaseClass
from core.chrome.chrome import Chrome
from core.device.device import Device
from core.osutils.command import run
from core.settings.settings import ANDROID_PACKAGE, IOS_PACKAGE
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.helpers.debug_chrome import DebugChromeHelpers


class DebugOnDevice(BaseClass):
    ANDROID_DEVICE_ID = Device.get_id(platform=Platform.ANDROID)
    IOS_DEVICE_ID = Device.get_id(platform=Platform.IOS)

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

    def test_001_debug_android(self):
        log = Tns.debug_android(attributes={'--path': self.app_name, '--device': self.ANDROID_DEVICE_ID})
        strings = [self.ANDROID_DEVICE_ID, 'Successfully installed on device with identifier']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=240, check_interval=10, clean_log=False)
        DebugChromeHelpers.verify_debugger_started(log)

        # Get Chrome URL and open it
        url = run(command="grep chrome-devtools " + log)
        Chrome.start(url)

    def test_002_debug_ios(self):
        log = Tns.debug_ios(attributes={'--path': self.app_name, '--device': self.IOS_DEVICE_ID})
        DebugChromeHelpers.attach_chrome(log)
        strings = [self.IOS_DEVICE_ID, 'Successfully started on device with identifier']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)
        DebugChromeHelpers.assert_not_detached(log)
