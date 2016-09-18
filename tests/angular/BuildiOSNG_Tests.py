from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_SYMLINK_PATH
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class BuildiOSNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        super(BuildiOSNGTests, cls).setUpClass()

        Xcode.cleanup_cache()
        Folder.cleanup('./' + cls.app_name)

        Tns.create_app(app_name=cls.app_name, attributes={"--ng": ""})
        Tns.platform_add_ios(attributes={"--path": cls.app_name,
                                         "--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                         "--symlink": ""
                                         })

    @classmethod
    def tearDownClass(cls):
        super(BuildiOSNGTests, cls).tearDownClass()
        Folder.cleanup('./' + cls.app_name)

    def test_010_build_ios_ng_project(self):
        output = Tns.build_ios(attributes={"--path": self.app_name})
        assert "build/emulator/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/emulator/TNSApp.app")

    def test_210_build_ios_ng_project_release_fordevice(self):
        output = Tns.build_ios(attributes={"--path": self.app_name,
                                           "--for-device": "",
                                           "--release": ""})
        assert "CONFIGURATION Release" in output
        assert "CodeSign" in output
        assert "build/device/TNSApp.app" in output
        assert File.exists(self.app_name + "/platforms/ios/build/device/TNSApp.ipa")
