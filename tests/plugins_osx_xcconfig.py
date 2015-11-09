'''
Test for plugin* commands in context of iOS
'''
import unittest

from helpers._os_lib import cleanup_folder, run_aut, file_exists
from helpers._tns_lib import build, IOS_RUNTIME_SYMLINK_PATH, \
    TNSPATH, create_project, platform_add, prepare, create_project_add_platform

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class PluginsiOSXcconfig(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # Delete derived data
        run_aut("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        cleanup_folder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_plugin_add_xcconfig_before_platform_add_ios(self):
        create_project(proj_name="TNS_App")

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/xcconfig-plugin --path TNS_App")
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert file_exists("TNS_App/node_modules/xcconfig-plugin/package.json")
        assert file_exists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert file_exists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert file_exists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")

        output = run_aut("cat TNS_App/package.json")
        assert "xcconfig-plugin" in output

        platform_add(
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            path="TNS_App",
            symlink=True)
        output = prepare(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = run_aut("cat TNS_App/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output
        output = run_aut("cat TNS_App/platforms/ios/plugins-release.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp/build-release.xcconfig")
        assert "#include \"../plugins-release.xcconfig\"" in output

        build(platform="ios", path="TNS_App")

    def test_202_plugin_add_xcconfig_after_platform_add_ios(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/xcconfig-plugin --path TNS_App")
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert file_exists("TNS_App/node_modules/xcconfig-plugin/package.json")
        assert file_exists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert file_exists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert file_exists(
            "TNS_App/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")

        output = run_aut("cat TNS_App/package.json")
        assert "xcconfig-plugin" in output

        output = build(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = run_aut("cat TNS_App/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output
        output = run_aut("cat TNS_App/platforms/ios/plugins-release.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp/build-release.xcconfig")
        assert "#include \"../plugins-release.xcconfig\"" in output
