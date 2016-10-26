"""
Tests for static binding generator
"""
import unittest
import os
import subprocess
import threading

from core.base_class.BaseClass import BaseClass
from core.tns.tns import Tns
from core.osutils.folder import Folder
from core.device.emulator import Emulator
from core.settings.settings import ADB_PATH


class StaticBindingGenerator(BaseClass):
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
        Tns.create_app(cls.app_name, attributes={"--copy-from": os.path.join("data", "apps", "sbg-test-app")})

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop_emulators()
        Folder.cleanup(cls.app_name)

    @unittest.skip("Fails due to known issue in SBG")
    def test_003_calling_custom_generated_classes_declared_in_manifest(self):
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
