import os

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns


class BuildAndroidNGTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Folder.cleanup('./' + cls.app_name)
        Tns.create_app_ng(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    def test_010_build_android_ng_project(self):
        Tns.build_android(attributes={"--path": self.app_name})
        assert File.exists(self.app_name + "/platforms/android/build/outputs/apk/TNSApp-debug.apk")

    def test_210_build_android_ng_project_release(self):
        output = Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                               " --keyStorePassword": ANDROID_KEYSTORE_PASS,
                                               " --keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                               " --keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                               " --release": "",
                                               "--path": self.app_name
                                               })
        assert "Project successfully prepared" in output
        assert "BUILD SUCCESSFUL" in output

        assert "Project successfully built" in output
        assert File.exists(self.app_name + "/platforms/android/build/outputs/apk/TNSApp-release.apk")
