import unittest

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, CURRENT_OS, \
    IOS_PACKAGE, SIMULATOR_NAME, ANDROID_PACKAGE
from core.tns.tns import Tns
from tests.webpack.helpers.helpers import Helpers


class WebPackHelloWorldJS(BaseClass):
    SIMULATOR_ID = ""

    image_original = 'hello-world-js'
    image_change = 'hello-world-js-js-css-xml'

    xml_change = ['app/main-page.xml', 'TAP', 'TEST']
    js_change = ['app/main-view-model.js', 'taps', 'clicks']
    css_change = ['app/app.css', '18', '32']

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

        Tns.create_app(cls.app_name, update_modules=True)
        Tns.update_webpack(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})

        if CURRENT_OS == OSType.OSX:
            Simulator.stop()
            cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
            Tns.platform_add_ios(attributes={'--path': cls.app_name, '--frameworkPath': IOS_PACKAGE})

    def setUp(self):
        Tns.kill()
        Helpers.emulator_cleanup(app_name=self.app_name)
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_001_android_build_release_with_bundle(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="js-android-bundle")
        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)
        self.assertEqual([], verification_errors)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_001_ios_build_release_with_bundle(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": ""})
        verification_errors = Helpers.verify_size(app_name=self.app_name, config="js-ios-bundle")
        self.assertEqual([], verification_errors)

    def test_100_android_build_release_with_bundle_and_uglify(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.uglify": "",
                                      "--env.aot": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="js-android-bundle-uglify")
        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)
        self.assertEqual([], verification_errors)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_100_ios_build_release_with_bundle_and_uglify(self):
        # Hack to workaround https://github.com/NativeScript/nativescript-dev-webpack/issues/602
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": ""})
        # ...remove the live above when the issues is fixed.

        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                  "--env.uglify": "", "--env.aot": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="js-ios-bundle-uglify")
        self.assertEqual([], verification_errors)

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Windows can't build with snapshot.")
    def test_110_android_build_release_with_bundle_and_snapshot(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.snapshot": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="js-android-bundle-snapshot",
                                                  check_embedded_script_size=True)
        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)
        self.assertEqual([], verification_errors)

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Windows can't build with snapshot.")
    def test_120_android_build_release_with_bundle_and_snapshot_and_uglify(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.uglify": "",
                                      "--env.aot": "",
                                      "--env.snapshot": ""})

        verification_errors = Helpers.verify_size(app_name=self.app_name, config="js-android-bundle-uglify-snapshot",
                                                  check_embedded_script_size=True)
        Helpers.run_android_via_adb(app_name=self.app_name, image=self.image_original)
        self.assertEqual([], verification_errors)

    def test_400_build_with_bundle_without_plugin(self):
        Tns.create_app(self.app_name)
        Npm.uninstall(package="nativescript-dev-webpack", option="--save-dev", folder=self.app_name)
        output = Tns.build_android(attributes={"--path": self.app_name, "--bundle": ""}, assert_success=False)
        assert "Passing --bundle requires a bundling plugin." in output
        assert "No bundling plugin found or the specified bundling plugin is invalid." in output
