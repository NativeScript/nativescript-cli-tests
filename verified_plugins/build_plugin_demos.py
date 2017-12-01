import csv
import os

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.git.git import Git
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_RUNTIME_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, TEST_RUN_HOME, IOS_RUNTIME_PATH, CURRENT_OS, TNS_PATH, BRANCH
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts
from verified_plugins.data.update_data import csv_writer

VERIFIED_PLUGINS_OUT = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'out')
WORKSPACE = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'workspace')
FAILED_CSV_PATH = os.path.join('verified_plugins', 'data', 'plugins_fail.csv')
PASS_CSV_PATH = os.path.join('verified_plugins', 'data', 'plugins_pass.csv')


def read_data():
    csv_file_path = os.path.join(TEST_RUN_HOME, 'verified_plugins', 'data', 'plugins.csv')
    csv_list = tuple(csv.reader(open(csv_file_path, 'rb'), delimiter=','))
    t = [tuple(l) for l in csv_list]
    return t


class BuildPluginDemos(BaseClass):
    FAILED_METADATA = []
    PASS_METADATA = []
    CURRENT_METADATA = []

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Folder.cleanup(VERIFIED_PLUGINS_OUT)
        Folder.cleanup(WORKSPACE)
        Folder.create(VERIFIED_PLUGINS_OUT)
        Folder.create(WORKSPACE)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        fail_count = len(getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups).failures)
        if fail_count == 0:
            self.PASS_METADATA.append(self.CURRENT_METADATA)
        else:
            self.FAILED_METADATA.append(self.CURRENT_METADATA)

        BaseClass.tearDown(self)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)

    @classmethod
    def tearDownClass(cls):
        csv_writer(cls.FAILED_METADATA, FAILED_CSV_PATH)
        csv_writer(cls.PASS_METADATA, PASS_CSV_PATH)

    @parameterized.expand(read_data())
    def test(self, name, repo, author, android_support, ios_support, downloads, start, demo_repo):

        self.CURRENT_METADATA = [name, repo, author, android_support, ios_support, downloads, start, demo_repo]

        # Navigate to so called `workspace` folder
        Folder.navigate_to(WORKSPACE)
        tns = os.path.join('..', '..', TNS_PATH)

        # Hack for native-autocomplete
        if 'native-' in name:
            name = name.replace('native-', 'nativescript-')

        # Clone demo (and handle the case when demo is in sub-folder)
        Folder.cleanup(name)
        demo_repo_url = demo_repo
        demo_repo_subfolder = None
        if '/tree/master/' in demo_repo_url:
            demo_repo_url = demo_repo.split('tree/master')[0].strip('/')
            demo_repo_subfolder = demo_repo.split('tree/master')[1].strip('/')
        Git.clone_repo(repo_url=demo_repo_url, local_folder=name)
        if demo_repo_subfolder is not None:
            plugin_name_original = name + '_original'
            Folder.cleanup(plugin_name_original)
            Folder.copy(name, plugin_name_original)
            Folder.cleanup(name)
            demo_folder = os.path.join(plugin_name_original, demo_repo_subfolder)
            Folder.copy(demo_folder, name)
            Folder.cleanup(plugin_name_original)

        # Check if demo is in demo folder
        if not File.exists(os.path.join(name, 'package.json')):
            print 'Demo is not directly in demo folder!'
            path = File.find(name, file_name='package.json', exact_match=True)
            path = path.rsplit(os.path.sep, 1)[0]
            Folder.copy(os.path.join(WORKSPACE, path), os.path.join(WORKSPACE, name + '_temp'))
            Folder.cleanup(os.path.join(WORKSPACE, name))
            Folder.copy(os.path.join(WORKSPACE, name + '_temp'), os.path.join(WORKSPACE, name))
            Folder.cleanup(os.path.join(WORKSPACE, name + '_temp'))

        # Check package.json
        json = TnsAsserts.get_package_json(name)
        typescript_in_dependencies = json.get('dependencies').get('nativescript-dev-typescript')
        assert typescript_in_dependencies is None, \
            'nativescript-dev-typescript found in dependencies, while it should be in devDependencies!'

        # Update plugins
        plugins_to_update = name
        if 'nativescript-dev-typescript' in str(TnsAsserts.get_package_json(name)):
            plugins_to_update = plugins_to_update + ';nativescript-dev-typescript'

        plugins_list = plugins_to_update.split(';')
        for plugin in plugins_list:
            if 'nativescript-dev-typescript' in plugin:
                Folder.navigate_to(name)
                run("npm uninstall nativescript-dev-typescript --save-dev")
                run("npm uninstall typescript --save-dev")
                if 'release' in BRANCH:
                    run("npm install typescript@2.1 --save-dev")
                    output = run("npm install nativescript-dev-typescript@0.3 --save-dev")
                else:
                    run("npm install typescript --save-dev")
                    output = run("npm install nativescript-dev-typescript --save-dev")
            elif '-dev-' in plugin:
                Folder.navigate_to(name)
                run("npm uninstall " + plugin + " --save-dev")
                output = run("npm install " + plugin + " --save-dev")
            else:
                Folder.navigate_to(name)
                run("npm uninstall " + plugin + " --save")
                output = run("npm install " + plugin + " --save")
            Folder.navigate_to(WORKSPACE, relative_from_current_folder=False)
            assert 'ERR' not in output, 'Failed to install ' + plugin

        # Update tns-core-modules
        Tns.update_modules(name)

        # Add platform and build it
        out_file_path = os.path.join(VERIFIED_PLUGINS_OUT, name)
        Folder.create(out_file_path)
        if android_support:
            Tns.platform_add_android(attributes={"--path": name, "--frameworkPath": ANDROID_RUNTIME_PATH},
                                     tns_path=tns)
            Tns.build_android(attributes={"--path": name,
                                          "--keyStorePath": ANDROID_KEYSTORE_PATH,
                                          "--keyStorePassword": ANDROID_KEYSTORE_PASS,
                                          "--keyStoreAlias": ANDROID_KEYSTORE_ALIAS,
                                          "--keyStoreAliasPassword": ANDROID_KEYSTORE_ALIAS_PASS,
                                          "--release": "",
                                          "--copy-to": out_file_path},
                              tns_path=tns)

        if ios_support and CURRENT_OS is OSType.OSX:
            Tns.platform_add_ios(attributes={"--path": name, "--frameworkPath": IOS_RUNTIME_PATH}, tns_path=tns)
            # Skip this because of https://github.com/NativeScript/nativescript-cli/issues/2357
            # Tns.build_ios(attributes={"--path": plugin_name, "--release": "", "--copy-to": out_file_path}, tns_path=tns)
            Tns.build_ios(attributes={"--path": name, "--forDevice": "", "--release": "",
                                      "--copy-to": out_file_path}, tns_path=tns)

        # If everything is OK, clean plugin folder
        Folder.cleanup(name)
