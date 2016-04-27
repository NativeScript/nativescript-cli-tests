"""
Test for plugin* commands in context of iOS
"""

import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, SUT_ROOT_FOLDER
from core.tns.tns import Tns


class PluginsiOSPods(unittest.TestCase):
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

    def test_001_plugin_add_multiple_pods(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/carousel"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)

        assert "TNS_App/node_modules/carousel" in output
        assert "Successfully installed plugin carousel." in output
        assert File.exists("TNS_App/node_modules/carousel/package.json")
        assert File.exists(
                "TNS_App/node_modules/carousel/platforms/ios/Podfile")

        output = run("cat TNS_App/package.json")
        assert "carousel" in output

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/keychain"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)

        assert "TNS_App/node_modules/keychain" in output
        assert "Successfully installed plugin keychain." in output
        assert File.exists("TNS_App/node_modules/keychain/package.json")
        assert File.exists(
                "TNS_App/node_modules/keychain/platforms/ios/Podfile")

        output = run("cat TNS_App/package.json")
        assert "keychain" in output

        output = Tns.build(platform="ios", path="TNS_App")
        assert "Installing pods..." in output
        assert "Successfully prepared plugin carousel for ios." in output
        assert "Successfully prepared plugin keychain for ios." in output

        output = run("cat TNS_App/platforms/ios/Podfile")
        assert "use_frameworks!" in output
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output
        assert "pod 'UICKeyChainStore'" in output

        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert File.exists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

        Tns.build(platform="ios", mode="release", for_device=True, path="TNS_App")

    def test_201_plugin_add_pod_google_maps_before_platform_add_ios(self):
        Tns.create_app(app_name="TNS_App")

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/googlesdk"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)

        assert "TNS_App/node_modules/googlesdk" in output
        assert "Successfully installed plugin googlesdk." in output
        assert File.exists("TNS_App/node_modules/googlesdk/package.json")
        assert File.exists(
                "TNS_App/node_modules/googlesdk/platforms/ios/Podfile")

        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "googlesdk" in output

        Tns.platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)
        output = Tns.prepare(platform="ios", path="TNS_App", log_trace=True)
        assert "The iOS Deployment Target is now 8.0" in output
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = run("cat TNS_App/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output

        # This deployment target comes from the CLI
        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'
        # output = run(
        #         "cat TNS_App/platforms/ios/Pods/Pods.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        # assert "IPHONEOS_DEPLOYMENT_TARGET = 8.1;" in output
        Tns.build(platform="ios", path="TNS_App")
        Tns.build(platform="ios", mode="release", for_device=True, path="TNS_App")

    def test_202_plugin_add_pod_google_maps_after_platform_add_ios(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/googlesdk"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "TNS_App/node_modules/googlesdk" in output
        assert "Successfully installed plugin googlesdk." in output
        assert File.exists("TNS_App/node_modules/googlesdk/package.json")
        assert File.exists(
                "TNS_App/node_modules/googlesdk/platforms/ios/Podfile")

        output = run("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "googlesdk" in output

        output = Tns.build(platform="ios", path="TNS_App")
        assert "The iOS Deployment Target is now 8.0" in output
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = run("cat TNS_App/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert File.exists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

        # This deployment target comes from the CLI
        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'
        # output = run(
        #         "cat TNS_App/platforms/ios/Pods/Pods.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        # assert "IPHONEOS_DEPLOYMENT_TARGET = 8.1;" in output

        Tns.build(platform="ios", mode="release", for_device=True, path="TNS_App")

    @unittest.skip(
            "This is not a valid scenario anymore. " + \
            "It fails because DEPLOYMENT_TARGET=7.0 which is updated during plugin add command.")
    def test_400_prepare_install_pods(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        run("cp QA-TestApps/CocoaPods/carousel/platforms/ios/Podfile TNS_App/platforms/ios")
        output = Tns.build(platform="ios", path="TNS_App")
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = run("cat TNS_App/platforms/ios/Podfile")
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output

        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert File.exists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

    def test_401_plugin_add_invalid_pod(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                symlink=True)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/invalidpod"
        output = Tns.plugin_add(path="TNS_App", plugin=plugin_path, assert_success=False)
        assert "TNS_App/node_modules/invalidpod" in output
        assert "Successfully installed plugin invalidpod." in output
        assert File.exists("TNS_App/node_modules/invalidpod/package.json")
        assert File.exists("TNS_App/node_modules/invalidpod/platforms/ios/Podfile")

        output = run("cat TNS_App/package.json")
        assert "invalidpod" in output

        output = Tns.prepare(platform="ios", path="TNS_App", assert_success=False)
        assert "Installing pods..." in output
        assert "Processing node_modules failed. Error:" in output

        output = run("cat TNS_App/platforms/ios/Podfile")
        assert "pod 'InvalidPod'" in output

        assert not File.exists("TNS_App/platforms/ios/TNSApp.xcworkspace")
        assert not File.exists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")
