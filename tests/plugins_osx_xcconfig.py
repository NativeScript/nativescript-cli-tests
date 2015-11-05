import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import Build, iosRuntimeSymlinkPath, \
    tnsPath, create_project, platform_add, Prepare, create_project_add_platform

# pylint: disable=R0201, C0111


class Plugins_OSX_Xcconfig(unittest.TestCase):

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

    def test_001_PluginAdd_Xcconfig_Before_platform_add_iOS(self):
        create_project(proj_name="TNS_App")

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/CocoaPods/xcconfig-plugin --path TNS_App")
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert FileExists("TNS_App/node_modules/xcconfig-plugin/package.json")
        assert FileExists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert FileExists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert FileExists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")

        output = runAUT("cat TNS_App/package.json")
        assert "xcconfig-plugin" in output

        platform_add(
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            path="TNS_App",
            symlink=True)
        output = Prepare(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = runAUT("cat TNS_App/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output
        output = runAUT("cat TNS_App/platforms/ios/plugins-release.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp/build-release.xcconfig")
        assert "#include \"../plugins-release.xcconfig\"" in output

        Build(platform="ios", path="TNS_App")

    def test_202_PluginAdd_Xcconfig_After_platform_add_iOS(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=iosRuntimeSymlinkPath,
            symlink=True)

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/CocoaPods/xcconfig-plugin --path TNS_App")
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert FileExists("TNS_App/node_modules/xcconfig-plugin/package.json")
        assert FileExists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert FileExists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert FileExists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")

        output = runAUT("cat TNS_App/package.json")
        assert "xcconfig-plugin" in output

        output = Build(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = runAUT("cat TNS_App/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output
        output = runAUT("cat TNS_App/platforms/ios/plugins-release.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp/build-release.xcconfig")
        assert "#include \"../plugins-release.xcconfig\"" in output
