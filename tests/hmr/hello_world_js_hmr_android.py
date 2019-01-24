import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.osutils.file import File
from core.settings.settings import EMULATOR_ID, ANDROID_PACKAGE, WEBPACK_PACKAGE, EMULATOR_NAME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.hmr.helpers_hmr import HelpersHMR
from tests.webpack.helpers.helpers import Helpers
from core.device.device import Device
# import hashlib
# import re


class HelloWorldJSHMRAndroid(BaseClass):


    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

        Tns.create_app(cls.app_name, update_modules=True)
        Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})

    def setUp(self):
        Tns.kill()
        Helpers.emulator_cleanup(app_name=self.app_name)
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_001_android_run_hmr(self):
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                        assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.run_hmr, not_existing_string_list=HelpersHMR.errors_hmr,
                         timeout=240)
        Helpers.android_screen_match(image=HelpersHMR.image_original, timeout=120)

        HelpersHMR.apply_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
        HelpersHMR.revert_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)

    def test_002_android_run_hmr_uninstall_app(self):
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                        assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.run_hmr_with_platforms, not_existing_string_list=HelpersHMR.errors_hmr,
                         timeout=240)
        Helpers.android_screen_match(image=HelpersHMR.image_original, timeout=120)

        HelpersHMR.apply_changes_js(app_name=self.app_name, log=log, platform=Platform.ANDROID)

        # Uninstall app while `tns run` is running
        Device.uninstall_app(app_prefix='org.nativescript.', platform=Platform.ANDROID)

        ReplaceHelper.rollback(self.app_name, HelpersHMR.js_change, sleep=10)
        strings = ['Restarting application on device', 'HMR: Hot Module Replacement Enabled. Waiting for signal.']
        Tns.wait_for_log(log_file=log, string_list=strings)

        Helpers.android_screen_match(image=HelpersHMR.image_original, timeout=120)

    @unittest.skip("https://github.com/NativeScript/nativescript-cli/issues/4123")
    def test_003_android_run_hmr_wrong_xml(self):
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                              assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.run_hmr,
                         not_existing_string_list=HelpersHMR.errors_hmr, timeout=240)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image=HelpersHMR.image_original)

        # Break the app with invalid xml changes
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML_INVALID_SYNTAX)

        # Verify console notify user for broken xml
        # strings = ['for activity org.nativescript.TestApp / com.tns.ErrorReportActivity']
        strings = ['com.tns.NativeScriptException', 'Parsing XML at', 'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)
        assert Adb.wait_for_text(device_id=EMULATOR_ID, text="Exception", timeout=30), "Error activity not found!"

        # Revert changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML_INVALID_SYNTAX)
        strings = ['JS: HMR: Hot Module Replacement Enabled. Waiting for signal.',
                   'Successfully synced application', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image=HelpersHMR.image_original)

    def test_008_android_run_hmr_console_log(self):
        source_js = os.path.join('data', "issues", 'console-log-hmr', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                              assert_success=False)

        strings = ['LOG Hello']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=120, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image=HelpersHMR.image_original)

    @unittest.skip("Don't clear behavior")
    def test_009_android_run_hmr_delete_file(self):
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                        assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.wp_run, not_existing_string_list=HelpersHMR.wp_errors,
                         timeout=240)
        HelpersHMR.android_screen_match(image=self.image_original, timeout=120)
        File.remove(self.app_name + 'app', 'main-view-model.js')

        self.apply_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
        self.revert_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
