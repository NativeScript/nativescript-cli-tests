"""
Verify pages templates looks ok
"""

import os

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.osutils.command import *
from core.settings.settings import ANDROID_RUNTIME_PATH, EMULATOR_ID, EMULATOR_NAME, IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.tns import Tns
import fileinput

class PageTemplatesTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Simulator.stop()
        Emulator.ensure_available()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()

    @parameterized.expand([
        ('blank-app-js', 'js', 'https://github.com/nativescript/templte-blank', 'Login', 'loginPageScreen'),
        ('', 'js', 'https://github.com/nativescript/templte-blank', 'Blank', 'blankPageScreen'),
        ('', 'js', 'https://github.com/nativescript/templte-blank', 'Signup', 'signupPageScreen'),
    ])
    def testJavaScript(self, appName, flavor, url, pageType, expectedImage):
        if appName == 'blank-app-js':
            #Initial run of the application
            Tns.run_ios(attributes={"--template": url}, assert_success=True, tns_path=appName)

        # Add page to application
        cmd = 'node addPage.js {pageName} {pageType} {flavor} {pathToApp}'.format(
            pageName=pageType, pageType=pageType, flavor=flavor, pathToApp=os.path.join(appName))
        run(cmd)

        # Set new page for home app page
        textToSearch = '''application.start({ moduleName:'''
        textToReplace = '''application.start({ moduleName: "{name}/{name}-page" });'''.format(name=pageType)
        tempFile = open("app.js", 'r+')
        for line in fileinput.input("app.js"):
            tempFile.write(line.replace(textToSearch, textToReplace))
        tempFile.close()

        # Verify iOS looks ok
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=expectedImage, tolerance=3.0)

    @parameterized.expand([
        ('blank-app-ts', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'Login', 'loginPageScreen'),
        ('', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'Blank', 'blankPageScreen'),
        ('', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'Signup', 'signupPageScreen'),
    ])
    def testTypeScript(self, appName, flavor, url, pageType, expectedImage):
        if appName == 'blank-app-ts':
            # Initial run of the app
            Tns.run_ios(attributes={"--template": url}, assert_success=True, tns_path=appName)

        # Add pages to application
        cmd = 'node addPage.js {pageName} {pageType} {flavor} {pathToApp}'.format(
            pageName=pageType, pageType=pageType, flavor=flavor, pathToApp=os.path.join(self.app_name))
        run(cmd)

        # Set new page for home app page
        textToSearch = '''app.start({ moduleName:'''
        textToReplace = '''app.start({ moduleName: '{name}/{name}-page' });'''.format(name=pageType)
        tempFile = open("app.ts", 'r+')
        for line in fileinput.input("app.ts"):
            tempFile.write(line.replace(textToSearch, textToReplace))
        tempFile.close()

        # Verify iOS looks ok
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=expectedImage, tolerance=3.0)

    @parameterized.expand([
        ('blank-app-ng', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'Login', 'loginPageScreen'),
        ('', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'Blank', 'blankPageScreen'),
        ('', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'Signup', 'signupPageScreen'),
    ])
    def testAngular(self, appName, flavor, url, pageType, expectedImage):
        # Create application
        Tns.run_ios(attributes={"--template": url}, assert_success=True, tns_path=appName)

        # Add pages to application
        cmd = 'node addPage.js {pageName} {pageType} {flavor} {pathToApp}'.format(
            pageName=pageType, pageType=pageType, flavor=flavor, pathToApp=os.path.join(self.app_name))
        run(cmd)

        # Set new page for home app page
        textToSearch = '''{ path: "", redirectTo: '''
        textToReplace = '''{ path: "", redirectTo: "/{name}", pathMatch: "full" },'''.format(name=pageType)
        tempFile = open("app-routing.module.ts", 'r+')
        for line in fileinput.input("app-routing.module.ts"):
            tempFile.write(line.replace(textToSearch, textToReplace))

        textToSearch = '''loadChildren:'''
        textToReplace = '''{ path: "{name}", loadChildren: "./{name}/{name}.module#{name}Module" }'''.format(name=pageType)
        for line in fileinput.input("app-routing.module.ts"):
            tempFile.write(line.replace(textToSearch, textToReplace))

        tempFile.close()

        # Verify iOS looks ok
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=expectedImage, tolerance=3.0)