"""
Tests for building projects for Android platform with different nsconfig setup.
"""
import datetime
import os
from zipfile import ZipFile

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_ALIAS_PASS, TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts
from tests.nsconfig.create_apps.create_ns_config_apps import CreateNSConfigApps


class BuildAndroidTests(BaseClass):
    debug_apk = "app-debug.apk"
    release_apk = "app-release.apk"

    app_name = ""
    platforms_android = ""

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

        File.remove(cls.debug_apk)
        File.remove(cls.release_apk)
        Folder.cleanup('temp')

        if File.exists(TEST_RUN_HOME + "/data/Projects/ChangeAppLocation"):
            assert "ChangeAppLocation" in TEST_RUN_HOME + "/data/Projects/ChangeAppLocation"
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocation", TEST_RUN_HOME + "/ChangeAppLocation")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndName",
                        TEST_RUN_HOME + "/ChangeAppLocationAndName")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocation", TEST_RUN_HOME + "/ChangeAppResLocation")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRoot",
                        TEST_RUN_HOME + "/ChangeAppResLocationInRoot")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameApp", TEST_RUN_HOME + "/RenameApp")
            Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppRes", TEST_RUN_HOME + "/RenameAppRes")
        else:
            CreateNSConfigApps.createApps()
            if not File.exists(TEST_RUN_HOME + "/ChangeAppLocation"):
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocation", TEST_RUN_HOME + "/ChangeAppLocation")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppLocationAndName",
                            TEST_RUN_HOME + "/ChangeAppLocationAndName")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocation",
                            TEST_RUN_HOME + "/ChangeAppResLocation")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/ChangeAppResLocationInRoot",
                            TEST_RUN_HOME + "/ChangeAppResLocationInRoot")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameApp", TEST_RUN_HOME + "/RenameApp")
                Folder.copy(TEST_RUN_HOME + "/data/Projects/RenameAppRes", TEST_RUN_HOME + "/RenameAppRes")
            else:
                assert "ChangeAppLocation" in TEST_RUN_HOME + "/"

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        # Verify application state at the end of the test is correct
        if File.exists(self.app_name):
            data = TnsAsserts.get_package_json(self.app_name)
            assert "tns-android" in data["nativescript"], "'tns-android' not found under `nativescript` in package.json"
            assert "tns-android" not in data["dependencies"], "'tns-android' found under `dependencies` in package.json"

            BaseClass.tearDown(self)
        Folder.cleanup(self.platforms_android + '/build/outputs')

    @classmethod
    def tearDownClass(cls):
        File.remove(cls.debug_apk)
        File.remove(cls.release_apk)
        Folder.cleanup('temp')

        Folder.cleanup("ChangeAppLocation")
        Folder.cleanup("ChangeAppLocationAndName")
        Folder.cleanup("ChangeAppResLocation")
        Folder.cleanup("ChangeAppResLocationInRoot")
        Folder.cleanup("RenameApp")
        Folder.cleanup("RenameAppRes")
        pass

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_001_build_android(self, app_name):
        self.app_name = app_name
        self.platforms_android = self.app_name + "/" + TnsAsserts.PLATFORM_ANDROID

        Tns.build_android(attributes={"--path": self.app_name})

        assert File.pattern_exists(self.platforms_android, "*.aar")
        assert not File.pattern_exists(self.platforms_android, "*.plist")
        assert not File.pattern_exists(self.platforms_android, "*.android.js")
        assert not File.pattern_exists(self.platforms_android, "*.ios.js")

        # Configs are respected
        assert 'debug' in File.read(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH, 'config.json'))

        # Verify incremental native build
        before_build = datetime.datetime.now()
        output = Tns.build_android(attributes={"--path": self.app_name})
        after_build = datetime.datetime.now()
        assert "Gradle build..." in output, "Gradle build not called."
        assert output.count("Gradle build...") is 1, "Only one gradle build is triggered."
        assert (after_build - before_build).total_seconds() < 20, "Incremental build takes more then 20 sec."

        # Verify platform specific files
        assert File.pattern_exists(self.platforms_android, "*.aar")
        assert not File.pattern_exists(self.platforms_android, "*.plist")
        assert not File.pattern_exists(self.platforms_android, "*.android.js")
        assert not File.pattern_exists(self.platforms_android, "*.ios.js")

        # Verify apk does not contain aar files
        archive = ZipFile(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_DEBUG_PATH, self.debug_apk))
        archive.extractall(self.app_name + "/temp")
        archive.close()
        assert not File.pattern_exists(self.app_name + "/temp", "*.aar")
        assert not File.pattern_exists(self.app_name + "/temp", "*.plist")
        assert not File.pattern_exists(self.app_name + "/temp", "*.android.*")
        assert not File.pattern_exists(self.app_name + "/temp", "*.ios.*")
        Folder.cleanup(self.app_name + "/temp")

        # Verify incremental native build
        before_build = datetime.datetime.now()
        output = Tns.build_android(attributes={"--path": self.app_name})
        after_build = datetime.datetime.now()
        assert "Gradle build..." in output, "Gradle build not called."
        assert output.count("Gradle build...") is 1, "Only one gradle build is triggered."
        assert (after_build - before_build).total_seconds() < 15, "Incremental build takes more then 15 sec."

        # Verify clean build force native project rebuild
        before_build = datetime.datetime.now()
        output = Tns.build_android(attributes={"--path": self.app_name, "--clean": ""})
        after_build = datetime.datetime.now()
        build_time = (after_build - before_build).total_seconds()
        assert "Gradle build..." in output, "Gradle build not called."
        assert output.count("Gradle build...") is 2, "Only one gradle build is triggered."
        assert build_time > 10, "Clean build takes less then 15 sec."
        assert build_time < 90, "Clean build takes more than 90 sec."

    @parameterized.expand([
        'ChangeAppLocation',
        'ChangeAppLocationAndName',
        'ChangeAppResLocation',
        'ChangeAppResLocationInRoot',
        'RenameApp',
        'RenameAppRes'
    ])
    def test_002_build_android_release(self, app_name):
        self.app_name = app_name

        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": ""
                                      }, log_trace=True)

        # Configs are respected
        assert 'release' in File.read(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH, 'config.json'))
        assert File.exists(os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APK_RELEASE_PATH, self.release_apk))
