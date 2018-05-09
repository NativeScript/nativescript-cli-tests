from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE
from core.tns.tns import Tns
from tests.nsconfig.build_android_ng_tests import BuildAndroidNGTests
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps
from tests.nsconfig.run_android_ng_tests import RunAndroidEmulatorTestsNG


class SuiteRunAndroidNG(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        CreateNSConfigApps.createAppsNG(cls.__name__)
        CreateNSConfigApps.createAppsLiveSyncNG(cls.__name__)

        #add platform
        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location_and_name_ng,
                                         "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_in_root_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_rename_app_ng, "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_rename_app_res_ng, "--frameworkPath": ANDROID_PACKAGE})

        #add platform livesync
        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location_ls_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location_and_name_ls_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_ls_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_in_root_ls_ng,
                                             "--frameworkPath": ANDROID_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_rename_app_ls_ng, "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_android(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app_res_ls_ng, "--frameworkPath": ANDROID_PACKAGE})

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


    def run_android_01(self):
        BuildAndroidNGTests()
        RunAndroidEmulatorTestsNG()
