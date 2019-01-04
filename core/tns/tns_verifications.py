"""
Verifications for NativeScript projects.
"""
import os

from core.json.json_utils import Json
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS, USE_YARN
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare


class TnsAsserts(object):
    NODE_MODULES = '/node_modules/'
    TNS_MODULES = NODE_MODULES + 'tns-core-modules/'
    HOOKS = '/hooks/'
    PLATFORM_IOS = os.path.join('platforms', 'ios/')
    PLATFORM_ANDROID = os.path.join('platforms', 'android/')
    PLATFORM_ANDROID_BUILD = os.path.join(PLATFORM_ANDROID, 'app', 'build')
    PLATFORM_ANDROID_APK_PATH = os.path.join(PLATFORM_ANDROID_BUILD, 'outputs', 'apk')
    PLATFORM_ANDROID_APK_RELEASE_PATH = os.path.join(PLATFORM_ANDROID_BUILD, 'outputs', 'apk', 'release')
    PLATFORM_ANDROID_APK_DEBUG_PATH = os.path.join(PLATFORM_ANDROID_BUILD, 'outputs', 'apk', 'debug')
    PLATFORM_ANDROID_SRC_MAIN_PATH = os.path.join(PLATFORM_ANDROID, 'app', 'src', 'main/')
    PLATFORM_ANDROID_APP_PATH = os.path.join(PLATFORM_ANDROID_SRC_MAIN_PATH, 'assets', 'app/')
    PLATFORM_ANDROID_NPM_MODULES_PATH = os.path.join(PLATFORM_ANDROID_APP_PATH, 'tns_modules/')
    PLATFORM_ANDROID_TNS_MODULES_PATH = os.path.join(PLATFORM_ANDROID_NPM_MODULES_PATH, 'tns-core-modules/')

    @staticmethod
    def _get_ios_app_path(app_name):
        normalized_app_name = app_name.replace(' ', '')
        normalized_app_name = normalized_app_name.replace('-', '')
        normalized_app_name = normalized_app_name.replace('_', '')
        return os.path.join(app_name, TnsAsserts.PLATFORM_IOS, normalized_app_name, 'app/')

    @staticmethod
    def _get_ios_modules_path(app_name):
        modules_path = os.path.join(TnsAsserts._get_ios_app_path(app_name), 'tns_modules', 'tns-core-modules/')
        return modules_path

    @staticmethod
    def get_modules_version(app_name):
        """
        Get version of `tns-core-modules` inside project
        :param app_name: Project name (path relative to TEST_RUN_HOME).
        :return: Value of `tns-core-modules`
        """
        return TnsAsserts.get_package_json(app_name=app_name).get('dependencies').get('tns-core-modules')

    @staticmethod
    def get_platform_version(app_name, platform):
        """
        Get version of `tns-core-modules` inside project
        :param app_name: Project name (path relative to TEST_RUN_HOME).
        :param platform: Platform as string - 'android' or `ios`
        :return: Value of `tns-core-modules`
        """
        return TnsAsserts.get_package_json(app_name=app_name).get('nativescript').get('tns-' + platform).get('version')

    @staticmethod
    def created(app_name, output=None, full_check=True):
        """
        Assert application is created properly.
        :param app_name: App name
        :param output: Output of `tns create command`
        :param full_check: If true everything will be checked. If false only console output will be checked.
        """

        # Assert console output is ok
        if output is not None:
            app = app_name.rsplit('/')[-1]
            if USE_YARN != "True":
                if Npm.version() < 5:
                    assert 'nativescript-theme-core' in output
            assert 'Project {0} was successfully created'.format(app) in output, 'Failed to create {0}'.format(app)

        if full_check:
            # Assert files are ok
            assert File.exists(app_name)
            assert File.exists(app_name + '/node_modules/tns-core-modules/package.json')
            assert File.exists(app_name + '/node_modules/tns-core-modules/LICENSE')
            assert File.exists(app_name + '/node_modules/tns-core-modules/xml/xml.js')
            assert File.exists(app_name + '/node_modules/nativescript-theme-core')

            # Assert content of package.json
            app_id = app_name.replace(' ', '').replace('_', '').replace('-', '').rsplit('/')[-1]
            strings = ['org.nativescript.{0}'.format(app_id), 'tns-core-modules', 'nativescript-theme-core']
            TnsAsserts.package_json_contains(app_name, string_list=strings)

    @staticmethod
    def created_ts(app_name, output=None):
        """
        Assert TypeScript application is created properly.
        :param app_name: App name
        :param output: Output of `tns create command`
        """

        # First make sure base app is created
        TnsAsserts.created(app_name=app_name, output=output)

        # Assert output contains TypeScript plugin
        if USE_YARN != "True":
            if Npm.version() < 5:
                assert 'nativescript-dev-typescript' in output

        # Assert files added with TypeScript plugin
        ts_config = os.path.join(app_name, 'tsconfig.json')
        ref_dts = os.path.join(app_name, 'references.d.ts')
        dts = os.path.join(app_name, TnsAsserts.TNS_MODULES, 'tns-core-modules.d.ts')

        # Assert content of files added with TypeScript plugin.
        assert File.exists(ts_config)
        assert not File.exists(ref_dts)
        assert File.exists(dts)

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
    def created_ng(app_name, output=None):
        """
        Assert TypeScript application is created properly.
        :param app_name: App name
        :param output: Output of `tns create command`
        """

        # First make sure base typescript app is created
        TnsAsserts.created_ts(app_name=app_name, output=output)

    @staticmethod
    def platform_added(app_name, platform=Platform.NONE, output=None):
        """
        Assert platform is added.
        :param app_name: Application name (folder where app is located).
        :param platform: Platforms that should be available.
        :param output: output of `tns platform add` command
        """

        # Verify console output is correct
        if output is not None:
            if platform is Platform.ANDROID:
                assert 'Platform android successfully added' in output
            if platform is Platform.IOS and CURRENT_OS == OSType.OSX:
                assert 'Platform ios successfully added' in output
            else: 
                assert 'Applications for platform ios can not be built on this OS'
            assert 'Project successfully created.' not in output

        # This is to handle test for app with space.
        # In this case we put app name inside ''.
        app_name = app_name.replace('\'', '')
        app_name = app_name.replace('\"', '')

        # Verify file and folder content
        if platform is Platform.NONE:
            assert not File.exists(os.path.join(app_name, TnsAsserts.PLATFORM_IOS))
            assert not File.exists(os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID))
        if platform is Platform.ANDROID or platform is Platform.BOTH:
            assert File.exists(os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID))
        if platform is Platform.IOS or platform is Platform.BOTH:
            if CURRENT_OS == OSType.OSX:
                assert File.exists(os.path.join(app_name, TnsAsserts.PLATFORM_IOS))
            else: 
                assert not File.exists(os.path.join(app_name, TnsAsserts.PLATFORM_IOS))

    @staticmethod
    def platform_list_status(output=None, prepared=Platform.NONE, added=Platform.NONE):
        """
        Assert platform list status
        :param output: Outout of `tns platform list` command
        :param prepared: Prepared platform.
        :param added: Added platform.
        """
        if output is not None:
            # Assert prepare status
            if prepared is Platform.NONE:
                if added is Platform.NONE:
                    assert 'The project is not prepared for' not in output
                else:
                    assert 'The project is not prepared for any platform' in output
            if prepared is Platform.ANDROID:
                assert 'The project is prepared for:  android' in output
            if prepared is Platform.IOS:
                assert 'The project is prepared for:  ios' in output
            if prepared is Platform.BOTH:
                assert 'The project is prepared for:  ios and android' in output

            # Assert platform added status
            if added is Platform.NONE:
                assert 'No installed platforms found. Use $ tns platform add' in output
                if CURRENT_OS is OSType.OSX:
                    assert 'Available platforms for this OS:  ios and android' in output
                else:
                    assert 'Available platforms for this OS:  android' in output
            if added is Platform.ANDROID:
                assert 'Installed platforms:  android' in output
            if added is Platform.IOS:
                assert 'Installed platforms:  ios' in output
            if added is Platform.BOTH:
                assert 'Installed platforms:  android and ios' in output

    @staticmethod
    def package_json_contains(app_name, string_list=None):
        """
        Assert package.json contains list of strings.
        :param app_name: Application name.
        :param string_list: List of strings.
        """
        package_json_path = os.path.join(app_name, 'package.json')
        output = File.read(package_json_path)
        for item in string_list:
            if item in output:
                print '{0} found in {1}.'.format(item, str(package_json_path))
            else:
                print 'package.json:'
                print output
                assert False, '{0} NOT found in {1}.'.format(item, str(package_json_path))

    @staticmethod
    def get_package_json(app_name):
        """
        Return content of package.json as json object.
        :param app_name: Application name.
        :return: package.json as json object.
        """
        path = os.path.join(app_name, 'package.json')
        return Json.read(file_path=path)

    @staticmethod
    def get_tsconfig_json(app_name):
        """
        Return content of package.json as json object.
        :param app_name: Application name.
        :return: package.json as json object.
        """
        path = os.path.join(app_name, 'tsconfig.json')
        return Json.read(file_path=path)

    @staticmethod
    def prepared(app_name, platform=Platform.BOTH, output=None, prepare=Prepare.FULL):
        """
        Assert project is prepared properly.
        :param app_name: Application name.
        :param platform: Platform that should be prepared.
        :param output: Output of `tns prepare` platform.
        :param prepare: Prepare type (SKIP, INCREMENTAL, FULL, FIRST_TIME)
        """

        def _incremental_prepare():
            assert 'Skipping prepare.' not in output
            assert 'Preparing project...' in output
            if platform is Platform.ANDROID or platform is Platform.BOTH:
                assert 'project successfully prepared (android)' in str(output).lower()
            if platform is Platform.IOS or platform is Platform.BOTH:
                assert 'project successfully prepared (ios)' in str(output).lower()

        def _full_prepare():
            _incremental_prepare()
            if platform is Platform.ANDROID or platform is Platform.BOTH:
                assert 'Successfully prepared plugin tns-core-modules for android.' in output
                assert 'Successfully prepared plugin tns-core-modules-widgets for android.' in output
            if platform is Platform.IOS or platform is Platform.BOTH:
                assert 'Successfully prepared plugin tns-core-modules for ios.' in output
                assert 'Successfully prepared plugin tns-core-modules-widgets for ios.' in output

        if output is not None:
            if prepare is Prepare.SKIP:
                assert 'Skipping prepare.' in output
                assert 'Preparing project...' not in output
            if prepare is Prepare.INCREMENTAL:
                _incremental_prepare()
                assert 'Successfully prepared plugin tns-core-modules for' not in output
                assert 'Successfully prepared plugin tns-core-modules-widgets for' not in output
            if prepare is Prepare.FULL:
                _full_prepare()
                assert 'Installing' not in output
                assert 'Project successfully created' not in output
            if prepare is Prepare.FIRST_TIME:
                _full_prepare()
                if platform is Platform.ANDROID or platform is Platform.BOTH:
                    assert 'Platform android successfully added' in output
                if platform is Platform.IOS or platform is Platform.BOTH:
                    assert 'Platform ios successfully added' in output
                assert 'Project successfully created' not in output

        if platform is Platform.ANDROID or platform is Platform.BOTH:
            app_path = os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
            modules_path = os.path.join(app_name, TnsAsserts.PLATFORM_ANDROID_TNS_MODULES_PATH)
            assert File.exists(os.path.join(app_path, 'main-view-model.js')), \
                'Application files does not exists in platforms folder.'
            assert File.exists(os.path.join(modules_path, 'application', 'application.js')), \
                'Modules does not exists in platforms folder.'
            assert File.exists(os.path.join(modules_path, 'xml', 'xml.js')), \
                'TNS Modules does not exists in platforms folder.'
            assert not File.exists(os.path.join(modules_path, 'application', 'application.android.js')), \
                'Prepare does not strip \'android\' from name of js files.'
            assert not File.exists(os.path.join(modules_path, 'application', 'application.ios.js')), \
                'Prepare does not skip \'ios\' specific js files.'

        if platform is Platform.IOS or platform is Platform.BOTH:
            app_path = TnsAsserts._get_ios_app_path(app_name)
            modules_path = TnsAsserts._get_ios_modules_path(app_name)
            assert File.exists(os.path.join(app_path, 'main-view-model.js')), \
                'Application files does not exists in platforms folder.'
            assert File.exists(os.path.join(modules_path, 'application', 'application.js')), \
                'Modules does not exists in platforms folder.'
            assert not File.exists(os.path.join(modules_path, 'application', 'application.android.js')), \
                'Prepare does not skip \'ios\' specific js files.'
            assert not File.exists(os.path.join(modules_path, 'application', 'application.ios.js')), \
                'Prepare does not strip \'ios\' from name of js files.'

    @staticmethod
    def can_not_find_device(output):
        """
        Assert output for invalid device.
        :param output: Output of tns command
        """
        assert "Could not find device by specified identifier" in output
        assert "To list currently connected devices and verify that the specified identifier exists" in output

    @staticmethod
    def invalid_device(output):
        """
        Assert output for invalid device.
        :param output: Output of tns command
        """

        assert "Searching for devices..." in output
        assert "Cannot find connected devices" in output
        assert "No emulator image available for device identifier" in output or \
               "No simulator image available for device identifier " in output
        assert "To list available emulator images, run 'tns device <Platform> --available-devices'" in output or \
               "To list available simulator images, run 'tns device <Platform> --available-devices" in output
        assert "To list currently connected devices and verify that the specified identifier exists, run 'tns device'" \
               in output
