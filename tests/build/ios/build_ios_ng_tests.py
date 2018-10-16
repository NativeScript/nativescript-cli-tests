import os

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_PACKAGE
from core.tns.tns import Tns
from core.xcode.xcode import Xcode


class BuildiOSNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Xcode.cleanup_cache()
        Tns.create_app_ng(app_name=cls.app_name, update_modules=True)
        Tns.platform_add_ios(attributes={"--path": cls.app_name, "--frameworkPath": IOS_PACKAGE})

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    def test_100_build_ios_ng_project(self):
        Tns.build_ios(attributes={"--path": self.app_name})

    def test_200_build_ios_ng_project_release_fordevice(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--for-device": "", "--release": ""})
        platform_folder = os.path.join(self.app_name, 'platforms', 'ios', self.app_name, 'app', 'app', 'item')
        assert File.pattern_exists(platform_folder, '*.js'), "JS files not found!"
        assert not File.pattern_exists(platform_folder, '*.ts'), "TS files found!"
