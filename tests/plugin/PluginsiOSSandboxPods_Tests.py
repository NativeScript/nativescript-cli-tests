"""
Test for plugin* commands in context of iOS
"""

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, SUT_ROOT_FOLDER
from core.tns.tns import Tns


class PluginsiOSSandboxPodsTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)

        # Delete derived data
        run("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        Folder.cleanup('./' + self.app_name)

    def test_001_plugin_add_sandbox_pod_can_write_in_app_folder(self):
        Tns.create_app(self.app_name)
        Tns. platform_add_ios(attributes={"--path": self.app_name,
                                          "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                          "--symlink": ""})

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/nativescript-ios-working-with-sandbox-plugin"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin nativescript-ios-working-with-sandbox-plugin." in output

        output = run("cat " + self.app_name + "/package.json")
        assert "nativescript-ios-working-with-sandbox-plugin" in output

        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        assert "Successfully prepared plugin " + \
               "nativescript-ios-working-with-sandbox-plugin for ios." in output

        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp/app/I_MADE_THIS_FILE.txt")
        assert "content" in output

    def test_401_plugin_add_sandbox_pod_can_not_write_outside_app_folder(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""})

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/nativescript-ios-fail-with-sandbox-plugin"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin nativescript-ios-fail-with-sandbox-plugin." in output

        output = run("cat " + self.app_name + "/package.json")
        assert "nativescript-ios-fail-with-sandbox-plugin" in output

        output = Tns.prepare_ios(attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully prepared " + \
               "plugin nativescript-ios-fail-with-sandbox-plugin for ios." in output
        
        assert "sh: ../I_MADE_THIS_FILE.txt: Operation not permitted" in output
        assert not File.exists(self.app_name + "/platforms/I_MADE_THIS_FILE.txt")
