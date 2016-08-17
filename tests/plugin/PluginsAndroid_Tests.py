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


class PluginsAndroid_Tests(unittest.TestCase):
    app_name = "TNS_App"

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./' + self.app_name)

    def tearDown(self):
        pass

    def test_001_plugin_add_before_platform_add_android(self):
        Tns.create_app(self.app_name)
        output = run(TNS_PATH + " plugin add tns-plugin --path " + self.app_name)
        if CURRENT_OS != OSType.WINDOWS:
            assert self.app_name + "/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = run("cat " + self.app_name +  + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_002_plugin_add_after_platform_add_android(self):
        Tns.create_app_platform_add(app_name=self.app_name, platform="android", framework_path=ANDROID_RUNTIME_PATH)
        output = run(TNS_PATH + " plugin add tns-plugin --path " + self.app_name)
        if CURRENT_OS != OSType.WINDOWS:
            assert self.app_name + "/node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_003_plugin_add_inside_project(self):
        Tns.create_app_platform_add(app_name=self.app_name, platform="android", framework_path=ANDROID_RUNTIME_PATH)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = run(os.path.join("..", TNS_PATH) + " plugin add tns-plugin")
        os.chdir(current_dir)
        if CURRENT_OS != OSType.WINDOWS:
            assert "node_modules/tns-plugin" in output
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_100_build_app_with_plugin_added_inside_project(self):
        Tns.create_app_platform_add(app_name=self.app_name, platform="android", framework_path=ANDROID_RUNTIME_PATH)

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = run(os.path.join("..", TNS_PATH) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        output = run(TNS_PATH + " build android --path " + self.app_name)
        assert "Project successfully prepared" in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert "ERROR" not in output
        assert "FAILURE" not in output

        assert File.exists(self.app_name + "/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

    def test_200_plugin_add_before_platform_add_android_and_build(self):
        Tns.create_app(self.app_name)
        output = run(TNS_PATH + " plugin add nativescript-telerik-ui --ignore-scripts --path " + self.app_name)
        if CURRENT_OS != OSType.WINDOWS:
            assert self.app_name + "/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/ios")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path=self.app_name)
        Tns.build(platform="android", path=self.app_name)

    def test_201_plugin_add_after_platform_add_android(self):
        Tns.create_app_platform_add(app_name=self.app_name, platform="android", framework_path=ANDROID_RUNTIME_PATH)
        output = run(TNS_PATH + " plugin add nativescript-telerik-ui --ignore-scripts --path " + self.app_name)
        if CURRENT_OS != OSType.WINDOWS:
            assert self.app_name + "/node_modules/nativescript-telerik-ui" in output
        assert "Successfully installed plugin nativescript-telerik-ui" in output
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/ios")
        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.build(platform="android", path=self.app_name)

    def test_300_build_app_with_plugin_added_outside_project(self):
        Tns.create_app_platform_add(app_name=self.app_name, platform="android", framework_path=ANDROID_RUNTIME_PATH)

        output = run(TNS_PATH + " plugin add tns-plugin --path " + self.app_name)
        assert "Successfully installed plugin tns-plugin" in output

        output = run(TNS_PATH + " build android --path " + self.app_name)
        assert "Project successfully prepared" in output

        assert "BUILD SUCCESSFUL" in output
        assert "Project successfully built" in output
        assert "ERROR" not in output
        assert "FAILURE" not in output
        assert File.exists(self.app_name + "/platforms/android/build/outputs/apk/TNSApp-debug.apk")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

        # Verify plugin commmand list used plugins
        output = run(TNS_PATH + " plugin --path " + self.app_name)
        assert "tns-plugin" in output

    @unittest.skip("This test breaks the xml parser.")
    def test_400_plugin_add_not_existing_plugin(self):
        Tns.create_app(self.app_name)
        output = run(TNS_PATH + " plugin add fakePlugin --path " + self.app_name)
        assert "no such package available" in output

    def test_401_plugin_add_invalid_plugin(self):
        Tns.create_app(self.app_name)
        output = run(TNS_PATH + " plugin add wd --path " + self.app_name)
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file contains a nativescript key and try again" in output

    def test_403_plugin_add_plugin_not_supported_on_specific_platform(self):
        Tns.create_app_platform_add(app_name=self.app_name, platform="android", framework_path=ANDROID_RUNTIME_PATH)
        output = run(TNS_PATH + " plugin add tns-plugin@1.0.2 --path " + self.app_name)
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output
