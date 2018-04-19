from core.base_class.BaseNSConfigClass import BaseNSConfigClass
from core.settings.settings import ANDROID_PACKAGE, IOS_PACKAGE
from core.tns.tns import Tns
from tests.nsconfig.run_android_tests import RunAndroidEmulatorTests
from tests.nsconfig.build_android_tests import BuildAndroidTests
from tests.nsconfig.debug_android_tests import DebugAndroidEmulatorTests
from tests.nsconfig.run_android_ng_tests import RunAndroidEmulatorTestsNG
from tests.nsconfig.build_android_ng_tests import BuildAndroidNGTests
from core.osutils.file import File
from core.osutils.folder import Folder

class SuiteRunAndroid(BaseNSConfigClass):
    @classmethod
    def setUpClass(cls):
        BaseNSConfigClass.setUpClass(cls.__name__)
        BaseNSConfigClass.createAppsNG(cls.__name__)
        BaseNSConfigClass.createAppsLiveSyncNG(cls.__name__)

        # add platform
        Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_location_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_location_and_name_ng,
                                         "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_res_location_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_res_location_in_root_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_rename_app_ng, "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_rename_app_res_ng, "--frameworkPath": ANDROID_PACKAGE})

        #add platform livesync
        Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_location_ls_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_location_and_name_ls_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_res_location_ls_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_change_app_res_location_in_root_ls_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": cls.app_name_rename_app_ls_ng, "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_android(
            attributes={"--path": cls.app_name_rename_app_res_ls_ng, "--frameworkPath": ANDROID_PACKAGE})

    def setUp(self):
        BaseNSConfigClass.setUp(self)

    def tearDown(self):
        Folder.cleanup(self.platforms_android + '/build/outputs')

    @classmethod
    def tearDownClass(cls):
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

        Folder.cleanup("ChangeAppLocationLSNG")
        Folder.cleanup("ChangeAppLocationAndNameLSNG")
        Folder.cleanup("ChangeAppResLocationLSNG")
        Folder.cleanup("ChangeAppResLocationInRootLSNG")
        Folder.cleanup("RenameAppLSNG")
        Folder.cleanup("RenameAppResLSNG")
        Folder.cleanup("ChangeAppLocationLSNG.app")
        File.remove("ChangeAppLocationLSNG.ipa")
        Folder.cleanup("ChangeAppLocationAndNameLSNG.app")
        File.remove("ChangeAppLocationAndNameLSNG.ipa")
        Folder.cleanup("ChangeAppResLocationLSNG.app")
        File.remove("ChangeAppResLocationLSNG.ipa")
        Folder.cleanup("ChangeAppResLocationInRootLSNG.app")
        File.remove("ChangeAppResLocationInRootLSNG.ipa")
        Folder.cleanup("RenameAppLSNG.app")
        File.remove("RenameAppLSNG.ipa")
        Folder.cleanup("RenameAppResLSNG.app")
        File.remove("RenameAppResLSNG.ipa")
        pass

    # def build_android(self):
    #     BuildAndroidTests()
    #
    # def run_android(self):
    #     RunAndroidEmulatorTests()
    #
    # def debug_android(self):
    #     DebugAndroidEmulatorTests()

def suite(self):
        suite.addTest(RunAndroidEmulatorTestsNG())
        suite.addTest(BuildAndroidNGTests())
        return suite