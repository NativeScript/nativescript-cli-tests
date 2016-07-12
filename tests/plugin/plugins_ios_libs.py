"""
Test for plugin* commands in context of iOS
"""

import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, SUT_ROOT_FOLDER
from core.tns.tns import Tns


class PluginsiOSLibs(unittest.TestCase):
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

    def test_201_plugin_add_static_lib_universal_before_platform_add_ios(self):
        Tns.create_app(app_name="TNS_App")

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/static-lib/hello-plugin"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "TNS_App/node_modules/hello" in output
        assert "Successfully installed plugin hello." in output
        assert File.exists("TNS_App/node_modules/hello/package.json")
        assert File.exists("TNS_App/node_modules/hello/hello-plugin.ios.js")
        assert File.exists(
                "TNS_App/node_modules/hello/platforms/ios/HelloLib.a")
        assert File.exists(
                "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Bye.h")
        assert File.exists(
                "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Hello.h")

        output = run("cat TNS_App/package.json")
        assert "static-lib/hello-plugin" in output

        Tns.platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)
        output = Tns.build(platform="ios", path="TNS_App")
        # It targets 8.0 since a dynamic framework was added to the widgets.
        
        assert File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/package.json")
        assert File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/hello-plugin.js")
        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"HelloLib.a\"")
        assert "HelloLib.a in Frameworks" in output

    def test_202_plugin_add_static_lib_universal_after_platform_add_ios(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/static-lib/hello-plugin"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "TNS_App/node_modules/hello" in output
        assert "Successfully installed plugin hello." in output
        assert File.exists("TNS_App/node_modules/hello/package.json")
        assert File.exists("TNS_App/node_modules/hello/hello-plugin.ios.js")
        assert File.exists(
                "TNS_App/node_modules/hello/platforms/ios/HelloLib.a")
        assert File.exists(
                "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Bye.h")
        assert File.exists(
                "TNS_App/node_modules/hello/platforms/ios/include/HelloLib/Hello.h")

        output = run("cat TNS_App/package.json")
        assert "static-lib/hello-plugin" in output

        output = Tns.build(platform="ios", path="TNS_App")
        # It targets 8.0 since a dynamic framework was added to the widgets.
        assert "The iOS Deployment Target is now 8.0" in output
        assert File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/package.json")
        assert File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/hello/hello-plugin.js")
        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"HelloLib.a\"")
        assert "HelloLib.a in Frameworks" in output

    def test_401_plugin_add_static_lib_non_universal(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/static-lib/bye-plugin"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "TNS_App/node_modules/bye" in output

        output = Tns.prepare(platform="ios", path="TNS_App", assert_success=False)
        assert "The static library at" in output
        assert "ByeLib.a is not built for one or more of " + \
               "the following required architectures:" in output
        assert "armv7, arm64, i386." in output
        assert "The static library must be built for all required architectures." in output
