"""
Test for android error activity.

Verify that:
 - If error happens error activity is displayed (debug mode).
 - Stack trace of the error is printed in console.
 - No error activity in release builds.
"""

import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_RUNTIME_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_ID, CURRENT_OS
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns


class AndroidErrorActivityTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)

        Tns.create_app(cls.app_name,
                       attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                       update_modules=True)
        Tns.platform_add_android(attributes={'--path': cls.app_name, '--frameworkPath': ANDROID_RUNTIME_PATH})

        # Break the app to test error activity
        file_change = ['app/app.js', 'application.start("main-page");', 'throw new Error("Kill the app!");']
        ReplaceHelper.replace(cls.app_name, file_change=file_change)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    @unittest.skipIf(CURRENT_OS == OSType.LINUX, "Temporary ignore on Linux.")
    def test_200_error_activity_shown_on_error(self):
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built',
                   'Successfully installed on device with identifier', EMULATOR_ID,
                   'Successfully synced application',
                   'Error: Kill the app!']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        assert Adb.wait_for_text(device_id=EMULATOR_ID, text="Exception"), "Error activity not found!"
        assert Adb.wait_for_text(device_id=EMULATOR_ID, text="Logcat"), "Error activity not found!"
        assert Adb.wait_for_text(device_id=EMULATOR_ID, text="Error: Kill the app!"), "Error activity not found!"

    def test_400_no_error_activity_in_release_builds(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          '--device': EMULATOR_ID,
                                          '--keyStorePath': ANDROID_KEYSTORE_PATH,
                                          '--keyStorePassword': ANDROID_KEYSTORE_PASS,
                                          '--keyStoreAlias': ANDROID_KEYSTORE_ALIAS,
                                          '--keyStoreAliasPassword': ANDROID_KEYSTORE_ALIAS_PASS,
                                          '--release': ''}, wait=False, assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        error = Adb.wait_for_text(device_id=EMULATOR_ID, text="Exception")
        assert not error, "Error activity found in release build!"
