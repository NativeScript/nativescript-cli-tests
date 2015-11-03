import unittest

from helpers._os_lib import CleanupFolder, FileExists, runAUT, replace
from helpers._tns_lib import CreateProject, CreateProjectAndAddPlatform, \
    iosRuntimeSymlinkPath, PlatformAdd, tnsPath

# pylint: disable=R0201, C0111
class Prepare_OSX(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App');

    def tearDown(self):
        CleanupFolder('./TNS_App');

    def test_001_Prepare_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        output = runAUT(tnsPath + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

    def test_010_Prepare_iOS_TnsCoreModules(self):
        CreateProject(projName="TNS_App", copyFrom="QA-TestApps/tns-modules-app/app")
        PlatformAdd(platform="ios", path="TNS_App", frameworkPath=iosRuntimeSymlinkPath, symlink=True)

        # Make a change in tns-core-modules to verify they are not overwritten.
        replace("TNS_App/node_modules/tns-core-modules/application/application-common.js", "(\"globals\");", "(\"globals\"); // test")

        # Verify tns-core-modules are copied to the native project, not app's tns_modules.
        for i in range(1, 3):
            print "Prepare number: " + str(i)

            output = runAUT(tnsPath + " prepare ios --path TNS_App")
            assert "You have tns_modules dir in your app folder" in output
            assert "Project successfully prepared" in output

            output = runAUT("cat TNS_App/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," in output

            output = runAUT("cat TNS_App/node_modules/tns-core-modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = runAUT("cat TNS_App/node_modules/tns-core-modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

            output = runAUT("cat TNS_App/platforms/ios/TNSApp/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = runAUT("cat TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

    def test_200_Prepare_Additional_AppResources_iOS(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)

        # Create new files in AppResources
        runAUT("cp TNS_App/app/App_Resources/iOS/Default.png TNS_App/app/App_Resources/iOS/newDefault.png")

        # Prepare project
        output = runAUT(tnsPath + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify XCode Project include files from App Resources folder
        output = runAUT("cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep newDefault.png")
        assert "newDefault.png" in output

    def test_201_Prepare_iOS_PlatformNotAdded(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " prepare ios --path TNS_App");
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output

        assert FileExists('TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')

    def test_300_Prepare_iOS_PreserveCase(self):
        CreateProjectAndAddPlatform(projName="TNS_App", platform="ios", frameworkPath=iosRuntimeSymlinkPath, symlink=True)
        runAUT("cp TNS_App/node_modules/tns-core-modules/application/application-common.js TNS_App/node_modules/tns-core-modules/application/New-application-common.js")
        runAUT("cp TNS_App/node_modules/tns-core-modules/application/application.android.js TNS_App/node_modules/tns-core-modules/application/New-application.android.js")
        runAUT("cp TNS_App/node_modules/tns-core-modules/application/application.ios.js TNS_App/node_modules/tns-core-modules/application/New-application.ios.js")

        output = runAUT(tnsPath + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify case is preserved
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application-common.js')
        assert FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application.js')
        assert not FileExists('TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application.ios.js')
