"""
Verify pages templates looks ok
"""

import os

from parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.osutils.command import *
from core.settings.settings import ANDROID_RUNTIME_PATH, EMULATOR_ID, EMULATOR_NAME, IOS_RUNTIME_PATH, SIMULATOR_NAME
from core.tns.tns import Tns
import fileinput
import sys

class PageTemplatesTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join('out', cls.__name__ + '.txt')
        BaseClass.setUpClass(logfile)
        Emulator.stop()
        Simulator.stop()
        # Emulator.ensure_available()
        # cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
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
        ('blank-app-js', 'js', 'https://github.com/nativescript/template-blank', 'login', 'loginPageScreen'),
        ('blank', 'js', 'https://github.com/nativescript/template-blank', 'Blank', 'blankPageScreen'),
        ('blank', 'js', 'https://github.com/nativescript/template-blank', 'Signup', 'signupPageScreen'),
    ])
    def testJavaScript(self, appName, flavor, url, pageType, expectedImage):
        if appName == 'blank-app-js':
            #Initial run of the application
            Tns.create_app(app_name=appName, attributes={"--template": url}, assert_success=True)
            os.chdir(os.path.join(appName))
            Tns.run_ios(attributes={"--emulator": ""}, wait=False, assert_success=False, tns_path="../node_modules/.bin/tns")


        # Add page to application
        os.chdir('..')
        print(os.path)
        cmd = 'node addPage.js {pageName} {pageType} {flavor} {pathToApp}'.format(
            pageName=pageType, pageType=pageType, flavor=flavor, pathToApp=os.path.join(appName))
        run(cmd)

        # Set new page for home app page
        textToSearch = 'application.start({ moduleName:'
        textToReplace = "application.start({ moduleName: " + "\"{name}/{name}-page\"".format(name=pageType) + " });"

        for line in fileinput.input("blank-app-js/app/app.js", inplace=True):
            if line.strip().startswith(textToSearch):
                line = textToReplace
            sys.stdout.write(line)


        # Verify iOS looks ok
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=SIMULATOR_NAME, expected_image=expectedImage, tolerance=3.0)

    @parameterized.expand([
        ('blank-app-ts', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'login', 'loginPageScreen'),
        ('blank', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'blank', 'blankPageScreen'),
        ('blank', 'ts', 'https://github.com/NativeScript/template-blank-ts', 'signup', 'signupPageScreen'),
    ])
    def testTypeScript(self, appName, flavor, url, pageType, expectedImage):
        if appName == 'blank-app-ts':
            # Initial run of the app
            Tns.create_app(app_name=appName, attributes={"--template": url}, assert_success=True)
            os.chdir(os.path.join(appName))
            Tns.run_ios(attributes={"--emulator": ""}, wait=False, assert_success=False,
                        tns_path="../node_modules/.bin/tns")

        # Add pages to application
        cmd = 'node addPage.js {pageName} {pageType} {flavor} {pathToApp}'.format(
            pageName=pageType, pageType=pageType, flavor=flavor, pathToApp=os.path.join(self.app_name))
        run(cmd)

        # Set new page for home app page
        textToSearch = 'app.start({ moduleName:'
        textToReplace = "app.start({ moduleName: " + "\"{name}/{name}-page\"".format(name=pageType) + "});"

        for line in fileinput.input("blank-app-ts/app/app.ts", inplace=True):
            if line.strip().startswith(textToSearch):
                line = textToReplace
            sys.stdout.write(line)

        # Verify iOS looks ok
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=SIMULATOR_NAME, expected_image=expectedImage, tolerance=3.0)

    @parameterized.expand([
        ('blank-app-ng', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'login', 'loginPageScreen'),
        ('blank', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'blank', 'blankPageScreen'),
        ('blank', 'ng', 'https://github.com/NativeScript/template-blank-ng', 'signup', 'signupPageScreen'),
    ])
    def testAngular(self, appName, flavor, url, pageType, expectedImage):
        if appName == 'blank-app-ts':
            Tns.create_app(app_name=appName, attributes={"--template": url}, assert_success=True)
            os.chdir(os.path.join(appName))
            Tns.run_ios(attributes={"--emulator": ""}, wait=False, assert_success=False,
                    tns_path="../node_modules/.bin/tns")

        # Add pages to application
        cmd = 'node addPage.js {pageName} {pageType} {flavor} {pathToApp}'.format(
            pageName=pageType, pageType=pageType, flavor=flavor, pathToApp=os.path.join(self.app_name))
        run(cmd)

        # Set new page for home app page
        textToSearch = '{ path: "", redirectTo: '
        textToReplace = "{ path: \"\", redirectTo: \"" + "/{name}\"".format(name=pageType) + ", pathMatch: \"full\" },"
        for line in fileinput.input("blank-app-ng/app/app-routing.module.ts", inplace=True):
            if line.strip().startswith(textToSearch):
                line = textToReplace
            sys.stdout.write(line)

        textToSearch = "loadChildren:"
        textToReplace = "{" + "path: \"{name}\",".format(name=pageType) + " loadChildren: \"./{name}/{name}.module#{name}Module\"".format(name=pageType) + "}"
        for line in fileinput.input("blank-app-ng/app/app-routing.module.ts", inplace=True):
            if line.strip().startswith(textToSearch):
                line = textToReplace
            sys.stdout.write(line)

        # Verify iOS looks ok
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=SIMULATOR_NAME, expected_image=expectedImage, tolerance=3.0)