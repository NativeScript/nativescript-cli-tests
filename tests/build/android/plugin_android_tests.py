"""
Test for plugin commands in context of Android
"""

import os
import time
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.helpers.adb import Adb
from core.java.java import Java
from core.npm.npm import Npm
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, ANDROID_PACKAGE, TEST_RUN_HOME
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts


class PluginsAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name, TEST_RUN_HOME + "/data/TestApp")

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        Folder.copy(TEST_RUN_HOME + "/data/TestApp", TEST_RUN_HOME + "/TestApp")

    def test_100_plugin_add_before_platform_add_android(self):
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
        Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")

        output = File.read(self.app_name + "/package.json")
        assert "org.nativescript.TestApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_101_plugin_add_after_platform_add_android(self):
        Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")

        output = File.read(self.app_name + "/package.json")
        assert "org.nativescript.TestApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_102_plugin_add_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = run(os.path.join("..", TNS_PATH) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")

        output = File.read(self.app_name + "/package.json")
        assert "org.nativescript.TestApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

        Tns.build_android(attributes={"--path": self.app_name}, log_trace=True)
        assert File.exists(self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_APK_DEBUG_PATH + "/app-debug.apk")
        assert File.exists(self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH + "/tns-plugin/index.js")

    @unittest.skipIf(Java.version() != "1.8", "nativescript-barcodescanner is not compatible with java 10+")
    def test_103_check_android_manifest_merged(self):
        plugin_name = "nativescript-barcodescanner"
        Tns.plugin_add(plugin_name, attributes={"--path": self.app_name})
        Tns.build_android(attributes={"--path": self.app_name})
        apk_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_DEBUG_PATH, "app-debug.apk")
        output = Adb.get_package_permission(apk_path)
        assert "android.permission.READ_EXTERNAL_STORAGE" in output
        assert "android.permission.WRITE_EXTERNAL_STORAGE" in output
        assert "android.permission.INTERNET" in output
        assert "android.permission.FLASHLIGHT" in output
        assert "android.permission.CAMERA" in output

    def test_104_plugin_create_android(self):
        #https://github.com/NativeScript/nativescript-cli/issues/1945
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
        output = Tns.plugin_create("nativescript-ui-listview", attributes={"--path": self.app_name})
        Tns.build_android(attributes={"--path": self.app_name})
        assert not File.exists(self.app_name + "/nativescript-ui-listview/src/scripts/postclone.js")

    def test_105_plugin_create_android_custom_plugin(self):
        #https://github.com/NativeScript/nativescript-cli/issues/1945
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
        output = Tns.plugin_create("nativescript-ui-listview",
                                   attributes={"--path": self.app_name, "--template":
                                       "https://github.com/NativeScript/nativescript-plugin-seed/tarball/master"})
        Tns.build_android(attributes={"--path": self.app_name})
        assert not File.exists(self.app_name + "/nativescript-ui-listview/src/scripts/postclone.js")

    def test_201_plugin_add_before_platform_add_android_and_build(self):
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
        Tns.plugin_add("nativescript-telerik-ui", attributes={"--ignore-scripts": "", "--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/ios")
        output = File.read(self.app_name + "/package.json")
        assert "org.nativescript.TestApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        Tns.build_android(attributes={"--path": self.app_name})

    def test_202_plugin_add_after_platform_add_android(self):
        Tns.plugin_add("nativescript-telerik-ui", attributes={"--ignore-scripts": "", "--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/ios")

        output = File.read(self.app_name + "/package.json")
        assert "org.nativescript.TestApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output

        Tns.build_android(attributes={"--path": self.app_name})

    def test_300_build_app_with_plugin_added_outside_project(self):
        Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name}, assert_success=False)

        Tns.build_android(attributes={"--path": self.app_name})
        assert File.exists(self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_APK_DEBUG_PATH + "/app-debug.apk")
        assert File.exists(self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH + "/tns-plugin/index.js")

        # Verify plugin command list used plugins
        output = Tns.run_tns_command("plugin", attributes={"--path": self.app_name})
        assert tns_plugin in output

    def test_310_plugin_platforms_should_not_exist_in_tnsmodules(self):
        #https://github.com/NativeScript/nativescript-cli/issues/3932
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
        Tns.plugin_add("nativescript-ui-listview", attributes={"--path": self.app_name}, assert_success=False)
        Folder.cleanup(self.app_name + "/node_modules")
        File.remove(self.app_name + "/package.json")
        copy = os.path.join('data', 'issues', 'nativescript-cli-3932', 'nativescript-ui-listview')
        paste = os.path.join(self.app_name + '/' + 'nativescript-ui-listview')
        Folder.copy(copy, paste)
        File.copy(TEST_RUN_HOME + "/data/issues/nativescript-cli-3932/package.json", TEST_RUN_HOME + "/TestApp")
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        Folder.navigate_to(self.app_name + "/nativescript-ui-listview")
        Npm.install(option='--ignore-scripts')
        Folder.navigate_to(TEST_RUN_HOME)
        Tns.build_android(attributes={"--path": self.app_name})

        app_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH)
        assert not File.exists(os.path.join(app_path, 'nativescript-ui-listview', 'node_modules', 'nativescript-ui-core', 'platforms'))

    @unittest.skip("Temporary issues with jcenter.")
    def test_390_plugin_with_promise_in_hooks(self):
        Tns.plugin_add("nativescript-fabric@1.0.6", attributes={"--path": self.app_name})
        output = Tns.prepare_android(attributes={"--path": self.app_name}, assert_success=False)
        assert "Failed to execute hook" in output
        assert "nativescript-fabric.js" in output
        assert "TypeError" not in output
        assert "Cannot read property" not in output

    def test_400_plugin_add_invalid_plugin(self):
        output = Tns.plugin_add("fakePlugin", attributes={"--path": self.app_name}, assert_success=False)
        assert "npm ERR!" in output

        output = Tns.plugin_add("wd", attributes={"--path": self.app_name}, assert_success=False)
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file contains a nativescript key and try again" in output

        time.sleep(2)
        Folder.cleanup(self.app_name)
        # Tns.create_app(self.app_name)
        Folder.copy(TEST_RUN_HOME + "/data/TestApp", TEST_RUN_HOME + "/TestApp")
        # Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        output = Tns.plugin_add("tns-plugin@1.0.2", attributes={"--path": self.app_name}, assert_success=False)
        assert tns_plugin + " is not supported for android" in output
        assert installed_plugin.format(tns_plugin) in output

    def test_410_plugin_remove_should_not_fail_if_plugin_name_has_dot(self):
        # https://github.com/NativeScript/nativescript-cli/issues/3451
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
        Tns.plugin_add("nativescript-socket.io", attributes={"--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/nativescript-socket.io")

        output = Tns.plugin_remove("nativescript-socket.io", attributes={"--path": self.app_name}, log_trace=True)
        assert "stdout: removed 1 package" in output
        assert "Successfully removed plugin nativescript-socket.io" in output
        assert "Exec npm uninstall nativescript-socket.io --save" in output

        output = File.read(self.app_name + "/package.json")
        assert "nativescript-socket.io" not in output
