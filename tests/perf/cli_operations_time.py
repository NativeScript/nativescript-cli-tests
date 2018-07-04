import csv
import os
from time import sleep

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.git.git import Git
from core.npm.npm import Npm
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE, TYPESCRIPT_PACKAGE, WEBPACK_PACKAGE, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS_PASS, ANDROID_KEYSTORE_ALIAS, TEST_RUN_HOME, PROVISIONING, IOS_PACKAGE
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_verifications import TnsAsserts
import re


def read_data(platform, app_name=None):
    csv_file_path = os.path.join(TEST_RUN_HOME, 'tests', 'perf', 'cli_operations_time_values.csv')
    csv_list = tuple(csv.reader(open(csv_file_path, 'rb'), delimiter=','))
    if app_name is None:
        return [tuple(l) for l in csv_list if l[2].startswith(platform)]
    else:
        return [tuple(l) for l in csv_list if (l[2].startswith(platform) and l[0] == app_name)]


class PerfBuildTests(BaseClass):
    platform = os.getenv('PLATFORM', None)
    APP_NAME = os.getenv('APP_NAME', None)
    DATA = read_data(platform, APP_NAME)

    @staticmethod
    def get_time(log):
        m = re.search('\d+\.\d+ real', log)
        time = m.group(0).split(".")[0]
        return float(time)

    @staticmethod
    def assert_time(expected, actual, tolerance=20, error_message="Startup time is not expected.",
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

    @staticmethod
    def report_add_column_titles():

        with open('perfResults.csv', 'a+') as csvfile:
            fieldnames = ['app_name', 'configuration', 'platform', 'action', 'expected_first_start',
                          'actual_first_start',
                          'expected_second_start', 'actual_second_start']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

    @staticmethod
    def report_add_data(demo, config, platform, expected_tns_create_time, actual_tns_create_time,
                        expected_tns_platform_add_time,
                        actual_tns_platform_add_time, expected_tns_build_time, actual_tns_build_time):
        with open('perfResults.csv', 'a+') as csvfile:
            fieldnames = ['app_name', 'configuration', 'platform', 'expected_tns_create_time',
                          'actual_tns_create_time',
                          'expected_tns_platform_add_time', 'actual_tns_platform_add_time',
                          'expected_tns_build_time', 'actual_tns_build_time']

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({'app_name': demo.split('/')[-1], 'configuration': config, 'platform': platform,
                             'expected_tns_create_time': str(expected_tns_create_time),
                             'actual_tns_create_time': str(actual_tns_create_time),
                             'expected_tns_platform_add_time': str(expected_tns_platform_add_time),
                             'actual_tns_platform_add_time': str(actual_tns_platform_add_time),
                             'expected_tns_build_time': str(expected_tns_build_time),
                             'actual_tns_build_time': str(actual_tns_build_time)
                             })

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Npm.cache_clean()
        Emulator.stop()
        Simulator.stop()
        PerfBuildTests.report_add_column_titles()

    def setUp(self):
        Tns.kill()
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @parameterized.expand(DATA)
    def test_tns_commands_time(self, demo, config, platform, expected_tns_create_time,
                               expected_tns_platform_add_time, expected_tns_build_time):

        perf_loop = int(os.getenv('RUN_TIMES', '3'))
        tns_create_log = ''
        tns_platform_add_log = ''
        tns_build_log = ''
        actual_tns_create_time = 0.0
        actual_tns_platform_add_time = 0.0
        actual_tns_build_time = 0.0
        for x in range(0, perf_loop):
            print "Number of run " + str((x + 1))
            if x > 0:
                sleep(60)
            if "ios" in platform:
                attributes = {"--path": self.app_name,
                              "--provision": PROVISIONING,
                              "--release": ""}
            else:
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
                Npm.cache_clean()
                sleep(10)
                tns_create_log = Tns.create_app(self.app_name, attributes={"--template": "https://github.com/" + demo},
                                                measureTime=True)
                Npm.cache_clean()
                sleep(20)
                if "android" in platform:
                    tns_platform_add_log = Tns.platform_add_android(
                        attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE},
                        measureTime=True)
                else:
                    tns_platform_add_log = Tns.platform_add_ios(
                        attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE},
                        measureTime=True)
                sleep(10)
                if "-ng" in demo:
                    Tns.update_angular(self.app_name)
                if "-ng" in demo or "-ts" in demo:
                    Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev', folder=self.app_name)
                    Npm.install(package=TYPESCRIPT_PACKAGE, option='--save-dev', folder=self.app_name)
                if "vue" not in demo:
                    Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=self.app_name)
                sleep(10)
            else:
                Npm.cache_clean()
                sleep(10)
                Folder.cleanup(self.app_name)
                Git.clone_repo(repo_url="https://github.com/" + demo, local_folder=self.app_name)
                if "android" in platform:
                    Tns.platform_remove(platform=Platform.ANDROID, attributes={"--path": self.app_name},
                                        assert_success=False)
                    sleep(5)
                    Npm.cache_clean()
                    sleep(10)
                    tns_platform_add_log = Tns.platform_add_android(
                        attributes={"--path": self.app_name, "--frameworkPath": ANDROID_PACKAGE},
                        measureTime=True)
                    sleep(20)
                else:
                    Tns.platform_remove(platform=Platform.IOS, attributes={"--path": self.app_name},
                                        assert_success=False)
                    sleep(5)
                    Npm.cache_clean()
                    sleep(10)
                    tns_platform_add_log = Tns.platform_add_ios(
                        attributes={"--path": self.app_name, "--frameworkPath": IOS_PACKAGE},
                        measureTime=True)
                    sleep(20)
                Tns.update_modules(self.app_name)
                Npm.uninstall(package="nativescript-dev-webpack", option='--save-dev', folder=self.app_name)
                Tns.install_npm(package=WEBPACK_PACKAGE, option='--save-dev', folder=self.app_name)

                json = str(TnsAsserts.get_package_json(self.app_name))
                if "angular" in json:
                    Tns.update_angular(self.app_name)
                if "typescript" in json:
                    Npm.uninstall(package="nativescript-dev-typescript", option='--save-dev', folder=self.app_name)
                    Npm.install(package=TYPESCRIPT_PACKAGE, option='--save-dev', folder=self.app_name)
                sleep(10)
            if "timeline" in config:
                package_json = os.path.join(self.app_name, 'app', 'package.json')
                File.replace(package_json, "\"main\": \"main.js\"", "\"main\": \"main.js\",\"profiling\": \"timeline\"")

            if "android" in platform:
                tns_build_log = Tns.build_android(attributes=attributes, measureTime=True)
            else:
                tns_build_log = Tns.build_ios(attributes=attributes, measureTime=True)
            if tns_create_log:
                actual_tns_create_time += PerfBuildTests.get_time(tns_create_log)
            actual_tns_platform_add_time += PerfBuildTests.get_time(tns_platform_add_log)
            actual_tns_build_time += PerfBuildTests.get_time(tns_build_log)
            run('rm -rf {0}'.format(self.app_name))

        if actual_tns_create_time != 0.0:
            actual_tns_create_time = actual_tns_create_time / perf_loop
        actual_tns_platform_add_time = actual_tns_platform_add_time / perf_loop
        actual_tns_build_time = actual_tns_build_time / perf_loop
        verification_errors = []
        PerfBuildTests.report_add_data(demo, config, platform, expected_tns_create_time, actual_tns_create_time,
                                       expected_tns_platform_add_time,
                                       actual_tns_platform_add_time, expected_tns_build_time, actual_tns_build_time)
        if actual_tns_create_time != 0.0:
            message = "Tns create project command for platform {1} for {0} with {4} configuration is {3} s. " \
                  "The expected time is {2} s.".format(demo,
                                                       platform, expected_tns_create_time,
                                                       actual_tns_create_time, config)
        if actual_tns_create_time != 0.0:
            verification_errors = PerfBuildTests.assert_time(expected=expected_tns_create_time,
                                                         actual=actual_tns_create_time,
                                                         tolerance=20,
                                                         error_message=message, verification_errors=verification_errors)

        message = "Tns platform add command for platform {1} for {0} with {4} configuration is {3} s. " \
                  "The expected time is {2} s.".format(demo, platform, expected_tns_platform_add_time,
                                                       actual_tns_platform_add_time, config)

        verification_errors = PerfBuildTests.assert_time(expected=expected_tns_platform_add_time,
                                                         actual=actual_tns_platform_add_time,
                                                         tolerance=20,
                                                         error_message=message, verification_errors=verification_errors)
        message = "Tns build command for platform {1} for {0} with {4} configuration is {3} s. " \
                  "The expected time is {2} s.".format(demo, platform, expected_tns_build_time,
                                                       actual_tns_build_time, config)

        verification_errors = PerfBuildTests.assert_time(expected=expected_tns_build_time, actual=actual_tns_build_time,
                                                         tolerance=20,
                                                         error_message=message, verification_errors=verification_errors)

        self.assertEqual([], verification_errors)
