"""
Tests for prepare command in context of Android
"""
import os
import time
import unittest

from core.base_class.BaseClass import BaseClass
from core.git.git import Git
from core.npm.npm import Npm
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, TEST_RUN_HOME, CURRENT_OS
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class PrepareAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def setUp(self):
        BaseClass.setUp(self)
        Folder.navigate_to(folder=TEST_RUN_HOME, relative_from_current_folder=False)

    def test_101_prepare_android(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})

        # Initial prepare should be full.
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.FULL)

        # If no file is touched next time prepare should be skipped at all.
        output = Tns.prepare_android(attributes={"--path": self.app_name}, assert_success=False)
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.SKIP)

        # If some JS/CSS/XML is changed incremental prepare should be done.
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_JS)
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.INCREMENTAL)

    def test_102_prepare_android_inside_project(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Folder.navigate_to(self.app_name)
        output = Tns.prepare_android(tns_path=os.path.join("..", TNS_PATH), assert_success=False)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.FULL)

    def test_200_prepare_android_platform_not_added(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.FIRST_TIME)

    def test_201_prepare_xml_error(self):
        Tns.create_app(self.app_name, update_modules=False)
        ReplaceHelper.replace(self.app_name, ReplaceHelper.CHANGE_XML_INVALID_SYNTAX)
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "main-page.xml has syntax errors." in output
        assert "unclosed xml attribute" in output

    def test_300_prepare_android_remove_old_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.prepare_android(attributes={"--path": self.app_name})

        # Add new files and delete old files
        time.sleep(1)
        File.copy(self.app_name + "/app/app.js", self.app_name + "/app/app-new.js")
        File.copy(self.app_name + "/app/app.css", self.app_name + "/app/app-new.css")
        File.copy(self.app_name + "/app/main-page.xml", self.app_name + "/app/main-page-new.xml")
        File.remove(self.app_name + "/app/app.js")
        File.remove(self.app_name + "/app/app.css")
        File.remove(self.app_name + "/app/main-page.xml")

        Tns.prepare_android(attributes={"--path": self.app_name})

        # Verify new files are in available in platforms folder
        app_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        assert File.exists(os.path.join(app_path, 'app-new.js'))
        assert File.exists(os.path.join(app_path, 'app-new.css'))
        assert File.exists(os.path.join(app_path, 'main-page-new.xml'))

        # Verify old files are removed from folder
        assert not File.exists(os.path.join(app_path, 'app.js'))
        assert not File.exists(os.path.join(app_path, 'app.css'))
        assert not File.exists(os.path.join(app_path, 'main-page.xml'))

    def test_301_prepare_android_platform_specific_files(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.prepare_android(attributes={"--path": self.app_name})

        # Add set of platform specific files
        File.copy(self.app_name + "/app/app.js", self.app_name + "/app/app.ios.js")
        File.copy(self.app_name + "/app/app.js", self.app_name + "/app/app.android.js")
        File.copy(self.app_name + "/app/app.js", self.app_name + "/app/appios.js")
        File.copy(self.app_name + "/app/app.js", self.app_name + "/app/appandroid.js")
        File.copy(self.app_name + "/app/app.js", self.app_name + "/app/ios.js")
        File.copy(self.app_name + "/app/app.js", self.app_name + "/app/android.js")

        File.copy(self.app_name + "/app/app.css", self.app_name + "/app/app.ios.css")
        File.copy(self.app_name + "/app/app.css", self.app_name + "/app/app.android.css")
        File.copy(self.app_name + "/app/app.js", self.app_name + "/app/appNew.js")
        File.copy(self.app_name + "/app/app.css", self.app_name + "/app/appNew.css")
        File.remove(self.app_name + "/app/app.js")
        File.remove(self.app_name + "/app/app.css")

        Tns.prepare_android(attributes={"--path": self.app_name})

        # Verify new files are in available in platforms folder
        app_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_APP_PATH)
        assert File.exists(os.path.join(app_path, 'app.css'))
        assert File.exists(os.path.join(app_path, 'app.js'))
        assert File.exists(os.path.join(app_path, 'appandroid.js'))
        assert File.exists(os.path.join(app_path, 'appios.js'))
        assert File.exists(os.path.join(app_path, 'android.js'))
        assert File.exists(os.path.join(app_path, 'ios.js'))
        assert not File.exists(os.path.join(app_path, 'app.ios.css'))
        assert not File.exists(os.path.join(app_path, 'app.android.css'))

    def test_310_prepare_should_flatten_scoped_dependencies(self):
        Tns.create_app_ng(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.prepare_android(attributes={"--path": self.app_name})

        # Verify scoped dependencies are flattened (verify #1783 is fixed)
        ng_path = os.path.join(self.app_name, TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH, '@angular', 'core')
        assert File.exists(ng_path), "Scoped dependencies are flattened, please see #1783!"

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Skip on Windows")
    def test_320_prepare_scoped_plugins(self):
        """
        Test for https://github.com/NativeScript/nativescript-cli/pull/3080

        Before this change we copied all NG components at following location (js demo of nativescript-facebook):
        platforms/android/src/main/assets/app/tns_modules/nativescript-facebook/node_modules/@angular

        Now folder above should be empty (or not existing at all).
        """

        Folder.cleanup("nativescript-facebook")
        Git.clone_repo(repo_url='git@github.com:NativeScript/nativescript-facebook.git',
                       local_folder="nativescript-facebook")
        Folder.navigate_to(folder="nativescript-facebook/src")
        output = run(command="npm run build")
        Folder.navigate_to(folder=TEST_RUN_HOME, relative_from_current_folder=False)
        assert "tsc" in output
        assert "ERR" not in output
        Tns.prepare_android(attributes={"--path": "nativescript-facebook/demo"})
        output = run(command="find nativescript-facebook/demo/platforms/android/ | grep @")
        assert "@angular/core" not in output, "@angular/* should not be in platforms folder."
        assert "@angular/router" not in output, "@angular/* should not be in platforms folder."

    def test_330_prepare_android_next(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name}, version="next")
        Folder.cleanup(os.path.join(self.app_name, "node_modules"))
        Folder.cleanup(os.path.join(self.app_name, "platforms"))
        android_version = Npm.get_version("tns-android@next")
        File.replace(file_path=os.path.join(self.app_name, "package.json"), str1=android_version, str2="next")
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.FIRST_TIME)

    def test_400_prepare_missing_or_missing_platform(self):
        Tns.create_app(self.app_name, update_modules=False)

        output = Tns.run_tns_command("prepare", attributes={"--path": self.app_name})
        assert "No platform specified." in output

        output = Tns.run_tns_command("prepare windows", attributes={"--path": self.app_name})
        assert "Invalid platform windows. Valid platforms are ios or android." in output

    @unittest.skipIf(CURRENT_OS == OSType.LINUX, "Skip on Linux")
    def test_401_prepare_project_with_many_dependencies(self):
        """
        Test for https://github.com/NativeScript/nativescript-cli/issues/2561
        """
        Tns.create_app_ng(app_name=self.app_name, template_version="2.5.0", update_modules=False)
        Npm.uninstall(package="tns-core-modules", option="--save-dev", folder=self.app_name)
        Npm.uninstall(package="nativescript-dev-android-snapshot", option="--save-dev", folder=self.app_name)
        Npm.uninstall(package="nativescript-dev-typescript", option="--save-dev", folder=self.app_name)
        Npm.install(package="tns-core-modules@2.5.0", option="--save-dev", folder=self.app_name)
        Npm.install(package="nativescript-dev-typescript@0.3", option="--save-dev", folder=self.app_name)
        Npm.install(package="lodash", option="--save", folder=self.app_name)
        Npm.install(package="moment", option="--save", folder=self.app_name)
        Npm.install(package="nativescript-cardview", option="--save", folder=self.app_name)
        Npm.install(package="nativescript-sqlite", option="--save", folder=self.app_name)
        Npm.install(package="nativescript-statusbar", option="--save", folder=self.app_name)
        Npm.install(package="nativescript-websockets", option="--save", folder=self.app_name)
        Npm.install(package="number-generator", option="--save", folder=self.app_name)
        Npm.install(package="eslint", option="--save", folder=self.app_name)
        Npm.install(package="eslint-plugin-compat", option="--save", folder=self.app_name)
        Tns.platform_add_android(version="2.5.0", attributes={"--path": self.app_name})
        Tns.prepare_android(attributes={"--path": self.app_name}, log_trace=True)
