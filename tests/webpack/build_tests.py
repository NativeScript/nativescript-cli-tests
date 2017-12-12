import datetime
import os
import random

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers.adb import Adb
from core.npm.npm import Npm
from core.osutils.file import File
from core.settings.settings import ANDROID_RUNTIME_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_ALIAS_PASS, EMULATOR_NAME, \
    EMULATOR_ID, OUTPUT_FOLDER
from core.tns.tns import Tns


class WebPackBuildAndRunTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

        Tns.create_app(cls.app_name)
        Npm.install(package="nativescript-dev-webpack@next", option='--save-dev', folder=cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        Tns.create_app_ts(cls.app_name_ts)
        Npm.install(package="nativescript-dev-webpack@next", option='--save-dev', folder=cls.app_name_ts)
        Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev')
        Npm.install(package="nativescript-dev-typescript@next", option='--save-dev', folder=cls.app_name_ts)
        Tns.platform_add_android(attributes={"--path": cls.app_name_ts, "--frameworkPath": ANDROID_RUNTIME_PATH})

        Tns.create_app_ng(cls.app_name_ng)
        Npm.install(package="nativescript-dev-webpack@next", option='--save-dev', folder=cls.app_name_ng)
        Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev')
        Npm.install(package="nativescript-dev-typescript@next", option='--save-dev', folder=cls.app_name_ts)
        Tns.platform_add_android(attributes={"--path": cls.app_name_ng, "--frameworkPath": ANDROID_RUNTIME_PATH})

    def setUp(self):
        File.remove(file_path=self.get_log_file(app_name=self.app_name))
        File.remove(file_path=self.get_log_file(app_name=self.app_name_ts))
        File.remove(file_path=self.get_log_file(app_name=self.app_name_ng))

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def get_log_file(self, app_name):
        return os.path.join(OUTPUT_FOLDER, 'build_steps_' + app_name + '.log')

    def log_action(self, app_name, text):
        import time
        time = time.time()
        timestamp = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        text = timestamp + ' ' + text
        File.append(file_path=self.get_log_file(app_name), text=text)

    def build_android_debug(self, app_name):
        Tns.kill()
        self.log_action(app_name=app_name, text="BUILD ANDROID - DEBUG")
        Tns.build_android(attributes={"--path": app_name})

    def build_android_release(self, app_name):
        Tns.kill()
        self.log_action(app_name=app_name, text="BUILD ANDROID - RELEASE")
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": app_name
                                      })

    def build_android_debug_webpack(self, app_name):
        Tns.kill()
        self.log_action(app_name=app_name, text="BUILD ANDROID - DEBUG & WEBPACK")
        Tns.build_android(attributes={"--path": app_name, "--bundle": ""})

    def build_android_release_webpack(self, app_name):
        Tns.kill()
        self.log_action(app_name=app_name, text="BUILD ANDROID - RELEASE & WEBPACK")
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": app_name,
                                      "--bundle": ""
                                      })

    def build_android_release_webpack_uglify(self, app_name):
        Tns.kill()
        self.log_action(app_name=app_name, text="BUILD ANDROID - RELEASE & WEBPACK")
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": app_name,
                                      "--bundle": ""
                                      })

    def build_android_release_webpack_snapshot(self, app_name):
        Tns.kill()
        self.log_action(app_name=app_name, text="BUILD ANDROID - RELEASE & WEBPACK")
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": app_name,
                                      "--bundle": ""
                                      })

    def build_android_release_webpack_snapshot(self, app_name):
        Tns.kill()
        self.log_action(app_name=app_name, text="BUILD ANDROID - RELEASE & WEBPACK")
        Tns.build_android(attributes={"--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--path": app_name,
                                      "--bundle": ""
                                      })

    def run_android(self, app_name, flavor):
        Tns.kill()
        Adb.clear_logcat(device_id=EMULATOR_ID)
        Adb.stop_application(device_id=EMULATOR_ID, app_id=Tns.get_app_id(app_name))
        self.log_action(app_name=app_name, text="RUN APP...")
        log = Tns.run_android(attributes={'--path': app_name, '--device': EMULATOR_ID}, wait=False,
                              assert_success=False)
        strings = ['Successfully installed on device with identifier', EMULATOR_ID, 'Successfully synced application']
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image='hello-world-' + flavor)
        Adb.stop_application(device_id=EMULATOR_ID, app_id=Tns.get_app_id(app_name))
        self.log_action(app_name=app_name, text="LOOKS OK")

    def test_100_build_android_js_project(self):
        for x in xrange(25):
            config = random.choice([1, 2, 3, 4])
            if config == 1:
                self.build_android_debug(self.app_name)
            if config == 2:
                self.build_android_release(self.app_name)
            if config == 3:
                self.build_android_debug_webpack(self.app_name)
            if config == 4:
                self.build_android_release_webpack(self.app_name)
            self.run_android(self.app_name, "js")

    def test_200_build_android_ts_project(self):
        for x in xrange(25):
            config = random.choice([1, 2, 3, 4])
            if config == 1:
                self.build_android_debug(self.app_name_ts)
            if config == 2:
                self.build_android_release(self.app_name_ts)
            if config == 3:
                self.build_android_debug_webpack(self.app_name_ts)
            if config == 4:
                self.build_android_release_webpack(self.app_name_ts)
            self.run_android(self.app_name_ts, "ts")

    def test_300_build_android_ng_project(self):
        for x in xrange(25):
            config = random.choice([1, 2, 3, 4])
            if config == 1:
                self.build_android_debug(self.app_name_ng)
            if config == 2:
                self.build_android_release(self.app_name_ng)
            if config == 3:
                self.build_android_debug_webpack(self.app_name_ng)
            if config == 4:
                self.build_android_release_webpack(self.app_name_ng)
            self.run_android(self.app_name_ng, "ng")
