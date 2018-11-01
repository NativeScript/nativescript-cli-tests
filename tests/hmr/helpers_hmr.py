import csv
import os
import time

from core.device.device import Device
from core.device.helpers.adb import Adb
from core.osutils.file import File
from core.osutils.os_type import OSType
from core.osutils.process import Process
from core.settings.settings import EMULATOR_ID, EMULATOR_NAME, SIMULATOR_NAME, TEST_RUN_HOME, CURRENT_OS
from core.tns.tns import Tns
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns_platform_type import Platform
from tests.webpack.helpers.helpers import Helpers


class HelpersHMR(object):
    no_wp_run = ['Successfully installed']
    no_wp_sync = ['Successfully synced application']
    wp = ['Webpack compilation complete']
    run_hmr = ['Webpack compilation complete', 'Successfully installed', 'HMR: Sync',
              'HMR: Hot Module Replacement Enabled. Waiting for signal.']
    run_hmr_with_platforms = ['Webpack compilation complete', 'HMR: Sync',
               'HMR: Hot Module Replacement Enabled. Waiting for signal.', 'Successfully synced application',
                              'Refreshing application on device']
    sync_hmr = ['Webpack compilation complete', 'Successfully synced application',
               'HMR: Checking for updates to the bundle.']
    errors_hmr = ['Module build failed', 'ENOENT']

    wp_run = ['Webpack compilation complete', 'Successfully installed']
    wp_sync = ['Webpack compilation complete', 'Successfully synced application']
    wp_sync_snapshot = ['Webpack compilation complete', 'Successfully synced app', 'Stripping the snapshot flag.']
    wp_errors = ['Module not found', 'Snapshot generation failed', 'ENOENT']

    SIMULATOR_ID = ""

    image_original = 'hello-world-js'
    image_change = 'hello-world-js-js-css-xml'

    xml_change = ['app/main-page.xml', 'TAP', 'TEST']
    js_change = ['app/main-view-model.js', 'taps', 'clicks']
    css_change = ['app/app.css', '18', '32']

    @staticmethod
    def apply_changes(app_name, log, platform):

        not_found_list = []
        # Change JS, XML and CSS
        ReplaceHelper.replace(app_name, HelpersHMR.js_change, sleep=10)
        strings = ['HMR: The following modules were updated:', './main-view-model.js', './main-page.js',
                   'Successfully transferred bundle.',
                   'HMR: Successfully applied update with hmr hash ']
        # strings = ['JS: HMR: The following modules were updated:', './main-view-model.js', './main-page.js',
        #            'Successfully transferred bundle.{0}.hot-update.js'.format(hash()),
        #            'JS: HMR: Successfully applied update with hmr hash {0}'.format(hashlib.sha1)]
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

        ReplaceHelper.replace(app_name, HelpersHMR.xml_change, sleep=10)
        strings = ['Refreshing application on device', 'HMR: Checking for updates to the bundle with hmr hash',
                   './main-page.xml', 'HMR: Successfully applied update with hmr hash']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        ReplaceHelper.replace(app_name, HelpersHMR.css_change, sleep=10)
        if platform == Platform.ANDROID:
            Tns.wait_for_log(log_file=log, string_list=['app.css'], clean_log=False)

        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.wp_sync, not_existing_string_list=HelpersHMR.wp_errors,
                         timeout=120)

        # Verify application looks correct
        if platform == Platform.ANDROID:
            Helpers.android_screen_match(image=HelpersHMR.image_change, timeout=120)
        if platform == Platform.IOS:
            Helpers.ios_screen_match(sim_id=HelpersHMR.SIMULATOR_ID, image=HelpersHMR.image_change,
                                     timeout=120)

    @staticmethod
    def apply_changes_js(app_name, log, platform):
        # Change JS
        ReplaceHelper.replace(app_name, HelpersHMR.js_change, sleep=10)
        strings = ['HMR: The following modules were updated:', './main-view-model.js', './main-page.js',
                   'Successfully transferred bundle.',
                   'HMR: Successfully applied update with hmr hash ']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 clicks left', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed).'

    @staticmethod
    def apply_changes_xml(app_name, log, platform):
        # Change XML after uninstall app from device
        ReplaceHelper.replace(app_name, HelpersHMR.xml_change, sleep=10)
        strings = ['Refreshing application on device',
                   'HMR: Sync...','JS: HMR: Hot Module Replacement Enabled. Waiting for signal.']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TEST')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

    @staticmethod
    def revert_changes_js(app_name, log, platform):
        # Change JS
        ReplaceHelper.rollback(app_name, HelpersHMR.js_change, sleep=10)
        strings = ['Refreshing application on device',
                   'HMR: Sync...','JS: HMR: Hot Module Replacement Enabled. Waiting for signal.']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 taps left', timeout=20)
            assert text_changed, 'Changes in JS file not applied (UI is not refreshed)'

    @staticmethod
    def revert_changes_xml(app_name, log, platform):
        # Change XML after uninstall app from device
        ReplaceHelper.rollback(app_name, HelpersHMR.xml_change, sleep=10)
        strings = ['HMR: Sync...', 'Refreshing application on device',
                   'HMR: Checking for updates to the bundle with hmr hash']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TAP')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

    @staticmethod
    def revert_changes(app_name, log, platform):
        # Clean old logs
        if CURRENT_OS is not OSType.WINDOWS:
            File.write(file_path=log, text="")

        # Revert XML changes
        ReplaceHelper.rollback(app_name, HelpersHMR.xml_change, sleep=10)
        strings = ['HMR: Sync...', 'Refreshing application on device', './main-page.xml',
                   'HMR: Checking for updates to the bundle with hmr hash']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='TAP')
            assert text_changed, 'Changes in XML file not applied (UI is not refreshed).'

        # Revert JS changes
        ReplaceHelper.rollback(app_name, HelpersHMR.js_change, sleep=10)
        strings = ['HMR: The following modules were updated:', './main-view-model.js', './main-page.js',
                   'Successfully transferred bundle.', 'HMR: Successfully applied update with hmr hash ']
        Tns.wait_for_log(log_file=log, string_list=strings)
        if platform == Platform.ANDROID:
            text_changed = Device.wait_for_text(device_id=EMULATOR_ID, text='42 taps left', timeout=20)
            assert text_changed, 'HMR: The following modules were updated:'

        # Revert CSS changes
        ReplaceHelper.rollback(app_name, HelpersHMR.css_change, sleep=10)
        Tns.wait_for_log(log_file=log, string_list=['app.css'], clean_log=False)

        # Verify application looks correct
        Tns.wait_for_log(log_file=log, string_list=HelpersHMR.wp_sync, not_existing_string_list=HelpersHMR.wp_errors,
                         timeout=60)
        if platform == Platform.ANDROID:
            Helpers.android_screen_match(image=HelpersHMR.image_original, timeout=120)
        if platform == Platform.IOS:
            Helpers.ios_screen_match(sim_id=HelpersHMR.SIMULATOR_ID, image=HelpersHMR.image_original,
                                     timeout=120)
