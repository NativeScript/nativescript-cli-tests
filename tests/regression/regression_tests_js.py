import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.java.java import Java
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import TEST_RUN_HOME, CURRENT_OS, SIMULATOR_NAME, \
    ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, \
    EMULATOR_ID
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from tests.webpack.helpers.helpers import Helpers


@unittest.skipIf(Java.version() != "1.8", "Run only if Java version is 8.")
class RegressionTestsJS(BaseClass):
    SIMULATOR_ID = ""

    image_original = 'hello-world-js'
    image_change = 'hello-world-js-js-css-xml'

    xml_change = ['app/main-page.xml', 'TAP', 'TEST']
    js_change = ['app/main-view-model.js', 'taps', 'clicks']
    css_change = ['app/app.css', '18', '32']

    target_app = os.path.join(TEST_RUN_HOME, BaseClass.app_name)
    source_app = os.path.join(TEST_RUN_HOME, 'data', 'apps', 'test-app-js-34')

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

        Folder.cleanup(cls.target_app)
        Folder.copy(cls.source_app, cls.target_app)
        
        Emulator.stop()
        Emulator.ensure_available()
        if CURRENT_OS == OSType.OSX:
            cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)

    def setUp(self):
        Tns.kill()
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_001_build_android(self):
        # Debug build
        Tns.build_android(attributes={"--path": self.app_name})

        # Release build
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": ""})

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_002_build_ios(self):
        Tns.build_ios(attributes={"--path": self.app_name}, log_trace=True)
        Tns.build_ios(attributes={"--path": self.app_name, "--release": ""}, log_trace=True)

        # Verify no aar and frameworks in platforms folder
        assert not File.pattern_exists(self.app_name + "/platforms/ios", "*.aar")
        assert not File.pattern_exists(self.app_name + "/platforms/ios/TestApp/app/tns_modules", "*.framework")

    def test_100_run_android(self):
        log = Tns.run_android(attributes={'--path': self.app_name,
                                          '--device': EMULATOR_ID}, wait=False, assert_success=False)
        Tns.wait_for_log(log_file=log, string_list=['Project successfully built', 'Successfully installed'],
                         timeout=180)
        Helpers.android_screen_match(image=self.image_original, timeout=80)

        # Change JS, XML and CSS
        ReplaceHelper.replace(self.app_name, self.js_change, sleep=10)
        ReplaceHelper.replace(self.app_name, self.xml_change, sleep=10)
        ReplaceHelper.replace(self.app_name, self.css_change, sleep=10)

        # Verify application looks correct
        Helpers.android_screen_match(image=self.image_change, timeout=80)

        # Revert changes
        ReplaceHelper.rollback(self.app_name, self.js_change, sleep=10)
        ReplaceHelper.rollback(self.app_name, self.xml_change, sleep=10)
        ReplaceHelper.rollback(self.app_name, self.css_change, sleep=10)

        # Verify application looks correct
        Helpers.android_screen_match(image=self.image_original, timeout=80)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_101_tns_run_ios(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns run ios` and wait until app is deployed
        log = Tns.run_ios(attributes={'--path': self.app_name, '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Project successfully built', 'Successfully installed on device with identifier', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=log, string_list=strings, timeout=150, check_interval=10)

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='hello-world-js', timeout=60)

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, self.js_change, sleep=10)
        ReplaceHelper.replace(self.app_name, self.xml_change, sleep=3)
        ReplaceHelper.replace(self.app_name, self.css_change, sleep=3)

        # Verify application looks correct
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID,
                            expected_image='hello-world-js-js-css-xml', timeout=60)

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_name, self.js_change, sleep=10)
        ReplaceHelper.rollback(self.app_name, self.xml_change, sleep=3)
        ReplaceHelper.rollback(self.app_name, self.css_change, sleep=3)

        # Verify app looks correct inside simulator
        Device.screen_match(device_name=SIMULATOR_NAME,
                            device_id=self.SIMULATOR_ID, expected_image='hello-world-js', timeout=60)

    def test_200_build_android_webpack(self):
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--bundle": "",
                                      "--env.uglify": "",
                                      "--env.snapshot": ""})
        Helpers.run_android_via_adb(app_name=self.app_name, config="release", image=self.image_original)

    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Run only on macOS.")
    def test_200_ios_build_release_with_bundle_and_uglify(self):
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": ""})
        Tns.build_ios(attributes={"--path": self.app_name, "--release": "", "--for-device": "", "--bundle": "",
                                  "--env.uglify": "", "--env.aot": ""})

        # verification_errors = Helpers.verify_size(app_name=self.app_name, config="js-ios-bundle-uglify")
        # self.assertEqual([], verification_errors)
