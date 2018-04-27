from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE
from core.tns.tns import Tns
from tests.nsconfig.build_android_ng_tests import BuildAndroidNGTests
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps
from tests.nsconfig.run_android_ng_tests import RunAndroidEmulatorTestsNG


# class Test1(unittest.TestCase):
    # def testOne(self):
    #     BaseNSConfigClass.createAppsNG(self.__name__)
    #     pass

# class Test1(unittest.TestCase):
#     def TestOne(self):
#         print "Hello 1"
#         pass
#
#     def TestTwo(self):
#         print "Hello 2"
#         pass
#
# class Test2(unittest.TestCase):
#     def TestThree(self):
#         pass
#     def testFour(self):
#         pass
#
# if __name__ == '__main__':
#     # Run only the tests in the specified classes
#
#     test_classes_to_run = [Test1, Test2]
#
#     loader = unittest.TestLoader()
#
#     suites_list = []
#     for test_class in test_classes_to_run:
#         suite = loader.loadTestsFromTestCase(test_class)
#         suites_list.append(suite)
#
#     big_suite = unittest.TestSuite(suites_list)
#
#     runner = unittest.TextTestRunner()
#     results = runner.run(big_suite)

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
