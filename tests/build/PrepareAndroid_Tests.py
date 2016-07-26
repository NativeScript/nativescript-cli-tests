"""
Tests for prepare command in context of Android
"""
import os
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, SUT_ROOT_FOLDER
from core.tns.tns import Tns


class PrepareAndroid_Tests(unittest.TestCase):
    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        Folder.cleanup('./TNS_App')

    def test_001_prepare_android(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        output = run(TNS_PATH + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/main-view-model.js')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.js')
        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
        "application/application.android.js')
        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
        "application/application.ios.js')

    def test_002_prepare_android_inside_project(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) + " prepare android")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/main-view-model.js')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.js')
        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/' +
            'application/application.android.js')
        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.ios.js')

    def test_010_prepare_android_ng_project(self):
        output = run(TNS_PATH + " create TNS_App --ng")
        assert "successfully created" in output
        Tns.platform_add(
            platform="android",
            path="TNS_App",
            framework_path=ANDROID_RUNTIME_PATH)
        Tns.prepare(platform="android", path="TNS_App")

        assert Folder.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/@angular')
        assert Folder.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/nativescript-angular')

    def test_200_prepare_android_patform_not_added(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " prepare android --path TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/tns_modules/xml/xml.js')

    def test_201_prepare_xml_error(self):
        Tns.create_app(app_name="TNS_App")
        File.replace("TNS_App/app/main-page.xml", "</Page>", "</Page")
        output = run(TNS_PATH + " prepare android --path TNS_App")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "main-page.xml has syntax errors." in output
        assert "unclosed xml attribute" in output

    def test_210_prepare_android_tns_core_modules(self):
        Tns.create_app(
            app_name="TNS_App",
            copy_from=SUT_ROOT_FOLDER + "/QA-TestApps/tns-modules-app/app")
        Tns.platform_add(
            platform="android",
            path="TNS_App",
            framework_path=ANDROID_RUNTIME_PATH)

        # Make a change in tns-core-modules to verify they are not overwritten.
        File.replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");",
            "(\"globals\"); // test")

        # Verify tns-core-modules are copied to the native project, not app's
        # tns_modules.
        for i in range(1, 3):
            print "prepare number: " + str(i)

            output = run(TNS_PATH + " prepare android --path TNS_App")
            assert "You have tns_modules dir in your app folder" in output
            assert "Project successfully prepared" in output

            output = run("cat TNS_App/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," in output

            output = run(
                "cat TNS_App/node_modules/tns-core-modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = run(
                "cat TNS_App/node_modules/tns-core-modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

            output = run(
                "cat TNS_App/platforms/android/src/main/assets/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = run(
                "cat TNS_App/platforms/android/src/main/assets/app/" +
                "tns_modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

    def test_300_prepare_android_remove_old_files(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        output = run(TNS_PATH + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output

        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.js')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.css')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/main-page.xml')

        run("mv TNS_App/app/app.js TNS_App/app/app-new.js")
        run("mv TNS_App/app/app.css TNS_App/app/app-new.css")
        run("mv TNS_App/app/main-page.xml TNS_App/app/main-page-new.xml")

        output = run(TNS_PATH + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app-new.js')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app-new.css')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/main-page-new.xml')

        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.js')
        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.css')
        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/main-page.xml')

    def test_301_prepare_android_platform_specific_files(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        output = run(TNS_PATH + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.css')

        run("cp TNS_App/app/app.js TNS_App/app/app.ios.js")
        run("cp TNS_App/app/app.js TNS_App/app/app.android.js")
        run("cp TNS_App/app/app.js TNS_App/app/appios.js")
        run("cp TNS_App/app/app.js TNS_App/app/appandroid.js")
        run("cp TNS_App/app/app.js TNS_App/app/ios.js")
        run("cp TNS_App/app/app.js TNS_App/app/android.js")
        run("cp TNS_App/app/app.css TNS_App/app/app.ios.css")
        run("cp TNS_App/app/app.css TNS_App/app/app.android.css")
        run("mv TNS_App/app/app.js TNS_App/app/appNew.js")
        run("mv TNS_App/app/app.css TNS_App/app/appNew.css")

        output = run(TNS_PATH + " prepare android --path TNS_App")
        assert "Project successfully prepared" in output
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.css')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.js')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/appandroid.js')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/appios.js')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/android.js')
        assert File.exists(
            'TNS_App/platforms/android/src/main/assets/app/ios.js')
        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.ios.css')
        assert not File.exists(
            'TNS_App/platforms/android/src/main/assets/app/app.android.css')

    def test_310_prepare_should_flatten_scoped_dependencies(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        Tns.plugin_add(plugin="nativescript-angular", path="TNS_App")
        Tns.prepare(platform="android", path="TNS_App")

        # Verify scoped dependencies are flattened (see #1783)
        assert File.exists('TNS_App/platforms/android/src/main/assets/app/tns_modules/@angular/core')

    def test_400_prepare_missing_platform(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " prepare --path TNS_App")
        assert "You need to provide all the required parameters." in output

    def test_401_prepare_invalid_platform(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " prepare windows --path TNS_App")
        assert "Invalid platform windows. Valid platforms are ios or android." in output
