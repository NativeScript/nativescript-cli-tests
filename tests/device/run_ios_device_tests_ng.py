"""
Test for `tns run ios` command with Angular apps (on real devices).
"""

import os
from time import sleep

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform


class RunIOSDeviceTestsNG(BaseClass):
    SIMULATOR_ID = ''
    DEVICES = Device.get_ids(platform=Platform.IOS)
    DEVICE_ID = Device.get_id(platform=Platform.IOS)

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        Device.ensure_available(platform=Platform.IOS)
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.IOS)

        # Create default NG app (to get right dependencies from package.json)
        Tns.create_app_ng(cls.app_name)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})

        # Copy the app folder (app is modified in order to get some console logs on loaded)
        source = os.path.join('data', 'apps', 'livesync-hello-world-ng', 'src')
        target = os.path.join(cls.app_name, 'src')
        Folder.cleanup(target)
        Folder.copy(src=source, dst=target)

    def setUp(self):
        BaseClass.setUp(self)
        Tns.kill()

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Simulator.stop()

    def test_001_tns_run_ios_ts_css_html(self):
        """Make valid changes in TS,CSS and XML"""

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--device': self.DEVICE_ID}, wait=False,
                          assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', self.DEVICE_ID,
                   'Successfully synced application',
                   'Application loaded!',
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=240, check_interval=10)

        # Verify initial state of the app
        assert Device.wait_for_text(device_id=self.DEVICE_ID, text="Ter Stegen",
                                    timeout=20), 'Hello-world NG App failed to start or it does not look correct!'

        # Change TS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_TS, sleep=10)
        strings = ['Successfully transferred', 'item.service.js', 'Successfully synced application',
                   'Application loaded!',  # This is to verify app is restarted.
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings, clean_log=False)
        text_changed = Device.wait_for_text(device_id=self.DEVICE_ID, text="Stegen Ter", timeout=20)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'
        log_content = File.read(log)
        print log
        assert 'item.service.ts' not in log_content, "CLI should NOT transfer TS files!"
        assert log_content.count('Application loaded!') == 1, "Console log messages are doubled!"
        File.write(file_path=log, text="")  # Clean log

        # Change HTML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_HTML, sleep=10)
        strings = ['items.component.html', 'Successfully synced application', 'Home page loaded!']
        not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        sleep(15)
        text_changed = Device.wait_for_text(device_id=self.DEVICE_ID, text="1", timeout=5)
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_CSS, sleep=10)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application', 'Home page loaded!']
        not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        Device.screen_match(device_name="iPhone5", device_id=self.DEVICE_ID, expected_image='ng-hello-world-home-dark',
                            tolerance=5.0)

        # Revert HTML and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_HTML, sleep=10)
        strings = ['items.component.html', 'Successfully synced application', 'Home page loaded!']
        not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        text_changed = Device.wait_for_text(device_id=self.DEVICE_ID, text="Stegen Ter", timeout=20)
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Revert TS and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_TS, sleep=10)
        strings = ['Successfully transferred', 'item.service.js', 'Successfully synced application',
                   'Application loaded!',  # This is to verify app is restarted.
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=self.DEVICE_ID, text="Ter Stegen", timeout=20)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'

        # Revert CSS and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_CSS, sleep=10)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application']
        not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        Device.screen_match(device_name="iPhone5", device_id=self.DEVICE_ID, expected_image='ng-hello-world-home-white',
                            tolerance=5.0)
