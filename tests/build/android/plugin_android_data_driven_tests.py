"""
Test for plugin commands in context of Android
"""
import os
import unittest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.java.java import Java
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_PACKAGE, TEST_RUN_HOME
from core.tns.tns import Tns


class PluginsAndroidDataDrivenTests(BaseClass):
    PLUGIN_DEMOS = [
        ('including-jar.tgz', 'no-aar-build', 'There is Jar in the plugin. This is actually nativescript-svg.'),
        ('jniLibs.tgz', 'aar-build', 'Plugin with jniLibs. This is actually nativescript-android-jpush.'),
        ('no-platform-android.tgz', 'no-aar-build', 'No platforms/android, platforms/ios exists.'),
        ('only-include-gradle.tgz', 'no-aar-build', 'platfroms/android contains only include.gradle.'),
        ('some-aar-in.tgz', 'no-aar-build', 'Some aar file is in the plugin.'),
        ('with-aar-file.tgz', 'no-aar-build', 'Plugin with aar files.'),
        ('with-assets-folder.tgz', 'aar-build', 'Plugin with assets folder.'),
        ('with-manifest.tgz', 'aar-build', 'Plugin with AndroidManifest.xml'),
        ('with-res-folder.tgz', 'aar-build', 'Plugin with res folder.'),
    ]

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Tns.create_app(cls.app_name)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_PACKAGE})
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")
        Folder.copy(TEST_RUN_HOME + "/" + cls.app_name, TEST_RUN_HOME + "/data/TestApp")

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup(TEST_RUN_HOME + "/data/TestApp")
        BaseClass.tearDownClass()

    @parameterized.expand(PLUGIN_DEMOS)
    @unittest.skipIf(Java.version() != "1.8", "Some of test plugins are not compatible with java 10+")
    def test_200_plugin(self, plugin, verification, comment):
        print "Test case: " + comment
        Folder.cleanup(self.app_name)
        Folder.copy(TEST_RUN_HOME + "/data/TestApp", TEST_RUN_HOME + "/TestApp")
        plugin_path = os.path.join(TEST_RUN_HOME, 'data', 'plugins', 'android', plugin)
        plugin_name = plugin.replace(".tgz", "")
        Tns.plugin_add(plugin_path, attributes={"--path": self.app_name})
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Successfully prepared plugin {0} for android".format(plugin_name) in output
        if "no-aar-build" in verification:
            assert "Built aar for" not in output
        else:
            assert "Built aar for" in output
            plugin_folder = plugin_name.replace("-", "_")
            aar_file = os.path.join(self.app_name, 'platforms', 'tempPlugin', plugin_folder, 'build', 'outputs',
                                    'aar', '{0}-release.aar'.format(plugin_folder))
            assert File.exists(aar_file)
