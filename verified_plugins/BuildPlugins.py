import csv
import os
from unittest import SkipTest

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.git.GitHub import GitHub
from core.osutils.command import run
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_RUNTIME_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, TEST_RUN_HOME, IOS_RUNTIME_PATH, CURRENT_OS, TNS_PATH
from core.tns.tns import Tns

VERIFIED_PLUGINS_OUT = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'out')
WORKSPACE = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'workspace')


def read_data():
    csv_file_path = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'data', 'plugins.csv')
    csv_list = tuple(csv.reader(open(csv_file_path, 'rb'), delimiter=','))
    t = [tuple(l) for l in csv_list]
    t.pop(0)
    return t


class BuildPlugins_Tests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Folder.cleanup(VERIFIED_PLUGINS_OUT)
        Folder.cleanup(WORKSPACE)
        Folder.create(VERIFIED_PLUGINS_OUT)
        Folder.create(WORKSPACE)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)

    @parameterized.expand(read_data())
    def test(self, plugin_name, platforms, status, author, plugin_repo, plugin_location, plugin_demo_repo,
             plugins_to_update, custom_script, comments):

        if 'deprecated' in status:

        # Navigate to so called `workspace` folder
        Folder.navigate_to(WORKSPACE)
        tns = os.path.join('..', '..', TNS_PATH)

        # Clone demo (and handle the case when demo is in sub-folder)
        Folder.cleanup(plugin_name)
        git_repo = plugin_demo_repo
        git_repo_subfolder = None
        if ';' in git_repo:
            git_repo = plugin_demo_repo.split(';')[0]
            git_repo_subfolder = plugin_demo_repo.split(';')[1]
        GitHub.clone_repo(repo_url=git_repo, local_folder=plugin_name)
        if git_repo_subfolder is not None:
            plugin_name_original = plugin_name + '_original'
            Folder.cleanup(plugin_name_original)
            Folder.copy(plugin_name, plugin_name_original)
            Folder.cleanup(plugin_name)
            demo_folder = os.path.join(plugin_name_original, git_repo_subfolder)
            Folder.copy(demo_folder, plugin_name)
            Folder.cleanup(plugin_name_original)

        # Update tns-core-modules
        Tns.update_modules(plugin_name, tns_path=tns)

        # Update plugins
        plugins_to_update = (plugin_name + ';' + plugins_to_update).rstrip(';')
        plugins_list = plugins_to_update.split(';')
        for plugin in plugins_list:
            if '-dev-' in plugin:
                Folder.navigate_to(plugin_name)
                run("npm uninstall " + plugin + " --save-dev")
                run("npm install " + plugin + " --save-dev")
                Folder.navigate_to(WORKSPACE, relative_from_current_folder=False)
            else:
                Tns.plugin_remove(plugin, attributes={"--path": plugin_name}, assert_success=False, tns_path=tns)
                Tns.plugin_add(plugin, attributes={"--path": plugin_name}, tns_path=tns)

        # Add platform and build it
        out_file_path = os.path.join(VERIFIED_PLUGINS_OUT, plugin_name)
        Folder.create(out_file_path)
        if "android" in platforms or "cross" in platforms:
            Tns.platform_add_android(attributes={"--path": plugin_name, "--frameworkPath": ANDROID_RUNTIME_PATH},
                                     tns_path=tns)
            Tns.build_android(attributes={"--path": plugin_name,
                                          "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                          "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                          "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                          "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                          "--release": "",
                                          "--copy-to": out_file_path},
                              tns_path=tns)

        if ("ios" in platforms or "cross" in platforms) and CURRENT_OS is OSType.OSX:
            Tns.platform_add_ios(attributes={"--path": plugin_name, "--frameworkPath": IOS_RUNTIME_PATH}, tns_path=tns)
            # Skip this because of https://github.com/NativeScript/nativescript-cli/issues/2357
            # Tns.build_ios(attributes={"--path": plugin_name, "--release": "", "--copy-to": out_file_path}, tns_path=tns)
            Tns.build_ios(attributes={"--path": plugin_name, "--forDevice": "", "--release": "",
                                      "--copy-to": out_file_path}, tns_path=tns)

        # If everything is OK, clean plugin folder
        Folder.cleanup(plugin_name)
