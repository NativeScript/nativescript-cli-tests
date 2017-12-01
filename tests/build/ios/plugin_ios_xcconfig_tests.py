"""
Test for plugin* commands in context of iOS
"""

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, TEST_RUN_HOME
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class PluginsiOSXcconfigTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Xcode.cleanup_cache()
        Folder.cleanup(self.app_name)

    def test_100_plugin_add_xcconfig_before_platform_add_ios(self):
        Tns.create_app(self.app_name)

        plugin_path = TEST_RUN_HOME + "/data/CocoaPods/xcconfig-plugin.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/package.json")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")
        assert "xcconfig-plugin" in File.read(self.app_name + "/package.json")

        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = File.read(self.app_name + "/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = File.read(self.app_name + "/platforms/ios/TestApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output

        Tns.build_ios(attributes={"--path": self.app_name})

    def test_202_plugin_add_xcconfig_after_platform_add_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        plugin_path = TEST_RUN_HOME + "/data/CocoaPods/xcconfig-plugin.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin xcconfig-plugin." in output
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/package.json")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/build.xcconfig")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/module.modulemap")
        assert File.exists(self.app_name + "/node_modules/xcconfig-plugin/platforms/ios/XcconfigPlugin.h")
        assert "xcconfig-plugin" in File.read(self.app_name + "/package.json")

        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Successfully prepared plugin xcconfig-plugin for ios." in output

        output = File.read(self.app_name + "/platforms/ios/plugins-debug.xcconfig")
        assert "OTHER_LDFLAGS = $(inherited) -l\"sqlite3\"" in output

        output = File.read(self.app_name + "/platforms/ios/TestApp/build-debug.xcconfig")
        assert "#include \"../plugins-debug.xcconfig\"" in output
