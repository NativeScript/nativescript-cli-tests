"""
Test for `tns run android` command (on real devices).

Verify `tns run android`
- Run on all available devices
- Changes are synced on physical devices
- Emulator is not started if physical device is attached
- `tns run android --emulator` starts emulator even if device is connected
- `tns run android --emulator` should deploy only on emulator
- `tns run android --device` should deploy only on specified device

TODO: Add tests for:
`tns run android --device <avd-name>` -> Should be able to start avd image
`tns run android --device --emulator` -> We should throw nice error
`--available-devices` and `-timeout` options
"""

import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.settings.settings import ANDROID_PACKAGE, IOS_PACKAGE, SIMULATOR_NAME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class RunBothPlatformsTests(BaseClass):
    SIMULATOR_ID = ''
    ANDROID_DEVICES = Device.get_ids(platform=Platform.ANDROID, include_emulators=True)
    IOS_DEVICES = Device.get_ids(platform=Platform.IOS)
    DEVICE_ID = Device.get_id(platform=Platform.ANDROID)

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.ensure_available()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
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
        Emulator.stop()

    def test_001_tns_run_on_all_devices(self):

        # Build to speed up run after that
        Tns.build_android(attributes={'--path': self.app_name})
        Tns.build_ios(attributes={'--path': self.app_name})

        # `tns run` should deploy on all devices, emulators and simulators
        log = Tns.run(attributes={'--path': self.app_name}, wait=False, assert_success=False)
        strings = ['Successfully installed on device with identifier', self.SIMULATOR_ID]
        for android_device_id in self.ANDROID_DEVICES:
            strings.append(android_device_id)
        for ios_device_id in self.ANDROID_DEVICES:
            strings.append(ios_device_id)
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10, clean_log=False)

        # Verify app is deployed and running on all available android devices
        for device_id in self.ANDROID_DEVICES:
            Device.wait_until_app_is_running(app_id=Tns.get_app_id(self.app_name), device_id=device_id, timeout=30)

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        strings = ['Successfully transferred main-view-model.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        for device_id in self.ANDROID_DEVICES:
            text_changed = Device.wait_for_text(device_id=device_id, text='42 clicks left', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed) on ' + device_id

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        strings = ['Successfully transferred main-page.xml', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        for device_id in self.ANDROID_DEVICES:
            text_changed = Device.wait_for_text(device_id=device_id, text='TEST', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed) on ' + device_id

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        strings = ['Successfully transferred app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
