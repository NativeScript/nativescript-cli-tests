import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import CURRENT_OS, ANDROID_RUNTIME_PATH, OSType, IOS_RUNTIME_PATH
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_installed_platforms import Platforms
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class TypescriptIOSTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Tns.create_app_ts(cls.app_name)
        Tns.platform_add_ios(attributes={"--frameworkPath": IOS_RUNTIME_PATH, "--path": cls.app_name})

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup('./' + cls.app_name)

    def test_001_prepare(self):
        """
        Assert prepare of TypeScript project works properly.
        - Prepare executes TypeScript plugin hooks
        - Prepare in debug should move .ts files to the platforms folder
        - Prepare in release should remove all .ts files to the platforms folder
        """

        # Assert initial prepare is full
        output = Tns.prepare_ios(attributes={"--path": self.app_name})
        TnsAsserts.prepared(app_name=self.app_name, prepare_type=Prepare.FULL, output=output,
                            platform=Platforms.IOS)

        # prepare should execute TypeScript plugin hooks
        assert before_prepare in output
        assert peer_typeScript in output
        assert error not in output.lower()
        # TODO: Finish the test

        '''
        if CURRENT_OS == OSType.OSX:
            # prepare in debug => .ts should go to the platforms folder
            output = Tns.prepare_ios(attributes={"--path": self.app_name})
            assert before_prepare in output
            assert peer_typeScript in output
            assert error not in output.lower()

            assert File.extension_exists(self.app_folder, ".js")
            assert not File.extension_exists(self.app_folder, ".map")
            assert File.extension_exists(self.app_folder, ".ts")

            assert File.extension_exists(self.assets_folder + "/app", ".js")
            assert not File.extension_exists(self.assets_folder + "/app", ".map")
            assert File.extension_exists(self.assets_folder + "/app", ".ts")
            assert File.extension_exists(self.modules_folder + "/application", ".js")
            assert not File.extension_exists(self.modules_folder + "/application", ".ts")

            # Verify inline source map in native iOS app
            output = File.read(self.app_name + "/platforms/ios/TNSApp/app/app.js")
            assert "//# sourceMappingURL=data:application/json;base64" in output
            '''

    def test_002_build(self):
        Tns.build_ios(attributes={"--path": self.app_name})
        # TODO: Finish the test
