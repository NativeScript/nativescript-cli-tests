"""
Test for plugin* commands in context of iOS
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, TEST_RUN_HOME
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class PluginsiOSSandboxPodsTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def setUp(self):
        BaseClass.setUp(self)
        Xcode.cleanup_cache()
        Folder.cleanup(self.app_name)

    def tearDown(self):
        File.replace(TEST_RUN_HOME + "/node_modules/nativescript/config/config.json", '"USE_POD_SANDBOX": true',
                     '"USE_POD_SANDBOX": false')

    def test_100_plugin_add_sandbox_pod_can_write_in_app_folder(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH})

        plugin = os.path.join(TEST_RUN_HOME, "data", "CocoaPods", "nativescript-ios-working-with-sandbox-plugin.tgz")
        output = Tns.plugin_add(plugin, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin nativescript-ios-working-with-sandbox-plugin." in output
        assert "nativescript-ios-working-with-sandbox-plugin" in File.read(self.app_name + "/package.json")

        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        assert "Successfully prepared plugin " + \
               "nativescript-ios-working-with-sandbox-plugin for ios." in output

        assert "content" in File.read(self.app_name + "/platforms/ios/TestApp/app/I_MADE_THIS_FILE.txt")

    def test_400_plugin_add_sandbox_pod_can_write_outside_app_folder_by_default(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH})

        plugin = os.path.join(TEST_RUN_HOME, "data", "CocoaPods", "nativescript-ios-fail-with-sandbox-plugin.tgz")
        output = Tns.plugin_add(plugin, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin nativescript-ios-fail-with-sandbox-plugin." in output
        assert "nativescript-ios-fail-with-sandbox-plugin" in File.read(self.app_name + "/package.json")

        output = Tns.prepare_ios(attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully prepared " + \
               "plugin nativescript-ios-fail-with-sandbox-plugin for ios." in output

        assert "sh: ../I_MADE_THIS_FILE.txt: Operation not permitted" not in output
        assert File.exists(self.app_name + "/platforms/I_MADE_THIS_FILE.txt")

    def test_401_plugin_add_sandbox_pod_can_not_write_outside_app_folder_if_use_pod_sandbox_is_true(self):
        File.replace("node_modules/nativescript/config/config.json", '"USE_POD_SANDBOX": false',
                     '"USE_POD_SANDBOX": true')
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        plugin = os.path.join(TEST_RUN_HOME, "data", "CocoaPods", "nativescript-ios-fail-with-sandbox-plugin.tgz")
        output = Tns.plugin_add(plugin, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin nativescript-ios-fail-with-sandbox-plugin." in output
        assert "nativescript-ios-fail-with-sandbox-plugin" in File.read(self.app_name + "/package.json")

        output = Tns.prepare_ios(attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully prepared " + \
               "plugin nativescript-ios-fail-with-sandbox-plugin for ios." in output

        assert "sh: ../I_MADE_THIS_FILE.txt: Operation not permitted" in output
        assert not File.exists(self.app_name + "/platforms/I_MADE_THIS_FILE.txt")
