import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, CURRENT_OS, IOS_RUNTIME_SYMLINK_PATH, OSType, \
    TEST_RUN_HOME, TNS_PATH, SUT_ROOT_FOLDER, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, \
    ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns


class TypescriptTests(BaseClass):
    app_folder = os.path.join(BaseClass.app_name, "app")
    node_modules_folder = os.path.join(BaseClass.app_name, "node_modules")
    platforms_folder = os.path.join(BaseClass.app_name, "platforms")
    hooks_folder = os.path.join(BaseClass.app_name, "hooks")
    assets_folder = os.path.join(BaseClass.app_name, "platforms", "android", "src", "main", "assets")

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)

        output = Tns.create_app(TypescriptTests.app_name, attributes={"--tsc": ""})
        assert "nativescript-dev-typescript@" in output
        assert "nativescript-hook@" in output

        assert File.extension_exists(TypescriptTests.node_modules_folder + "/tns-core-modules", ".d.ts")
        assert File.exists(TypescriptTests.app_name + "/tsconfig.json")
        assert File.exists(TypescriptTests.node_modules_folder + "/typescript/bin/tsc")
        assert not Folder.is_empty(TypescriptTests.node_modules_folder + "/nativescript-dev-typescript")
        assert File.exists(TypescriptTests.hooks_folder + "/before-prepare/nativescript-dev-typescript.js")
        assert File.exists(TypescriptTests.hooks_folder + "/before-watch/nativescript-dev-typescript.js")

        output = run("cat " + TypescriptTests.app_name + "/package.json")
        assert "devDependencies" in output
        assert "nativescript-dev-typescript" in output

        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH,
                                             "--path": TypescriptTests.app_name
                                             })
        if CURRENT_OS == OSType.OSX:
            Tns.platform_add_ios(attributes={"--frameworkPath": IOS_RUNTIME_SYMLINK_PATH,
                                             "--path": TypescriptTests.app_name,
                                             "--symlink": ""
                                             })

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(TypescriptTests.platforms_folder)

    def tearDown(self):
        BaseClass.setUp(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup('./' + cls.app_name)

    def test_001_prepare(self):

        # prepare in debug => .ts should go to the platforms folder
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert "error" not in output

        assert File.extension_exists(self.app_folder, ".js")
        assert File.extension_exists(self.app_folder, ".map")
        assert File.extension_exists(self.app_folder, ".ts")

        # Verify source map in app
        output = run("cat ./" + self.app_folder + "/app.js")
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
            output = Tns.prepare_ios(attributes={"--path": self.app_name})
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert "error" not in output

            assert File.extension_exists(self.app_folder, ".js")
            assert File.extension_exists(self.app_folder, ".map")
            assert File.extension_exists(self.app_folder, ".ts")

            assert File.extension_exists(self.assets_folder + "/app", ".js")
            assert File.extension_exists(self.assets_folder + "/app", ".map")
            assert File.extension_exists(self.assets_folder + "/app", ".ts")
            assert File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".js")
            assert not File.extension_exists(self.assets_folder + "/app/tns_modules/application", ".ts")

            # Verify source map in native iOS app
            output = run("cat ./" + self.app_name + "/platforms/ios/TNSApp/app/app.js")
            assert "//# sourceMappingURL=app.js.map" in output

            output = run("cat ./" + self.app_name + "/platforms/ios/TNSApp/app/app.js.map")
            assert "\"file\":\"app.js\"" in output
            assert "\"sources\":[\"app.ts\"]" in output

    def test_002_build(self):
        output = Tns.build_android(attributes={"--path": self.app_name})
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert "error TS" not in output
        assert "error" not in output

    def test_201_prepare_release(self):
        # prepare in release => .ts should NOT go to the platforms folder
        output = Tns.prepare_android(attributes={"--path": self.app_name,
                                                 "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                                 "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                                 "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                                 "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                                 "--copy-to": "./",
                                                 "--release": ""
                                                 })
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
            output = Tns.prepare_ios(attributes={"--path": self.app_name,
                                                 "--release": ""
                                                 })
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

    def test_301_prepare_after_node_modules_deleted(self):
        Folder.cleanup(self.node_modules_folder)
        # Next line is because prepare does not work if you npm install packages with relative path before that
        Folder.navigate_to(self.app_name)
        Tns.run_tns_command("prepare android", tns_path=".." + os.path.sep + TNS_PATH)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        # Verify that the `prepare` command installs correct dependencies.
        assert File.exists(self.node_modules_folder + "/nativescript-dev-typescript")
        assert File.exists(self.node_modules_folder + "/tns-core-modules")
        assert File.exists(self.node_modules_folder + "/typescript")

    def test_302_build_with_platform_dts(self):
        Folder.navigate_to(self.app_name)
        run("npm install " + SUT_ROOT_FOLDER + os.sep + "tns-platform-declarations.tgz --save-dev")
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        File.exists(self.app_name + "/node_modules/tns-platform-declarations/tns-core-modules/android17.d.ts")
        File.exists(self.app_name + "/node_modules/tns-platform-declarations/tns-core-modules/ios/ios.d.ts")
        andr_ref = "/// <reference path=\"./node_modules/tns-platform-declarations/tns-core-modules/android17.d.ts\" />"
        File.append(self.app_name + os.sep + "references.d.ts", andr_ref)
        output = Tns.build_android(attributes={"--path": self.app_name})
        assert "error TS" not in output

        # TODO: Un commend when https://github.com/NativeScript/NativeScript/issues/2724 is fixed
        # if CURRENT_OS == OSType.OSX:
        #     ios_ref =
        #     "/// <reference path=\"./node_modules/tns-platform-declarations/tns-core-modules/ios/ios.d.ts\" />"
        #     File.append(self.app_name + os.sep + "references.d.ts", ios_ref)
        #     output = Tns.build_ios(attributes={"--path": self.app_name})
        #     assert "error TS" not in output
