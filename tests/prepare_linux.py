import unittest
import os

from helpers._os_lib import CleanupFolder, FileExists, runAUT, replace
from helpers._tns_lib import androidRuntimePath, create_project, create_project_add_platform, \
    platform_add, tnsPath

# pylint: disable=R0201, C0111


class Prepare_Linux(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')

    def tearDown(self):
        CleanupFolder('./TNS_App')

    def test_001_Prepare_Android(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/main-view-model.js')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.js')
        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.android.js')
        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.ios.js')

    def test_002_Prepare_Android_InsideProject(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " prepare android")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/main-view-model.js')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.js')
        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.android.js')
        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.ios.js')

    def test_010_Prepare_Android_TnsCoreModules(self):
        create_project(
            proj_name="TNS_App",
            copy_from="QA-TestApps/tns-modules-app/app")
        platform_add(
            platform="android",
            path="TNS_App",
            framework_path=androidRuntimePath)

        # Make a change in tns-core-modules to verify they are not overwritten.
        replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");",
            "(\"globals\"); // test")

        # Verify tns-core-modules are copied to the native project, not app's
        # tns_modules.
        for i in range(1, 3):
            print "Prepare number: " + str(i)

            output = runAUT(tnsPath + " prepare android --path TNS_App")
            assert "You have tns_modules dir in your app folder" in output
            assert "Project successfully prepared" in output

            output = runAUT("cat TNS_App/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," in output

            output = runAUT(
                "cat TNS_App/node_modules/tns-core-modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = runAUT(
                "cat TNS_App/node_modules/tns-core-modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

            output = runAUT(
                "cat TNS_App/platforms/android/src/main/assets/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = runAUT(
                "cat TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

    def test_210_Prepare_Android_PlatformNotAdded(self):
        create_project(proj_name="TNS_App")
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/xml/xml.js')

    def test_300_Prepare_Android_RemoveOldFiles(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output

        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.js')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.css')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/main-page.xml')

        runAUT("mv TNS_App/app/app.js TNS_App/app/app-new.js")
        runAUT("mv TNS_App/app/app.css TNS_App/app/app-new.css")
        runAUT("mv TNS_App/app/main-page.xml TNS_App/app/main-page-new.xml")

        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app-new.js')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app-new.css')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/main-page-new.xml')

        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.js')
        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.css')
        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/main-page.xml')

    def test_301_Prepare_Android_PlatformSpecificFiles(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=androidRuntimePath)
        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.css')

        runAUT("cp TNS_App/app/app.js TNS_App/app/app.ios.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/app.android.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/appios.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/appandroid.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/ios.js")
        runAUT("cp TNS_App/app/app.js TNS_App/app/android.js")
        runAUT("cp TNS_App/app/app.css TNS_App/app/app.ios.css")
        runAUT("cp TNS_App/app/app.css TNS_App/app/app.android.css")
        runAUT("mv TNS_App/app/app.js TNS_App/app/appNew.js")
        runAUT("mv TNS_App/app/app.css TNS_App/app/appNew.css")

        output = runAUT(tnsPath + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.css')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.js')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/appandroid.js')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/appios.js')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/android.js')
        assert FileExists(
            'TNS_App/platforms/android/src/main/assets/app/ios.js')
        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.ios.css')
        assert not FileExists(
            'TNS_App/platforms/android/src/main/assets/app/app.android.css')

    def test_400_Prepare_MissingPlatform(self):
        create_project(proj_name="TNS_App")
        output = runAUT(tnsPath + " prepare --path TNS_App")
        assert "You need to provide all the required parameters." in output

    def test_401_Prepare_InvalidPlatform(self):
        create_project(proj_name="TNS_App")
        output = runAUT(tnsPath + " prepare windows --path TNS_App")
        assert "Invalid platform windows. Valid platforms are ios or android." in output
