"""
Verify pages templates looks ok
"""

import fileinput
import sys
import unittest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.command import *
from core.osutils.folder import Folder
from core.settings.settings import SIMULATOR_NAME, TEST_RUN_HOME
from core.tns.tns import Tns


class PageTemplatesTests(BaseClass):
    folder = os.path.join(TEST_RUN_HOME, 'tests', 'pageTemplates')
    log = ""

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
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
        self.log = Tns.run_ios(attributes={'--path': 'blank-js', '--emulator': ''}, wait=False, assert_success=False)
        strings = ['Successfully synced', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Add page to application
        print(os.path)
        cmd = 'node {addPageScript} {pageName} {page_type} js blank-js'.format(
            addPageScript=os.path.join(self.folder, 'addPageNext.js'), pageName=page_type, page_type=page_type)
        run(cmd)
        strings = ['Successfully synced application', 'Successfully transferred', page_type, self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Set new page for home app page
        text_to_search = 'application.start({ moduleName:'
        text_to_replace = "application.start({ moduleName: " + "\"{name}/{name}-page\"".format(name=page_type) + " });\n"
        for line in fileinput.input("blank-js/app/app.js", inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        strings = ['Successfully synced application', 'Successfully transferred', 'app.js', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Verify iOS looks ok
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID, expected_image=expected_image,
                            tolerance=3.0)

    @unittest.skipIf(CURRENT_OS == OSType.OSX, "Temporary ignore on Linux.")
    # @parameterized.expand([
    #    ('blank-app-ts', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'login', 'loginPageScreen'),
    #    ('blank', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'blank', 'blankPageScreen'),
    #    ('blank', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'signup', 'signupPageScreen'),
    # ])
    def test_typescript(self, app_name, flavor, url, page_type, expected_image):
        if app_name == 'blank-app-ts':
            # Initial run of the app
            Tns.create_app(app_name=app_name, attributes={"--template": url}, assert_success=True)
            Tns.run_ios(attributes={'--path': self.app_name, "--emulator": ""}, wait=False, assert_success=False)

        # Add pages to application
        cmd = 'node {addPageScript} {pageName} {page_type} {flavor} {pathToApp}'.format(
            addPageScript=os.path.join(self.folder, 'addPage.js'), pageName=page_type, page_type=page_type,
            flavor=flavor, pathToApp=os.path.join(app_name))
        run(cmd)

        # Set new page for home app page
        text_to_search = 'app.start({ moduleName:'
        text_to_replace = "app.start({ moduleName: " + "\"{name}/{name}-page\"".format(name=page_type) + "});"

        for line in fileinput.input("blank-app-ts/app/app.ts", inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        # Verify iOS looks ok
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID, expected_image=expected_image,
                            tolerance=3.0)

    @unittest.skipIf(CURRENT_OS == OSType.OSX, "Temporary ignore on Linux.")
    # @parameterized.expand([
    ##    ('blank-app-ng', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'login', 'loginPageScreen'),
    #    ('blank', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'blank', 'blankPageScreen'),
    #    ('blank', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'signup', 'signupPageScreen'),
    # ])
    def test_angular(self, app_name, flavor, url, page_type, expected_image):
        if app_name == 'blank-app-ng':
            Tns.create_app(app_name=app_name, attributes={"--template": url}, assert_success=True)
            Tns.run_ios(attributes={'--path': self.app_name, "--emulator": ""}, wait=False, assert_success=False)

        # Add pages to application
        cmd = 'node {addPageScript} {pageName} {page_type} {flavor} {pathToApp}'.format(
            addPageScript=os.path.join(self.folder, 'addPage.js'), pageName=page_type, page_type=page_type,
            flavor=flavor, pathToApp=os.path.join(app_name))
        run(cmd)

        # Set new page for home app page
        text_to_search = '{ path: "", redirectTo: '
        text_to_replace = "{ path: \"\", redirectTo: \"" + "/{name}\"".format(name=page_type) + \
                          ", pathMatch: \"full\" },"
        for line in fileinput.input("blank-app-ng/app/app-routing.module.ts", inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        text_to_search = "loadChildren:"
        text_to_replace = "{" + "path: \"{name}\",".format(
            name=page_type) + " loadChildren: \"./{name}/{name}.module#{name}Module\"".format(name=page_type) + "}"
        for line in fileinput.input("blank-app-ng/app/app-routing.module.ts", inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        # Verify iOS looks ok
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID, expected_image=expected_image,
                            tolerance=3.0)
