from core.base_class.BaseClass import BaseClass
from tests.nsconfig.build_android_tests import BuildAndroidTests
from tests.nsconfig.build_ios_tests import BuildiOSTests
from core.osutils.file import File
from core.osutils.folder import Folder

class SuiteRun(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        BaseClass.createApps(cls.__name__)

    def setUp(self):
        BaseClass.setUp(self)

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
        pass

def suite(self):
    # suite = unittest.TestSuite()
    suite.addTest(BuildAndroidTests())
    suite.addTest(BuildiOSTests())
    return suite