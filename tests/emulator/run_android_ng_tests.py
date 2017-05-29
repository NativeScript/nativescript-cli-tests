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
        Tns.create_app_ng(self.app_name)
        Tns.platform_add_android(attributes={'--path': self.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

    def tearDown(self):
        Process.kill(proc_name='node')  # Stop 'node' to kill the livesync after each test method.
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
                   'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify initial state of the app
        assert Device.wait_for_text(device_id=EMULATOR_ID, text="Ter Stegen",
                                    timeout=20), 'Hello-world NG App failed to start or it does not look correct!'

        # This is to ensure 'Change HTML and wait until app is synced' will be checked properly
        assert not Device.wait_for_text(device_id=EMULATOR_ID, text='9', timeout=5)

        # Change TS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_TS, sleep=10)
        strings = ['Successfully transferred', 'item.service.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Stegen Ter", timeout=20)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'

        # Change HTML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_HTML, sleep=10)
        strings = ['Successfully transferred', 'items.component.html', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='9', timeout=20)
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.NG_CHANGE_CSS, sleep=10)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image='ng-hello-world-home-dark',
                            tolerance=5.0)

        # Revert HTML and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_HTML, sleep=10)
        strings = ['Successfully transferred', 'items.component.html', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Stegen Ter", timeout=20)
        assert text_changed, 'Changes in HTML file not applied (UI is not refreshed).'

        # Revert TS and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_TS, sleep=10)
        strings = ['Successfully transferred', 'item.service.js', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text="Ter Stegen", timeout=20)
        assert text_changed, 'Changes in TS file not applied (UI is not refreshed).'

        # Revert CSS and wait until app is synced
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.NG_CHANGE_CSS, sleep=10)
        strings = ['Successfully transferred', 'app.css', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='ng-hello-world-home-white', tolerance=5.0)
