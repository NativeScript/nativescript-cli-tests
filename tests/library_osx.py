'''
Test for library command in context of iOS
'''
import unittest

from helpers._os_lib import cleanup_folder, check_file_exists, folder_exists, run_aut
from helpers._tns_lib import IOS_RUNTIME_PATH, \
    build, create_project, platform_add, library_add


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class LibraryiOS(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_library_add_ios_framework(self):
        create_project(proj_name="TNS_App")
        platform_add(
            platform="ios",
            framework_path=IOS_RUNTIME_PATH,
            path="TNS_App")

        library_add(
            platform="ios",
            lib_path="QA-TestApps/external-lib/TelerikUI.framework",
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

    def test_401_library_add_ios_no_lib(self):
        create_project(proj_name="TNS_App")
        platform_add(
            platform="ios",
            framework_path=IOS_RUNTIME_PATH,
            path="TNS_App")

        output = library_add(
            platform="ios",
            lib_path="TelerikUI.framework",
            path="TNS_App",
            assert_success=False)
        assert ".framework does not exist" in output
        assert not folder_exists("TNS_App/lib")
