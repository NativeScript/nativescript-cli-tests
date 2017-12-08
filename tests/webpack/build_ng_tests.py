import os
import random

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts


class WebPackBuildNGTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app_ng(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(cls.app_name)

    def build_android_debug(self):
        print "BUILD ANDROID - DEBUG"
        Tns.build_android(attributes={"--path": self.app_name})

    def build_android_release(self):
        print "BUILD ANDROID - RELEASE"
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": self.app_name
                                      })
        platform_folder = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH, 'item')
        assert File.pattern_exists(platform_folder, '*.js'), "JS files not found!"
        assert not File.pattern_exists(platform_folder, '*.ts'), "TS files found!"

    def build_android_debug_webpack(self):
        print "BUILD ANDROID - DEBUG & WebPack"
        Tns.build_android(attributes={"--path": self.app_name, "--bundle": ""})

    def build_android_release_webpack(self):
        print "BUILD ANDROID - RELEASE & WebPack"
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": self.app_name,
                                      "--bundle": ""
                                      })
        platform_folder = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH, 'item')
        assert File.pattern_exists(platform_folder, '*.js'), "JS files not found!"
        assert not File.pattern_exists(platform_folder, '*.ts'), "TS files found!"

    def test_300_build_android_ng_project(self):
        for x in xrange(20):
            config = random.choice([1, 2, 3, 4])
            if config == 1:
                self.build_android_debug()
            if config == 2:
                self.build_android_release()
            if config == 3:
                self.build_android_debug_webpack()
            if config == 4:
                self.build_androbuild_android_release_webpackid_debug()
