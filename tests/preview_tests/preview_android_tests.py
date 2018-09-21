import os

from core.base_class.BaseClass import BaseClass

from core.preview_app.preview import Preview

from core.device.emulator import Emulator

from core.tns.tns import Tns

from core.device.device import Device

from core.osutils.file import File

from core.tns.tns_platform_type import Platform

from core.tns.replace_helper import ReplaceHelper

from core.settings.settings import TEST_RUN_HOME, EMULATOR_ID, EMULATOR_NAME

class PreviewCommandTestsAndroid(BaseClass):

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.kill()
        Emulator.stop()
        Emulator.ensure_available()
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID)

        Preview.get_app_packages()
        Preview.install_preview_app(EMULATOR_ID, platform=Platform.ANDROID)

        Tns.create_app(BaseClass.app_name,
                           attributes={'--template': os.path.join('data', 'apps', 'livesync-hello-world.tgz')},
                           update_modules=True)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    def test_001_tns_preview_android_js_css_xml(self):
        """Make valid changes in JS,CSS and XML"""

        # `tns preview` and take the app url and open it in Preview App
        output = Tns.preview(attributes={'--path': self.app_name}, wait=False,
                        log_trace=True,assert_success=False)
        log = File.read(output)
        url = Preview.get_url(log)
        Preview.run_app(url, EMULATOR_ID, platform=Platform.ANDROID)
                              
        strings = ['Start syncing changes for platform android',
                   'Project successfully prepared (android)',
                   'Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=output, string_list=strings, timeout=180, check_interval=10)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')

        # Change JS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        # NB! Update strings list when showin which file is synced is implemented
        #strings = ['Successfully transferred main-view-model.js', 'Successfully synced changes for platform android']
        strings = ['Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=20)
        assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        # Change XML and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        # NB! Update strings list when showin which file is synced is implemented
        #strings = ['Successfully transferred main-page.xml', 'Successfully synced changes for platform android']
        strings = ['Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)
        text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
        assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Change CSS and wait until app is synced
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        # NB! Update strings list when showin which file is synced is implemented
        #strings = ['Successfully transferred app.css', 'Successfully synced changes for platform android']
        strings = ['Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify application looks correct
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_js_css_xml')

        # Rollback all the changes
        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_JS, sleep=10)
        # NB! Update strings list when showin which file is synced is implemented
        #strings = ['Successfully transferred main-view-model.js', 'Successfully synced changes for platform android']
        strings = ['Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_CSS, sleep=3)
        # NB! Update strings list when showin which file is synced is implemented
        #strings = ['Successfully transferred app.css', 'Successfully synced changes for platform android']
        strings = ['Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        ReplaceHelper.rollback(self.app_name, ReplaceHelper.CHANGE_XML, sleep=3)
        # NB! Update strings list when showin which file is synced is implemented
        #strings = ['Successfully transferred main-page.xml', 'Successfully synced changes for platform android']
        strings = ['Successfully synced changes for platform android']
        Tns.wait_for_log(log_file=log, string_list=strings)

        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='livesync-hello-world_home')
