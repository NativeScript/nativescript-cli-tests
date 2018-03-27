"""
Verify tns features like run works properly with starter kit templates
"""
import unittest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_PACKAGE, IOS_PACKAGE, TYPESCRIPT_PACKAGE, \
    CURRENT_OS, WEBPACK_PACKAGE, EMULATOR_ID, SIMULATOR_NAME, SASS_PACKAGE
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from tests.webpack.helpers.helpers import Helpers


class StarterKitsTemplateTests(BaseClass):
    DEMOS = [
        'template-master-detail',
        'template-master-detail-ts',
        'template-master-detail-ng'
    ]

    xml_change = ['app/cars/cars-list-page.xml', 'Browse', 'Best Car Ever!']
    html_change = ['app/cars/car-list.component.html', 'Browse', 'Best Car Ever!']
    js_change = ['app/cars/shared/car-model.js', 'name: options.name,', 'name: options.transmission,']
    ts_change = ['app/cars/shared/car-model.ts', 'this._name = options.name;', 'this._name = options.transmission;']
    ts_change_ng = ['app/cars/shared/car.model.ts', 'this.name = options.name;', 'this.name = options.transmission;']
    sass_root_level_variable_change = ['app/_app-variables.scss', '$accent-dark: #3A53FF !default;',
                                       '$accent-dark: #FFFFFF !default;']
    sass_root_level_android_change = ["app/app.android.scss", "@import 'app-common';",
                                      "@import 'app-common'; .text-primary {color: $accent-dark;}"]
    sass_root_level_ios_change = ["app/app.ios.scss", "@import 'app-common';",
                                  "@import 'app-common'; .text-primary {color: $accent-dark;}"]
    sass_nested_level_change = ['app/cars/_cars-list-common.scss', 'padding: 8 15 4 15;', 'padding: 50 50 50 50;']

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
        Npm.uninstall(package="nativescript-dev-webpack", option='--save-dev', folder=demo)
        Npm.install(package=WEBPACK_PACKAGE, option='--save-dev', folder=demo)
        Npm.uninstall(package="nativescript-dev-sass", option='--save-dev', folder=demo)
        Npm.install(package=SASS_PACKAGE, option='--save-dev', folder=demo)
        if CURRENT_OS == OSType.OSX:
            Tns.platform_add_ios(attributes={'--path': demo, '--frameworkPath': IOS_PACKAGE})

    @parameterized.expand(DEMOS)
    def test_100_run_android(self, demo):
        Tns.kill()
        log = Tns.run_android(attributes={'--path': demo,
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=180)
        Helpers.android_screen_match(image=demo + '_home', tolerance=1.0)

        # Change JS, XML and CSS
        if '-ng' in demo:
            ReplaceHelper.replace(demo, self.ts_change_ng)
            ReplaceHelper.replace(demo, self.html_change)
        if '-ts' in demo:
            ReplaceHelper.replace(demo, self.ts_change)
            ReplaceHelper.replace(demo, self.xml_change)
        else:
            ReplaceHelper.replace(demo, self.js_change)
            ReplaceHelper.replace(demo, self.xml_change)
            assert Device.wait_for_text("Best Car Ever!"), "XML Changes not applied!"
        ReplaceHelper.replace(demo, self.sass_root_level_variable_change)
        ReplaceHelper.replace(demo, self.sass_root_level_android_change)
        ReplaceHelper.replace(demo, self.sass_nested_level_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.android_screen_match(image=demo + '_sync')

        # Revert changes
        if '-ng' in demo:
            ReplaceHelper.rollback(demo, self.ts_change_ng)
            ReplaceHelper.rollback(demo, self.html_change)
        if '-ts' in demo:
            ReplaceHelper.rollback(demo, self.ts_change)
            ReplaceHelper.rollback(demo, self.xml_change)
        else:
            ReplaceHelper.rollback(demo, self.js_change)
            ReplaceHelper.rollback(demo, self.xml_change)
            assert Device.wait_for_text("Browse"), "XML Changes not applied!"
        ReplaceHelper.rollback(demo, self.sass_root_level_variable_change)
        ReplaceHelper.rollback(demo, self.sass_root_level_android_change)
        ReplaceHelper.rollback(demo, self.sass_nested_level_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.android_screen_match(image=demo + '_home')

    @parameterized.expand(DEMOS)
    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_100_run_ios(self, demo):
        Tns.kill()
        log = Tns.run_ios(attributes={'--path': demo, '--emulator': ''}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=demo + '_home', tolerance=1.0)
        Helpers.wait_webpack_watcher()

        # Change JS, XML and CSS
        if '-ng' in demo:
            ReplaceHelper.replace(demo, self.ts_change_ng)
            ReplaceHelper.replace(demo, self.html_change)
        if '-ts' in demo:
            ReplaceHelper.replace(demo, self.ts_change)
            ReplaceHelper.replace(demo, self.xml_change)
        else:
            ReplaceHelper.replace(demo, self.js_change)
            ReplaceHelper.replace(demo, self.xml_change)
        ReplaceHelper.replace(demo, self.sass_root_level_variable_change)
        ReplaceHelper.replace(demo, self.sass_root_level_ios_change)
        ReplaceHelper.replace(demo, self.sass_nested_level_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=demo + '_sync')

        # Revert changes
        if '-ng' in demo:
            ReplaceHelper.rollback(demo, self.ts_change_ng)
            ReplaceHelper.rollback(demo, self.html_change)
        if '-ts' in demo:
            ReplaceHelper.rollback(demo, self.ts_change)
            ReplaceHelper.rollback(demo, self.xml_change)
        else:
            ReplaceHelper.rollback(demo, self.js_change)
            ReplaceHelper.rollback(demo, self.xml_change)
        ReplaceHelper.rollback(demo, self.sass_root_level_variable_change)
        ReplaceHelper.rollback(demo, self.sass_root_level_ios_change)
        ReplaceHelper.rollback(demo, self.sass_nested_level_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.no_wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=demo + '_home')

    @parameterized.expand(DEMOS)
    def test_200_run_android_bundle(self, demo):
        Tns.kill()
        log = Tns.run_android(attributes={'--path': demo,
                                          '--bundle': '',
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=180)
        Helpers.android_screen_match(image=demo + '_home', tolerance=1.0)
        Helpers.wait_webpack_watcher()

        # Change JS, XML and CSS
        if '-ng' in demo:
            ReplaceHelper.replace(demo, self.ts_change_ng)
            ReplaceHelper.replace(demo, self.html_change)
        if '-ts' in demo:
            ReplaceHelper.replace(demo, self.ts_change)
            ReplaceHelper.replace(demo, self.xml_change)
        else:
            ReplaceHelper.replace(demo, self.js_change)
            ReplaceHelper.replace(demo, self.xml_change)
        ReplaceHelper.replace(demo, self.sass_root_level_variable_change)
        ReplaceHelper.replace(demo, self.sass_root_level_android_change)
        ReplaceHelper.replace(demo, self.sass_nested_level_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.android_screen_match(image=demo + '_sync')

        # Revert changes
        if '-ng' in demo:
            ReplaceHelper.rollback(demo, self.ts_change_ng)
            ReplaceHelper.rollback(demo, self.html_change)
        if '-ts' in demo:
            ReplaceHelper.rollback(demo, self.ts_change)
            ReplaceHelper.rollback(demo, self.xml_change)
        else:
            ReplaceHelper.rollback(demo, self.js_change)
            ReplaceHelper.rollback(demo, self.xml_change)
        ReplaceHelper.rollback(demo, self.sass_root_level_variable_change)
        ReplaceHelper.rollback(demo, self.sass_root_level_android_change)
        ReplaceHelper.rollback(demo, self.sass_nested_level_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.android_screen_match(image=demo + '_home')

    @parameterized.expand(DEMOS)
    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_200_run_ios_bundle(self, demo):
        Tns.kill()
        log = Tns.run_ios(attributes={'--path': demo, '--emulator': '', '--bundle': ''}, wait=False,
                          assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_run, not_existing_string_list=Helpers.wp_errors,
                         timeout=240)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=demo + '_home', tolerance=1.0)
        Helpers.wait_webpack_watcher()

        # Change JS, XML and CSS
        if '-ng' in demo:
            ReplaceHelper.replace(demo, self.ts_change_ng)
            ReplaceHelper.replace(demo, self.html_change)
        if '-ts' in demo:
            ReplaceHelper.replace(demo, self.ts_change)
            ReplaceHelper.replace(demo, self.xml_change)
        else:
            ReplaceHelper.replace(demo, self.js_change)
            ReplaceHelper.replace(demo, self.xml_change)
        ReplaceHelper.replace(demo, self.sass_root_level_variable_change)
        ReplaceHelper.replace(demo, self.sass_root_level_ios_change)
        ReplaceHelper.replace(demo, self.sass_nested_level_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=demo + '_sync')

        # Revert changes
        if '-ng' in demo:
            ReplaceHelper.rollback(demo, self.ts_change_ng)
            ReplaceHelper.rollback(demo, self.html_change)
        if '-ts' in demo:
            ReplaceHelper.rollback(demo, self.ts_change)
            ReplaceHelper.rollback(demo, self.xml_change)
        else:
            ReplaceHelper.rollback(demo, self.js_change)
            ReplaceHelper.rollback(demo, self.xml_change)
        ReplaceHelper.rollback(demo, self.sass_root_level_variable_change)
        ReplaceHelper.rollback(demo, self.sass_root_level_ios_change)
        ReplaceHelper.rollback(demo, self.sass_nested_level_change)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=Helpers.wp_sync, not_existing_string_list=Helpers.wp_errors)
        Helpers.ios_screen_match(sim_id=self.SIMULATOR_ID, image=demo + '_home')
