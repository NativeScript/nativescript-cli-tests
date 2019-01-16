import urllib.request

from core.settings.settings import SUT_FOLDER

from core.base_class.BaseClass import BaseClass


class BuildAndroidTests(BaseClass):
    
    bundletool_path = os.path.join(SUT_FOLDER,"bundletool-all-0.8.0.jar")

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

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



