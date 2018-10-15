"""
Test for plugin create command.
"""

import os
import unittest

from core.base_class.BaseClass import BaseClass
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS
from core.tns.tns import Tns


class PluginCreateTests(BaseClass):
    plugin_name = "nativescript-test-plugin"

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.plugin_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_100_plugin_create(self):
        Tns.plugin_create(name=self.plugin_name)

    def test_200_plugin_create_with_path(self):
        Tns.plugin_create(name=self.plugin_name, attributes={"--path": "plugin-folder"})

    def test_201_plugin_create_custom_template(self):
        plugin_url = "https://github.com/NativeScript/nativescript-plugin-seed/tarball/master"
        output = Tns.plugin_create(name=self.plugin_name, attributes={"--template": plugin_url})
        assert "Make sure your custom template is compatible with the Plugin Seed" in output

    def test_202_plugin_create_custom_user_and_plugin_name(self):
        Tns.plugin_create(name=self.plugin_name, attributes={"--username": "gitUser", "--pluginName": "customName"})
        # TODO: Assert username and pluginName are replaced in generated files.

    def test_300_build_demo(self):
        # TODO: Run npm scripts from plugin seed (build plugin, link plugin and then build the app).
        Tns.plugin_create(name=self.plugin_name)
        demo_path = self.plugin_name + os.sep + 'demo'
        Tns.build_android(attributes={"--path": demo_path})
        if CURRENT_OS == OSType.OSX:
            Tns.build_ios(attributes={"--path": demo_path})

    @unittest.skip("Skip because of https://github.com/NativeScript/nativescript-cli/issues/3962")
    def test_400_plugin_create_with_wrong_template(self):
        plugin_url = "https://github.com/NativeScript/nativescript-plugin-seed/"
        output = Tns.plugin_create(name=self.plugin_name, attributes={"--template": plugin_url}, assert_success=False)
        assert "successfully created" not in output, "It is expected plugin create to fail in this test case."
        assert not Folder.exists(self.plugin_name), "Plugin folder should not exists if create operation fails."
