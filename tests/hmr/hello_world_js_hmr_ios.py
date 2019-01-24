import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.simulator import Simulator
from core.osutils.file import File
from core.settings.settings import IOS_PACKAGE, SIMULATOR_NAME, WEBPACK_PACKAGE, EMULATOR_ID
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.hmr.helpers_hmr import HelpersHMR
from core.tns.replace_helper import ReplaceHelper
from tests.webpack.helpers.helpers import Helpers
from core.device.device import Device
# import hashlib
# import re

class HelloWorldJSHMRIOS(BaseClass):


    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)

        Tns.create_app(cls.app_name, update_modules=True)
        Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=cls.app_name)
        Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})

    def setUp(self):
        Tns.kill()
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_001_ios_run_hmr(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                        assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.run_hmr, not_existing_string_list=HelpersHMR.errors_hmr,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)
        Helpers.wait_webpack_watcher()

        HelpersHMR.apply_changes(app_name=self.app_name, log=log, platform=Platform.IOS)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_change,
                                 timeout=120)
        HelpersHMR.revert_changes(app_name=self.app_name, log=log, platform=Platform.IOS)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original,
                                 timeout=120)

    def test_002_ios_run_hmr_uninstall_app(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                            assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.run_hmr_with_platforms, not_existing_string_list=HelpersHMR.errors_hmr,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)
        Helpers.wait_webpack_watcher()
        
        # Change file to trigger livesync
        ReplaceHelper.replace(self.app_name, HelpersHMR.js_change, sleep=10)

        # Uninstall app while `tns run` is running
        Simulator.uninstall("org.nativescript." + self.app_name)

        # Verify app is installed on device again and changes are synced
        strings = ['Webpack compilation complete', 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=self.SIMULATOR_ID, text='42 clicks left')
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        HelpersHMR.revert_changes_js(app_name=self.app_name, log=log, platform=Platform.IOS)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)
        Helpers.wait_webpack_watcher()

    @unittest.skip("https://github.com/NativeScript/nativescript-cli/issues/4123")
    def test_003_ios_run_hmr_wrong_xml(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                            assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.run_hmr_with_platforms, not_existing_string_list=HelpersHMR.errors_hmr,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)
        Helpers.wait_webpack_watcher()

        HelpersHMR.apply_changes_js(app_name=self.app_name, log=log, platform=Platform.IOS)

        # Uninstall app while `tns run` is running
        Simulator.uninstall("org.nativescript." + self.app_name)

        HelpersHMR.revert_changes_js(app_name=self.app_name, log=log, platform=Platform.IOS)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)
        Helpers.wait_webpack_watcher()

    def test_008_ios_run_hmr_console_log(self):
        source_js = os.path.join('data', "issues", 'console-log-hmr', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                                assert_success=False)
        strings = ['LOG Hello']
        Tns.wait_for_log(log_file=log, string_list=strings)

        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)

    @unittest.skip("Don't clear behavior")
    def test_004_android_run_hmr_delete_file(self):
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
                        assert_success=False)

        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.wp_run, not_existing_string_list=HelpersHMR.wp_errors,
                         timeout=240)
        HelpersHMR.android_screen_match(image=self.image_original, timeout=120)
        File.remove(self.app_name + 'app', 'main-view-model.js')

        self.apply_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
        self.revert_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)