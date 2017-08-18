"""
Test for plugin* commands in context of iOS
"""

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, TEST_RUN_HOME
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class PluginsiOSLibsTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Xcode.cleanup_cache()
        Folder.cleanup(self.app_name)

    def test_200_plugin_add_static_lib_universal(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        plugin_path = TEST_RUN_HOME + "/data/static-lib/hello-plugin.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin hello." in output

        assert File.exists(self.app_name + "/node_modules/hello/package.json")
        assert File.exists(self.app_name + "/node_modules/hello/hello-plugin.ios.js")
        assert File.exists(self.app_name + "/node_modules/hello/platforms/ios/HelloLib.a")
        assert File.exists(self.app_name + "/node_modules/hello/platforms/ios/include/HelloLib/Bye.h")
        assert File.exists(self.app_name + "/node_modules/hello/platforms/ios/include/HelloLib/Hello.h")
        assert "static-lib/hello-plugin" in File.read(self.app_name + "/package.json")

        Tns.build_ios(attributes={"--path": self.app_name})

        assert File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/hello/package.json")
        assert File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/hello/hello-plugin.js")
        output = run(
            "cat " + self.app_name + "/platforms/ios/TestApp.xcodeproj/project.pbxproj | grep \"HelloLib.a\"")
        assert "HelloLib.a in Frameworks" in output

    def test_401_plugin_add_static_lib_non_universal(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        plugin_path = TEST_RUN_HOME + "/data/static-lib/bye-plugin.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin bye" in output

        output = Tns.prepare_ios(attributes={"--path": self.app_name}, assert_success=False)
        assert "The static library at" in output
        assert "ByeLib.a is not built for one or more of " + \
               "the following required architectures:" in output
        assert "armv7, arm64, i386." in output
        assert "The static library must be built for all required architectures." in output
