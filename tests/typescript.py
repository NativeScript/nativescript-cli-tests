# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a funct
# pylint: disable=C0103, C0111, R0201


import platform, unittest
from core.commons import run
from core.constants import ANDROID_RUNTIME_PATH, IOS_RUNTIME_SYMLINK_PATH, TNS_PATH
from core.file import File
from core.folder import Folder
from core.tns import Tns


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
        Tns.create_app(app_name="TNS_App", copy_from="template-hello-world-ts")
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

        output = File.cat("TNS_App/package.json")
        assert "devDependencies" in output
        assert "nativescript-dev-typescript" in output

        output = Tns.prepare(path="TNS_App", platform="android")
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert not "error" in output

        assert File.extension_exists("TNS_App/app", ".js")
        assert File.extension_exists("TNS_App/app", ".ts")

        assert File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".js")
        assert not File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".ts")
        assert not File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules", ".ts")
        Tns.build(platform="android", path="TNS_App")

        if 'Darwin' in platform.platform():
            Tns.platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)

            output = Tns.prepare(platform="ios", path="TNS_App")
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert not "error" in output

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
