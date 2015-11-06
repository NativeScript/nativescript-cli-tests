import unittest

from helpers._os_lib import cleanup_folder, check_file_exists, folder_exists, run_aut
from helpers._tns_lib import iosRuntimePath, \
    build, create_project, platform_add, library_add

# pylint: disable=R0201, C0111


class Library_OSX(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_Library_Add_iOS_Framework(self):
        create_project(proj_name="TNS_App")
        platform_add(
            platform="ios",
            framework_path=iosRuntimePath,
            path="TNS_App")

        library_add(
            platform="ios",
            libPath="QA-TestApps/external-lib/TelerikUI.framework",
            path="TNS_App")
        assert (
            check_file_exists(
                "TNS_App/lib/iOS/TelerikUI.framework",
                "library_add_Framework_1.1.0.txt"))

        build(platform="ios", path="TNS_App")
        output = run_aut(
            "cat TNS_App/platforms/ios/TNSApp.xcodeproj/project.pbxproj | grep TelerikUI")
        assert "TelerikUI.framework in Frameworks" in output
        assert "TelerikUI.framework in Embed Frameworks" in output
        assert "/TelerikUI.framework" in output
        assert not "TNS_App/lib/iOS/TelerikUI.framework" in output

    def test_401_Library_Add_iOS_NoLib(self):
        create_project(proj_name="TNS_App")
        platform_add(
            platform="ios",
            framework_path=iosRuntimePath,
            path="TNS_App")

        output = library_add(
            platform="ios",
            libPath="TelerikUI.framework",
            path="TNS_App",
            assertSuccess=False)
        assert ".framework does not exist" in output
        assert not folder_exists("TNS_App/lib")
