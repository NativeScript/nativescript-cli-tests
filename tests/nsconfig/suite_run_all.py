from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE, IOS_PACKAGE
from core.tns.tns import Tns
from tests.nsconfig.build_android_tests import BuildAndroidTests
from tests.nsconfig.build_ios_tests import BuildiOSTests
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps
from tests.nsconfig.debug_android_tests import DebugAndroidEmulatorTests
from tests.nsconfig.debug_ios_chrome_tests import DebugiOSChromeSimulatorTests
from tests.nsconfig.debug_ios_inspector_tests import DebugiOSInspectorSimulatorTests
from tests.nsconfig.run_android_tests import RunAndroidEmulatorTests
from tests.nsconfig.run_ios_tests import RunIOSSimulatorTests


class SuiteRunAll(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        CreateNSConfigApps.createApps()
        CreateNSConfigApps.createAppsLiveSync()

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location,
                                             "--frameworkPath": ANDROID_PACKAGE})

        # add platform
        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_change_app_location, "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location_and_name,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(attributes={"--path": CreateNSConfigApps.app_name_change_app_location_and_name,
                                         "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location, "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_in_root,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_in_root,
                                         "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app, "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app, "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app_res, "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app_res, "--frameworkPath": IOS_PACKAGE})

        # add platform livesync projects
        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location_ls,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_change_app_location_ls, "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_location_and_name_ls,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_change_app_location_and_name_ls,
                        "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_ls,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_ls,
                                         "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_in_root_ls,
                                             "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_change_app_res_location_in_root_ls,
                        "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app_ls, "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app_ls, "--frameworkPath": IOS_PACKAGE})

        Tns.platform_add_android(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app_res_ls, "--frameworkPath": ANDROID_PACKAGE})
        Tns.platform_add_ios(
            attributes={"--path": CreateNSConfigApps.app_name_rename_app_res_ls, "--frameworkPath": IOS_PACKAGE})

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup("ChangeAppLocation")
        Folder.cleanup("ChangeAppLocationAndName")
        Folder.cleanup("ChangeAppResLocation")
        Folder.cleanup("ChangeAppResLocationInRoot")
        Folder.cleanup("RenameApp")
        Folder.cleanup("RenameAppRes")
        Folder.cleanup("ChangeAppLocation.app")
        File.remove("ChangeAppLocation.ipa")
        Folder.cleanup("ChangeAppLocationAndName.app")
        File.remove("ChangeAppLocationAndName.ipa")
        Folder.cleanup("ChangeAppResLocation.app")
        File.remove("ChangeAppResLocation.ipa")
        Folder.cleanup("ChangeAppResLocationInRoot.app")
        File.remove("ChangeAppResLocationInRoot.ipa")
        Folder.cleanup("RenameApp.app")
        File.remove("RenameApp.ipa")
        Folder.cleanup("RenameAppRes.app")
        File.remove("RenameAppRes.ipa")

        Folder.cleanup("ChangeAppLocationLS")
        Folder.cleanup("ChangeAppLocationAndNameLS")
        Folder.cleanup("ChangeAppResLocationLS")
        Folder.cleanup("ChangeAppResLocationInRootLS")
        Folder.cleanup("RenameAppLS")
        Folder.cleanup("RenameAppResLS")
        Folder.cleanup("ChangeAppLocationLS.app")
        File.remove("ChangeAppLocationLS.ipa")
        Folder.cleanup("ChangeAppLocationAndNameLS.app")
        File.remove("ChangeAppLocationAndNameLS.ipa")
        Folder.cleanup("ChangeAppResLocationLS.app")
        File.remove("ChangeAppResLocationLS.ipa")
        Folder.cleanup("ChangeAppResLocationInRootLS.app")
        File.remove("ChangeAppResLocationInRootLS.ipa")
        Folder.cleanup("RenameAppLS.app")
        File.remove("RenameAppLS.ipa")
        Folder.cleanup("RenameAppResLS.app")
        File.remove("RenameAppResLS.ipa")
        pass

    def suite(self):
        BuildAndroidTests()
        BuildiOSTests()
        RunAndroidEmulatorTests()
        RunIOSSimulatorTests()
        DebugAndroidEmulatorTests()
        DebugiOSInspectorSimulatorTests()
        DebugiOSChromeSimulatorTests()
<<<<<<< Updated upstream
=======
        BuildiOSNGTests()
        BuildAndroidNGTests()
        RunIOSSimulatorTestsNG()
        RunAndroidEmulatorTestsNG()
>>>>>>> Stashed changes
