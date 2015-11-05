import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import Build, iosRuntimeSymlinkPath, \
    tnsPath, create_project, platform_add, Prepare, create_project_add_platform

# pylint: disable=R0201, C0111


class Plugins_OSX_Libs(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # Delete derived data
        runAUT("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        CleanupFolder('./TNS_App')

    def tearDown(self):
        pass

    def test_201_PluginAdd_StaticLib_Universal_Before_platform_add_iOS(self):
        create_project(proj_name="TNS_App")

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/static-lib/hello-plugin --path TNS_App")
        assert "TNS_App/node_modules/hello" in output
        assert "Successfully installed plugin hello." in output
        assert FileExists("TNS_App/node_modules/hello/package.json")
        assert FileExists("TNS_App/node_modules/hello/hello-plugin.ios.js")
        assert FileExists(
            "TNS_App/node_modules/hello/platforms/ios/HelloLib.a")
        assert FileExists(
            "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Bye.h")
        assert FileExists(
            "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Hello.h")

        output = runAUT("cat TNS_App/package.json")
        assert "static-lib/hello-plugin" in output

        platform_add(
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            path="TNS_App",
            symlink=True)
        output = Build(platform="ios", path="TNS_App")
        assert "The iOS Deployment Target is now 8.0" not in output
        assert FileExists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/package.json")
        assert FileExists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/hello-plugin.js")
        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"HelloLib.a\"")
        assert "HelloLib.a in Frameworks" in output

    def test_202_PluginAdd_StaticLib_Universal_After_platform_add_iOS(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/static-lib/hello-plugin --path TNS_App")
        assert "TNS_App/node_modules/hello" in output
        assert "Successfully installed plugin hello." in output
        assert FileExists("TNS_App/node_modules/hello/package.json")
        assert FileExists("TNS_App/node_modules/hello/hello-plugin.ios.js")
        assert FileExists(
            "TNS_App/node_modules/hello/platforms/ios/HelloLib.a")
        assert FileExists(
            "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Bye.h")
        assert FileExists(
            "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Hello.h")

        output = runAUT("cat TNS_App/package.json")
        assert "static-lib/hello-plugin" in output

        output = Build(platform="ios", path="TNS_App")
        assert "The iOS Deployment Target is now 8.0" not in output
        assert FileExists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/package.json")
        assert FileExists(
            "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/hello-plugin.js")
        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"HelloLib.a\"")
        assert "HelloLib.a in Frameworks" in output

    def test_401_PluginAdd_StaticLib_NonUniversal(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/static-lib/bye-plugin --path TNS_App")
        assert "TNS_App/node_modules/bye" in output

        output = Prepare(platform="ios", path="TNS_App", assertSuccess=False)
        assert "The static library at" in output
        assert "ByeLib.a is not built for one or more of the following required architectures:" in output
        assert "armv7, arm64, i386." in output
        assert "The static library must be built for all required architectures." in output
