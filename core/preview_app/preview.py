"""
Helper for working with Preview App
"""
import os

import shutil

import re

import urllib

from core.device.helpers.adb import Adb

from core.device.simulator import Simulator

from core.tns.tns_platform_type import Platform

from core.osutils.file import File

from core.osutils.command_log_level import CommandLogLevel

from core.osutils.command import run

from core.settings.settings import  SUT_FOLDER, PREVIEW_APP_PATH_ANDROID, PREVIEW_APP_PATH_IOS, EMULATOR_ID

class Preview(object):

    @staticmethod
    def get_app_packages():
        """Copy Preview App packages from Shares to local folder"""
        shutil.copy2(PREVIEW_APP_PATH_ANDROID.strip(), SUT_FOLDER)        
        shutil.copy2(PREVIEW_APP_PATH_IOS.strip(), SUT_FOLDER)
        """Unpack the .tgz file to get the nsplaydev.app"""
        File.unpack_tar(PREVIEW_APP_PATH_IOS, SUT_FOLDER)

    @staticmethod
    def install_preview_app(device_id, platform=Platform.BOTH):
        """Installs Preview App on emulator and simulator"""
        package_android = File.find(base_path = SUT_FOLDER, file_name="app-universal-release.apk")
        package_ios = os.path.join(SUT_FOLDER, 'nsplaydev.app')
        if platform is Platform.IOS:
            Simulator.install(package_ios)
        elif platform is Platform.ANDROID: 
            Adb.install(package_android, device_id)
        elif platform is Platform.BOTH: 
            Adb.install(package_android, device_id)
            Simulator.install(package_ios)

    @staticmethod
    def install_playground_app(device_id, platform=Platform.BOTH):
        """Installs Playground App on emulator and simulator"""
        package_android = os.path.join(SUT_FOLDER, "app-release.apk")
        package_ios = os.path.join(SUT_FOLDER, 'nsplay.app')
        if platform is Platform.IOS:
            Simulator.install(package_ios)
        elif platform is Platform.ANDROID: 
            Adb.install(package_android, device_id)
        elif platform is Platform.BOTH: 
            Adb.install(package_android, device_id)
            Simulator.install(package_ios)
    
    @staticmethod
    def get_url(output):
        """Get preview URL form tns log.This is the url you need to load in Preview app
           in order to see and sync your project"""
        url = re.findall("(nsplay[^\s']+)", output)[0]
        url = urllib.unquote(url)
        url=url.replace('?', '\?')
        url=url.replace('&', '\&')
        return url 

    @staticmethod
    def run_app(url, emulator_id, platform):
        """Runs your project in the Preview App on simulator or emulator"""
        if platform is Platform.IOS:
            cmd = "xcrun simctl openurl {0} {1}.".format(emulator_id, url)
            output = run(command=cmd, log_level=CommandLogLevel.COMMAND_ONLY)
        elif platform is Platform.ANDROID:
            cmd = 'adb -s {0} shell am start -a android.intent.action.VIEW -d "{1}" org.nativescript.preview'.format(emulator_id, url)
            output = run(command=cmd, log_level=CommandLogLevel.COMMAND_ONLY)

    @staticmethod
    def dismiss_simulator_alert():
        """When preview url is loaded in simulator there is alert for confirmation.
           This method will dismiss it. It is implemented only for one instance of simulator for the moment"""
        dismiss_sim_alert = os.path.join(TEST_RUN_HOME, 'core', 'device', 'helpers', 'send_enter_to_simulator.scpt')
        command = "osascript " + dismiss_sim_alert
        run(command, log_level=CommandLogLevel.FULL)