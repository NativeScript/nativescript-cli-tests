import unittest

from helpers._os_lib import CleanupFolder, runAUT, FileExists
from helpers._tns_lib import Build, iosRuntimeSymlinkPath, \
    tnsPath, CreateProject, PlatformAdd, Prepare, CreateProjectAndAddPlatform

# pylint: disable=R0201, C0111


class Plugins_OSX_Pods(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # Delete derived data
        runAUT("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        CleanupFolder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_PluginAdd_MultiplePods(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/CocoaPods/carousel --path TNS_App")
        assert "TNS_App/node_modules/carousel" in output
        assert "Successfully installed plugin carousel." in output
        assert FileExists("TNS_App/node_modules/carousel/package.json")
        assert FileExists(
            "TNS_App/node_modules/carousel/platforms/ios/Podfile")

        output = runAUT("cat TNS_App/package.json")
        assert "carousel" in output

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/CocoaPods/keychain --path TNS_App")
        assert "TNS_App/node_modules/keychain" in output
        assert "Successfully installed plugin keychain." in output
        assert FileExists("TNS_App/node_modules/keychain/package.json")
        assert FileExists(
            "TNS_App/node_modules/keychain/platforms/ios/Podfile")

        output = runAUT("cat TNS_App/package.json")
        assert "keychain" in output

        output = Build(platform="ios", path="TNS_App")
        assert "Installing pods..." in output
        assert "Successfully prepared plugin carousel for ios." in output
        assert "Successfully prepared plugin keychain for ios." in output

        output = runAUT("cat TNS_App/platforms/ios/Podfile")
        assert "use_frameworks!" in output
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output
        assert "pod 'UICKeyChainStore'" in output

        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert FileExists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

        Build(platform="ios", mode="release", forDevice=True, path="TNS_App")

    def test_201_PluginAdd_Pod_GoogleMaps_Before_PlatformAdd_iOS(self):
        CreateProject(projName="TNS_App")

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/CocoaPods/googlesdk --path TNS_App")
        assert "TNS_App/node_modules/googlesdk" in output
        assert "Successfully installed plugin googlesdk." in output
        assert FileExists("TNS_App/node_modules/googlesdk/package.json")
        assert FileExists(
            "TNS_App/node_modules/googlesdk/platforms/ios/Podfile")

        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "googlesdk" in output

        PlatformAdd(
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            path="TNS_App",
            symlink=True)
        output = Prepare(platform="ios", path="TNS_App", logTrace=True)
        assert "The iOS Deployment Target is now 8.0" in output
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = runAUT("cat TNS_App/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output

        # This deployment target comes from the CLI
        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'
        output = runAUT(
            "cat TNS_App/platforms/ios/Pods/Pods.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.1;" in output
        Build(platform="ios", path="TNS_App")
        Build(platform="ios", mode="release", forDevice=True, path="TNS_App")

    def test_202_PluginAdd_Pod_GoogleMaps_After_PlatformAdd_iOS(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/CocoaPods/googlesdk --path TNS_App")
        assert "TNS_App/node_modules/googlesdk" in output
        assert "Successfully installed plugin googlesdk." in output
        assert FileExists("TNS_App/node_modules/googlesdk/package.json")
        assert FileExists(
            "TNS_App/node_modules/googlesdk/platforms/ios/Podfile")

        output = runAUT("cat TNS_App/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "googlesdk" in output

        output = Build(platform="ios", path="TNS_App")
        assert "The iOS Deployment Target is now 8.0" in output
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = runAUT("cat TNS_App/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert FileExists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

        # This deployment target comes from the CLI
        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'
        output = runAUT(
            "cat TNS_App/platforms/ios/Pods/Pods.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.1;" in output

        Build(platform="ios", mode="release", forDevice=True, path="TNS_App")

    @unittest.skip(
        "This is not a valid scenario anymore. It fails because DEPLOYMENT_TARGET=7.0 which is updated during plugin add command.")
    def test_400_Prepare_Install_Pods(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)

        runAUT(
            "cp QA-TestApps/CocoaPods/carousel/platforms/ios/Podfile TNS_App/platforms/ios")
        output = Build(platform="ios", path="TNS_App")
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = runAUT("cat TNS_App/platforms/ios/Podfile")
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output

        output = runAUT(
            "cat TNS_App/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert FileExists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")

    def test_401_PluginAdd_InvalidPod(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)

        output = runAUT(
            tnsPath +
            " plugin add QA-TestApps/CocoaPods/invalidpod --path TNS_App")
        assert "TNS_App/node_modules/invalidpod" in output
        assert "Successfully installed plugin invalidpod." in output
        assert FileExists("TNS_App/node_modules/invalidpod/package.json")
        assert FileExists(
            "TNS_App/node_modules/invalidpod/platforms/ios/Podfile")

        output = runAUT("cat TNS_App/package.json")
        assert "invalidpod" in output

        output = Prepare(platform="ios", path="TNS_App", assertSuccess=False)
        assert "Installing pods..." in output
        assert "Processing node_modules failed. Error:" in output

        output = runAUT("cat TNS_App/platforms/ios/Podfile")
        assert "pod 'InvalidPod'" in output

        assert not FileExists("TNS_App/platforms/ios/TNSApp.xcworkspace")
        assert not FileExists("TNS_App/platforms/ios/Pods/Pods.xcodeproj")
