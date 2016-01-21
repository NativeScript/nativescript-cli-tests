"""
Tests for prepare command in context of iOS
"""

import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH, CURRENT_OS, OSType
from core.tns.tns import Tns


class PrepareiOS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if CURRENT_OS != OSType.OSX:
            raise NameError("Can not run iOS tests on non OSX OS.")

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    def test_001_prepare_ios(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH, symlink=True)

        output = run(TNS_PATH + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

    def test_010_prepare_ios_tns_core_modules(self):
        Tns.create_app(app_name="TNS_App", copy_from="data/projects/helloworld-1.2.1/app")
        Tns.platform_add(platform="ios", path="TNS_App",
                         framework_path=IOS_RUNTIME_SYMLINK_PATH, symlink=True)

        # Make a change in tns-core-modules to verify they are not overwritten.
        File.replace("TNS_App/node_modules/tns-core-modules/application/application-common.js",
                     "(\"globals\");",
                     "(\"globals\"); // test")

        # Verify tns-core-modules are copied to the native project, not app's tns_modules.
        for i in range(1, 3):
            print "prepare number: " + str(i)

            output = run(TNS_PATH + " prepare ios --path TNS_App")
            assert "You have tns_modules dir in your app folder" in output
            assert "Project successfully prepared" in output

            output = run("cat TNS_App/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," in output

            output = run("cat TNS_App/node_modules/tns-core-modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = run("cat TNS_App/node_modules/" +
                         "tns-core-modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

            output = run("cat TNS_App/platforms/ios/TNSApp/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = run("cat TNS_App/platforms/ios/" +
                         "TNSApp/app/tns_modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

    def test_200_prepare_additional_appresources(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH, symlink=True)

        # Create new files in AppResources
        run("cp TNS_App/app/App_Resources/iOS/Default.png" +
            " TNS_App/app/App_Resources/iOS/newDefault.png")

        # prepare project
        output = run(TNS_PATH + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify XCode Project include files from App Resources folder
        output = run(
                "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep newDefault.png")
        assert "newDefault.png" in output

    def test_201_prepare_ios_platform_not_added(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " prepare ios --path TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output

        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/main-view-model.js')
        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')

    def test_300_prepare_ios_preserve_case(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH, symlink=True)
        run("cp TNS_App/node_modules/tns-core-modules/application/application-common.js" +
            " TNS_App/node_modules/tns-core-modules/application/New-application-common.js")
        run("cp TNS_App/node_modules/tns-core-modules/application/application.android.js" +
            " TNS_App/node_modules/tns-core-modules/application/New-application.android.js")
        run("cp TNS_App/node_modules/tns-core-modules/application/application.ios.js" +
            " TNS_App/node_modules/tns-core-modules/application/New-application.ios.js")

        output = run(TNS_PATH + " prepare ios --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.js')
        assert not File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.android.js')
        assert not File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/application.ios.js')

        # Verify case is preserved
        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application-common.js')
        assert File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application.js')
        assert not File.exists(
                'TNS_App/platforms/ios/TNSApp/app/tns_modules/application/New-application.ios.js')

    @unittest.skip("Ignore because of https://github.com/NativeScript/nativescript-cli/issues/1027")
    def test_301_prepare_android_does_not_prepare_ios(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios",
                                    framework_path=IOS_RUNTIME_SYMLINK_PATH, symlink=True)

        Tns.plugin_add(plugin="nativescript-social-share", path="TNS_App", assert_success=True)
        Tns.plugin_add(plugin="nativescript-iqkeyboardmanager", path="TNS_App", assert_success=True)

        output = Tns.prepare(path="TNS_App", platform="android")
        assert " " in output  # TODO: Add assert string
