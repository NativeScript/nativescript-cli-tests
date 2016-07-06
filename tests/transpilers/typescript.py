import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, CURRENT_OS, IOS_RUNTIME_SYMLINK_PATH, OSType, \
    TEST_RUN_HOME, TNS_PATH
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
        output = run(TNS_PATH + " create TNS_App --tsc")
        assert "nativescript-dev-typescript@" in output
        assert "nativescript-hook@" in output

        assert File.extension_exists(
            "TNS_App/node_modules/tns-core-modules", ".d.ts")
        assert File.exists("TNS_App/tsconfig.json")
        assert File.exists("TNS_App/node_modules/typescript/bin/tsc")
        assert not Folder.is_empty("TNS_App/node_modules/nativescript-dev-typescript")
        assert File.exists("TNS_App/hooks/before-prepare/nativescript-dev-typescript.js")
        assert File.exists("TNS_App/hooks/before-watch/nativescript-dev-typescript.js")

        output = run("cat TNS_App/package.json")
        assert "devDependencies" in output
        assert "nativescript-dev-typescript" in output

        Tns.platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path="TNS_App")
        if CURRENT_OS == OSType.OSX:
            Tns.platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)

    def test_101_transpilation_typescript_prepare_debug(self):

        # prepare in debug => .ts should go to the platforms folder
        output = Tns.prepare(path="TNS_App", platform="android")
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert "error" not in output

        assert File.extension_exists("TNS_App/app", ".js")
        assert File.extension_exists("TNS_App/app", ".map")
        assert File.extension_exists("TNS_App/app", ".ts")

        # Verify source map in app
        output = run("cat ./TNS_App/app/app.js")
        assert "//# sourceMappingURL=app.js.map" in output

        output = run("cat ./TNS_App/app/app.js.map")
        assert "\"file\":\"app.js\"" in output
        assert "\"sources\":[\"app.ts\"]" in output

        assert File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".js")
        assert File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".map")
        assert File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".ts")
        assert File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/application", ".js")
        assert not File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/application", ".ts")

        # Verify source map in native android app
        output = run("cat ./TNS_App/platforms/android/src/main/assets/app/app.js")
        assert "//# sourceMappingURL=app.js.map" in output

        output = run("cat ./TNS_App/platforms/android/src/main/assets/app/app.js.map")
        assert "\"file\":\"app.js\"" in output
        assert "\"sources\":[\"app.ts\"]" in output

        if CURRENT_OS == OSType.OSX:

            # prepare in debug => .ts should go to the platforms folder
            output = Tns.prepare(platform="ios", path="TNS_App")
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert "error" not in output

            assert File.extension_exists("TNS_App/app", ".js")
            assert File.extension_exists("TNS_App/app", ".map")
            assert File.extension_exists("TNS_App/app", ".ts")

            assert File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app", ".js")
            assert File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app", ".map")
            assert File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app", ".ts")
            assert File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/application", ".js")
            assert not File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/application", ".ts")

            # Verify source map in native iOS app
            output = run("cat ./TNS_App/platforms/ios/TNSApp/app/app.js")
            assert "//# sourceMappingURL=app.js.map" in output

            output = run("cat ./TNS_App/platforms/ios/TNSApp/app/app.js.map")
            assert "\"file\":\"app.js\"" in output
            assert "\"sources\":[\"app.ts\"]" in output

    def test_201_transpilation_typescript_prepare_release(self):
        # prepare in release => .ts should NOT go to the platforms folder
        output = Tns.prepare(path="TNS_App", platform="android", release=True)
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert "error" not in output

        assert File.extension_exists("TNS_App/app", ".js")
        assert File.extension_exists("TNS_App/app", ".map")
        assert File.extension_exists("TNS_App/app", ".ts")

        assert File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".js")
        assert not File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".map")
        assert not File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".ts")
        assert File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/application", ".js")
        assert not File.extension_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules/application", ".ts")

        if CURRENT_OS == OSType.OSX:

            # prepare in release => .ts should NOT go to the platforms folder
            output = Tns.prepare(platform="ios", path="TNS_App", release=True)
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert "error" not in output

            assert File.extension_exists("TNS_App/app", ".js")
            assert File.extension_exists("TNS_App/app", ".map")
            assert File.extension_exists("TNS_App/app", ".ts")

            assert File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app", ".js")
            assert not File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app", ".map")
            assert not File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app", ".ts")
            assert File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/application", ".js")
            assert not File.extension_exists(
                "TNS_App/platforms/android/src/main/assets/app/tns_modules/application", ".ts")

    def test_301_transpilation_after_node_modules_deleted(self):
        Folder.cleanup("TNS_App/node_modules")
        # Next line is because prepare does not work if you npm install packages with relative path before that
        Folder.navigate_to("TNS_App")
        run(".." + os.path.sep + TNS_PATH + " prepare android")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        # Verify that the `prepare` command installs correct dependencies.
        assert File.exists("TNS_App/node_modules/nativescript-dev-typescript")
        assert File.exists("TNS_App/node_modules/tns-core-modules")
        assert File.exists("TNS_App/node_modules/typescript")
