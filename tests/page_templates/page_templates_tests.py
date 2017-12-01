"""
Verify pages templates looks ok
"""

import fileinput
import sys

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.npm.npm import Npm
from core.osutils.command import *
from core.osutils.folder import Folder
from core.settings.settings import SIMULATOR_NAME, TEST_RUN_HOME, IOS_RUNTIME_PATH, EMULATOR_NAME, EMULATOR_ID, \
    ANDROID_RUNTIME_PATH
from core.tns.tns import Tns


class PageTemplatesTests(BaseClass):
    folder = os.path.join(TEST_RUN_HOME, 'tests', 'page_templates')
    log = ""

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()
        Simulator.stop()
        cls.SIMULATOR_ID = Simulator.ensure_available(simulator_name=SIMULATOR_NAME)
        Folder.cleanup("extensions")
        File.remove("user-settings.json")
        output = Tns.run_tns_command(
            command='extension install nativescript-starter-kits@next --profileDir ' + TEST_RUN_HOME)
        assert "Successfully installed extension nativescript-starter-kits" in output
        assert "Successfully loaded extension nativescript-starter-kits" in output
        Tns.run_tns_command(command='usage-reporting disable --profileDir ' + TEST_RUN_HOME)
        Tns.run_tns_command(command='error-reporting disable --profileDir ' + TEST_RUN_HOME)
        Npm.install(package='global-modules-path', option='--save', folder=cls.folder)

        base_url = "https://github.com/nativescript/"
        Tns.create_app(app_name="blank-js", attributes={"--template": base_url + "template-blank"})
        Tns.create_app(app_name="blank-ts", attributes={"--template": base_url + "template-blank-ts"})
        Tns.create_app(app_name="blank-ng", attributes={"--template": base_url + "template-blank-ng"})
        Tns.platform_add_ios(attributes={"--path": "blank-js", "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.platform_add_ios(attributes={"--path": "blank-ts", "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.platform_add_ios(attributes={"--path": "blank-ng", "--frameworkPath": IOS_RUNTIME_PATH})
        Tns.platform_add_android(attributes={"--path": "blank-js", "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.platform_add_android(attributes={"--path": "blank-ts", "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.platform_add_android(attributes={"--path": "blank-ng", "--frameworkPath": ANDROID_RUNTIME_PATH})

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        Tns.kill()
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup("blank-js")
        Folder.cleanup("blank-ts")
        Folder.cleanup("blank-ng")
        BaseClass.tearDownClass()

    @parameterized.expand([
        ('js', 'login', 'loginPageScreen'),
        ('js', 'blank', 'blankPageScreen'),
        ('js', 'signup', 'signupPageScreen'),
        ('ts', 'login', 'loginPageScreen'),
        ('ts', 'blank', 'blankPageScreen'),
        ('ts', 'signup', 'signupPageScreen'),
        ('ng', 'login', 'loginPageScreen'),
        ('ng', 'blank', 'blankPageScreen'),
        ('ng', 'signup', 'signupPageScreen')
    ])
    def test_page_templates(self, flavor, page_type, expected_image):

        # Initial run of the app
        self.log = Tns.run_ios(attributes={'--path': 'blank-' + flavor, '--emulator': ''}, wait=False,
                               assert_success=False)
        strings = ['Successfully synced', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)
        Tns.kill()

        # Add page to application
        print(os.path)
        cmd = 'node {addPageScript} {pageName} {page_type} {flavor} blank-{flavor}'.format(
            addPageScript=os.path.join(self.folder, 'add.js'), pageName=page_type, page_type=page_type,
            flavor=flavor)
        output = run(cmd)
        assert "Flavor" in output
        assert "Error" not in output

        # Set new page for home app page
        if 'js' in flavor:
            file_to_replace = 'app.js'
            path = 'blank-js/app/' + file_to_replace
            text_to_search = 'application.start({ moduleName:'
            text_to_replace = "application.start({ moduleName: " + "\"{name}/{name}-page\"".format(name=page_type) + \
                              " });\n"
        if 'ts' in flavor:
            file_to_replace = 'app.ts'
            path = 'blank-ts/app/' + file_to_replace
            text_to_search = 'app.start({ moduleName:'
            text_to_replace = "app.start({ moduleName: " + "\"{name}/{name}-page\"".format(name=page_type) + "});\n"

        if 'ng' in flavor:
            file_to_replace = 'app-routing.module.ts'
            path = 'blank-ng/app/' + file_to_replace
            text_to_search = '{ path: "home", loadChildren:'
            text_to_replace = '{ path: "home", loadChildren: "./' + page_type + '/' + page_type + '.module#' + \
                              page_type.title() + 'Module" }\n'

        for line in fileinput.input(path, inplace=True):
            if line.strip().startswith(text_to_search):
                line = text_to_replace
            sys.stdout.write(line)

        # Sync again
        self.log = Tns.run_ios(attributes={'--path': 'blank-' + flavor, '--emulator': ''}, wait=False,
                               assert_success=False)
        strings = ['Successfully synced application', 'Successfully transferred', self.SIMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)

        # Verify iOS looks ok
        image = '{expected_image}-ios-{flavor}'.format(expected_image=expected_image, flavor=flavor)
        Device.screen_match(device_name=SIMULATOR_NAME, device_id=self.SIMULATOR_ID, expected_image=image)

        # Verify Android looks ok
        self.log = Tns.run_android(attributes={'--path': 'blank-' + flavor, '--emulator': ''}, wait=False,
                                   assert_success=False)
        strings = ['Successfully synced', EMULATOR_ID]
        Tns.wait_for_log(log_file=self.log, string_list=strings, timeout=150, check_interval=10)
        image = '{expected_image}-android-{flavor}'.format(expected_image=expected_image, flavor=flavor)
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID, expected_image=image)
