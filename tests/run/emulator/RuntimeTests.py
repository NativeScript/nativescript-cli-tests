"""
Tests for static binding generator
"""
import os
import subprocess
import threading
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ADB_PATH, ANDROID_RUNTIME_PATH
from core.settings.strings import successfully_built
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
        Emulator.stop_emulators()
        Emulator.ensure_available()
        Folder.cleanup('./' + cls.app_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop_emulators()
        Folder.cleanup(cls.app_name)

    @unittest.skip("Fails due to known issue in SBG")
    def test_200_calling_custom_generated_classes_declared_in_manifest(self):
        Tns.create_app(self.app_name, attributes={"--template": os.path.join("data", "apps", "sbg-test-app")})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH, "--path": self.app_name})

        print ("Running app for android")
        if Emulator.ensure_available():
            subprocess.Popen([ADB_PATH, "-e", "logcat", "-c"])
        # run application
        Tns.run_android(attributes={"--emulator": "",
                                    "--path": self.app_name,
                                    "--timeout": "120",
                                    "--justlaunch": ""
                                    })

        # wait 2 seconds to get emulator logcat
        process = subprocess.Popen([ADB_PATH, "-e", "logcat"], stdout=subprocess.PIPE)
        threading.Timer(10, process.terminate).start()
        output = process.communicate()[0]

        # make sure app hasn't crashed
        assert "Displayed org.nativescript.TNSApp/com.tns.ErrorReportActivity" not in output, "App crashed with error activity"

        # check if we got called from custom activity that overrides the default one
        assert "we got called from onCreate of custom-nativescript-activity.js" in output, "Expected output not found"

        # make sure we called custom activity declared in manifest
        assert "we got called from onCreate of my-custom-class.js" in output, "Expected output not found"

    def test_300_verbose_log_android(self):
        Tns.create_app(self.app_name, attributes={"--template": os.path.join("data", "apps", "verbose-hello-world")})
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH, "--path": self.app_name})

        output = File.cat(os.path.join(self.app_name, "app", "app.js"))
        assert "__enableVerboseLogging()" in output, "Verbose logging not enabled in app.js"

        output = Tns.run_android(attributes={"--emulator": "", "--justlaunch": "",
                                             "--path": self.app_name,
                                             }, timeout=180)

        assert successfully_built in output
        lines = output.split('\n')
        count = len(lines)

        print "The verbose log contains {} lines.".format(str(count))
        assert count < 1000, \
            "The verbose log contains more than 1000 lines. It contains {} lines.".format(str(count))
        assert "***" not in output, "The verbose log contains an exception."
