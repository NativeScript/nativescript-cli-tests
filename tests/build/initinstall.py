"""
Test for init and install command
"""
import fileinput
import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, CURRENT_OS, OSType


class InitAndInstall(unittest.TestCase):
    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    def test_001_init_defaults(self):

        run("mkdir TNS_App")

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) + " init --force")
        os.chdir(current_dir)

        assert "Project successfully initialized" in output
        assert File.exists("TNS_App/package.json")
        assert not File.exists("TNS_App/app")
        assert not File.exists("TNS_App/platform")

        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "tns-android" in output
        assert "tns-core-modules" in output
        if CURRENT_OS == OSType.OSX:
            assert "tns-ios" in output

    def test_002_init_path(self):
        output = run(TNS_PATH + " init --path TNS_App --force")
        assert "Project successfully initialized" in output
        assert File.exists("TNS_App/package.json")
        assert not File.exists("TNS_App/app")
        assert not File.exists("TNS_App/platform")

        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "tns-android" in output
        if CURRENT_OS == OSType.OSX:
            assert "tns-ios" in output

    def test_003_init_update_existing_file(self):
        self.test_002_init_path()

        # Modify existing file
        for line in fileinput.input("TNS_App/package.json", inplace=1):
            print line.replace("org.nativescript.TNSApp", "org.nativescript.TestApp"),
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TestApp" in output

        # Overwrite changes
        self.test_002_init_path()

    def test_004_install_defaults(self):
        self.test_002_init_path()

        output = run(TNS_PATH + " install --path TNS_App")
        assert "Project successfully created" in output

        # Not valid for 1.3.0+
        # assert File.exists("TNS_App/platforms/android/build.gradle")
        assert File.exists("TNS_App/platforms/android/build.gradle")

        if CURRENT_OS == OSType.OSX:
            assert File.exists("TNS_App/platforms/ios/TNSApp.xcodeproj")

    def test_005_install_node_modules(self):
        self.test_002_init_path()

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        run("npm i gulp --save-dev")
        run("npm i lodash --save")
        os.chdir(current_dir)
        output = run("cat TNS_App/package.json")
        assert "devDependencies" in output
        assert "gulp" in output
        assert "lodash" in output

        Folder.cleanup('./TNS_App/node_modules')
        assert not File.exists("TNS_App/node_modules")

        output = run(TNS_PATH + " install --path TNS_App")
        assert "Project successfully created" in output
        assert File.exists("TNS_App/node_modules/lodash")
        assert File.exists("TNS_App/node_modules/gulp")

        # Not valid for 1.3.0+
        # assert File.exists("TNS_App/platforms/android/build.gradle")
        assert File.exists("TNS_App/platforms/android/build.gradle")

        if CURRENT_OS == OSType.OSX:
            assert File.exists("TNS_App/platforms/ios/TNSApp.xcodeproj")

    def test_300_install_node_modules_if_node_modules_folder_exists(self):
        self.test_002_init_path()

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        run("npm i gulp --save-dev")
        run("npm i lodash --save")

        os.chdir(current_dir)
        output = run("cat TNS_App/package.json")
        assert "devDependencies" in output
        assert "gulp" in output
        assert "lodash" in output

        output = run(TNS_PATH + " install --path TNS_App")
        assert "Project successfully created" in output
        assert File.exists("TNS_App/node_modules/lodash")
        assert File.exists("TNS_App/node_modules/gulp")
        assert File.exists("TNS_App/platforms/android/build.gradle")
        if CURRENT_OS == OSType.OSX:
            assert File.exists("TNS_App/platforms/ios/TNSApp.xcodeproj")

    def test_301_install_and_prepare(self):
        self.test_002_init_path()

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        run("npm i gulp --save-dev")
        run("npm i lodash --save")

        os.chdir(current_dir)
        run("cp -R template-hello-world TNS_App/app")
        output = run("cat TNS_App/package.json")
        assert "devDependencies" in output
        assert "gulp" in output
        assert "lodash" in output

        output = run(TNS_PATH + " install --path TNS_App")
        assert "Project successfully created" in output
        assert File.exists("TNS_App/node_modules/lodash")
        assert File.exists("TNS_App/node_modules/gulp")
        assert File.exists("TNS_App/platforms/android/build.gradle")

        output = run(TNS_PATH + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output

        assert File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/lodash")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/gulp")

        print "CURRENT_OS: " + CURRENT_OS
        if CURRENT_OS == OSType.OSX:
            assert File.exists("TNS_App/platforms/ios/TNSApp.xcodeproj")
            output = run(TNS_PATH + " prepare ios --path TNS_App")
            assert "Project successfully prepared" in output
            assert File.exists(
                    "TNS_App/platforms/ios/TNSApp/app/tns_modules/lodash")
            assert not File.exists(
                    "TNS_App/platforms/ios/TNSApp/app/tns_modules/gulp")

    def test_400_install_in_not_existing_folder(self):
        output = run(TNS_PATH + " install --path TNS_App")
        assert "No project found" in output
