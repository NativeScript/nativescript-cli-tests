import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, CURRENT_OS, IOS_RUNTIME_SYMLINK_PATH, OSType, \
    TEST_RUN_HOME, TNS_PATH
from core.tns.tns import Tns


class Typescript_Tests(unittest.TestCase):
    app_name = "TNS_App"
    app_folder = os.path.join(app_name, "app")
    node_modules_folder = os.path.join(app_name, "node_modules")
    hooks_folder = os.path.join(app_name, "Hooks")
    assets_folder = os.path.join(app_name, "platforms", "android", "src", "main", "assets")

    @classmethod
    def setUpClass(cls):
        Folder.cleanup(cls.app_name)

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
        Folder.cleanup(cls.app_name)

    def test_001_transpilation_typescript(self):
        output = run(TNS_PATH + " create " + self.app_name + " --tsc")
        assert "nativescript-dev-typescript@" in output
        assert "nativescript-hook@" in output

        assert File.extension_exists(self.node_modules_folder + "/tns-core-modules", ".d.ts")
        assert File.exists(self.app_name + "/tsconfig.json")
        assert File.exists(self.node_modules_folder + "/typescript/bin/tsc")
        assert not Folder.is_empty(self.node_modules_folder + "/nativescript-dev-typescript")
        assert File.exists(self.hooks_folder + "/before-prepare/nativescript-dev-typescript.js")
        assert File.exists(self.hooks_folder + "/before-watch/nativescript-dev-typescript.js")

        output = run("cat " + self.app_name + "/package.json")
        assert "devDependencies" in output
        assert "nativescript-dev-typescript" in output

        Tns.platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path=self.app_name)
        if CURRENT_OS == OSType.OSX:
            Tns.platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                path=self.app_name,
                symlink=True)

    def test_101_transpilation_typescript_prepare_debug(self):

        # prepare in debug => .ts should go to the platforms folder
        output = Tns.prepare(path=self.app_name, platform="android")
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert "error" not in output

        assert File.extension_exists(self.app_folder, ".js")
        assert File.extension_exists(self.app_folder, ".map")
        assert File.extension_exists(self.app_folder, ".ts")

        # Verify source map in app
        output = run("cat ./" + self.app_folder + "app.js")
        assert "//# sourceMappingURL=app.js.map" in output

        output = run("cat ./" + self.app_folder + "/app.js.map")
        assert "\"file\":\"app.js\"" in output
        assert "\"sources\":[\"app.ts\"]" in output

        assert File.extension_exists(self.assets_folder + "/app", ".js")
        assert File.extension_exists(self.assets_folder + "/app", ".map")
        assert File.extension_exists(self.assets_folder + "/app", ".ts")
        assert File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".js")
        assert not File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".ts")

        # Verify source map in native android app
        output = run("cat ./" + self.assets_folder + "/app/app.js")
        assert "//# sourceMappingURL=app.js.map" in output

        output = run("cat ./" + self.assets_folder + "/app/app.js.map")
        assert "\"file\":\"app.js\"" in output
        assert "\"sources\":[\"app.ts\"]" in output

        if CURRENT_OS == OSType.OSX:

            # prepare in debug => .ts should go to the platforms folder
            output = Tns.prepare(platform="ios", path=self.app_name)
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert "error" not in output

            assert File.extension_exists(self.app_folder, ".js")
            assert File.extension_exists(self.app_folder, ".map")
            assert File.extension_exists(self.app_folder, ".ts")

            assert File.extension_exists(self.assets_folder + "/app", ".js")
            assert File.extension_exists(self.assets_folder + "app", ".map")
            assert File.extension_exists(self.assets_folder + "/app", ".ts")
            assert File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".js")
            assert not File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".ts")

            # Verify source map in native iOS app
            output = run("cat ./" + self.app_name + "/platforms/ios/TNSApp/app/app.js")
            assert "//# sourceMappingURL=app.js.map" in output

            output = run("cat ./" + self.app_name + "/platforms/ios/TNSApp/app/app.js.map")
            assert "\"file\":\"app.js\"" in output
            assert "\"sources\":[\"app.ts\"]" in output

    def test_201_transpilation_typescript_prepare_release(self):
        # prepare in release => .ts should NOT go to the platforms folder
        output = Tns.prepare(path=self.app_name, platform="android", release=True)
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert "error" not in output

        assert File.extension_exists(self.app_folder, ".js")
        assert File.extension_exists(self.app_folder, ".map")
        assert File.extension_exists(self.app_folder, ".ts")

        assert File.extension_exists(self.assets_folder + "/app", ".js")
        assert not File.extension_exists(self.assets_folder + "/app", ".map")
        assert not File.extension_exists(self.assets_folder + "/app", ".ts")
        assert File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".js")
        assert not File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".ts")

        if CURRENT_OS == OSType.OSX:

            # prepare in release => .ts should NOT go to the platforms folder
            output = Tns.prepare(platform="ios", path=self.app_name, release=True)
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert "error" not in output

            assert File.extension_exists(self.app_folder, ".js")
            assert File.extension_exists(self.app_folder, ".map")
            assert File.extension_exists(self.app_folder, ".ts")

            assert File.extension_exists(self.assets_folder + "/app", ".js")
            assert not File.extension_exists(self.assets_folder + "/app", ".map")
            assert not File.extension_exists(self.assets_folder + "/app", ".ts")
            assert File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".js")
            assert not File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".ts")

    def test_301_transpilation_after_node_modules_deleted(self):
        Folder.cleanup(self.node_modules_folder)
        # Next line is because prepare does not work if you npm install packages with relative path before that
        Folder.navigate_to(self.app_name)
        run(".." + os.path.sep + TNS_PATH + " prepare android")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        # Verify that the `prepare` command installs correct dependencies.
        assert File.exists(self.node_modules_folder + "/nativescript-dev-typescript")
        assert File.exists(self.node_modules_folder + "/tns-core-modules")
        assert File.exists(self.node_modules_folder + "/typescript")
