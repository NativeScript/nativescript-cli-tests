"""
Test for plugin* commands in context of iOS
"""

import os
import time

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, IOS_RUNTIME_PATH, ANDROID_RUNTIME_PATH, TEST_RUN_HOME
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts
from core.xcode.xcode import Xcode


class PluginsiOSTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Xcode.cleanup_cache()
        Folder.cleanup(self.app_name)
        run("rm -rf ~/.gradle")

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    def test_100_plugin_add_before_platform_add_ios(self):
        Tns.create_app(self.app_name)
        output = Tns.plugin_add(tns_plugin, attributes={"--path": self.app_name})
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = run("cat " + self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert tns_plugin in output

    def test_101_plugin_add_after_platform_add_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.plugin_add(tns_plugin, attributes={"--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")

        output = File.read(self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert tns_plugin in output

    def test_201_plugin_add_before_platform_add_ios(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.plugin_add("nativescript-telerik-ui", attributes={"--ignore-scripts": "",
                                                              "--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/Android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/iOS")

        output = File.read(self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output

        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_202_plugin_add_after_platform_add_ios(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.plugin_add("nativescript-telerik-ui", attributes={"--ignore-scripts": "",
                                                              "--path": self.app_name
                                                              })

        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/Android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/iOS")
        output = File.read(self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_203_plugin_add_inside_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_tns_command("plugin add tns-plugin", tns_path=os.path.join("..", TNS_PATH))
        os.chdir(current_dir)
        assert installed_plugin.format(tns_plugin) in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = File.read(self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert tns_plugin in output

    def test_204_build_app_with_plugin_inside_project(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.plugin_add(name="tns-plugin", tns_path=os.path.join("..", TNS_PATH), assert_success=False)
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        Tns.build_ios(attributes={"--path": self.app_name})

    def test_300_build_app_with_plugin_outside(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.plugin_add(tns_plugin, attributes={"--path": self.app_name})
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_301_build_app_for_both_platforms(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.plugin_add(tns_plugin, attributes={"--path": self.app_name})

        # Verify files of the plugin
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/test.android.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/test.ios.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/test2.android.xml")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/test2.ios.xml")

        Tns.build_ios(attributes={"--path": self.app_name})
        Tns.build_android(attributes={"--path": self.app_name})

        assert File.exists(os.path.join(self.app_name, debug_apk_path))
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/index.js")

        # Verify platform specific files
        assert File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test.js")
        assert File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test2.xml")
        assert not File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test.ios.js")
        assert not File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test.android.js")
        assert not File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test2.android.xml")

        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test.js")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/tns-plugin/test2.xml")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/"
                                               "app/tns_modules/tns-plugin/test.ios.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/"
                                               "app/tns_modules/tns-plugin/test2.ios.xml")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/"
                                               "app/tns_modules/tns-plugin/test.android.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/"
                                               "app/tns_modules/tns-plugin/test2.android.xml")

    def test_302_plugin_and_npm_modules_in_same_project(self):
        Tns.create_app(self.app_name, update_modules=True)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.plugin_add("nativescript-social-share", attributes={"--path": self.app_name})

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = run("npm install nativescript-appversion --save")
        os.chdir(current_dir)
        assert "ERR!" not in output
        assert "nativescript-appversion@" in output

        Tns.build_android(attributes={"--path": self.app_name}, assert_success=True)

        # Verify plugin and npm module files
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                           "nativescript-social-share/package.json")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                           "nativescript-social-share/social-share.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                               "nativescript-social-share/social-share.android.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                               "nativescript-social-share/social-share.ios.js")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                           "nativescript-appversion/package.json")
        assert File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                           "nativescript-appversion/appversion.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                               "nativescript-appversion/appversion.android.js")
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/" +
                               "nativescript-appversion/appversion.ios.js")

    def test_320_CFBundleURLTypes_overridden_from_plugin(self):
        """
        Test for issue https://github.com/NativeScript/nativescript-cli/issues/2936
        """
        Tns.create_app(self.app_name)
        plugin_path = os.path.join(TEST_RUN_HOME, 'data', 'plugins', 'CFBundleURLName-Plugin.tgz')
        Tns.plugin_add(plugin_path, attributes={"--path": self.app_name})
        Tns.prepare_ios(attributes={"--path": self.app_name})
        plist = File.read(os.path.join(TEST_RUN_HOME, self.app_name, 'platforms', 'ios', self.app_name,
                                       self.app_name + "-Info.plist"))
        assert "<key>NSAllowsArbitraryLoads</key>" in plist, \
            "NSAppTransportSecurity from plugin is not found in final Info.plist"
        assert "<string>bar</string>" in plist, "CFBundleURLTypes from plugin is not found in final Info.plist"

    def test_401_plugin_add_invalid_plugin(self):
        Tns.create_app(self.app_name)
        output = Tns.plugin_add("wd", attributes={"--path": self.app_name}, assert_success=False)
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file " + \
               "contains a nativescript key and try again" in output

    def test_403_plugin_add_plugin_not_supported_on_specific_platform(self):
        time.sleep(2)
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        # Verify iOS only plugin
        output = Tns.plugin_add("tns-plugin@1.0.2", attributes={"--path": self.app_name}, assert_success=False)
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output

        # Verify Android only plugin
        output = Tns.plugin_add(" acra-telerik-analytics", attributes={"--path": self.app_name}, assert_success=False)
        assert "acra-telerik-analytics is not supported for ios" in output
        assert "Successfully installed plugin acra-telerik-analytics" in output

        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.FULL)
        assert not File.pattern_exists(self.app_name + "/platforms/ios", pattern="*.aar")

        output = Tns.prepare_android(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.FULL)
        assert File.pattern_exists(self.app_name + "/platforms/android", pattern="*.aar")
        assert File.pattern_exists(self.app_name + "/platforms/android", pattern="*ACRA*")
