"""
Test for building projects with iOS platform
"""
import os

from core.base_class.BaseClass import BaseClass
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE, TNS_PATH, TEST_RUN_HOME, ANDROID_PACKAGE, PROVISIONING, \
    DISTRIBUTION_PROVISIONING, DEVELOPMENT_TEAM
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.xcode.xcode import Xcode


class BuildiOSTests(BaseClass):
    app_name_dash = "test-app"
    app_name_space = "Test App"
    app_name_noplatform = "Test_AppNoPlatform"
    app_name_ios = "testapp_ios"

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app(cls.app_name)
        Tns.platform_add_ios(attributes={"--path": cls.app_name, "--frameworkPath": IOS_PACKAGE})

        Folder.cleanup("TestApp.app")
        File.remove("TestApp.ipa")

        Xcode.cleanup_cache()


    def setUp(self):
        BaseClass.setUp(self)
        Simulator.stop()
        Folder.cleanup(self.app_name_dash)
        Folder.cleanup(self.app_name_space)
        Folder.cleanup(self.app_name_ios)
        Folder.cleanup(self.app_name_noplatform)
        Folder.cleanup(self.app_name_noplatform + '/platforms/ios/build')

        Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name}, assert_success=False)

    def tearDown(self):
        BaseClass.tearDown(self)
        assert not Simulator.is_running()[0], "Simulator started after " + self._testMethodName

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup("TestApp.app")
        File.remove("TestApp.ipa")

        Folder.cleanup(cls.app_name)
        Folder.cleanup(cls.app_name_noplatform)
        Folder.cleanup(cls.app_name_dash)
        Folder.cleanup(cls.app_name_space)

    def test_001_build_ios(self):
        Tns.build_ios(attributes={"--path": self.app_name}, log_trace=True)
        Tns.build_ios(attributes={"--path": self.app_name, "--release": ""}, log_trace=True)
        Tns.build_ios(attributes={"--path": self.app_name, "--forDevice": ""}, log_trace=True)

        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
        Tns.build_ios(attributes={"--path": self.app_name, "--forDevice": "", "--release": ""}, log_trace=True)

        # Verify no aar and frameworks in platforms folder
        assert not File.pattern_exists(self.app_name + "/platforms/ios", "*.aar")
        assert not File.pattern_exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules", "*.framework")

        # Verify ipa has both armv7 and arm64 archs
        run("mv " + self.app_name + "/platforms/ios/build/device/TestApp.ipa TestApp-ipa.tgz")
        run("unzip -o TestApp-ipa.tgz")
        output = run("lipo -info Payload/TestApp.app/TestApp")
        Folder.cleanup("Payload")
        assert "Architectures in the fat file: Payload/TestApp.app/TestApp are: armv7 arm64" in output

    def test_190_build_ios_distribution_provisions(self):
        Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)

        # List all provisions and verify them
        output = Tns.build_ios(attributes={"--path": self.app_name, "--provision": ""}, assert_success=False)
        assert "Provision Name" in output
        assert "Provision UUID" in output
        assert "App Id" in output
        assert "Team" in output
        assert "Type" in output
        assert "Due" in output
        assert "Devices" in output
        assert PROVISIONING in output
        assert DISTRIBUTION_PROVISIONING in output
        assert DEVELOPMENT_TEAM in output

        # Build with correct distribution provision
        build_attributes = {"--path": self.app_name, "--forDevice": "", "--release": "",
                            "--provision": DISTRIBUTION_PROVISIONING}
        Tns.build_ios(attributes=build_attributes)

        # Verify that passing wrong provision shows user friendly error
        output = Tns.build_ios(attributes={"--path": self.app_name, "--provision": "fake"}, assert_success=False)
        assert "Failed to find mobile provision with UUID or Name: fake" in output

    def test_200_build_ios_inside_project(self):
        Folder.navigate_to(self.app_name)
        output = Tns.build_ios(tns_path=os.path.join("..", TNS_PATH), attributes={"--path": self.app_name},
                               assert_success=False, log_trace=True)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "build/emulator/TestApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/emulator/TestApp.app")

    def test_210_build_ios_platform_not_added_or_platforms_deleted(self):
        Tns.create_app(self.app_name_noplatform)
        Tns.build_ios(attributes={"--path": self.app_name_noplatform})

    def test_300_build_ios_with_dash(self):
        Tns.create_app(self.app_name_dash)
        Tns.platform_add_ios(attributes={"--path": self.app_name_dash, "--frameworkPath": IOS_PACKAGE})
        Tns.build_ios(attributes={"--path": self.app_name_dash})

        # Verify project id
        output = File.read(self.app_name_dash + os.sep + "package.json")
        assert app_identifier in output

    def test_301_build_ios_with_space(self):
        Tns.create_app(self.app_name_space)
        Tns.platform_add_ios(attributes={"--path": "\"" + self.app_name_space + "\"",
                                         "--frameworkPath": IOS_PACKAGE})

        Tns.build_ios(attributes={"--path": "\"" + self.app_name_space + "\""})

    def test_302_build_ios_with_ios_in_path(self):
        Tns.create_app(self.app_name_ios)
        Tns.platform_add_ios(attributes={"--path": self.app_name_ios, "--frameworkPath": IOS_PACKAGE})
        Tns.build_ios(attributes={"--path": self.app_name_ios})

    def test_310_build_ios_with_copy_to(self):
        Folder.cleanup("TestApp.app")
        File.remove("TestApp.ipa")

        # Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        Tns.build_ios(attributes={"--path": self.app_name, "--copy-to": "./"}, log_trace=True)
        assert File.exists("TestApp.app")

        Tns.build_ios(attributes={"--path": self.app_name, "--forDevice": "", "--release": "", "--copy-to": "./"},
                      log_trace=True)
        assert File.exists("TestApp.ipa")

    def test_320_build_ios_with_custom_entitlements(self):
        Tns.build_ios(attributes={"--path": self.app_name})

        # Add entitlements in app/App_Resources/iOS/app.entitlements
        source = os.path.join(TEST_RUN_HOME, 'data', 'entitlements', 'app.entitlements')
        target = os.path.join(self.app_name, 'app', 'App_Resources', 'iOS', 'app.entitlements')
        File.copy(src=source, dest=target)

        # Build again and verify entitlements are merged
        Tns.build_ios(attributes={"--path": self.app_name})
        entitlements_path = self.app_name + '/platforms/ios/' + self.app_name + '/' + self.app_name + '.entitlements'
        assert File.exists(entitlements_path), "Entitlements file is missing!"
        entitlements_content = File.read(entitlements_path)
        assert '<key>aps-environment</key>' in entitlements_content, "Entitlements file content is wrong!"
        assert '<string>development</string>' in entitlements_content, "Entitlements file content is wrong!"

        # Install plugin with entitlements, build again and verify entitlements are merged
        plugin_path = os.path.join(TEST_RUN_HOME, 'data', 'plugins', 'nativescript-test-entitlements-1.0.0.tgz')
        Npm.install(package=plugin_path, option='--save', folder=self.app_name)
        Tns.build_ios(attributes={"--path": self.app_name})
        entitlements_content = File.read(entitlements_path)
        assert '<key>aps-environment</key>' in entitlements_content, "Entitlements file content is wrong!"
        assert '<string>development</string>' in entitlements_content, "Entitlements file content is wrong!"
        assert '<key>inter-app-audio</key>' in entitlements_content, "Entitlements file content is wrong!"
        assert '<true/>' in entitlements_content, "Entitlements file content is wrong!"

        # Build in release, for device (provision without entitlements)
        output = Tns.build_ios(attributes={"--path": self.app_name, "--forDevice": "", "--release": ""},
                               assert_success=False)
        assert "Provisioning profile " in output
        assert "doesn't include the inter-app-audio and aps-environment entitlements" in output

    def test_400_build_ios_with_wrong_param(self):
        Tns.create_app(self.app_name_noplatform)
        output = Tns.build_ios(attributes={"--path": self.app_name_noplatform, "--" + invalid: ""},
                               assert_success=False)
        assert invalid_option.format(invalid) in output
        assert error not in output.lower()

    def test_450_resources_update_ios(self):
        target_app = os.path.join(TEST_RUN_HOME, BaseClass.app_name)
        source_app = os.path.join(TEST_RUN_HOME, 'data', 'apps', 'test-app-js-34')
        Folder.cleanup(target_app)
        Folder.copy(source_app, target_app)

        output = Tns.run_tns_command("resources update ios", attributes={"--path": self.app_name})
        assert "The ios does not need to have its resources updated." in output
