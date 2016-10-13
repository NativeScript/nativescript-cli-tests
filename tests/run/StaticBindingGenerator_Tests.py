"""
Tests for static binding generator
"""
import unittest
import os
import subprocess
import threading

from core.base_class.BaseClass import BaseClass
from core.tns.tns import Tns
from core.osutils.file import File
from core.osutils.folder import Folder
from core.device.emulator import Emulator
from core.settings.settings import ANDROID_RUNTIME_PATH, ADB_PATH


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

    # def test_001_platform_add_verify_initial_state(self):
    #     # check that we have a custom javascript file in the app
    #     print str.format("Checking if {0} file is there...", self.custom_js_file)
    #     js_file_exists = File.exists(self.custom_js_file)
    #     print "Check result: " + repr(js_file_exists)

        # print "####################### Adding android platform #######################"
        # output = Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH,
        #                                               "--path": self.app_name
        #                                               })
        # print output

        # # check that we do not have folder gen before the project is built
        # print str.format("Checking if {0} folder is there...", self.gen_folder)
        # gen_folder_exsists = Folder.exists(self.gen_folder)
        # print "Check result: " + repr(gen_folder_exsists)
        #
        # # check that we do not have generated custom java file before the project is built
        # print str.format("Checking if {0} file is there...", self.generated_java_file)
        # gen_file_exists = File.exists(self.generated_java_file)
        # print "Check result: " + repr(gen_file_exists)
        #
        # # asserting final results
        # print str.format("js_file_exists: {0}, gen_folder_exsists: {1}, gen_file_exsists: {2}", js_file_exists,
        #                  gen_folder_exsists, gen_file_exists)
        # assert (js_file_exists is True) and (gen_folder_exsists is False) and (gen_file_exists is False)

    # def test_002_on_build_verify_file_generation(self):
    #     print ("####################### Building app for android #######################")
    #     output = Tns.build_android(attributes={"--path": self.app_name})
    #
    #     if "BUILD SUCCESSFUL" in output:
    #         # check that gen folder is created
    #         print str.format("Checking if {0} folder is generated...", self.gen_folder)
    #         gen_folder_exists = Folder.exists(self.gen_folder)
    #         print "Check result: " + repr(gen_folder_exists)
    #
    #         # check that gen folder is not empty
    #         print str.format("Checking if {0} folder is not empty...", self.gen_folder)
    #         gen_folder_not_empty = True if len(os.listdir(self.gen_folder)) > 0 else False
    #         print "Check result: " + repr(gen_folder_not_empty)
    #
    #         # check that generated custom java file is created
    #         print str.format("Checking if {0} folder is not empty...", self.generated_java_file)
    #         gen_java_file_exists = File.exists(self.generated_java_file)
    #         print "Check result: " + repr(gen_java_file_exists)
    #
    #         # asserting final results
    #         print str.format("gen_folder_exists: {0}, gen_folder_not_empty: {1}, gen_java_file_exists: {2}",
    #                          gen_folder_exists, gen_folder_not_empty, gen_java_file_exists)
    #         assert (gen_folder_exists is True) and (gen_folder_not_empty is True) and (gen_java_file_exists is True), \
    #             "File and folders not created"
    #     else:
    #         assert False, "Build failed"
    
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

        #make sure app hasn't crashed
        assert "Displayed org.nativescript.TNSApp/com.tns.ErrorReportActivity" not in output, "App crashed with error activity"

        # check if we got called from custom activity that overrides the default one
        assert "we got called from onCreate of custom-nativescript-activity.js" in output, "Expected output not found"

        # make sure we called custom activity declared in manifest
        assert "we got called from onCreate of my-custom-class.js" in output, "Expected output not found"
