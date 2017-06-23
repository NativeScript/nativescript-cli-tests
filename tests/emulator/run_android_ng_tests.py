"""
Test for `tns run android` command on Angular projects

Run should sync all the changes correctly:
 - Valid changes in CSS, TS, HTML should be applied.
"""

import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.folder import Folder
from core.osutils.process import Process
from core.settings.settings import ANDROID_RUNTIME_PATH, EMULATOR_ID, EMULATOR_NAME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns


class RunAndroidEmulatorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)

        # Create default NG app (to get right dependencies from package.json)
        Tns.create_app_ng(self.app_name)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

        # Copy the app folder (app is modified in order to get some console logs on loaded)
        source = os.path.join('data', 'apps', 'livesync-hello-world-ng', 'app')
        target = os.path.join(self.app_name, 'app')
        Folder.cleanup(target)
        Folder.copy(src=source, dst=target)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    def test_001_tns_run_android_ts_css_html(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application',
                   'Application loaded!',
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify initial state of the app
        assert Device.wait_for_text(device_id=EMULATOR_ID, text="Ter Stegen",
                                    timeout=20), 'Hello-world NG App failed to start or it does not look correct!'

        # This is to ensure 'Change HTML and wait until app is synced' will be checked properly
        assert not Device.wait_for_text(device_id=EMULATOR_ID, text='9', timeout=5)

        # Change TS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_TS, sleep=10)
        strings = ['Successfully transferred', 'item.service.js', 'Successfully synced application',
                   'Application loaded!',  # This is to verify app is restarted.
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Stegen Ter", timeout=20)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'

        # Change HTML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_HTML, sleep=10)
        strings = ['items.component.html', 'Successfully synced application', 'Home page loaded!']
        not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='9', timeout=20)
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_CSS, sleep=10)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application', 'Home page loaded!']
        not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image='ng-hello-world-home-dark',
                            tolerance=5.0)

        # Revert HTML and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_HTML, sleep=10)
        strings = ['items.component.html', 'Successfully synced application', 'Home page loaded!']
        not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Stegen Ter", timeout=20)
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Revert TS and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_TS, sleep=10)
        strings = ['Successfully transferred', 'item.service.js', 'Successfully synced application',
                   'Application loaded!',  # This is to verify app is restarted.
                   'Home page loaded!']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Ter Stegen", timeout=20)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'

        # Revert CSS and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_CSS, sleep=10)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application', 'Home page loaded!']
        not_existing_strings = ['Application loaded!']  # This is to verify app is NOT restarted.
        Tns.wait_for_log(log_file=log, string_list=strings, not_existing_string_list=not_existing_strings)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='ng-hello-world-home-white', tolerance=5.0)
