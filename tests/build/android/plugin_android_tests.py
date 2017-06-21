"""
Test for plugin commands in context of Android
"""

import os
import unittest
import xml.etree.ElementTree as ET
from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, CURRENT_OS, OSType, ANDROID_RUNTIME_PATH
from core.tns.tns import Tns
import time
from core.settings.strings import *


class PluginsAndroidTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)

    def test_100_plugin_add_before_platform_add_android(self):
        Tns.create_app(self.app_name)
        Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")

        output = File.read(self.app_name + "/package.json")
        assert "org.nativescript.TestApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_101_plugin_add_after_platform_add_android(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")

        output = File.read(self.app_name + "/package.json")
        assert "org.nativescript.TestApp" in output
        assert "dependencies" in output
        assert "tns-plugin" in output

    def test_102_plugin_add_inside_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,"--frameworkPath": ANDROID_RUNTIME_PATH})
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

    def test_103_check_android_manifest_merged(self):
        plugin_name = "nativescript-barcodescanner"
        plugin_manifest_path = os.path.join(self.app_name, "node_modules", plugin_name, "platforms",
                                            "android", "AndroidManifest.xml")
        src_manifest = os.path.join(self.platforms_android, "src", plugin_name, "AndroidManifest.xml")
        res_manifest = os.path.join(self.platforms_android, "build", "intermediates", "manifests")

        Tns.create_app(self.app_name)
        Tns.plugin_add(plugin_name, attributes={"--path": self.app_name})
        assert File.exists(plugin_manifest_path)
        plugin_manifest_file = ET.parse(plugin_manifest_path)
        root = plugin_manifest_file.getroot()
        assert File.find_text('<manifest xmlns:android="http://schemas.android.com/apk/res/android">',
                              plugin_manifest_path)
        assert File.find_text('<?xml version="1.0" encoding="UTF-8"?>', plugin_manifest_path)
        Tns.prepare_android(attributes={"--path": self.app_name})
        assert File.exists(src_manifest)
        Tns.build_android(attributes={"--path": self.app_name})
        assert File.pattern_exists(res_manifest, "AndroidManifest.xml")
        merged_manifest_file = ET.parse(os.path.join(res_manifest, "full", "F1F2", "debug", "AndroidManifest.xml"))
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
        print res
        assert res is True, "Manifest not merged completely"

    def test_200_build_app_with_plugin_added_inside_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = run(os.path.join("..", TNS_PATH) + " plugin add tns-plugin")
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        output = Tns.build_android(attributes={"--path": self.app_name})
        assert successfully_prepared in output

        assert build_successful in output
        assert successfully_built in output
        assert error not in output.lower()
        assert "FAILURE" not in output

        assert File.exists(self.app_name + "/platforms/android/build/outputs/apk/TestApp-debug.apk")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

    def test_201_plugin_add_before_platform_add_android_and_build(self):
        Tns.create_app(self.app_name)
        Tns.plugin_add("nativescript-telerik-ui", attributes={"--ignore-scripts": "", "--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/ios")
        output = File.read(self.app_name + "/package.json")
        assert "org.nativescript.TestApp" in output
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.build_android(attributes={"--path": self.app_name})

    def test_202_plugin_add_after_platform_add_android(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
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
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.plugin_add("tns-plugin", attributes={"--path": self.app_name}, assert_success=False)

        Tns.build_android(attributes={"--path": self.app_name})
        assert File.exists(self.app_name + "/platforms/android/build/outputs/apk/TestApp-debug.apk")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

        # Verify plugin commmand list used plugins
        output = Tns.run_tns_command("plugin", attributes={"--path": self.app_name})
        assert tns_plugin in output

    def test_400_plugin_add_not_existing_plugin(self):
        Tns.create_app(self.app_name)
        output = Tns.plugin_add("fakePlugin", attributes={"--path": self.app_name}, assert_success=False)
        assert "no such package available" in output

    def test_401_plugin_add_invalid_plugin(self):
        Tns.create_app(self.app_name)
        output = Tns.plugin_add("wd", attributes={"--path": self.app_name}, assert_success=False)
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file contains a nativescript key and try again" in output

    def test_403_plugin_add_plugin_not_supported_on_specific_platform(self):
        time.sleep(2)
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        output = Tns.plugin_add("tns-plugin@1.0.2", attributes={"--path": self.app_name}, assert_success=False)
        assert tns_plugin + " is not supported for android" in output
        assert installed_plugin.format(tns_plugin) in output
