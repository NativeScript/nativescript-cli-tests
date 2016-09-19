"""
Test for plugin* commands in context of iOS
"""

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, SUT_ROOT_FOLDER
from core.tns.tns import Tns


class PluginsiOSXcconfigTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        # Delete derived data
        run("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        Folder.cleanup('./' + self.app_name)

    def test_001_plugin_add_xcconfig_before_platform_add_ios(self):
        Tns.create_app(self.app_name)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/xcconfig-plugin"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/package.json")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")

        output = run("cat " + self.app_name + "/package.json")
        assert "xcconfig-plugin" in output

        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = run("cat " + self.app_name + "/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output
        output = run("cat " + self.app_name + "/platforms/ios/plugins-release.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp/build-release.xcconfig")
        assert "#include \"../plugins-release.xcconfig\"" in output

        Tns.build_ios(attributes={"--path": self.app_name})

    def test_202_plugin_add_xcconfig_after_platform_add_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/xcconfig-plugin"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/package.json")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")

        output = run("cat " + self.app_name + "/package.json")
        assert "xcconfig-plugin" in output

        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = run("cat " + self.app_name + "/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output
        output = run("cat " + self.app_name + "/platforms/ios/plugins-release.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp/build-release.xcconfig")
        assert "#include \"../plugins-release.xcconfig\"" in output
