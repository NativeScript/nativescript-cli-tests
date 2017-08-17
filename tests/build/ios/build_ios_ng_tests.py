import os

from core.base_class.BaseClass import BaseClass
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class BuildiOSNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Xcode.cleanup_cache()

        Tns.create_app_ng(app_name=cls.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={"--path": cls.app_name, "--frameworkPath": IOS_RUNTIME_PATH})

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    def test_100_build_ios_ng_project(self):
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_200_build_ios_ng_project_release_fordevice(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--for-device": "", "--release": ""})
