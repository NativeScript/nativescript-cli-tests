"""
Verify tns features like run works properly with starter kit templates
"""
import unittest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_PACKAGE, IOS_PACKAGE, TYPESCRIPT_PACKAGE, \
    CURRENT_OS, WEBPACK_PACKAGE, EMULATOR_ID, SIMULATOR_NAME
from core.tns.tns import Tns
from tests.webpack.helpers.helpers import Helpers


class StarterKitsTemplateTests(BaseClass):
    DEMOS = [
        'template-master-detail',
        'template-master-detail-ts',
        'template-master-detail-ng'
    ]

    SIMULATOR_ID = ""

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Npm.cache_clean()
        Emulator.stop()
        Emulator.ensure_available()
        if CURRENT_OS == OSType.OSX:
            Simulator.stop()
            cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)

    def setUp(self):
        Tns.kill()
        BaseClass.tearDown(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @parameterized.expand(DEMOS)
    def test_000_prepare_apps(self, demo):
        Tns.create_app(demo, attributes={"--template": "https://github.com/NativeScript/" + demo})
        Tns.platform_add_android(attributes={"--path": demo, "--frameworkPath": ANDROID_PACKAGE})
        if "-ng" in demo:
            Tns.update_angular(demo)
        if "-ng" in demo or "-ts" in demo:
            Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev', folder=demo)
            Npm.install(package=TYPESCRIPT_PACKAGE, option='--save-dev', folder=demo)
            Npm.install(package=WEBPACK_PACKAGE, option='--save-dev', folder=demo)

        if CURRENT_OS == OSType.OSX:
            Tns.platform_add_ios(attributes={'--path': demo, '--frameworkPath': IOS_PACKAGE})

    @parameterized.expand(DEMOS)
    def test_100_run_android(self, demo):
        log = Tns.run_android(attributes={'--path': demo,
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=180)
        Helpers.android_screen_match(image=demo + '_home')

    @parameterized.expand(DEMOS)
    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_100_run_ios(self, demo):
        log = Tns.run_ios(attributes={'--path': demo, '--emulator': '', '--bundle': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=demo + '_home')
        Helpers.wait_webpack_watcher()

    @parameterized.expand(DEMOS)
    def test_200_run_android_bundle(self, demo):
        log = Tns.run_android(attributes={'--path': demo,
                                          '--bundle': '',
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=180)
        Helpers.android_screen_match(image=demo + '_home')
        Helpers.wait_webpack_watcher()

    @parameterized.expand(DEMOS)
    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_200_run_ios_bundle(self, demo):
        log = Tns.run_ios(attributes={'--path': demo, '--emulator': '', '--bundle': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=demo + '_home')
        Helpers.wait_webpack_watcher()
