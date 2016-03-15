"""
Test for plugin* commands in context of Android
"""


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, CURRENT_OS, OSType, ANDROID_RUNTIME_PATH
from core.tns.tns import Tns


class PluginsAndroid(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    def test_001_plugin_add_before_platform_add_android(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " plugin add tns-plugin --path TNS_App")
        if CURRENT_OS != OSType.WINDOWS:
            assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists("TNS_App/node_modules/tns-plugin/index.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_002_plugin_add_after_platform_add_android(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="android", \
                                    framework_path=ANDROID_RUNTIME_PATH)
        output = run(TNS_PATH + " plugin add tns-plugin --path TNS_App")
        if CURRENT_OS != OSType.WINDOWS:
            assert "TNS_App/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists("TNS_App/node_modules/tns-plugin/index.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_003_plugin_add_inside_project(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) + " plugin add tns-plugin")
        os.chdir(current_dir)
        if CURRENT_OS != OSType.WINDOWS:
            assert "node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists("TNS_App/node_modules/tns-plugin/index.js")
        assert File.exists("TNS_App/node_modules/tns-plugin/package.json")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_100_build_app_with_plugin_added_inside_project(self):

        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        output = run(TNS_PATH + " build android --path TNS_App")
        assert "Project successfully prepared" in output

        # Not valid for 1.3.0+
        # assert "Creating TNSApp-debug-unaligned.apk and signing it with a debug key..." in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output
        assert not "FAILURE" in output

        assert File.exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert File.exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

    def test_200_plugin_add_before_platform_add_android(self):
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
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/android")
        assert File.exists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/ios")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.platform_add(
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH,
            path="TNS_App")
        Tns.build(platform="android", path="TNS_App")

    def test_201_plugin_add_after_platform_add_android(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        output = run(
            TNS_PATH +
            " plugin add nativescript-telerik-ui --path TNS_App")
        if CURRENT_OS != OSType.WINDOWS:
            assert "TNS_App/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert File.exists(
            "TNS_App/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/android")
        assert File.exists(
            "TNS_App/node_modules/nativescript-telerik-ui/platforms/ios")
        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.build(platform="android", path="TNS_App")

    def test_300_build_app_with_plugin_added_outside_project(self):

        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)

        output = run(TNS_PATH + " plugin add tns-plugin --path TNS_App")
        assert "Successfully installed plugin tns-plugin" in output

        output = run(TNS_PATH + " build android --path TNS_App")
        assert "Project successfully prepared" in output

        # Not valid for 1.3.0+
        # assert "Creating TNSApp-debug-unaligned.apk and signing it with a debug key..." in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert not "ERROR" in output
        assert not "FAILURE" in output
        assert File.exists(
            "TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert File.exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

    @unittest.skip("This test breaks the xml parser.")
    def test_400_plugin_add_not_existing_plugin(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " plugin add fakePlugin --path TNS_App")
        assert "no such package available" in output

    def test_401_plugin_add_invalid_plugin(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " plugin add wd --path TNS_App")
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file " + \
            "contains a nativescript key and try again" in output

    def test_403_plugin_add_plugin_not_supported_on_specific_platform(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        output = run(
            TNS_PATH +
            " plugin add tns-plugin@1.0.2 --path TNS_App")
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output
