import os

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TEST_RUN_HOME
from core.tns.tns import Tns
from core.xcode.xcode import Xcode
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class BuildiOSNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Xcode.cleanup_cache()

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
        Folder.cleanup("ChangeAppLocationNG.app")
        File.remove("ChangeAppLocationNG.ipa")
        Folder.cleanup("ChangeAppLocationAndNameNG.app")
        File.remove("ChangeAppLocationAndNameNG.ipa")
        Folder.cleanup("ChangeAppResLocationNG.app")
        File.remove("ChangeAppResLocationNG.ipa")
        Folder.cleanup("ChangeAppResLocationInRootNG.app")
        File.remove("ChangeAppResLocationInRootNG.ipa")
        Folder.cleanup("RenameAppNG.app")
        File.remove("RenameAppNG.ipa")
        Folder.cleanup("RenameAppResNG.app")
        File.remove("RenameAppResNG.ipa")

    @parameterized.expand([
        'ChangeAppLocationNG',
        'ChangeAppLocationAndNameNG',
        'ChangeAppResLocationNG',
        'ChangeAppResLocationInRootNG',
        'RenameAppNG',
        'RenameAppResNG'
    ])
    def test_100_build_ios_ng_project(self, app_name):
        Tns.build_ios(attributes={"--path": app_name})

    @parameterized.expand([
        'ChangeAppLocationNG',
        'ChangeAppLocationAndNameNG',
        'ChangeAppResLocationNG',
        'ChangeAppResLocationInRootNG',
        'RenameAppNG',
        'RenameAppResNG'
    ])
    def test_200_build_ios_ng_project_release_fordevice(self, app_name):
        Tns.build_ios(attributes={"--path": app_name, "--for-device": "", "--release": ""})
        platform_folder = os.path.join(app_name, 'platforms', 'ios', app_name, 'app', 'item')
        assert File.pattern_exists(platform_folder, '*.js'), "JS files not found!"
        assert not File.pattern_exists(platform_folder, '*.ts'), "TS files found!"
