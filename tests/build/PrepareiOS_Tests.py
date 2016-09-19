"""
Tests for prepare command in context of iOS
"""

import re

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, CURRENT_OS, OSType
from core.tns.tns import Tns


class PrepareiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        super(PrepareiOSTests, cls).setUpClass()
        if CURRENT_OS != OSType.OSX:
            raise NameError("Can not run iOS tests on non OSX OS.")

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def test_001_prepare_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""})

        Tns.prepare_ios(attributes={"--path": self.app_name})

        # Verify app and modules are processed and available in platform folder
        assert File.exists(self.app_name + '/platforms/ios/TNSApp/app/main-view-model.js')
        assert File.exists(self.app_name + '/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not File.exists(self.app_name +
                               '/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not File.exists(self.app_name + '/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify Xcode Schemes
        output = run("xcodebuild -project " + self.app_name + "/platforms/ios/TNSApp.xcodeproj/ -list")
        assert "This project contains no schemes." not in output
        result = re.search("Targets:\n\s*TNSApp", output)
        assert result is not None
        result = re.search("Schemes:\n\s*TNSApp", output)
        assert result is not None

    def test_200_prepare_additional_appresources(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        # Create new files in AppResources
        run("cp " + self.app_name + "/app/App_Resources/iOS/Assets.xcassets/AppIcon.appiconset/icon-50.png " +
            self.app_name + "/app/App_Resources/iOS/newDefault.png")

        # prepare project
        Tns.prepare_ios(attributes={"--path": self.app_name})

        # Verify app and modules are processed and available in platform folder
        assert File.exists(self.app_name + '/platforms/ios/TNSApp/app/main-view-model.js')
        assert File.exists(self.app_name + '/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not File.exists(self.app_name +
                               '/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not File.exists(self.app_name + '/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify XCode Project include files from App Resources folder
        output = run(
                "cat " + self.app_name + "/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep newDefault.png")
        assert "newDefault.png" in output

    def test_201_prepare_ios_platform_not_added(self):
        Tns.create_app(self.app_name)
        Tns.prepare_ios(attributes={"--path": self.app_name})

        assert File.exists(self.app_name + '/platforms/ios/TNSApp/app/main-view-model.js')
        assert File.exists(self.app_name + '/platforms/ios/TNSApp/app/tns_modules/application/application.js')

    def test_210_prepare_ios_tns_core_modules(self):
        Tns.create_app(self.app_name, attributes={"--copy-from": "data/projects/helloworld-1.2.1/app"})
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        # Make a change in tns-core-modules to verify they are not overwritten.
        File.replace(self.app_name + "/node_modules/tns-core-modules/application/application-common.js",
                     "(\"globals\");",
                     "(\"globals\"); // test")

        # Verify tns-core-modules are copied to the native project, not app's tns_modules.
        for i in range(1, 3):
            print "prepare number: " + str(i)

            output = Tns.prepare_ios(attributes={"--path": self.app_name})
            assert "You have tns_modules dir in your app folder" in output

            output = File.read(self.app_name + "/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," in output

            output = File.read(self.app_name + "/node_modules/tns-core-modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = File.read(self.app_name + "/node_modules/tns-core-modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output
            output = File.read(self.app_name + "/platforms/ios/TNSApp/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = File.read(
                self.app_name + "/platforms/ios/TNSApp/app/tns_modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

    def test_300_prepare_ios_preserve_case(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })
        run("cp " + self.app_name + "/node_modules/tns-core-modules/application/application-common.js" +
            " " + self.app_name + "/node_modules/tns-core-modules/application/New-application-common.js")
        run("cp " + self.app_name + "/node_modules/tns-core-modules/application/application.android.js" +
            " " + self.app_name + "/node_modules/tns-core-modules/application/New-application.android.js")
        run("cp " + self.app_name + "/node_modules/tns-core-modules/application/application.ios.js" +
            " " + self.app_name + "/node_modules/tns-core-modules/application/New-application.ios.js")

        Tns.prepare_ios(attributes={"--path": self.app_name})

        # Verify app and modules are processed and available in platform folder
        assert File.exists(self.app_name + '/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not File.exists(self.app_name +
                               '/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not File.exists(self.app_name + '/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify case is preserved
        assert File.exists(self.app_name +
                           '/platforms/ios/TNSApp/app/tns_modules/application/New-application-common.js')
        assert File.exists(self.app_name + '/platforms/ios/TNSApp/app/tns_modules/application/New-application.js')
        assert not File.exists(self.app_name +
                               '/platforms/ios/TNSApp/app/tns_modules/application/New-application.ios.js')

    def test_301_prepare_android_does_not_prepare_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

        Tns.plugin_add("nativescript-social-share", attributes={"--path": self.app_name})
        Tns.plugin_add("nativescript-iqkeyboardmanager", attributes={"--path": self.app_name})

        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "nativescript-iqkeyboardmanager is not supported for android" in output
        assert "Successfully prepared plugin nativescript-social-share for android" in output
