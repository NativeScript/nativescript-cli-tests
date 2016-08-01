"""
Test for plugin* commands in context of iOS
"""

import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, SUT_ROOT_FOLDER
from core.tns.tns import Tns


class PluginsiOSXcconfig_Tests(unittest.TestCase):
    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # Delete derived data
        run("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    def test_001_plugin_add_xcconfig_before_platform_add_ios(self):
        Tns.create_app(app_name="TNS_App")

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/xcconfig-plugin"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert File.exists("TNS_App/node_modules/xcconfig-plugin/package.json")
        assert File.exists(
                "TNS_App/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert File.exists(
                "TNS_App/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert File.exists(
                "TNS_App/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")

        output = run("cat TNS_App/package.json")
        assert "xcconfig-plugin" in output

        Tns.platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)
        output = Tns.prepare(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = run("cat TNS_App/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output
        output = run("cat TNS_App/platforms/ios/plugins-release.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = run(
                "cat TNS_App/platforms/ios/TNSApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
        output = run(
                "cat TNS_App/platforms/ios/TNSApp/build-release.xcconfig")
        assert "#include \"../plugins-release.xcconfig\"" in output

        Tns.build(platform="ios", path="TNS_App")

    def test_202_plugin_add_xcconfig_after_platform_add_ios(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/xcconfig-plugin"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert File.exists("TNS_App/node_modules/xcconfig-plugin/package.json")
        assert File.exists(
                "TNS_App/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert File.exists(
                "TNS_App/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert File.exists(
                "TNS_App/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")

        output = run("cat TNS_App/package.json")
        assert "xcconfig-plugin" in output

        output = Tns.build(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = run("cat TNS_App/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output
        output = run("cat TNS_App/platforms/ios/plugins-release.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = run(
                "cat TNS_App/platforms/ios/TNSApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
        output = run(
                "cat TNS_App/platforms/ios/TNSApp/build-release.xcconfig")
        assert "#include \"../plugins-release.xcconfig\"" in output
