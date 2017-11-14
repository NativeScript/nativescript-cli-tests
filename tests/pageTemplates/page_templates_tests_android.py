"""
Verify pages templates looks ok
"""

import fileinput
import sys
import unittest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.npm.npm import Npm
from core.osutils.command import *
from core.osutils.folder import Folder
from core.settings.settings import EMULATOR_ID, EMULATOR_NAME, TEST_RUN_HOME
from core.tns.tns import Tns


class PageTemplatesTestsAndroid(BaseClass):
    folder = os.path.join(TEST_RUN_HOME, 'tests', 'pageTemplates')
    log = ""

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Emulator.ensure_available()
        Folder.cleanup(cls.app_name)
        Folder.cleanup("extensions")
        File.remove("user-settings.json")
        output = Tns.run_tns_command(
            command='extension install nativescript-starter-kits --profileDir ' + TEST_RUN_HOME)
        assert "Successfully installed extension nativescript-starter-kits" in output
        assert "Successfully loaded extension nativescript-starter-kits" in output
        Tns.run_tns_command(command='usage-reporting disable --profileDir ' + TEST_RUN_HOME)
        Tns.run_tns_command(command='error-reporting disable --profileDir ' + TEST_RUN_HOME)
        Npm.install(package='global-modules-path', option='--save', folder=cls.folder)

        base_url = "https://github.com/nativescript/"
        Tns.create_app(app_name="blank-js", attributes={"--template": base_url + "template-blank"})
        Tns.create_app(app_name="blank-ts", attributes={"--template": base_url + "template-blank-ts"})
        Tns.create_app(app_name="blank-ng", attributes={"--template": base_url + "template-blank-ng"})

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @parameterized.expand([
        ('login', 'loginPageScreen'),
        ('blank', 'blankPageScreen'),
        ('signup', 'signupPageScreen')
    ])
    def test_javascript(self, page_type, expected_image):
        self.log = Tns.run_android(attributes={'--path': 'blank-js', '--emulator': ''}, wait=False,
                                   assert_success=False)
        strings = ['Successfully synced', EMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Add page to application
        print(os.path)
        cmd = 'node {addPageScript} {pageName} {page_type} js blank-js'.format(
            addPageScript=os.path.join(self.folder, 'addPageNext.js'), pageName=page_type, page_type=page_type)
        run(cmd)
        strings = ['Successfully synced application', 'Successfully transferred', page_type, EMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Set new page for home app page
        text_to_search = 'application.start({ moduleName:'
        text_to_replace = "application.start({ moduleName: " + "\"{name}/{name}-page\"".format(name=page_type) + \
                          " });\n"
        for line in fileinput.input("blank-js/app/app.js", inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        strings = ['Successfully synced application', 'Successfully transferred', 'app.js', EMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Verify android looks ok
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=expected_image,
                            tolerance=3.0)

    @parameterized.expand([
        ('login', 'loginPageScreen'),
        ('blank', 'blankPageScreen'),
        ('signup', 'signupPageScreen')
    ])
    def test_typescript(self, page_type, expected_image):
        self.log = Tns.run_android(attributes={'--path': 'blank-ts', '--emulator': ''}, wait=False,
                                   assert_success=False)
        strings = ['Successfully synced', EMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Add page to application
        print(os.path)
        cmd = 'node {addPageScript} {pageName} {page_type} ts blank-ts'.format(
            addPageScript=os.path.join(self.folder, 'addPageNext.js'), pageName=page_type, page_type=page_type)
        run(cmd)
        strings = ['Successfully synced application', 'Successfully transferred', page_type, EMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Set new page for home app page
        text_to_search = 'app.start({ moduleName:'
        text_to_replace = "app.start({ moduleName: " + "\"{name}/{name}-page\"".format(name=page_type) + "});\n"

        for line in fileinput.input("blank-ts/app/app.ts", inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        # Verify android looks ok
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=expected_image,
                            tolerance=3.0)

    @parameterized.expand([
        ('login', 'loginPageScreen'),
        ('blank', 'blankPageScreen'),
        ('signup', 'signupPageScreen'),
    ])
    def test_angular(self, page_type, expected_image):
        self.log = Tns.run_android(attributes={'--path': 'blank-ng', '--emulator': ''}, wait=False,
                                   assert_success=False)
        strings = ['Successfully synced', EMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Add page to application
        print(os.path)
        cmd = 'node {addPageScript} {pageName} {page_type} ng blank-ng'.format(
            addPageScript=os.path.join(self.folder, 'addPageNext.js'), pageName=page_type, page_type=page_type)
        run(cmd)
        strings = ['Successfully synced application', 'Successfully transferred', page_type, EMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Set new page for home app page
        text_to_search = '{ path: "", redirectTo: '
        text_to_replace = "{ path: \"\", redirectTo: \"" + "/{name}\"".format(name=page_type) + \
                          ", pathMatch: \"full\" },\n"
        for line in fileinput.input("blank-ng/app/app-routing.module.ts", inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        text_to_search = "loadChildren:"
        text_to_replace = "{" + "path: \"{name}\",".format(
            name=page_type) + " loadChildren: \"./{name}/{name}.module#{name}Module\"".format(name=page_type) + "}\n"
        for line in fileinput.input("blank-ng/app/app-routing.module.ts", inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        # Verify android looks ok
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=expected_image,
                            tolerance=3.0)
