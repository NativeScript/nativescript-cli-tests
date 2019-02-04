# -*- coding: utf-8 -*-
"""
Test for `tns run ios` command with Angular apps (on simulator).
"""

import os

from nose.tools import timed

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE, SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.tns import Tns


class IOSRuntimeTests(BaseClass):
    SIMULATOR_ID = ''
    plugin_path = os.path.join(TEST_RUN_HOME, 'data', 'plugins', 'sample-plugin', 'src')

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Folder.cleanup(cls.app_name)

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

    @staticmethod
    def create_ng_app(app_name):
        # Create default NG app (to get right dependencies from package.json)
        Tns.create_app_ng(app_name)
        Tns.platform_add_ios(attributes={'--path': app_name, '--frameworkPath': IOS_PACKAGE})

        # Copy the app folder (app is modified in order to get some console logs on loaded)
        source = os.path.join('data', 'apps', 'livesync-hello-world-ng', 'src')
        target = os.path.join(app_name, 'src')
        Folder.cleanup(target)
        Folder.copy(src=source, dst=target)

    @timed(360)
    def test_201_test_init_mocha_js_stacktrace(self):
        # https://github.com/NativeScript/ios-runtime/issues/565
        Tns.create_app(app_name=self.app_name)
        Npm.install(package='mocha', folder=self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE})
        Tns.run_tns_command("test init", attributes={"--framework": "mocha", "--path": self.app_name})

        copy = os.path.join('data', 'issues', 'ios-runtime-565', 'example.js')
        paste = os.path.join(self.app_name, 'app', 'tests')
        Folder.copy(copy, paste)

        output = File.read(self.app_name + "/app/tests/example.js")
        assert "Mocha test" in output
        assert "Test" in output
        assert "Array" not in output

        output = Tns.run_tns_command("test ios", attributes={"--emulator": "", "--path": self.app_name},
                                     log_trace=True, wait=False)
        strings = ['JavaScript stack trace', '@file:///app/tests/example.js:5:25']
        Tns.wait_for_log(log_file=output, string_list=strings, timeout=90)

    def test_280_tns_run_ios_console_time(self):
        self.create_ng_app(self.app_name)
        # Replace app.component.ts to use console.time() and console.timeEnd()
        source = os.path.join('data', 'issues', 'ios-runtime-843', 'app.component.ts')
        target = os.path.join(self.app_name, 'src', 'app', 'app.component.ts')
        File.copy(src=source, dest=target)

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False,
                          assert_success=False)

        # Verify initial state of the app
        strings = ['Project successfully built', 'Successfully installed on device with identifier', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)

        assert Device.wait_for_text(device_id=self.SIMULATOR_ID, text="Ter Stegen",
                                    timeout=20), 'Hello-world NG App failed to start or it does not look correct!'

        # Verify console.time() works - issue https://github.com/NativeScript/ios-runtime/issues/843
        console_time = ['CONSOLE INFO startup:']
        Tns.wait_for_log(log_file=log, string_list=console_time)

    def test_290_tns_run_ios_console_dir(self):
        # NOTE: This test depends on creation of app in test_280_tns_run_ios_console_time
        # Replace app.component.ts to use console.time() and console.timeEnd()
        source = os.path.join('data', 'issues', 'ios-runtime-875', 'items.component.ts')
        target = os.path.join(self.app_name, 'src', 'app', 'item', 'items.component.ts')
        File.copy(src=source, dest=target)

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False,
                          assert_success=False, log_trace=True)

        # Verify sync and initial state of the app
        strings = ['name: Ter Stegen', 'role: Goalkeeper', 'object dump end', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=90, check_interval=10, clean_log=False)

    def test_380_tns_run_ios_plugin_dependencies(self):
        """
        issue https://github.com/NativeScript/ios-runtime/issues/890
        Check app is running when reference plugin A - plugin A depends on plugin B which depends on plugin C.
        Plugin A has dependency only to plugin B.
        Old behavior (version < 4.0.0) was in plugin A to reference plugin B and C.
        """

        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_PACKAGE})

        # Add plugin with specific dependencies
        Tns.plugin_add(self.plugin_path, attributes={"--path": self.app_name})

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=150, check_interval=10)

        folder_path = os.path.join(os.getcwd(), self.app_name, "platforms", "ios", self.app_name, "app",
                                   "tns_modules", "nativescript-ui-core")
        assert Folder.exists(folder_path), "Cannot find folder: " + folder_path

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    def test_385_methods_with_same_name_and_different_parameters(self):
        """
        https://github.com/NativeScript/ios-runtime/issues/877
        PR https://github.com/NativeScript/ios-runtime/pull/1013
        """

        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_PACKAGE})

        # Add plugin with specific dependencies
        Tns.plugin_add(self.plugin_path, attributes={"--path": self.app_name})

        # Replace main-page.js to call methods with the same name but different parameters count
        source_js = os.path.join('data', "issues", 'ios-runtime-877', 'main-page.js')
        target_js = os.path.join(self.app_name, 'app', 'main-page.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', self.SIMULATOR_ID,
                   ' SayName no param!', 'SayName with 1 param!', 'SayName with 2 params!']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=150, check_interval=10)

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='livesync-hello-world_home')

    def test_386_check_native_crash_will_not_crash_when_discardUncaughtJsExceptions_used(self):
        """
            Test native crash will not crash the app when discardUncaughtJsExceptions used
            https://github.com/NativeScript/ios-runtime/issues/1051
        """

        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name,
                       attributes={'--template': os.path.join('sut', 'tns-template-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_PACKAGE})

        source_js = os.path.join('data', "issues", 'ios-runtime-1051', 'app.js')
        target_js = os.path.join(self.app_name, 'app', 'app.js')
        File.copy(src=source_js, dest=target_js)

        source_js = os.path.join('data', "issues", 'ios-runtime-1051', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        # Change app package.json so it contains the options for discardUncaughtJsExceptions
        source_js = os.path.join('data', "issues", 'ios-runtime-1051', 'package.json')
        target_js = os.path.join(self.app_name, 'app', 'package.json')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)

        strings = ['Project successfully built',
                   'Successfully installed on device with identifier',
                   'Successfully synced application'
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=240, check_interval=10, clean_log=False)
        try:
            strings = ["CONSOLE LOG file:///app/app.js:4:16: The folder “not-existing-path” doesn’t exist.",
                       "JS: 1   contentsOfDirectoryAtPathError@file:///app/main-view-model.js:6:47"
                       ]
            Tns.wait_for_log(log_file=log, string_list=strings,
                             timeout=100, check_interval=10, clean_log=False)
            Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                                expected_image='no-crash-image', tolerance=1)
        except Exception as e:
            print str(e)
            assert 1 == 2, 'Native crash should not crash the app when discardUncaughtJsExceptions is used!'

    def test_387_test_pointers_and_conversions_to_string(self):
        """
            Test pointers and conversions to strings
            https://github.com/NativeScript/ios-runtime/pull/1069
            https://github.com/NativeScript/ios-runtime/issues/921
        """

        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name,
                       attributes={'--template': os.path.join('sut', 'tns-template-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_ios(attributes={'--path': self.app_name, '--frameworkPath': IOS_PACKAGE})

        source_js = os.path.join('data', "issues", 'ios-runtime-921', 'special-value', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)

        strings = ['Project successfully built',
                   'Successfully installed on device with identifier',
                   'Successfully synced application'
                   ]

        Tns.wait_for_log(log_file=log, string_list=strings, timeout=240, check_interval=10, clean_log=False)
        try:
            strings = ["<Pointer: 0xfffffffffffffffe>",
                       "<Pointer: 0xffffffffffffffff>",
                       "<Pointer: 0x800000000>"]

            Tns.wait_for_log(log_file=log, string_list=strings,
                             timeout=100, check_interval=10, clean_log=False)
        except Exception as e:
            print str(e)
            assert 1 == 2, '-1 pointer is not correct(interop.Pointer)!'

        source_js = os.path.join('data', "issues", 'ios-runtime-921', 'wrapped-value', 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        try:
            strings = ["wrapped: <Pointer: 0xfffffffffffffffe>",
                       "wrapped: <Pointer: 0xffffffffffffffff>",
                       "wrapped: <Pointer: 0x800000000>"]

            Tns.wait_for_log(log_file=log, string_list=strings,
                             timeout=100, check_interval=10, clean_log=False)
        except Exception as e:
            print str(e)
            assert 1 == 2, 'wrapped pointers are not working correctly(interop.Pointer(new Number(value)))!'

        source_js = os.path.join('data', "issues", 'ios-runtime-921', 'toHexString-and-toDecimalString',
                                 'main-view-model.js')
        target_js = os.path.join(self.app_name, 'app', 'main-view-model.js')
        File.copy(src=source_js, dest=target_js)

        try:
            strings = ["Hex: 0xfffffffffffffffe",
                       "Decimal: -2",
                       "Hex: 0xffffffffffffffff",
                       "Decimal: -1",
                       "Hex: 0x800000000",
                       "Decimal: 34359738368"]

            Tns.wait_for_log(log_file=log, string_list=strings,
                             timeout=100, check_interval=10, clean_log=False)
        except Exception as e:
            print str(e)
            assert 1 == 2, 'toHexString and toDecimalString are not working correctly!'
