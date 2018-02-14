import os

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts


class BuildAndroidNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app_ng(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    def test_001_build_android_ng_project(self):
        Tns.build_android(attributes={"--path": self.app_name})

    def test_200_build_android_ng_project_release(self):
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": self.app_name
                                      })
        platform_folder = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH, 'item')
        assert File.pattern_exists(platform_folder, '*.js'), "JS files not found!"
        assert not File.pattern_exists(platform_folder, '*.ts'), "TS files found!"
