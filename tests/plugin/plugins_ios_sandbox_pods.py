"""
Test for plugin* commands in context of iOS
"""

import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, SUT_ROOT_FOLDER
from core.tns.tns import Tns


class PluginsiOSSandboxPods(unittest.TestCase):
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

    def test_001_plugin_add_sandbox_pod_can_write_in_app_folder(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/nativescript-ios-working-with-sandbox-plugin"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "Successfully installed plugin nativescript-ios-working-with-sandbox-plugin." in output

        output = run("cat TNS_App/package.json")
        assert "nativescript-ios-working-with-sandbox-plugin" in output

        output = Tns.prepare(platform="ios", path="TNS_App")
        assert "Successfully prepared plugin " + \
               "nativescript-ios-working-with-sandbox-plugin for ios." in output

        output = run(
                "cat TNS_App/platforms/ios/TNSApp/app/I_MADE_THIS_FILE.txt")
        assert "content" in output

    def test_401_plugin_add_sandbox_pod_can_not_write_outside_app_folder(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/nativescript-ios-fail-with-sandbox-plugin"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "Successfully installed plugin nativescript-ios-fail-with-sandbox-plugin." in output

        output = run("cat TNS_App/package.json")
        assert "nativescript-ios-fail-with-sandbox-plugin" in output

        output = Tns.prepare(platform="ios", path="TNS_App", assert_success=False)
        assert "Successfully prepared " + \
               "plugin nativescript-ios-fail-with-sandbox-plugin for ios." in output
        
        assert "sh: ../I_MADE_THIS_FILE.txt: Operation not permitted" in output
        assert not File.exists("TNS_App/platforms/I_MADE_THIS_FILE.txt")
