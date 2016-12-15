"""
Verifications for NativeScript projects.
"""

from core.osutils.file import File


class TnsVerifications(object):
    PLATFORM_ANDROID_APP_PATH = "/platforms/android/src/main/assets/app/"
    PLATFORM_ANDROID_NPM_MODULES_PATH = PLATFORM_ANDROID_APP_PATH + "tns_modules/"
    PLATFORM_ANDROID_TNS_MODULES_PATH = PLATFORM_ANDROID_NPM_MODULES_PATH + "tns-core-modules/"

    @staticmethod
    def get_ios_app_path(app_name):
        normalized_app_name = app_name.replace(' ', '')
        normalized_app_name = normalized_app_name.replace('-', '')
        normalized_app_name = normalized_app_name.replace('_', '')
        return app_name + '/platforms/ios/' + normalized_app_name + '/app/'

    @staticmethod
    def get_ios_modules_path(app_name):
        modules_path = TnsVerifications.get_ios_app_path(app_name) + 'tns_modules/tns-core-modules/'
        return modules_path

    @staticmethod
    def prepared_android(app_name):
        assert File.exists(app_name + TnsVerifications.PLATFORM_ANDROID_APP_PATH + 'main-view-model.js')
        assert File.exists(app_name + TnsVerifications.PLATFORM_ANDROID_TNS_MODULES_PATH + 'application/application.js')
        assert File.exists(app_name + TnsVerifications.PLATFORM_ANDROID_TNS_MODULES_PATH + 'xml/xml.js')
        assert not File.exists(
            app_name + TnsVerifications.PLATFORM_ANDROID_TNS_MODULES_PATH + "application/application.android.js")
        assert not File.exists(
            app_name + TnsVerifications.PLATFORM_ANDROID_TNS_MODULES_PATH + 'application/application.ios.js')

    @staticmethod
    def prepared_ios(app_name):
        app_path = TnsVerifications.get_ios_app_path(app_name)
        modules_path = TnsVerifications.get_ios_modules_path(app_name)
        assert File.exists(app_path + 'main-view-model.js')
        assert File.exists(modules_path + 'application/application.js')
        assert not File.exists(modules_path + 'application/application.android.js')
        assert not File.exists(modules_path + 'application/application.ios.js')
