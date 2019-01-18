import urllib.request

from core.settings.settings import SUT_FOLDER, EMULATOR_NAME, EMULATOR_ID

from core.base_class.BaseClass import BaseClass

from core.osutils.command import run

from core.osutils.command_log_level import CommandLogLevel


class AndroidAppBundleTests(BaseClass):
    
    bundletool_path = os.path.join(SUT_FOLDER,"bundletool-all-0.8.0.jar")

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Emulator.stop()
        Emulator.ensure_available()

        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})

        #Download bundletool
        url = 'https://github.com/google/bundletool/releases/download/0.8.0/bundletool-all-0.8.0.jar'
        urllib.request.urlretrieve(url, SUT_FOLDER)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Tns.kill()

    def test_001_build_android_app_bundle(self):
        """Build app with android app bundle option. Verify the output(app.aab) and use bundletool to deploy on device"""
        # This is required to ensure the app is in initial state
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        path_to_aab = os.path.join(self.app_name, "platforms", "android", "app", "build", "outputs", "bundle", "debug", "app.aab")

        Tns.build_android(attributes={"--path": self.app_name, "--aab":""})
        assert "The build result is located at:" in output
        assert path_to_aab in output
        assert File.exists(path_to_aab)

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Skip on Windows")
    def test_002_build_android_app_bundle_env_snapshot(self):
        """Build app with android app bundle option with --bundle and optimisations for snapshot.
           Verify the output(app.aab) and use bundletool to deploy on device."""
        
        # This is required to ensure the app is in initial state
        Folder.cleanup(self.app_name)
        Tns.create_app(self.app_name)
        path_to_aab = os.path.join(self.app_name, "platforms", "android", "app", "build", "outputs", "bundle", "release", "app.aab")

        #Configure app with snapshot optimisations
        source = os.path.join('data', 'abdoid-app-bundle', 'app.gradle')
        target = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'app.gradle' )
        File.copy(src=source, dest=target)

        source = os.path.join('data', 'abdoid-app-bundle', 'webpack.config.js')
        target = os.path.join(self.app_name, 'app', 'App_Resources', 'Android', 'webpack.config.js' )
        File.copy(src=source, dest=target)

        

        #env.snapshot is applicable only in release build 
        Tns.build_android(attributes={"--path": self.app_name,
                                      "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                      "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                      "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                      "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                      "--release": "",
                                      "--aab": "",
                                      "--env.uglify": "",
                                      "--env.snapshot": "",
                                      "--bundle": ""
                                      })
        assert "The build result is located at:" in output
        assert path_to_aab in output
        assert File.exists(path_to_aab)

        #Verify app can be deployed on emulator via bundletool
        # Use bundletool to create the .apks file
        path_to_apks = os.path.join(self.app_name,'app.apks')
        build_command = 'java -jar ' + bundletool_path + ' build-apks --bundle=' + path_to_aab + /
            ' --output=' path_to_apks + ' --ks=' + ANDROID_KEYSTORE_PATH + /
            ' --ks-pass=' + keyStorePassword + ' --ks-key-alias=' + keyStoreAlias + keyStoreAlias + /
            ' --key-pass=' + keyStoreAliasPassword
        log = run(build_command, timeout=timeout, wait=False, log_level=CommandLogLevel.FULL)
        assert not "error" in output, "create of .apks file failed"

        # deploy on device
        deploy_command = 'java -jar ' + bundletool_path + ' install-apks --apks=' + path_to_apks
        command = 'java -jar ' + bundletool_path + ' build-apks --bundle=' + path_to_aab + /
            ' --output=' path_to_apks + ' --ks=' + ANDROID_KEYSTORE_PATH + /
            ' --ks-pass=' + keyStorePassword + ' --ks-key-alias=' + keyStoreAlias + keyStoreAlias + /
            ' --key-pass=' + keyStoreAliasPassword
        log = run(deploy_command, timeout=timeout, wait=False, log_level=CommandLogLevel.FULL)
        assert not "error" in output, "deploy of app failed"
        
        # Verify app looks correct inside emulator
        Device.screen_match(device_name=EMULATOR_NAME, device_id=EMULATOR_ID,
                            expected_image='hello-world-js')



