import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, IOS_RUNTIME_SYMLINK_PATH, CURRENT_OS, OSType, \
    SUT_ROOT_FOLDER
from core.tns.tns import Tns


class TypeScript(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Folder.cleanup('TNS_App')

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('TNS_App')

    def test_001_transpilation_typescript(self):
        Tns.create_app(app_name="TNS_App", copy_from=SUT_ROOT_FOLDER + os.path.sep + "template-hello-world-ts")
        Tns.platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path="TNS_App")

        assert File.extension_exists(
                "TNS_App/node_modules/tns-core-modules", ".d.ts")

        output = run(TNS_PATH + " install typescript --path TNS_App")
        assert "nativescript-dev-typescript@" in output
        assert "nativescript-hook@" in output

        assert File.exists("TNS_App/tsconfig.json")
        assert File.exists("TNS_App/node_modules/typescript/bin/tsc")
        assert not Folder.is_empty("TNS_App/node_modules/nativescript-dev-typescript")
        assert File.exists("TNS_App/hooks/before-prepare/nativescript-dev-typescript.js")
        assert File.exists("TNS_App/hooks/before-watch/nativescript-dev-typescript.js")

        output = run("cat TNS_App/package.json")
        assert "devDependencies" in output
        assert "nativescript-dev-typescript" in output

        output = Tns.prepare(path="TNS_App", platform="android")
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert "error" not in output

        assert File.extension_exists("TNS_App/app", ".js")
        assert File.extension_exists("TNS_App/app", ".ts")

        assert File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app", ".js")
        assert not File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app", ".ts")
        assert not File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules", ".ts")
        Tns.build(platform="android", path="TNS_App")

        if CURRENT_OS == OSType.OSX:
            Tns.platform_add(
                    platform="ios",
                    framework_path=IOS_RUNTIME_SYMLINK_PATH,
                    path="TNS_App",
                    symlink=True)

            output = Tns.prepare(platform="ios", path="TNS_App")
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert "error" not in output

            assert File.extension_exists("TNS_App/app", ".js")
            assert File.extension_exists("TNS_App/app", ".ts")

            assert File.extension_exists(
                    "TNS_App/platforms/ios/TNSApp/app", ".js")
            assert not File.extension_exists(
                    "TNS_App/platforms/ios/TNSApp/app", ".ts")
            assert not File.extension_exists(
                    "TNS_App/platforms/ios/TNSApp/app/tns_modules", ".ts")
            Tns.build(platform="ios", path="TNS_App")

    def test_201_transpilation_after_node_modules_deleted(self):
        run("rm -rf TNS_App/node_modules")
        Tns.prepare(platform="android", path="TNS_App")

        # Verify that the `prepare` command installs correct dependencies.
        output = run("ls TNS_App/node_modules | wc -l")
        assert "3" in output, "The 'prepare' command does not install correct dependences."
