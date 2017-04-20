"""
Tests for prepare command in context of Android
"""
import os
import time

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, TEST_RUN_HOME
from core.tns.replace_helper import ReplaceHelper
from core.tns.tns import Tns
from core.tns.tns_platform_type import Platform
from core.tns.tns_prepare_type import Prepare
from core.tns.tns_verifications import TnsAsserts


class PrepareAndroidTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)

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
        TnsAsserts.prepared(self.app_name, platform=Platform.ANDROID, output=output, prepare=Prepare.FIRST_TIME)
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
        app_path = self.app_name + TnsAsserts.PLATFORM_ANDROID_APP_PATH
        assert File.exists(app_path + 'app-new.js')
        assert File.exists(app_path + 'app-new.css')
        assert File.exists(app_path + 'main-page-new.xml')

        # Verify old files are removed from folder
        assert not File.exists(app_path + 'app.js')
        assert not File.exists(app_path + 'app.css')
        assert not File.exists(app_path + 'main-page.xml')

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
        app_path = self.app_name + TnsAsserts.PLATFORM_ANDROID_APP_PATH
        assert File.exists(app_path + 'app.css')
        assert File.exists(app_path + 'app.js')
        assert File.exists(app_path + 'appandroid.js')
        assert File.exists(app_path + 'appios.js')
        assert File.exists(app_path + 'android.js')
        assert File.exists(app_path + 'ios.js')
        assert not File.exists(app_path + 'app.ios.css')
        assert not File.exists(app_path + 'app.android.css')

    def test_310_prepare_should_flatten_scoped_dependencies(self):
        Tns.create_app_ng(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        Tns.prepare_android(attributes={"--path": self.app_name})

        # Verify scoped dependencies are flattened (verify #1783 is fixed)
        ng_path_in_platforms_folder = self.app_name + TnsAsserts.PLATFORM_ANDROID_NPM_MODULES_PATH + '@angular/core'
        assert File.exists(ng_path_in_platforms_folder), "Scoped dependencies are flattened, please see #1783!"

    def test_400_prepare_missing_or_missing_platform(self):
        Tns.create_app(self.app_name, update_modules=False)

        output = Tns.run_tns_command("prepare", attributes={"--path": self.app_name})
        assert "No platform specified." in output

        output = Tns.run_tns_command("prepare windows", attributes={"--path": self.app_name})
        assert "Invalid platform windows. Valid platforms are ios or android." in output
