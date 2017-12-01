"""
Test for plugin* commands in context of iOS
"""

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, TEST_RUN_HOME
from core.settings.strings import *
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class PluginsiOSPodsTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def setUp(self):
        BaseClass.setUp(self)
        Xcode.cleanup_cache()
        Folder.cleanup(self.app_name)

    def test_100_plugin_add_multiple_pods(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        plugin_path = TEST_RUN_HOME + "/data/CocoaPods/carousel.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin carousel." in output
        assert File.exists(self.app_name + "/node_modules/carousel/package.json")
        assert File.exists(self.app_name + "/node_modules/carousel/platforms/ios/Podfile")
        assert "carousel" in File.read(self.app_name + "/package.json")

        plugin_path = TEST_RUN_HOME + "/data/CocoaPods/keychain.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin keychain." in output
        assert File.exists(self.app_name + "/node_modules/keychain/package.json")
        assert File.exists(self.app_name + "/node_modules/keychain/platforms/ios/Podfile")
        assert "keychain" in File.read(self.app_name + "/package.json")

        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Installing pods..." in output
        assert "Successfully prepared plugin carousel for ios." in output
        assert "Successfully prepared plugin keychain for ios." in output

        output = File.read(self.app_name + "/platforms/ios/Podfile")
        assert "use_frameworks!" in output
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output
        assert "pod 'UICKeyChainStore'" in output

        output = File.read(self.app_name + "/platforms/ios/TestApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TestApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert File.exists(self.app_name + "/platforms/ios/Pods/Pods.xcodeproj")

        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": ""})

    def test_201_plugin_add_pod_google_maps_before_platform_add_ios(self):
        Tns.create_app(self.app_name)

        plugin_path = TEST_RUN_HOME + "/data/CocoaPods/googlesdk.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin googlesdk." in output
        assert File.exists(self.app_name + "/node_modules/googlesdk/package.json")
        assert File.exists(self.app_name + "/node_modules/googlesdk/platforms/ios/Podfile")

        output = File.read(self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert "googlesdk" in output

        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        output = Tns.prepare_ios(attributes={"--path": self.app_name}, log_trace=True)

        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Installing pods..." in output

        output = File.read(self.app_name + "/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = File.read(self.app_name + "/platforms/ios/TestApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TestApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output

        # This deployment target comes from the CLI
        output = File.read(self.app_name + "/platforms/ios/TestApp.xcodeproj/project.pbxproj")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'

        Tns.build_ios(attributes={"--path": self.app_name})
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": ""})

    def test_202_plugin_add_pod_google_maps_after_platform_add_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        plugin_path = TEST_RUN_HOME + "/data/CocoaPods/googlesdk.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin googlesdk." in output
        assert File.exists(self.app_name + "/node_modules/googlesdk/package.json")
        assert File.exists(self.app_name + "/node_modules/googlesdk/platforms/ios/Podfile")

        output = File.read(self.app_name + "/package.json")
        assert app_identifier in output.lower()
        assert "dependencies" in output
        assert "googlesdk" in output

        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Installing pods..." in output

        output = File.read(self.app_name + "/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = File.read(self.app_name + "/platforms/ios/TestApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TestApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert File.exists(self.app_name + "/platforms/ios/Pods/Pods.xcodeproj")

        # This deployment target comes from the CLI
        output = File.read(self.app_name + "/platforms/ios/TestApp.xcodeproj/project.pbxproj")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'

        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": ""})

    def test_401_plugin_add_invalid_pod(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        plugin_path = TEST_RUN_HOME + "/data/CocoaPods/invalidpod.tgz"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert "Successfully installed plugin invalidpod." in output
        assert File.exists(self.app_name + "/node_modules/invalidpod/package.json")
        assert File.exists(self.app_name + "/node_modules/invalidpod/platforms/ios/Podfile")

        output = File.read(self.app_name + "/package.json")
        assert "invalidpod" in output

        output = Tns.prepare_ios(attributes={"--path": self.app_name}, assert_success=False)
        assert "Installing pods..." in output
        assert "Command pod failed with exit code 1" in output
        assert "pod 'InvalidPod'" in File.read(self.app_name + "/platforms/ios/Podfile")

        assert not File.exists(self.app_name + "/platforms/ios/TestApp.xcworkspace")
        assert not File.exists(self.app_name + "/platforms/ios/Pods/Pods.xcodeproj")
