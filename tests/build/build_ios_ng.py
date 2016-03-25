import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH, TNS_PATH
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class BuildiOSNG(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Xcode.cleanup_cache()
        Folder.cleanup('./TNS_App')

        output = run(TNS_PATH + " create TNS_App --ng")
        assert "successfully created" in output
        Tns.platform_add(
            platform="ios",
            path="TNS_App",
            framework_path=IOS_RUNTIME_SYMLINK_PATH, symlink=True)

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./TNS_App')

    def test_010_build_ios_ng_project(self):
        output = run(TNS_PATH + " build ios --path TNS_App")
        assert "Project successfully prepared" in output
        assert "build/emulator/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/emulator/TNSApp.app")

    def test_210_build_ios_ng_project_release_fordevice(self):
        output = run(TNS_PATH +
                     " build ios --path TNS_App --for-device --release")
        assert "Project successfully prepared" in output
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert "** BUILD SUCCEEDED **" in output
        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/ios/build/device/TNSApp.ipa")
