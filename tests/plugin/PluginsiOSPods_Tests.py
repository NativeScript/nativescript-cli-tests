"""
Test for plugin* commands in context of iOS
"""

import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, SUT_ROOT_FOLDER
from core.tns.tns import Tns


class PluginsiOSPods_Tests(unittest.TestCase):
    app_name = "TNS_App"

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # Delete derived data
        run("rm -rf ~/Library/Developer/Xcode/DerivedData/*")
        Folder.cleanup('./' + self.app_name)

    def tearDown(self):
        pass

    def test_001_plugin_add_multiple_pods(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/carousel"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)

        assert self.app_name + "/node_modules/carousel" in output
        assert "Successfully installed plugin carousel." in output
        assert File.exists(self.app_name + "/node_modules/carousel/package.json")
        assert File.exists(self.app_name + "/node_modules/carousel/platforms/ios/Podfile")

        output = run("cat " + self.app_name + "/package.json")
        assert "carousel" in output

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/keychain"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)

        assert self.app_name + "/node_modules/keychain" in output
        assert "Successfully installed plugin keychain." in output
        assert File.exists(self.app_name + "/node_modules/keychain/package.json")
        assert File.exists(self.app_name + "/node_modules/keychain/platforms/ios/Podfile")

        output = run("cat " + self.app_name + "/package.json")
        assert "keychain" in output

        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Installing pods..." in output
        assert "Successfully prepared plugin carousel for ios." in output
        assert "Successfully prepared plugin keychain for ios." in output

        output = run("cat " + self.app_name + "/platforms/ios/Podfile")
        assert "use_frameworks!" in output
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output
        assert "pod 'UICKeyChainStore'" in output

        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert File.exists(self.app_name + "/platforms/ios/Pods/Pods.xcodeproj")

        Tns.build_ios(attributes={"--path": self.app_name,
                                  "--release": "",
                                  "--for-device": ""
                                  })

    def test_201_plugin_add_pod_google_maps_before_platform_add_ios(self):
        Tns.create_app(self.app_name)

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/googlesdk"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)

        assert self.app_name + "/node_modules/googlesdk" in output
        assert "Successfully installed plugin googlesdk." in output
        assert File.exists(self.app_name + "/node_modules/googlesdk/package.json")
        assert File.exists(self.app_name + "/node_modules/googlesdk/platforms/ios/Podfile")

        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "googlesdk" in output

        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        output = Tns.prepare_ios(attributes={"--path": self.app_name}, log_trace=True)
        
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Installing pods..." in output

        output = run("cat " + self.app_name + "/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output

        # This deployment target comes from the CLI
        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'
        # output = run(
        #         "cat " + self.app_name + "/platforms/ios/Pods/Pods.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        # assert "IPHONEOS_DEPLOYMENT_TARGET = 8.1;" in output
        Tns.build_ios(attributes={"--path": self.app_name})
        Tns.build_ios(attributes={"--path": self.app_name,
                                  "--release": "",
                                  "--for-device": ""
                                  })

    def test_202_plugin_add_pod_google_maps_after_platform_add_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/googlesdk"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert self.app_name + "/node_modules/googlesdk" in output
        assert "Successfully installed plugin googlesdk." in output
        assert File.exists(self.app_name + "/node_modules/googlesdk/package.json")
        assert File.exists(self.app_name + "/node_modules/googlesdk/platforms/ios/Podfile")

        output = run("cat " + self.app_name + "/package.json")
        assert "org.nativescript.TNSApp" in output
        assert "dependencies" in output
        assert "googlesdk" in output

        output = Tns.build_ios(attributes={"--path": self.app_name})
        
        assert "Successfully prepared plugin googlesdk for ios." in output
        assert "Installing pods..." in output

        output = run("cat " + self.app_name + "/platforms/ios/Podfile")
        assert "source 'https://github.com/CocoaPods/Specs.git'" in output
        assert "platform :ios, '8.1'" in output
        assert "pod 'GoogleMaps'" in output
        assert "use_frameworks!" in output

        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert File.exists(self.app_name + "/platforms/ios/Pods/Pods.xcodeproj")

        # This deployment target comes from the CLI
        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        assert "IPHONEOS_DEPLOYMENT_TARGET = 8.0;" in output
        # This deployment target comes from the Podfile - platform :ios, '8.1'
        # output = run(
        #         "cat " + self.app_name + "/platforms/ios/Pods/Pods.xcodeproj/project.pbxproj | grep \"DEPLOYMENT\"")
        # assert "IPHONEOS_DEPLOYMENT_TARGET = 8.1;" in output

        Tns.build_ios(attributes={"--path": self.app_name,
                                  "--release": "",
                                  "--for-device": ""
                                  })

    @unittest.skip(
            "This is not a valid scenario anymore. " +
            "It fails because DEPLOYMENT_TARGET=7.0 which is updated during plugin add command.")
    def test_400_prepare_install_pods(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "symlink": ""
                                         })

        run("cp QA-TestApps/CocoaPods/carousel/platforms/ios/Podfile " + self.app_name + "/platforms/ios")
        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "Creating project scheme..." in output
        assert "Installing pods..." in output

        output = run("cat " + self.app_name + "/platforms/ios/Podfile")
        assert "pod 'iCarousel'" in output
        assert "pod 'AFNetworking'" in output

        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp.xcworkspace/contents.xcworkspacedata")
        assert "location = \"group:TNSApp.xcodeproj\">" in output
        assert "location = \"group:Pods/Pods.xcodeproj\">" in output
        assert File.exists(self.app_name + "/platforms/ios/Pods/Pods.xcodeproj")

    def test_401_plugin_add_invalid_pod(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        plugin_path = SUT_ROOT_FOLDER + "/QA-TestApps/CocoaPods/invalidpod"
        output = Tns.plugin_add(plugin_path, attributes={"--path": self.app_name}, assert_success=False)
        assert self.app_name + "/node_modules/invalidpod" in output
        assert "Successfully installed plugin invalidpod." in output
        assert File.exists(self.app_name + "/node_modules/invalidpod/package.json")
        assert File.exists(self.app_name + "/node_modules/invalidpod/platforms/ios/Podfile")

        output = run("cat " + self.app_name + "/package.json")
        assert "invalidpod" in output

        output = Tns.prepare_ios(attributes={"--path": self.app_name}, assert_success=False)
        assert "Installing pods..." in output
        assert "Processing node_modules failed. Error:" in output

        output = run("cat " + self.app_name + "/platforms/ios/Podfile")
        assert "pod 'InvalidPod'" in output

        assert not File.exists(self.app_name + "/platforms/ios/TNSApp.xcworkspace")
        assert not File.exists(self.app_name + "/platforms/ios/Pods/Pods.xcodeproj")
