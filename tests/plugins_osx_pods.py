'''
Test for plugin* commands in context of iOS
'''
import unittest

from helpers._os_lib import cleanup_folder, run_aut, file_exists
from helpers._tns_lib import build, IOS_RUNTIME_SYMLINK_PATH, \
    TNSPATH, create_project, platform_add, prepare, create_project_add_platform

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class PluginsiOSPods(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # Delete derived data
        run_aut("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        cleanup_folder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_plugin_add_multiple_pods(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/carousel --path TNS_App")
        assert "TNS_App/node_modules/carousel" in output
        assert "Successfully installed plugin carousel." in output
        assert file_exists("TNS_App/node_modules/carousel/package.json")
        assert file_exists(
            "TNS_App/node_modules/carousel/platforms/ios/Podfile")

        output = run_aut("cat TNS_App/package.json")
        assert "carousel" in output

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/keychain --path TNS_App")
        assert "TNS_App/node_modules/keychain" in output
        assert "Successfully installed plugin keychain." in output
        assert file_exists("TNS_App/node_modules/keychain/package.json")
        assert file_exists(
            "TNS_App/node_modules/keychain/platforms/ios/Podfile")

        output = run_aut("cat TNS_App/package.json")
        assert "keychain" in output

        output = build(platform="ios", path="TNS_App")
        assert "Installing pods..." in output
        assert "Successfully prepared plugin carousel for ios." in output
        assert "Successfully prepared plugin keychain for ios." in output

        output = run_aut("cat TNS_App/platforms/ios/Podfile")
        assert "use_frameworks!" in output
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output
        assert "pod 'UICKeyChainStore'" in output

        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert file_exists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

        build(platform="ios", mode="release", for_device=True, path="TNS_App")

    def test_201_plugin_add_pod_google_maps_before_platform_add_ios(self):
        create_project(proj_name="TNS_App")

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/googlesdk --path TNS_App")
        assert "TNS_App/node_modules/googlesdk" in output
        assert "Successfully installed plugin googlesdk." in output
        assert file_exists("TNS_App/node_modules/googlesdk/package.json")
        assert file_exists(
            "TNS_App/node_modules/googlesdk/platforms/ios/Podfile")

        output = run_aut("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "googlesdk" in output

        platform_add(
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            path="TNS_App",
            symlink=True)
        output = prepare(platform="ios", path="TNS_App", log_trace=True)
        assert "The iOS Deployment Target is now 8.0" in output
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = run_aut("cat TNS_App/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output

        # This deployment target comes from the CLI
        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_deployMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'
        output = run_aut(
            "cat TNS_App/platforms/ios/Pods/Pods.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_deployMENT_TARGET = 8.1;" in output
        build(platform="ios", path="TNS_App")
        build(platform="ios", mode="release", for_device=True, path="TNS_App")

    def test_202_plugin_add_pod_google_maps_after_platform_add_ios(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/googlesdk --path TNS_App")
        assert "TNS_App/node_modules/googlesdk" in output
        assert "Successfully installed plugin googlesdk." in output
        assert file_exists("TNS_App/node_modules/googlesdk/package.json")
        assert file_exists(
            "TNS_App/node_modules/googlesdk/platforms/ios/Podfile")

        output = run_aut("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "googlesdk" in output

        output = build(platform="ios", path="TNS_App")
        assert "The iOS Deployment Target is now 8.0" in output
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = run_aut("cat TNS_App/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert file_exists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

        # This deployment target comes from the CLI
        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_deployMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'
        output = run_aut(
            "cat TNS_App/platforms/ios/Pods/Pods.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_deployMENT_TARGET = 8.1;" in output

        build(platform="ios", mode="release", for_device=True, path="TNS_App")

    @unittest.skip(
        "This is not a valid scenario anymore. " + \
        "It fails because DEPLOYMENT_TARGET=7.0 which is updated during plugin add command.")
    def test_400_prepare_install_pods(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        run_aut(
            "cp QA-TestApps/CocoaPods/carousel/platforms/ios/Podfile TNS_App/platforms/ios")
        output = build(platform="ios", path="TNS_App")
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = run_aut("cat TNS_App/platforms/ios/Podfile")
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output

        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert file_exists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

    def test_401_plugin_add_invalid_pod(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="ios",
            framework_path=IOS_RUNTIME_SYMLINK_PATH,
            symlink=True)

        output = run_aut(
            TNSPATH +
            " plugin add QA-TestApps/CocoaPods/invalidpod --path TNS_App")
        assert "TNS_App/node_modules/invalidpod" in output
        assert "Successfully installed plugin invalidpod." in output
        assert file_exists("TNS_App/node_modules/invalidpod/package.json")
        assert file_exists(
            "TNS_App/node_modules/invalidpod/platforms/ios/Podfile")

        output = run_aut("cat TNS_App/package.json")
        assert "invalidpod" in output

        output = prepare(platform="ios", path="TNS_App", assert_success=False)
        assert "Installing pods..." in output
        assert "Processing node_modules failed. Error:" in output

        output = run_aut("cat TNS_App/platforms/ios/Podfile")
        assert "pod 'InvalidPod'" in output

        assert not file_exists("TNS_App/platforms/ios/TNSApp.xcworkspace")
        assert not file_exists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")
