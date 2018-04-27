import os

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_ALIAS_PASS, TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class BuildAndroidNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

        if File.exists(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationNG"):
            assert "ChangeAppLocationNG" in TEST_RUN_HOME + "/data/Projects/ChangeAppLocationNG"
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationNG", TEST_RUN_HOME + "/ChangeAppLocationNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameNG",
                        TEST_RUN_HOME + "/ChangeAppLocationAndNameNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationNG", TEST_RUN_HOME + "/ChangeAppResLocationNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootNG",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRootNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppNG", TEST_RUN_HOME + "/RenameAppNG")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppResNG", TEST_RUN_HOME + "/RenameAppResNG")
        else:
            CreateNSConfigApps.createAppsNG(cls.__name__)
            if not File.exists(TEST_RUN_HOME + "/ChangeAppLocationNG"):
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationNG", TEST_RUN_HOME + "/ChangeAppLocationNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndNameNG",
                            TEST_RUN_HOME + "/ChangeAppLocationAndNameNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationNG", TEST_RUN_HOME + "/ChangeAppResLocationNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRootNG",
                            TEST_RUN_HOME + "/ChangeAppResLocationInRootNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppNG", TEST_RUN_HOME + "/RenameAppNG")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppResNG", TEST_RUN_HOME + "/RenameAppResNG")
            else:
                assert "ChangeAppLocationNG" in TEST_RUN_HOME + "/"

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

        Folder.cleanup("ChangeAppLocationNG")
        Folder.cleanup("ChangeAppLocationAndNameNG")
        Folder.cleanup("ChangeAppResLocationNG")
        Folder.cleanup("ChangeAppResLocationInRootNG")
        Folder.cleanup("RenameAppNG")
        Folder.cleanup("RenameAppResNG")

    @parameterized.expand([
        'ChangeAppLocationNG',
        'ChangeAppLocationAndNameNG',
        'ChangeAppResLocationNG',
        'ChangeAppResLocationInRootNG',
        'RenameAppNG',
        'RenameAppResNG'
    ])
    def test_001_build_android_ng_project(self, app_name):
        Tns.build_android(attributes={"--path": app_name})

    @parameterized.expand([
        'ChangeAppLocationNG',
        'ChangeAppLocationAndNameNG',
        'ChangeAppResLocationNG',
        'ChangeAppResLocationInRootNG',
        'RenameAppNG',
        'RenameAppResNG'
    ])
    def test_200_build_android_ng_project_release(self, app_name):
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": app_name
                                      })
        platform_folder = os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH, 'item')
        assert File.pattern_exists(platform_folder, '*.js'), "JS files not found!"
        assert not File.pattern_exists(platform_folder, '*.ts'), "TS files found!"
