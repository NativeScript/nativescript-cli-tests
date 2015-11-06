import unittest

from helpers._os_lib import cleanup_folder, file_exists, run_aut, replace
from helpers._tns_lib import create_project, create_project_add_platform, \
    iosRuntimeSymlinkPath, platform_add, tnsPath

# pylint: disable=R0201, C0111


class Prepare_OSX(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')

    def tearDown(self):
        cleanup_folder('./TNS_App')

    def test_001_prepare_iOS(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)
        output = run_aut(tnsPath + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

    def test_010_prepare_iOS_TnsCoreModules(self):
        create_project(
            proj_name="TNS_App",
            copy_from="QA-TestApps/tns-modules-app/app")
        platform_add(
            platform="ios",
            path="TNS_App",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)

        # Make a change in tns-core-modules to verify they are not overwritten.
        replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");",
            "(\"globals\"); // test")

        # Verify tns-core-modules are copied to the native project, not app's
        # tns_modules.
        for i in range(1, 3):
            print "prepare number: " + str(i)

            output = run_aut(tnsPath + " prepare ios --path TNS_App")
            assert "You have tns_modules dir in your app folder" in output
            assert "Project successfully prepared" in output

            output = run_aut("cat TNS_App/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," in output

            output = run_aut(
                "cat TNS_App/node_modules/tns-core-modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = run_aut(
                "cat TNS_App/node_modules/tns-core-modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

            output = run_aut(
                "cat TNS_App/platforms/ios/TNSApp/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = run_aut(
                "cat TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

    def test_200_prepare_Additional_AppResources_iOS(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)

        # Create new files in AppResources
        run_aut("cp TNS_App/app/App_Resources/iOS/Default.png TNS_App/app/App_Resources/iOS/newDefault.png")

        # prepare project
        output = run_aut(tnsPath + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify XCode Project include files from App Resources folder
        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep newDefault.png")
        assert "newDefault.png" in output

    def test_201_prepare_iOS_PlatformNotAdded(self):
        create_project(proj_name="TNS_App")
        output = run_aut(tnsPath + " prepare ios --path TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output

        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')

    def test_300_prepare_iOS_PreserveCase(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)
        run_aut("cp TNS_App/node_modules/tns-core-modules/application/application-common.js TNS_App/node_modules/tns-core-modules/application/New-application-common.js")
        run_aut("cp TNS_App/node_modules/tns-core-modules/application/application.android.js TNS_App/node_modules/tns-core-modules/application/New-application.android.js")
        run_aut("cp TNS_App/node_modules/tns-core-modules/application/application.ios.js TNS_App/node_modules/tns-core-modules/application/New-application.ios.js")

        output = run_aut(tnsPath + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify case is preserved
        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application-common.js')
        assert file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application.js')
        assert not file_exists(
            'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application.ios.js')
