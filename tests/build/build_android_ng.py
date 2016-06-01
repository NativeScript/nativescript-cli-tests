import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns


class BuildAndroidNG(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Folder.cleanup('./TNS_App')
        output = run(TNS_PATH + " create TNS_App --ng")
        assert "successfully created" in output
        Tns.platform_add(
            platform="android",
            path="TNS_App",
            framework_path=ANDROID_RUNTIME_PATH)

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

    def test_010_build_android_ng_project(self):
        Tns.build(platform="android", path="TNS_App")
        assert File.exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_210_build_android_ng_project_release(self):
        output = run(TNS_PATH + " build android --keyStorePath " + ANDROID_KEYSTORE_PATH +
                     " --keyStorePassword " + ANDROID_KEYSTORE_PASS +
                     " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS +
                     " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS +
                     " --release --path TNS_App")

        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        assert "Project successfully built" in output
        assert File.exists("TNS_App/platforms/android/build/outputs/apk/TNSApp-release.apk")
