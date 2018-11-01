import unittest

import os

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, CURRENT_OS, \
    IOS_PACKAGE, SIMULATOR_NAME, ANDROID_PACKAGE, WEBPACK_PACKAGE
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from tests.hmr.helpers_hmr import HelpersHMR
from tests.webpack.helpers.helpers import Helpers
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
        Helpers.emulator_cleanup(app_name=self.app_name)
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

        HelpersHMR.apply_changes(app_name=self.app_name, log=log, platform=Platform.IOS)
        HelpersHMR.revert_changes(app_name=self.app_name, log=log, platform=Platform.IOS)

    def test_002_ios_run_hmr_uninstall_app(self):
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                            assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.run_hmr_with_platforms, not_existing_string_list=HelpersHMR.errors_hmr,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)

        HelpersHMR.apply_changes_js(app_name=self.app_name, log=log, platform=Platform.IOS)

        # Uninstall app while `tns run` is running
        Device.uninstall_app(app_prefix='org.nativescript.', platform=Platform.IOS)

        HelpersHMR.revert_changes_js(app_name=self.app_name, log=log, platform=Platform.IOS)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)

    def test_003_ios_run_hmr_console_log(self):
        source_js = os.path.join('data', "issues", 'console-log-hmr', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': '', '--hmr': ''}, wait=False,
                                assert_success=False)
        strings = ['LOG Hello']
        Tns.wait_for_log(log_file=log, string_list=strings)

        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=HelpersHMR.image_original, timeout=120)

    # def test_004_android_run_hmr_delete_file(self):
    #     log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID, '--hmr': ''}, wait=False,
    #                     assert_success=False)
    #
    #     Tns.wait_for_log(log_file=log, string_list=HelpersHMR.wp_run, not_existing_string_list=HelpersHMR.wp_errors,
    #                      timeout=240)
    #     HelpersHMR.android_screen_match(image=self.image_original, timeout=120)
    #     File.remove(self.app_name + 'app', 'main-view-model.js')
    #
    #     self.apply_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)
    #     self.revert_changes(app_name=self.app_name, log=log, platform=Platform.ANDROID)