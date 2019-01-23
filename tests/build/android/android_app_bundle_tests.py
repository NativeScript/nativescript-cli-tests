import os

import urllib

import unittest

from core.settings.settings import SUT_FOLDER, EMULATOR_NAME, EMULATOR_ID, \
     ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_PATH,\
     ANDROID_KEYSTORE_ALIAS_PASS, CURRENT_OS, OSType, ANDROID_PACKAGE, TEST_RUN_HOME

from core.device.helpers.adb import Adb

from core.base_class.BaseClass import BaseClass

from core.osutils.file import File

from core.device.device import Device

from core.osutils.folder import Folder

from core.osutils.command import run

from core.osutils.command_log_level import CommandLogLevel

from core.device.emulator import Emulator, EMULATOR_ID, EMULATOR_NAME

from core.tns.tns import Tns
class AndroidAppBundleTests(BaseClass):
    
    bundletool_path = os.path.join(SUT_FOLDER,"bundletool.jar")
    path_to_apks = os.path.join(BaseClass.app_name,'app.apks')

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

        Tns.create_app(BaseClass.app_name)
        Tns.platform_add_android(attributes={"--path": BaseClass.app_name, "--frameworkPath": ANDROID_PACKAGE})
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name, TEST_RUN_HOME + "/data/TestApp")

        #Download bundletool
        url = 'https://github.com/google/bundletool/releases/download/0.8.0/bundletool-all-0.8.0.jar'
        urllib.urlretrieve(url, os.path.join(SUT_FOLDER, 'bundletool.jar'))

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")

    def setUp(self):
        BaseClass.setUp(self)
        # Ensure app is in initial state
        Folder.navigate_to(folder=TEST_RUN_HOME, relative_from_current_folder=False)
        Folder.cleanup(self.app_name)
        Folder.copy(TEST_RUN_HOME + "/data/TestApp", TEST_RUN_HOME + "/TestApp")

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    @staticmethod
    def bundletool_build(bundletool_path, path_to_aab, path_to_apks):
        build_command = ('java -jar {0} build-apks --bundle="{1}" --output="{2}" --ks="{3}" --ks-pass=pass:"{4}" --ks-key-alias="{5}"' \
                          ' --key-pass=pass:"{6}"').format(bundletool_path, path_to_aab, path_to_apks, ANDROID_KEYSTORE_PATH,
                        ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS)
        output = run(build_command, log_level=CommandLogLevel.FULL)
        assert not "Error" in output, "create of .apks file failed"

    @staticmethod
    def bundletool_deploy(bundletool_path, path_to_apks, device_id):
        deploy_command = ('java -jar {0} install-apks --apks="{1}" --device-id={2}').format(bundletool_path, path_to_apks, EMULATOR_ID)
        output = run(deploy_command, log_level=CommandLogLevel.FULL)
        assert not "Error" in output, "deploy of app failed"
        assert  "The APKs have been extracted in the directory:" in output, "deploy of app failed"

    def test_001_build_android_app_bundle(self):
        """Build app with android app bundle option. Verify the output(app.aab) and use bundletool to deploy on device"""
        path_to_aab = os.path.join(self.app_name, "platforms", "android", "app", "build", "outputs", "bundle", "debug", "app.aab")

        output = Tns.build_android(attributes={"--path": self.app_name, "--aab":""}, assert_success=False)
        assert "The build result is located at:" in output
        assert path_to_aab in output
        assert File.exists(path_to_aab)

        #Verify app can be deployed on emulator via bundletool
        # Use bundletool to create the .apks file
        self.bundletool_build(self.bundletool_path, path_to_aab, self.path_to_apks)
        assert File.exists(self.path_to_apks)

        # Deploy on device
        self.bundletool_deploy(self.bundletool_path, self.path_to_apks, device_id=EMULATOR_ID)
        
        # Start the app on device
        Adb.start_app(EMULATOR_ID, "org.nativescript.TestApp")
        
        # Verify app looks correct inside emulator
        app_started = Device.wait_for_text(device_id=EMULATOR_ID, text='TAP')
        assert app_started, 'App is not started on device'

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Skip on Windows")
    def test_002_build_android_app_bundle_env_snapshot(self):
        """Build app with android app bundle option with --bundle and optimisations for snapshot.
           Verify the output(app.aab) and use bundletool to deploy on device."""
        # This test will not run on windows because env.snapshot option is not available on that OS
        
        path_to_aab = os.path.join(self.app_name, "platforms", "android", "app", "build", "outputs", "bundle", "release", "app.aab")
      
        #Configure app with snapshot optimisations
        source = os.path.join('data', 'abdoid-app-bundle', 'app.gradle')
        target = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'app.gradle' )
        File.copy(src=source, dest=target)

        source = os.path.join('data', 'abdoid-app-bundle', 'webpack.config.js')
        target = os.path.join(self.app_name, 'webpack.config.js' )
        File.copy(src=source, dest=target)

        #env.snapshot is applicable only in release build 
        output = Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--aab": "",
                                      "--env.uglify": "",
                                      "--env.snapshot": "",
                                      "--bundle": ""
                                      }, assert_success=False)
        assert "The build result is located at:" in output
        assert path_to_aab in output
        assert File.exists(path_to_aab)

        #Verify app can be deployed on emulator via bundletool
        # Use bundletool to create the .apks file
        self.bundletool_build(self.bundletool_path, path_to_aab, self.path_to_apks)
        assert File.exists(self.path_to_apks)

        # Verify that the correct .so file is included in the package
        File.unzip(self.path_to_apks, os.path.join(self.app_name, 'apks'))
        File.unzip(os.path.join(self.app_name, 'apks', 'splits', 'base-x86.apk'), os.path.join(self.app_name,'base_apk'))
        assert File.exists(os.path.join(self.app_name, 'base_apk', 'lib', 'x86', 'libNativeScript.so'))

        # Deploy on device
        self.bundletool_deploy(self.bundletool_path, self.path_to_apks, device_id=EMULATOR_ID)
        
        # Start the app on device
        Adb.start_app(EMULATOR_ID, "org.nativescript.TestApp")
        
        # Verify app looks correct inside emulator
        app_started = Device.wait_for_text(device_id=EMULATOR_ID, text='TAP')
        assert app_started, 'App is not started on device'



