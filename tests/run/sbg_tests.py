"""
Tests for static binding generator
"""
import unittest
import os

from core.tns.tns import Tns
from core.osutils.file import File
from core.osutils.folder import Folder
from core.device.emulator import Emulator
from core.settings.settings import ANDROID_RUNTIME_PATH


class StaticBindingGenerator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Folder.cleanup('TNS_App')
        Emulator.stop_emulators()
        # setup app
        Tns.create_app(app_name="TNS_App", copy_from=os.path.join("data", "apps", "sbg-test-app"))

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        Emulator.stop_emulators()
        Folder.cleanup('TNS_App')

    app_folder = "TNS_App"
    custom_js_file = os.path.join(app_folder, "app", "my-custom-class.js")
    tns_folder = os.path.join(app_folder, "platforms", "android", "src", "main", "java", "com", "tns")
    gen_folder = os.path.join(tns_folder, "gen")
    generated_java_file = os.path.join(tns_folder, "MyJavaClass.java")

    def test_001_platform_add_verify_initial_state(self):
        # check that we have a custom javascript file in the app
        print str.format("Checking if {0} file is there...", self.custom_js_file)
        js_file_exists = File.exists(self.custom_js_file)
        print "Check result: " + repr(js_file_exists)

        print "####################### Adding android platform #######################"
        output = Tns.platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path=self.app_folder)
        print output

        # check that we do not have folder gen before the project is built
        print str.format("Checking if {0} folder is there...", self.gen_folder)
        gen_folder_exsists = Folder.exists(self.gen_folder)
        print "Check result: " + repr(gen_folder_exsists)

        # check that we do not have generated custom java file before the project is built
        print str.format("Checking if {0} file is there...", self.generated_java_file)
        gen_file_exists = File.exists(self.generated_java_file)
        print "Check result: " + repr(gen_file_exists)

        # asserting final results
        print str.format("js_file_exists: {0}, gen_folder_exsists: {1}, gen_file_exsists: {2}", js_file_exists,
                         gen_folder_exsists, gen_file_exists)
        assert (js_file_exists == True) & (gen_folder_exsists == False) & (gen_file_exists == False)

    def test_002_on_build_verify_file_generation(self):
        print ("####################### Building app for android #######################")
        output = Tns.build(platform="android", path=self.app_folder)

        if "BUILD SUCCESSFUL" in output:
            # check that gen folder is created
            print str.format("Checking if {0} folder is generated...", self.gen_folder)
            gen_folder_exists = Folder.exists(self.gen_folder)
            print "Check result: " + repr(gen_folder_exists)

            # check that gen folder is not empty
            print str.format("Checking if {0} folder is not empty...", self.gen_folder)
            gen_folder_not_empty = True if len(os.listdir(self.gen_folder)) > 0 else False
            print "Check result: " + repr(gen_folder_not_empty)

            # check that generated custom java file is created
            print str.format("Checking if {0} folder is not empty...", self.generated_java_file)
            gen_java_file_exists = File.exists(self.generated_java_file)
            print "Check result: " + repr(gen_java_file_exists)

            # asserting final results
            print str.format("gen_folder_exists: {0}, gen_folder_not_empty: {1}, gen_java_file_exists: {2}",
                             gen_folder_exists, gen_folder_not_empty, gen_java_file_exists)
            assert (gen_folder_exists == True) & (gen_folder_not_empty == True) & (gen_java_file_exists == True), \
                "File and folders not created"
        else:
            assert False, "Build failed"
    #
    # def test_003_running_app_class_called(self):
    #     print ("Running app for android")
    #     output = Tns.run(platform="android", emulator=True, path=self.app_folder)
    #     assert "------we got called from onCreate" in output, "Expected output not found"
