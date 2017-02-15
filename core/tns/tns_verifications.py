"""
Verifications for NativeScript projects.
"""

from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS
from core.tns.tns_installed_platforms import Platforms
from core.tns.tns_prepare_type import Prepare


class TnsAsserts(object):
    PLATFORM_IOS = "/platforms/ios/"
    PLATFORM_ANDROID = "/platforms/android/"
    PLATFORM_ANDROID_APP_PATH = PLATFORM_ANDROID + "src/main/assets/app/"
    PLATFORM_ANDROID_NPM_MODULES_PATH = PLATFORM_ANDROID_APP_PATH + "tns_modules/"
    PLATFORM_ANDROID_TNS_MODULES_PATH = PLATFORM_ANDROID_NPM_MODULES_PATH + "tns-core-modules/"

    @staticmethod
    def __get_ios_app_path(app_name):
        normalized_app_name = app_name.replace(' ', '')
        normalized_app_name = normalized_app_name.replace('-', '')
        normalized_app_name = normalized_app_name.replace('_', '')
        return app_name + TnsAsserts.PLATFORM_IOS + normalized_app_name + '/app/'

    @staticmethod
    def __get_ios_modules_path(app_name):
        modules_path = TnsAsserts.__get_ios_app_path(app_name) + 'tns_modules/tns-core-modules/'
        return modules_path

    @staticmethod
    def created(app_name, output=None):
        if output is not None:
            assert "nativescript-theme-core" in output
            assert "nativescript-dev-android-snapshot" in output
            assert "Project {0} was successfully created".format(app_name.rsplit('/')[-1]) in output
        assert File.exists(app_name)
        assert File.exists(app_name + "/node_modules/tns-core-modules/package.json")
        assert File.exists(app_name + "/node_modules/tns-core-modules/LICENSE")
        assert File.exists(app_name + "/node_modules/tns-core-modules/xml/xml.js")
        assert Folder.is_empty(app_name + "/platforms")

        app_id = app_name.replace(" ", "").replace("_", "").replace("-", "").rsplit('/')[-1]
        strings = ["org.nativescript.{0}".format(app_id), "tns-core-modules", "nativescript-theme-core",
                   "nativescript-dev-android-snapshot"]
        TnsAsserts.package_json_contains(app_name, string_list=strings)

    @staticmethod
    def platform_added(app_name, platform=Platforms.NONE, output=None):
        """
        Assert platform is added.
        :param app_name: Application name (folder where app is located).
        :param platform: Platforms that should be available.
        :param output: output of `tns platform add` command
        """

        # Verify console output is correct
        if output is not None:
            if platform is Platforms.ANDROID:
                assert "tns-android" in output
            if platform is Platforms.IOS:
                assert "tns-ios" in output
            assert "Copying template files..." in output
            assert "Project successfully created." in output

        # This is to handle test for app with space.
        # In this case we put app name inside "".
        app_name = app_name.replace("\"", "")

        # Verify file and folder content
        if platform is Platforms.NONE:
            assert not File.exists(app_name + TnsAsserts.PLATFORM_ANDROID)
            assert not File.exists(app_name + TnsAsserts.PLATFORM_IOS)
        if platform is Platforms.ANDROID:
            assert not File.exists(app_name + TnsAsserts.PLATFORM_IOS)
            assert File.exists(app_name + TnsAsserts.PLATFORM_ANDROID)
            assert not Folder.is_empty(
                    app_name + TnsAsserts.PLATFORM_ANDROID + "/build-tools/android-static-binding-generator")
        if platform is Platforms.IOS:
            assert not File.exists(app_name + TnsAsserts.PLATFORM_ANDROID)
            assert File.exists(app_name + TnsAsserts.PLATFORM_IOS)
        if platform is Platforms.BOTH:
            assert File.exists(app_name + TnsAsserts.PLATFORM_ANDROID)
            assert File.exists(app_name + TnsAsserts.PLATFORM_IOS)

    @staticmethod
    def platform_list_status(app_name, output=None, prepared=Platforms.NONE, added=Platforms.NONE):
        if output is not None:
            # Assert prepare status
            if prepared is Platforms.NONE:
                if added is Platforms.NONE:
                    assert "The project is not prepared for" not in output
                else:
                    assert "The project is not prepared for any platform" in output
            if prepared is Platforms.ANDROID:
                assert "The project is prepared for:  android" in output
            if prepared is Platforms.IOS:
                assert "The project is prepared for:  ios" in output
            if prepared is Platforms.BOTH:
                assert "The project is prepared for:  ios and android" in output

            # Assert platform added status
            if added is Platforms.NONE:
                assert "No installed platforms found. Use $ tns platform add" in output
                if CURRENT_OS is OSType.OSX:
                    assert "Available platforms for this OS:  ios and android" in output
                else:
                    assert "Available platforms for this OS:  android" in output
            if added is Platforms.ANDROID:
                assert "Installed platforms:  android" in output
            if added is Platforms.IOS:
                assert "Installed platforms:  ios" in output
            if added is Platforms.BOTH:
                assert "Installed platforms:  android and ios" in output

    @staticmethod
    def package_json_contains(app_name, string_list=None):
        package_json_path = app_name + "/package.json"
        output = File.read(package_json_path)
        for item in string_list:
            if item in output:
                print "{0} found in {1}.".format(item, package_json_path)
            else:
                print "pacakge.json:"
                print output
                assert False, "{0} NOT found in {1}.".format(item, package_json_path)

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
