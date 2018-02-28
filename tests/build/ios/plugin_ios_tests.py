"""
Test for plugin* commands in context of iOS
"""

import os
import time

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, IOS_PACKAGE, ANDROID_PACKAGE, TEST_RUN_HOME
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts
from core.xcode.xcode import Xcode


class PluginsiOSTests(BaseClass):
    debug_apk = "app-debug.apk"

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app(cls.app_name)
        Tns.platform_add_ios(attributes={"--path": cls.app_name, "--frameworkPath": IOS_PACKAGE})
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name, TEST_RUN_HOME + "/data/TestApp")

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")

    def setUp(self):
        BaseClass.setUp(self)
        Xcode.cleanup_cache()
        Folder.cleanup(self.app_name)
        run("rm -rf ~/.gradle")
        Folder.cleanup(self.app_name)
        Folder.copy(TEST_RUN_HOME + "/data/TestApp", TEST_RUN_HOME + "/TestApp")

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    def test_100_plugin_add_before_platform_add_ios(self):
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name}, assert_success=False)
        output = Tns.plugin_add(tns_plugin, attributes={"--path": self.app_name})
        assert "Successfully installed plugin tns-plugin" in output
        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")
        output = run("cat " + self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert tns_plugin in output

    def test_101_plugin_add_after_platform_add_ios(self):
        Tns.plugin_add(tns_plugin, attributes={"--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/tns-plugin/index.js")
        assert File.exists(self.app_name + "/node_modules/tns-plugin/package.json")

        output = File.read(self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert tns_plugin in output

    def test_201_plugin_add_before_platform_add_ios(self):
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name}, assert_success=False)
        Tns.plugin_add("nativescript-telerik-ui", attributes={"--ignore-scripts": "",
                                                              "--path": self.app_name})

        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/package.json")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/Android")
        assert File.exists(self.app_name + "/node_modules/nativescript-telerik-ui/platforms/iOS")

        output = File.read(self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert "nativescript-telerik-ui" in output

        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE})
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_202_plugin_add_after_platform_add_ios(self):
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
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.plugin_add(name="tns-plugin", tns_path=os.path.join("..", TNS_PATH), assert_success=False)
        os.chdir(current_dir)
        assert "Successfully installed plugin tns-plugin" in output

        Tns.build_ios(attributes={"--path": self.app_name})

    def test_300_build_app_with_plugin_outside(self):
        Tns.plugin_add(tns_plugin, attributes={"--path": self.app_name})
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_301_build_app_for_both_platforms(self):
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
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

        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_DEBUG_PATH, self.debug_apk))
        assert File.exists(
            os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "tns-plugin/index.js"))

        # Verify platform specific files
        assert File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test.js")
        assert File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test2.xml")
        assert not File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test.ios.js")
        assert not File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test2.ios.xml")
        assert not File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test.android.js")
        assert not File.exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules/tns-plugin/test2.android.xml")

        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "tns-plugin/test.js"))
        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "tns-plugin/test2.xml"))
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "tns-plugin/test.ios.js"))
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "tns-plugin/test2.ios.xml"))
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "tns-plugin/test.android.js"))
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "tns-plugin/test2.android.xml"))

    def test_302_plugin_and_npm_modules_in_same_project(self):
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name}, assert_success=False)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        Tns.plugin_add("nativescript-social-share", attributes={"--path": self.app_name})

        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = run("npm install nativescript-appversion --save")
        os.chdir(current_dir)
        assert "ERR!" not in output
        assert "nativescript-appversion@" in output

        Tns.build_android(attributes={"--path": self.app_name}, assert_success=True)

        # Verify plugin and npm module files
        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "nativescript-social-share/package.json"))
        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "nativescript-social-share/social-share.js"))
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "nativescript-social-share/social-share.android.js"))
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "nativescript-social-share/social-share.ios.js"))
        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "nativescript-appversion/package.json"))
        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "nativescript-appversion/appversion.js"))
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "nativescript-appversion/appversion.android.js"))
        assert not File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, "nativescript-appversion/appversion.ios.js"))

    def test_320_CFBundleURLTypes_overridden_from_plugin(self):
        """
        Test for issue https://github.com/NativeScript/nativescript-cli/issues/2936
        """
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name}, assert_success=False)
        plugin_path = os.path.join(TEST_RUN_HOME, 'data', 'plugins', 'CFBundleURLName-Plugin.tgz')
        Tns.plugin_add(plugin_path, attributes={"--path": self.app_name})
        Tns.prepare_ios(attributes={"--path": self.app_name})
        plist = File.read(os.path.join(TEST_RUN_HOME, self.app_name, 'platforms', 'ios', self.app_name,
                                       self.app_name + "-Info.plist"))
        assert "<key>NSAllowsArbitraryLoads</key>" in plist, \
            "NSAppTransportSecurity from plugin is not found in final Info.plist"
        assert "<string>bar</string>" in plist, "CFBundleURLTypes from plugin is not found in final Info.plist"

    def test_401_plugin_add_invalid_plugin(self):
        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name}, assert_success=False)
        output = Tns.plugin_add("wd", attributes={"--path": self.app_name}, assert_success=False)
        assert "wd is not a valid NativeScript plugin" in output
        assert "Verify that the plugin package.json file " + \
               "contains a nativescript key and try again" in output

        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE})
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})

        # Verify iOS only plugin
        output = Tns.plugin_add("tns-plugin@1.0.2", attributes={"--path": self.app_name}, assert_success=False)
        assert "tns-plugin is not supported for android" in output
        assert "Successfully installed plugin tns-plugin" in output

        # Verify Android only plugin
        output = Tns.plugin_add("acra-telerik-analytics", attributes={"--path": self.app_name}, assert_success=False)
        assert "acra-telerik-analytics is not supported for ios" in output
        assert "Successfully installed plugin acra-telerik-analytics" in output

        Tns.build_ios(attributes={"--path": self.app_name})
        assert not File.pattern_exists(self.app_name + "/platforms/ios", pattern="*.aar")
        assert not File.pattern_exists(self.app_name + "/platforms/ios", pattern="*acra*")

        Tns.build_android(attributes={"--path": self.app_name})
        assert File.pattern_exists(self.app_name + "/platforms/android", pattern="*.aar")
        assert File.pattern_exists(self.app_name + "/platforms/android", pattern="*acra*")
