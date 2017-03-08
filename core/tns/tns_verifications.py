'''
Verifications for NativeScript projects.
'''
import json
import os
import re

from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS
from core.tns.tns_installed_platforms import Platforms
from core.tns.tns_prepare_type import Prepare


class TnsAsserts(object):
    NODE_MODULES = '/node_modules/'
    TNS_MODULES = NODE_MODULES + 'tns-core-modules/'
    HOOKS = '/hooks/'
    PLATFORM_IOS = '/platforms/ios/'
    PLATFORM_ANDROID = '/platforms/android/'
    PLATFORM_ANDROID_APP_PATH = PLATFORM_ANDROID + 'src/main/assets/app/'
    PLATFORM_ANDROID_NPM_MODULES_PATH = PLATFORM_ANDROID_APP_PATH + 'tns_modules/'
    PLATFORM_ANDROID_TNS_MODULES_PATH = PLATFORM_ANDROID_NPM_MODULES_PATH + 'tns-core-modules/'

    @staticmethod
    def __read_json(path):
        """
        Read content of json file.
        :param path: Path to file.
        :return: Content of file as json object.
        """

        # This is to handle test for app with space.
        # In this case we put app name inside ''.
        path = path.replace('\'', '')
        path = path.replace('\"', '')

        # Check if file exists
        assert File.exists(path), 'Failed to find file: ' + path

        # Read it...
        with open(path) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def _get_modules_version(app_name):
        """
        Get version of `tns-core-modules` inside project
        :param app_name: Project name (path relative to TEST_RUN_HOME).
        :return: Value of `tns-core-modules`
        """
        return TnsAsserts.get_package_json(app_name=app_name).get('dependencies').get('tns-core-modules')

    @staticmethod
    def _get_ios_app_path(app_name):
        normalized_app_name = app_name.replace(' ', '')
        normalized_app_name = normalized_app_name.replace('-', '')
        normalized_app_name = normalized_app_name.replace('_', '')
        return app_name + TnsAsserts.PLATFORM_IOS + normalized_app_name + '/app/'

    @staticmethod
    def _get_ios_modules_path(app_name):
        modules_path = TnsAsserts._get_ios_app_path(app_name) + 'tns_modules/tns-core-modules/'
        return modules_path

    @staticmethod
    def created(app_name, output=None, full_check=True):
        '''
        Assert application is created properly.
        :param app_name: App name
        :param output: Outout of `tns create command`
        :param full_check: If true everything will be checked. If false only console output will be checked.
        '''

        # Assert console output is ok
        if output is not None:
            app = app_name.rsplit('/')[-1]
            assert 'nativescript-theme-core' in output
            assert 'nativescript-dev-android-snapshot' in output
            assert 'Project {0} was successfully created'.format(app) in output, 'Failed to create {0}'.format(app)

        if full_check:
            # Assert files are ok
            assert File.exists(app_name)
            assert File.exists(app_name + '/node_modules/tns-core-modules/package.json')
            assert File.exists(app_name + '/node_modules/tns-core-modules/LICENSE')
            assert File.exists(app_name + '/node_modules/tns-core-modules/xml/xml.js')
            assert Folder.is_empty(app_name + '/platforms')

            # Assert content of package.json
            app_id = app_name.replace(' ', '').replace('_', '').replace('-', '').rsplit('/')[-1]
            strings = ['org.nativescript.{0}'.format(app_id), 'tns-core-modules', 'nativescript-theme-core',
                       'nativescript-dev-android-snapshot']
            TnsAsserts.package_json_contains(app_name, string_list=strings)

    @staticmethod
    def created_ts(app_name, output=None):
        '''
        Assert TypeScript application is created properly.
        :param app_name: App name
        :param output: Outout of `tns create command`
        '''

        # First make sure base app is created
        TnsAsserts.created(app_name=app_name, output=output)

        # Assert output contains TypeScript plugin
        assert 'nativescript-dev-typescript' in output

        # Assert files added with TypeScript plugin
        ts_config = os.path.join(app_name, 'tsconfig.json')
        ref_dts = os.path.join(app_name, 'references.d.ts')
        dts = os.path.join(app_name, TnsAsserts.TNS_MODULES, 'tns-core-modules.d.ts')

        # Assert content of files added with TypeScript plugin.
        modules_version = TnsAsserts._get_modules_version(app_name=app_name)
        modules_version = re.sub("\D", "", modules_version)

        File.exists(ts_config)
        File.exists(ref_dts)
        File.exists(dts)
        red_tds_content = File.read(ref_dts)
        if modules_version[0] < 3:
            assert './node_modules/tns-core-modules/tns-core-modules.d.ts' in red_tds_content
        else:
            assert './node_modules/tns-core-modules/tns-core-modules.d.ts' not in red_tds_content
            ts_config_json = TnsAsserts.get_tsconfig_json(app_name=app_name)
            paths = ts_config_json.get('compilerOptions').get('paths')
            assert paths is not None, 'Paths missing in tsconfig.json'
            assert '/node_modules/tns-core-modules/' in str(paths), \
                '"/node_modules/tns-core-modules/" not found in paths section iof tsconfig.json'

        assert not Folder.is_empty(app_name + TnsAsserts.NODE_MODULES + '/nativescript-dev-typescript')
        assert File.exists(app_name + TnsAsserts.HOOKS + 'before-prepare/nativescript-dev-typescript.js')
        assert File.exists(app_name + TnsAsserts.HOOKS + 'before-watch/nativescript-dev-typescript.js')
        assert File.exists(app_name + TnsAsserts.NODE_MODULES + 'typescript/bin/tsc')

    @staticmethod
    def platform_added(app_name, platform=Platforms.NONE, output=None):
        '''
        Assert platform is added.
        :param app_name: Application name (folder where app is located).
        :param platform: Platforms that should be available.
        :param output: output of `tns platform add` command
        '''

        # Verify console output is correct
        if output is not None:
            if platform is Platforms.ANDROID:
                assert 'tns-android' in output
            if platform is Platforms.IOS:
                assert 'tns-ios' in output
            assert 'Copying template files...' in output
            assert 'Project successfully created.' in output

        # This is to handle test for app with space.
        # In this case we put app name inside ''.
        app_name = app_name.replace('\'', '')
        app_name = app_name.replace('\"', '')

        # Verify file and folder content
        if platform is Platforms.NONE:
            assert not File.exists(app_name + TnsAsserts.PLATFORM_ANDROID)
            assert not File.exists(app_name + TnsAsserts.PLATFORM_IOS)
        if platform is Platforms.ANDROID or platform is Platforms.BOTH:
            assert File.exists(app_name + TnsAsserts.PLATFORM_ANDROID)
            assert not Folder.is_empty(
                app_name + TnsAsserts.PLATFORM_ANDROID + '/build-tools/android-static-binding-generator')
        if platform is Platforms.IOS or platform is Platforms.BOTH:
            assert File.exists(app_name + TnsAsserts.PLATFORM_IOS)

    @staticmethod
    def platform_list_status(output=None, prepared=Platforms.NONE, added=Platforms.NONE):
        '''
        Assert platform list status
        :param output: Outout of `tns platform list` command
        :param prepared: Prepared platform.
        :param added: Added platform.
        '''
        if output is not None:
            # Assert prepare status
            if prepared is Platforms.NONE:
                if added is Platforms.NONE:
                    assert 'The project is not prepared for' not in output
                else:
                    assert 'The project is not prepared for any platform' in output
            if prepared is Platforms.ANDROID:
                assert 'The project is prepared for:  android' in output
            if prepared is Platforms.IOS:
                assert 'The project is prepared for:  ios' in output
            if prepared is Platforms.BOTH:
                assert 'The project is prepared for:  ios and android' in output

            # Assert platform added status
            if added is Platforms.NONE:
                assert 'No installed platforms found. Use $ tns platform add' in output
                if CURRENT_OS is OSType.OSX:
                    assert 'Available platforms for this OS:  ios and android' in output
                else:
                    assert 'Available platforms for this OS:  android' in output
            if added is Platforms.ANDROID:
                assert 'Installed platforms:  android' in output
            if added is Platforms.IOS:
                assert 'Installed platforms:  ios' in output
            if added is Platforms.BOTH:
                assert 'Installed platforms:  android and ios' in output

    @staticmethod
    def package_json_contains(app_name, string_list=None):
        """
        Assert package.json contains list of strings.
        :param app_name: Application name.
        :param string_list: List of strings.
        """
        package_json_path = app_name + '/package.json'
        output = File.read(package_json_path)
        for item in string_list:
            if item in output:
                print '{0} found in {1}.'.format(item, package_json_path)
            else:
                print 'package.json:'
                print output
                assert False, '{0} NOT found in {1}.'.format(item, package_json_path)

    @staticmethod
    def get_package_json(app_name):
        """
        Return content of package.json as json object.
        :param app_name: Application name.
        :return: package.json as json object.
        """
        path = os.path.join(app_name, 'package.json')
        return TnsAsserts.__read_json(path=path)

    @staticmethod
    def get_tsconfig_json(app_name):
        """
        Return content of package.json as json object.
        :param app_name: Application name.
        :return: package.json as json object.
        """
        path = os.path.join(app_name, 'tsconfig.json')
        return TnsAsserts.__read_json(path=path)

    @staticmethod
    def prepared(app_name, platform=Platforms.BOTH, output=None, prepare_type=Prepare.FULL):
        '''
        Assert project is prepared properly.
        :param app_name: Application name.
        :param platform: Platform that should be prepared.
        :param output: Output of `tns prepare` platform.
        :param prepare_type: Prepare type (SKIP, INCREMENTAL, FULL, FIRST_TIME)
        '''

        def _incremental_prepare():
            assert 'Skipping prepare.' not in output
            assert 'Preparing project...' in output
            if platform is Platforms.ANDROID or platform is Platforms.BOTH:
                assert 'Project successfully prepared (android)' in output
            if platform is Platforms.IOS or platform is Platforms.BOTH:
                assert 'Project successfully prepared (ios)' in output

        def _full_prepare():
            _incremental_prepare()
            if platform is Platforms.ANDROID or platform is Platforms.BOTH:
                assert 'Successfully prepared plugin tns-core-modules for android.' in output
                assert 'Successfully prepared plugin tns-core-modules-widgets for android.' in output
            if platform is Platforms.IOS or platform is Platforms.BOTH:
                assert 'Successfully prepared plugin tns-core-modules for ios.' in output
                assert 'Successfully prepared plugin tns-core-modules-widgets for ios.' in output

        if output is not None:
            if prepare_type is Prepare.SKIP:
                assert 'Skipping prepare.' in output
                assert 'Preparing project...' not in output
            if prepare_type is Prepare.INCREMENTAL:
                _incremental_prepare()
                assert 'Successfully prepared plugin tns-core-modules for' not in output
                assert 'Successfully prepared plugin tns-core-modules-widgets for' not in output
            if prepare_type is Prepare.FULL:
                _full_prepare()
                assert 'Installing' not in output
                assert 'Project successfully created' not in output
            if prepare_type is Prepare.FIRST_TIME:
                _full_prepare()
                assert 'Installing' in output
                assert 'Project successfully created' in output
                if platform is Platforms.ANDROID or platform is Platforms.BOTH:
                    assert 'tns-android' in output
                if platform is Platforms.IOS or platform is Platforms.BOTH:
                    assert 'tns-ios' in output

                    # Ignore because of https://github.com/NativeScript/nativescript-cli/issues/2586
                    # if platform is Platforms.ANDROID or platform is Platforms.BOTH:
                    #     app_path = app_name + TnsAsserts.PLATFORM_ANDROID_APP_PATH
                    #     modules_path = app_name + TnsAsserts.PLATFORM_ANDROID_TNS_MODULES_PATH
                    #     assert File.exists(app_path + 'main-view-model.js'), \
                    #         'Application files does not exists in platforms folder.'
                    #     assert File.exists(modules_path + 'application/application.js'), \
                    #         'Modules does not exists in platforms folder.'
                    #     assert File.exists(modules_path + 'xml/xml.js'), 'TNS Modules does not exists in platforms folder.'
                    #     assert not File.exists(modules_path + 'application/application.android.js'), \
                    #         'Prepare does not strip \'android\' from name of js files.'
                    #     assert not File.exists(modules_path + 'application/application.ios.js'), \
                    #         'Prepare does not skip \'ios\' specific js files.'
                    #
                    # if platform is Platforms.IOS or platform is Platforms.BOTH:
                    #     app_path = TnsAsserts._get_ios_app_path(app_name)
                    #     modules_path = TnsAsserts._get_ios_modules_path(app_name)
                    #     assert File.exists(app_path + 'main-view-model.js'), \
                    #         'Application files does not exists in platforms folder.'
                    #     assert File.exists(modules_path + 'application/application.js'), \
                    #         'Modules does not exists in platforms folder.'
                    #     assert not File.exists(modules_path + 'application/application.android.js'), \
                    #         'Prepare does not skip \'ios\' specific js files.'
                    #     assert not File.exists(modules_path + 'application/application.ios.js'), \
                    #         'Prepare does not strip \'ios\' from name of js files.'
