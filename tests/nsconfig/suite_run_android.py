from core.base_class.BaseNSConfigClass import BaseNSConfigClass
from tests.nsconfig.run_android_tests import RunAndroidEmulatorTests
from tests.nsconfig.build_android_tests import BuildAndroidTests
from tests.nsconfig.debug_android_tests import DebugAndroidEmulatorTests
from core.osutils.file import File
from core.osutils.folder import Folder

class SuiteRunAndroid(BaseNSConfigClass):
    @classmethod
    def setUpClass(cls):
        BaseNSConfigClass.setUpClass(cls.__name__)
        BaseNSConfigClass.createApps(cls.__name__)
        BaseNSConfigClass.createAppsLiveSync(cls.__name__)

    def setUp(self):
        BaseNSConfigClass.setUp(self)

    def tearDown(self):
        Folder.cleanup(self.platforms_android + '/build/outputs')

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

    # def build_android(self):
    #     BuildAndroidTests()
    #
    # def run_android(self):
    #     RunAndroidEmulatorTests()
    #
    # def debug_android(self):
    #     DebugAndroidEmulatorTests()

def suite(self):
        suite.addTest(BuildAndroidTests())
        suite.addTest(RunAndroidEmulatorTests())
        suite.addTest(DebugAndroidEmulatorTests())
        return suite