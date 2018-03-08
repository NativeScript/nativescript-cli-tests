"""
Test for plugin commands in context of Android
"""

import os
import time
import unittest
import xml.etree.ElementTree as ET

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, ANDROID_PACKAGE, TEST_RUN_HOME
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts
from core.tns.tns_platform_type import Platform


class PluginsAndroidTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})
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

    @unittest.skip("Skip the test because of https://github.com/NativeScript/android-runtime/issues/903")
    def test_103_check_android_manifest_merged(self):
        plugin_name = "nativescript-barcodescanner"
        plugin_manifest_path = os.path.join(self.app_name, "node_modules", plugin_name, "platforms",
                                            "android", "AndroidManifest.xml")
        res_manifest = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_BUILD, "intermediates", "manifests")

        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        Tns.plugin_add(plugin_name, attributes={"--path": self.app_name})
        assert File.exists(plugin_manifest_path)
        plugin_manifest_file = ET.parse(plugin_manifest_path)
        root = plugin_manifest_file.getroot()
        assert File.find_text('<manifest xmlns:android="http://schemas.android.com/apk/res/android">',
                              plugin_manifest_path)
        assert File.find_text('<?xml version="1.0" encoding="UTF-8"?>', plugin_manifest_path)
        Tns.build_android(attributes={"--path": self.app_name})
        assert File.pattern_exists(res_manifest, "AndroidManifest.xml")
        merged_manifest_file = ET.parse(os.path.join(res_manifest, "full", "debug", "AndroidManifest.xml"))
        root2 = merged_manifest_file.getroot()
        res = False
        for child in root:
            for element in root2.findall(child.tag):
                if child.attrib == element.attrib:
                    res = True
                    break
                else:
                    res = False
            if child.tag == "application":
                for i in root.find("application"):
                    for j in root2.find("application"):
                        if i.tag == j.tag and i.attrib == j.attrib:
                            res = True
                            break
                        else:
                            res = False
        assert res is True, "Manifest not merged completely"

    @unittest.skip("missing tns-android 4.0 on NPM")
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

    @unittest.skip("missing tns-android 4.0 on NPM")
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
