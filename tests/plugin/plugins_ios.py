"""
Test for plugin* commands in context of iOS
"""

import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, IOS_RUNTIME_SYMLINK_PATH, CURRENT_OS, OSType, IOS_RUNTIME_PATH, \
    ANDROID_RUNTIME_SYMLINK_PATH, ANDROID_RUNTIME_PATH
from core.tns.tns import Tns


class PluginsiOS(unittest.TestCase):
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
        Folder.cleanup('./TNS_App')

    def test_001_plugin_add_before_platform_add_ios(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " plugin add tns-plugin --path TNS_App")
        assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists("TNS_App/node_modules/tns-plugin/index.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_002_plugin_add_after_platform_add_ios(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        output = run(TNS_PATH + " plugin add tns-plugin --path TNS_App")
        assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists("TNS_App/node_modules/tns-plugin/index.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_201_plugin_add_before_platform_add_ios(self):
        Tns.create_app(app_name="TNS_App")
        output = run(
                TNS_PATH +
                " plugin add nativescript-telerik-ui --path TNS_App")
        if CURRENT_OS != OSType.WINDOWS:
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert File.exists(
                "TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(
                "TNS_App/node_modules/nativescript-telerik-ui/platforms/Android")
        assert File.exists(
                "TNS_App/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True,
                path="TNS_App")
        Tns.build(platform="ios", path="TNS_App")

    def test_202_plugin_add_after_platform_add_ios(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        output = run(
                TNS_PATH +
                " plugin add nativescript-telerik-ui --path TNS_App")
        if CURRENT_OS != OSType.WINDOWS:
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert File.exists(
                "TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(
                "TNS_App/node_modules/nativescript-telerik-ui/platforms/Android")
        assert File.exists(
                "TNS_App/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.build(platform="ios", path="TNS_App")

    def test_203_plugin_add_inside_project(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_PATH)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists("TNS_App/node_modules/tns-plugin/index.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_204_build_app_with_plugin_inside_project(self):

        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        output = run(TNS_PATH + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

    def test_300_build_app_with_plugin_outside(self):

        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        output = run(TNS_PATH + " plugin add tns-plugin --path TNS_App")
        assert "Successfully installed plugin tns-plugin" in output

        output = run(TNS_PATH + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

    def test_301_build_app_for_both_platforms(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        Tns.platform_add(
                platform="android",
                framework_path=ANDROID_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)

        output = run(TNS_PATH + " plugin add tns-plugin --path TNS_App")
        assert "Successfully installed plugin tns-plugin" in output

        # Verify files of the plugin
        assert File.exists("TNS_App/node_modules/tns-plugin/index.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/package.json")
        assert File.exists("TNS_App/node_modules/tns-plugin/test.android.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/test.ios.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/test2.android.xml")
        assert File.exists("TNS_App/node_modules/tns-plugin/test2.ios.xml")

        output = run(TNS_PATH + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "** BUILD SUCCEEDED **" in output
        assert not "ERROR" in output
        assert not "malformed" in output

        output = run(TNS_PATH + " build android --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output

        assert File.exists(
                "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

        # Verify platform specific files
        assert File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.js")
        assert File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.xml")
        assert not File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.ios.js")
        assert not File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test.android.js")
        assert not File.exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules/tns-plugin/test2.android.xml")

        assert File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.js")
        assert File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.xml")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.ios.js")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.android.js")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.android.xml")

    def test_302_plugin_and_npm_modules_in_same_project(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)

        output = run(
                TNS_PATH +
                " plugin add nativescript-social-share --path TNS_App")
        assert "Successfully installed plugin nativescript-social-share" in output

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run("npm install nativescript-appversion --save")
        os.chdir(current_dir)
        assert not "ERR!" in output
        assert "nativescript-appversion@" in output

        output = run(TNS_PATH + " build android --path TNS_App")
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        # Verify plugin and npm module files
        assert File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
                "nativescript-social-share/package.json")
        assert File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
                "nativescript-social-share/social-share.js")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
                "nativescript-social-share/social-share.android.js")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
                "nativescript-social-share/social-share.ios.js")

        assert File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
                "nativescript-appversion/package.json")
        assert File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
                "nativescript-appversion/appversion.js")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
                "nativescript-appversion/appversion.android.js")
        assert not File.exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
                "nativescript-appversion/appversion.ios.js")

    def test_401_plugin_add_invalid_plugin(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " plugin add wd --path TNS_App")
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file " + \
               "contains a nativescript key and try again" in output

    def test_403_plugin_add_PluginNotSupportedOnSpecificPlatform(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)
        Tns.platform_add(
                platform="android",
                framework_path=ANDROID_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)

        output = run(
                TNS_PATH +
                " plugin add tns-plugin@1.0.2 --path TNS_App")
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output
