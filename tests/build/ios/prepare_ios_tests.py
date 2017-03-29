"""
Tests for prepare command in context of iOS
"""

import os.path
import re

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH, CURRENT_OS, OSType
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class PrepareiOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        if CURRENT_OS != OSType.OSX:
            raise NameError("Can not run iOS tests on non OSX OS.")

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def test_101_prepare_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        # Initial prepare should be full.
        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.FULL)

        # If no file is touched next time prepare should be skipped at all.
        output = Tns.prepare_ios(attributes={"--path": self.app_name}, assert_success=False)
        TnsAsserts.prepared(self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.SKIP)

        # If some JS/CSS/XML is changed incremental prepare should be done.
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.INCREMENTAL)

        # Verify Xcode Schemes
        output = run("xcodebuild -project " + self.app_name + "/platforms/ios/TNSApp.xcodeproj/ -list")
        assert "This project contains no schemes." not in output
        result = re.search("Targets:\n\s*TNSApp", output)
        assert result is not None
        result = re.search("Schemes:\n\s*TNSApp", output)
        assert result is not None

    def test_200_prepare_additional_appresources(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        # prepare project
        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.FULL)

        # Create new files in AppResources
        File.copy(self.app_name + "/app/App_Resources/iOS/Assets.xcassets/AppIcon.appiconset/icon-50.png",
                  self.app_name + "/app/App_Resources/iOS/newDefault.png")

        # prepare project
        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.INCREMENTAL)

        # Verify XCode Project include files from App Resources folder
        output = run("cat " + self.app_name + "/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep newDefault.png")
        assert "newDefault.png" in output

    def test_201_prepare_ios_platform_not_added(self):
        Tns.create_app(self.app_name)
        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.FIRST_TIME)

    def test_300_prepare_ios_preserve_case(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})
        File.copy(self.app_name + "/node_modules/tns-core-modules/application/application-common.js",
                  self.app_name + "/node_modules/tns-core-modules/application/New-application-common.js")
        File.copy(self.app_name + "/node_modules/tns-core-modules/application/application.android.js",
                  self.app_name + "/node_modules/tns-core-modules/application/New-application.android.js")
        File.copy(self.app_name + "/node_modules/tns-core-modules/application/application.ios.js",
                  self.app_name + "/node_modules/tns-core-modules/application/New-application.ios.js")

        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.IOS, output=output, prepare=Prepare.FULL)

        # Verify case is preserved
        path = TnsAsserts._get_ios_modules_path(self.app_name)
        assert File.exists(path + 'application/New-application-common.js')
        assert File.exists(path + 'application/New-application.js')
        assert not File.exists(path + 'application/New-application.ios.js')

    def test_301_prepare_android_does_not_prepare_ios(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

        Tns.plugin_add("nativescript-social-share", attributes={"--path": self.app_name})
        Tns.plugin_add("nativescript-iqkeyboardmanager", attributes={"--path": self.app_name})

        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "nativescript-iqkeyboardmanager is not supported for android" in output
        assert "Successfully prepared plugin nativescript-social-share for android" in output
