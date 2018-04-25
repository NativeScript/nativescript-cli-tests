import csv
import os
from time import sleep

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device import emulator
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.helpers import adb
from core.device.helpers.adb import Adb
from core.device.simulator import Simulator
from core.git.git import Git
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE, TYPESCRIPT_PACKAGE, WEBPACK_PACKAGE, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS_PASS, ANDROID_KEYSTORE_ALIAS, TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts
from tests.webpack.helpers.helpers import Helpers


def read_data(device_id, app_name=None):
    assert device_id in Device.get_ids(platform=Platform.ANDROID), "{0} not found!".format(device_id)
    csv_file_path = os.path.join(TEST_RUN_HOME, 'tests', 'perf', 'values.csv')
    csv_list = tuple(csv.reader(open(csv_file_path, 'rb'), delimiter=','))

    if app_name is None:
        return [tuple(l) for l in csv_list if l[3].startswith(device_id)]
    else:
        return [tuple(l) for l in csv_list if (l[3].startswith(device_id) and l[0] == app_name)]


class PerfTests(BaseClass):
    DEVICE_ID = os.getenv('DEVICE_TOKEN', None)
    APP_NAME = os.getenv('APP_NAME', None)
    DATA = read_data(DEVICE_ID, APP_NAME)

    @staticmethod
    def assert_time(expected, actual, tolerance=10, error_message="Startup time is not expected.",
                    verification_errors=[]):
        print "Actual startup: " + str(actual)
        print "Expected startup: " + str(expected)
        x = int(expected)
        y = int(actual)
        if actual >= 0:
            diff = abs(x - y) * 1.00
            try:
                assert diff <= x * tolerance * 0.01, error_message
            except AssertionError, e:
                verification_errors.append(str(e))
            return verification_errors

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Npm.cache_clean()
        Emulator.stop()
        Simulator.stop()

    def setUp(self):
        Tns.kill()
        BaseClass.tearDown(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @parameterized.expand(DATA)
    def test_prepare_android(self, demo, config, device_name, device_id, first_start, second_start):

        attributes = {"--path": self.app_name,
                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                      "--release": ""}

        if "webpack" in config:
            attr = {"--bundle": "", "--env.uglify": "", "--env.aot": ""}
            attributes.update(attr)

        if "snapshot" in config:
            attr = {"--env.snapshot": ""}
            attributes.update(attr)

        if "template" in demo:
            Tns.create_app(self.app_name, attributes={"--template": "https://github.com/" + demo})
            Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
            if "-ng" in demo:
                Tns.update_angular(self.app_name)
            if "-ng" in demo or "-ts" in demo:
                Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev', folder=self.app_name)
                Npm.install(package=TYPESCRIPT_PACKAGE, option='--save-dev', folder=self.app_name)
            if "vue" not in demo:
                Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=self.app_name)
        else:
            Folder.cleanup(self.app_name)
            Git.clone_repo(repo_url="https://github.com/" + demo, local_folder=self.app_name)
            Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name}, assert_success=False)
            Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE})
            Tns.update_modules(self.app_name)
            Npm.uninstall(package="nativescript-dev-webpack", option='--save-dev', folder=self.app_name)
            Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=self.app_name)

            json = str(TnsAsserts.get_package_json(self.app_name))
            if "angular" in json:
                Tns.update_angular(self.app_name)
            if "typescript" in json:
                Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev', folder=self.app_name)
                Npm.install(package=TYPESCRIPT_PACKAGE, option='--save-dev', folder=self.app_name)

        Tns.build_android(attributes=attributes)
        apk = Helpers.get_apk_path(app_name=self.app_name, config='release')
        destination = os.path.join(TEST_RUN_HOME, "{0}-{1}.apk".format(demo.split('/')[-1], config))
        destination_info = os.path.join(TEST_RUN_HOME, "{0}-{1}.txt".format(demo.split('/')[-1], config))
        File.remove(destination)
        File.remove(destination_info)
        File.copy(src=apk, dest=destination)
        File.write(file_path=destination_info, text=Tns.get_app_id(self.app_name))

    @parameterized.expand(DATA)
    def test_start_time(self, demo, config, device_name, device_id, first_start, second_start):
        verification_errors = []

        timesToRun = int(os.getenv('RUN_TIMES', '3'))
        old_way_of_testing_performance = os.getenv('OLD_WAY_OF_TESTING', False)

        app_id = File.read(os.path.join(TEST_RUN_HOME, "{0}-{1}.txt".format(demo.split('/')[-1], config))).strip()
        apk = os.path.join(TEST_RUN_HOME, "{0}-{1}.apk".format(demo.split('/')[-1], config))
        release_apk = os.path.join(TEST_RUN_HOME, "release-apps", "{0}-{1}.apk".format(demo.split('/')[-1], config))
        start_time_expected = 0
        second_start_expected = 0
        if old_way_of_testing_performance is False:
            for x in range(0, timesToRun):
                sleep(30)
                print "Test run number {0} for release app(for expected time).".format(x + 1)

                Adb.clear_logcat(device_id=self.DEVICE_ID)
                Adb.stop_application(device_id=self.DEVICE_ID, app_id=app_id)
                Adb.uninstall(app_id=app_id, device_id=self.DEVICE_ID, assert_success=False)
                assert not Adb.is_application_running(device_id=self.DEVICE_ID, app_id=app_id)

                Adb.install(apk_file_path=release_apk, device_id=self.DEVICE_ID)
                Device.turn_on_screen(device_id=self.DEVICE_ID)
                sleep(5)

                # Verify first start
                Adb.clear_logcat(device_id=self.DEVICE_ID)
                Adb.start_app(device_id=self.DEVICE_ID, app_id=app_id)
                sleep(5)
                Device.wait_until_app_is_running(device_id=self.DEVICE_ID, app_id=app_id, timeout=10)
                start_time = int(Device.get_start_time(self.DEVICE_ID, app_id=app_id))
                start_time_expected = start_time_expected + start_time

                # Verify second start
                Device.turn_on_screen(device_id=self.DEVICE_ID)
                Adb.stop_application(device_id=self.DEVICE_ID, app_id=app_id)
                assert not Adb.is_application_running(device_id=self.DEVICE_ID, app_id=app_id)
                sleep(5)
                Device.turn_on_screen(device_id=self.DEVICE_ID)
                Adb.clear_logcat(device_id=self.DEVICE_ID)
                sleep(5)
                Adb.start_app(device_id=self.DEVICE_ID, app_id=app_id)
                sleep(5)
                Device.wait_until_app_is_running(device_id=self.DEVICE_ID, app_id=app_id, timeout=10)
                start_time = int(Device.get_start_time(self.DEVICE_ID, app_id=app_id))
                second_start_expected = second_start_expected + start_time

            start_time_expected = start_time_expected / timesToRun
            second_start_expected = second_start_expected / timesToRun
        else:
            start_time_expected = first_start
            second_start_expected = second_start
            Adb.reboot_device(self.DEVICE_ID)
            sleep(65)
            Adb.kill_server()
            Adb.start_server()
            Adb.usb()

        start_time_actual = 0
        second_start_actual = 0
        for x in range(0, timesToRun):
            sleep(30)
            print "Test run number {0} for actual time.".format(x + 1)

            Adb.clear_logcat(device_id=self.DEVICE_ID)
            Adb.stop_application(device_id=self.DEVICE_ID, app_id=app_id)
            Adb.uninstall(app_id=app_id, device_id=self.DEVICE_ID, assert_success=False)
            assert not Adb.is_application_running(device_id=self.DEVICE_ID, app_id=app_id)

            Adb.install(apk_file_path=apk, device_id=self.DEVICE_ID)
            Device.turn_on_screen(device_id=self.DEVICE_ID)
            sleep(5)

            # Verify first start
            Adb.clear_logcat(device_id=self.DEVICE_ID)
            Adb.start_app(device_id=self.DEVICE_ID, app_id=app_id)
            sleep(5)
            Device.wait_until_app_is_running(device_id=self.DEVICE_ID, app_id=app_id, timeout=10)
            start_time = int(Device.get_start_time(self.DEVICE_ID, app_id=app_id))
            start_time_actual = start_time_actual + start_time

            # Verify second start
            Device.turn_on_screen(device_id=self.DEVICE_ID)
            Adb.stop_application(device_id=self.DEVICE_ID, app_id=app_id)
            assert not Adb.is_application_running(device_id=self.DEVICE_ID, app_id=app_id)
            sleep(5)
            Device.turn_on_screen(device_id=self.DEVICE_ID)
            Adb.clear_logcat(device_id=self.DEVICE_ID)
            sleep(5)
            Adb.start_app(device_id=self.DEVICE_ID, app_id=app_id)
            sleep(5)
            Device.wait_until_app_is_running(device_id=self.DEVICE_ID, app_id=app_id, timeout=10)
            start_time = int(Device.get_start_time(self.DEVICE_ID, app_id=app_id))
            second_start_actual = second_start_actual + start_time

        start_time_actual = start_time_actual / timesToRun
        second_start_actual = second_start_actual / timesToRun

        if old_way_of_testing_performance is False:
            with open('perfResults.csv', 'a+') as csvfile:
                fieldnames = ['app_name', 'configuration', 'device_name', 'expected_first_start', 'actual_first_start',
                              'expected_second_start', 'actual_second_start']

                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'app_name': demo.split('/')[-1], 'configuration': config, 'device_name' : device_name,
                                 'expected_first_start': str(start_time_expected),
                                 'actual_first_start':str(start_time_actual),
                                 'expected_second_start':str(second_start_expected),
                                 'actual_second_start':str(second_start_actual)})

        message = "{0} with {4} configuration first start on {1} is {2} ms. The expected first start is {3} ms".format(
            demo,
            device_name,
            start_time_actual,
            start_time_expected,
            config)

        verification_errors = PerfTests.assert_time(expected=start_time_expected, actual=start_time_actual,
                                                    tolerance=10,
                                                    error_message=message, verification_errors=verification_errors)

        message = "{0} with {4} configuration second start on {1} is {2} ms.The expected second start is {3} ms".format(
            demo,
            device_name,
            second_start_actual,
            second_start_expected,
            config)

        verification_errors = PerfTests.assert_time(expected=second_start_expected, actual=second_start_actual,
                                                    tolerance=10,
                                                    error_message=message, verification_errors=verification_errors)

        self.assertEqual([], verification_errors)
