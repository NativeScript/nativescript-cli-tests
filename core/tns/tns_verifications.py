"""
Verifications for NativeScript projects.
"""

from core.osutils.file import File
from core.tns.tns_installed_platforms import Platforms
from core.tns.tns_prepare_type import Prepare


class TnsAsserts(object):
    PLATFORM_ANDROID_APP_PATH = "/platforms/android/src/main/assets/app/"
    PLATFORM_ANDROID_NPM_MODULES_PATH = PLATFORM_ANDROID_APP_PATH + "tns_modules/"
    PLATFORM_ANDROID_TNS_MODULES_PATH = PLATFORM_ANDROID_NPM_MODULES_PATH + "tns-core-modules/"

    @staticmethod
    def __get_ios_app_path(app_name):
        normalized_app_name = app_name.replace(' ', '')
        normalized_app_name = normalized_app_name.replace('-', '')
        normalized_app_name = normalized_app_name.replace('_', '')
        return app_name + '/platforms/ios/' + normalized_app_name + '/app/'

    @staticmethod
    def __get_ios_modules_path(app_name):
        modules_path = TnsAsserts.__get_ios_app_path(app_name) + 'tns_modules/tns-core-modules/'
        return modules_path

    @staticmethod
    def prepared(app_name, platform=Platforms.BOTH, output=None, prepare_type=Prepare.FULL):

        def _incremental_prepare():
            assert "Skipping prepare." not in output
            assert "Preparing project..." in output
            if platform is Platforms.ANDROID or platform is Platforms.BOTH:
                assert "Project successfully prepared (android)" in output
            if platform is Platforms.IOS or platform is Platforms.BOTH:
                assert "Project successfully prepared (ios)" in output

        def _full_prepare():
            _incremental_prepare()
            if platform is Platforms.ANDROID or platform is Platforms.BOTH:
                assert "Successfully prepared plugin tns-core-modules for android." in output
                assert "Successfully prepared plugin tns-core-modules-widgets for android." in output
            if platform is Platforms.IOS or platform is Platforms.BOTH:
                assert "Successfully prepared plugin tns-core-modules for ios." in output
                assert "Successfully prepared plugin tns-core-modules-widgets for ios." in output

        if output is not None:
            if prepare_type is Prepare.SKIP:
                assert "Skipping prepare." in output
                assert "Preparing project..." not in output
            if prepare_type is Prepare.INCREMENTAL:
                _incremental_prepare()
                assert "Successfully prepared plugin tns-core-modules for" not in output
                assert "Successfully prepared plugin tns-core-modules-widgets for" not in output
            if prepare_type is Prepare.FULL:
                _full_prepare()
                assert "Installing" not in output
                assert "Project successfully created" not in output
            if prepare_type is Prepare.FIRST_TIME:
                _full_prepare()
                assert "Installing" in output
                assert "Project successfully created" in output
                if platform is Platforms.ANDROID or platform is Platforms.BOTH:
                    assert "tns-android" in output
                if platform is Platforms.IOS or platform is Platforms.BOTH:
                    assert "tns-ios" in output

        if platform is Platforms.ANDROID or platform is Platforms.BOTH:
            app_path = app_name + TnsAsserts.PLATFORM_ANDROID_APP_PATH
            modules_path = app_name + TnsAsserts.PLATFORM_ANDROID_TNS_MODULES_PATH
            assert File.exists(app_path + 'main-view-model.js'), \
                "Application files does not exists in platforms folder."
            assert File.exists(modules_path + 'application/application.js'), \
                "Modules does not exists in platforms folder."
            assert File.exists(modules_path + 'xml/xml.js'), "TNS Modules does not exists in platforms folder."
            assert not File.exists(modules_path + "application/application.android.js"), \
                "Prepare does not strip 'android' from name of js files."
            assert not File.exists(modules_path + 'application/application.ios.js'), \
                "Prepare does not skip 'ios' specific js files."

        if platform is Platforms.IOS or platform is Platforms.BOTH:
            app_path = TnsAsserts.__get_ios_app_path(app_name)
            modules_path = TnsAsserts.__get_ios_modules_path(app_name)
            assert File.exists(app_path + 'main-view-model.js'), \
                "Application files does not exists in platforms folder."
            assert File.exists(modules_path + 'application/application.js'), \
                "Modules does not exists in platforms folder."
            assert not File.exists(modules_path + 'application/application.android.js'), \
                "Prepare does not skip 'ios' specific js files."
            assert not File.exists(modules_path + 'application/application.ios.js'), \
                "Prepare does not strip 'ios' from name of js files."
