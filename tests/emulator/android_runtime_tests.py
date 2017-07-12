"""
Test for specific needs of Android runtime.
"""
import os
import subprocess
import threading
from time import sleep

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.helpers.adb import ADB_PATH, Adb
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, EMULATOR_ID
from core.tns.tns import Tns


class RuntimeTests(BaseClass):
    custom_js_file = os.path.join(BaseClass.app_name, "app", "my-custom-class.js")
    tns_folder = os.path.join(BaseClass.app_name, "platforms", "android", "src", "main", "java", "com", "tns")
    gen_folder = os.path.join(tns_folder, "gen")
    generated_java_file = os.path.join(tns_folder, "MyJavaClass.java")

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.ensure_available()
        Folder.cleanup('./' + cls.app_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    def test_200_calling_custom_generated_classes_declared_in_manifest(self):
        Tns.create_app(self.app_name, attributes={"--template": os.path.join("data", "apps", "sbg-test-app.tgz")})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH, "--path": self.app_name})
        Adb.clear_logcat(device_id=EMULATOR_ID)
        Tns.run_android(attributes={"--path": self.app_name, "--device": EMULATOR_ID, "--justlaunch": ""})
        sleep(10)
        output = Adb.get_logcat(device_id=EMULATOR_ID)

        # make sure app hasn't crashed
        assert "Displayed org.nativescript.TNSApp/com.tns.ErrorReportActivity" not in output, \
            "App crashed with error activity"
        # check if we got called from custom activity that overrides the default one
        assert "we got called from onCreate of custom-nativescript-activity.js" in output, "Expected output not found"
        # make sure we called custom activity declared in manifest
        assert "we got called from onCreate of my-custom-class.js" in output, "Expected output not found"

    def test_300_verbose_log_android(self):
        Tns.create_app(self.app_name,
                       attributes={"--template": os.path.join("data", "apps", "verbose-hello-world.tgz")})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH, "--path": self.app_name})

        output = File.cat(os.path.join(self.app_name, "app", "app.js"))
        assert "__enableVerboseLogging()" in output, "Verbose logging not enabled in app.js"

        # `tns run android` and wait until app is deployed
        log = Tns.run_android(attributes={'--path': self.app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', EMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10, clean_log=False)
        sleep(10)

        log_string = File.read(log)
        assert "TNS.Native" in log_string, "__enableVerboseLogging() do not enable TNS.Native logs!"
        assert "TNS.Java" in log_string, "__enableVerboseLogging() do not enable TNS.Java logs!"
