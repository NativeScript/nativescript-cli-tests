import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import CURRENT_OS, ANDROID_RUNTIME_PATH, OSType
from core.settings.strings import *
from core.tns.tns import Tns
from core.tns.tns_installed_platforms import Platforms
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class TypescriptAndroidTests(BaseClass):

    app_folder = TnsAsserts.PLATFORM_ANDROID_APP_PATH
    node_modules_folder = TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH
    platforms_folder = os.path.join(BaseClass.app_name, "platforms")
    assets_folder = os.path.join(platforms_folder, "android", "src", "main", "assets")
    modules_folder = os.path.join(assets_folder, "app", "tns_modules", "tns-core-modules")

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Tns.create_app_ts(cls.app_name)
        Tns.platform_add_android(attributes={"--frameworkPath": ANDROID_RUNTIME_PATH, "--path": cls.app_name})

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
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        TnsAsserts.prepared(app_name=self.app_name, prepare_type=Prepare.FULL, output=output,
                            platform=Platforms.ANDROID)

        # prepare should execute TypeScript plugin hooks
        assert before_prepare in output
        assert peer_typeScript in output
        assert error not in output.lower()

        '''
        # prepare in debug => .ts should go to the platforms folder
        assert File.extension_exists(self.assets_folder, ".js")
        assert not File.extension_exists(self.assets_folder, ".map")
        assert File.extension_exists(self.assets_folder, ".ts")

        # Verify inline source map in app
        output = File.read(self.assets_folder + "app.js")
        assert "//# sourceMappingURL=data:application/json;base64" in output

        assert File.extension_exists(self.assets_folder + "app", ".js")
        assert not File.extension_exists(self.assets_folder + "app", ".map")
        assert File.extension_exists(self.assets_folder + "app", ".ts")
        assert File.extension_exists(self.modules_folder + "application", ".js")
        assert not File.extension_exists(self.modules_folder + "application", ".ts")

        # Verify inline source map in native android app
        output = run("cat ./" + self.assets_folder + "/app/app.js")
        assert "//# sourceMappingURL=data:application/json;base64" in output
        '''

    '''
    def test_002_build(self):
        output = Tns.build_android(attributes={"--path": self.app_name})
        if CURRENT_OS == OSType.OSX:
            # Tests workflow:
            # prepare android
            # prepare ios
            # build android
            assert before_prepare in output
            assert peer_typeScript in output
        else:
            # Tests workflow:
            # prepare android
            # build android
            assert skipping_prepare in output
            assert building in output
        assert error not in output.lower()

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
        assert before_prepare in output

        assert peer_typeScript in output
        assert error not in output.lower()

        assert File.extension_exists(self.app_folder, ".js")
        assert not File.extension_exists(self.app_folder, ".map")
        assert File.extension_exists(self.app_folder, ".ts")

        # Verify inline source map in app
        output = run("cat ./" + self.app_folder + "/app.js")
        assert "//# sourceMappingURL=data:application/json;base64" not in output

        assert File.extension_exists(self.assets_folder + "/app", ".js")
        assert not File.extension_exists(self.assets_folder + "/app", ".map")
        assert not File.extension_exists(self.assets_folder + "/app", ".ts")

        if "release" in CLI_PATH.lower():  # TODO: Use Settings.BRANCH
            # In this case we have a snapshot, tns-core-modules should not be available in platforms folder
            assert not Folder.exists(self.modules_folder + "/application")
        else:
            assert File.extension_exists(self.modules_folder + "/application", ".js")
            assert not File.extension_exists(self.modules_folder + "/application", ".ts")

        if CURRENT_OS == OSType.OSX:
            self.assets_folder = os.path.join(self.app_name, "platforms", "ios",
                                              self.app_name.replace("_", "").replace(" ", ""))

            # prepare in release => .ts should NOT go to the platforms folder
            output = Tns.prepare_ios(attributes={"--path": self.app_name,
                                                 "--release": ""
                                                 })
            assert before_prepare in output
            assert peer_typeScript in output
            assert error not in output.lower()

            assert File.extension_exists(self.app_folder, ".js")
            assert not File.extension_exists(self.app_folder, ".map")
            assert File.extension_exists(self.app_folder, ".ts")

            assert File.extension_exists(self.assets_folder + "/app", ".js")
            assert not File.extension_exists(self.assets_folder + "/app", ".map")
            assert not File.extension_exists(self.assets_folder + "/app", ".ts")

            if "release" in CLI_PATH.lower():  # TODO: Use Settings.BRANCH
                assert not Folder.exists(self.modules_folder + "/application")
            else:
                assert File.extension_exists(self.modules_folder + "/application", ".js")
                assert not File.extension_exists(self.modules_folder + "/application", ".ts")

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
        assert error not in output.lower()

        # TODO: Un commend when https://github.com/NativeScript/NativeScript/issues/2724 is fixed
        # if CURRENT_OS == OSType.OSX:
        #     ios_ref =
        #     "/// <reference path=\"./node_modules/tns-platform-declarations/tns-core-modules/ios/ios.d.ts\" />"
        #     File.append(self.app_name + os.sep + "references.d.ts", ios_ref)
        #     output = Tns.build_ios(attributes={"--path": self.app_name})
        #     assert "error TS" not in output

    def test_303_check_ts_compatibility(self):
        Folder.navigate_to(self.app_name)
        version = run("npm show typescript version ")
        print ("Latest npm version is " + version)
        run("npm remove typescript --save-dev")
        assert File.exists(os.path.join(os.getcwd(), "node_modules", "typescript")) == False
        run("npm install typescript@" + version)
        assert File.exists(os.path.join(os.getcwd(), "node_modules", "typescript"))
        output = run("npm list")
        assert "typescript@" + version in output

        Folder.navigate_to(TEST_RUN_HOME)
        File.copy(os.path.join(os.getcwd(), "data", "apps", "ts_compatibility", "AndroidManifest.xml"),
                  os.path.join(self.app_name, "app", "App_Resources", "Android"))
        File.copy(os.path.join(os.getcwd(), "data", "apps", "ts_compatibility", "myCustomActivity.android.ts"),
                  os.path.join(self.app_name, "app"))
        File.copy(os.path.join(os.getcwd(), "data", "apps", "ts_compatibility", "typings.d.ts"), self.app_name)
        subprocess.Popen([ADB_PATH, "-e", "logcat", "-c"])
        if CURRENT_OS != OSType.WINDOWS:
            Tns.run_android(attributes={"--path": self.app_name,
                                        "--avd": "Emulator-Api23-Default",
                                        "--justlaunch": "",
                                        "--timeout": "320"})

            process = subprocess.Popen([ADB_PATH, "-e", "logcat"], stdout=subprocess.PIPE)
            threading.Timer(10, process.terminate).start()
            output = process.communicate()[0]
            sleep(2)
            assert "java.lang.ClassNotFoundException: Didn't find class \"org.nativescript.a.MyCustomActivity\"" \
                   not in output, "Exception in output"
    '''