"""
Tests for prepare command in context of Android
"""
import os

from core.base_class.BaseClass import BaseClass
from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, TEST_RUN_HOME
from core.tns.tns import Tns


class PrepareAndroidTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def test_001_prepare_android(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

        Tns.prepare_android(attributes={"--path": self.app_name})

        # Verify app and modules are processed and available in platform folder
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-view-model.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                           'application/application.js')
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/"
                                               "application/application.android.js")
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                               'application/application.ios.js')

    def test_002_prepare_android_inside_project(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Folder.navigate_to(self.app_name)
        output = Tns.prepare_android(tns_path=os.path.join("..", TNS_PATH), assert_success=False)
        Folder.navigate_to(TEST_RUN_HOME, relative_from_current_folder=False)
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-view-model.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                           'application/application.js')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                               'application/application.android.js')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                               'application/application.ios.js')

    def test_200_prepare_android_patform_not_added(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/xml/xml.js')

    def test_201_prepare_xml_error(self):
        Tns.create_app(self.app_name, update_modules=False)
        File.replace(self.app_name + "/app/main-page.xml", "</Page>", "</Page")
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "main-page.xml has syntax errors." in output
        assert "unclosed xml attribute" in output

    def test_300_prepare_android_remove_old_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.prepare_android(attributes={"--path": self.app_name})
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.css')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-page.xml')

        run("mv " + self.app_name + "/app/app.js " + self.app_name + "/app/app-new.js")
        run("mv " + self.app_name + "/app/app.css " + self.app_name + "/app/app-new.css")
        run("mv " + self.app_name + "/app/main-page.xml " + self.app_name + "/app/main-page-new.xml")

        Tns.prepare_android(attributes={"--path": self.app_name})
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app-new.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app-new.css')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-page-new.xml')

        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.js')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.css')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-page.xml')

    def test_301_prepare_android_platform_specific_files(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.prepare_android(attributes={"--path": self.app_name})
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.css')

        run("cp " + self.app_name + "/app/app.js " + self.app_name + "/app/app.ios.js")
        run("cp " + self.app_name + "/app/app.js " + self.app_name + "/app/app.android.js")
        run("cp " + self.app_name + "/app/app.js " + self.app_name + "/app/appios.js")
        run("cp " + self.app_name + "/app/app.js " + self.app_name + "/app/appandroid.js")
        run("cp " + self.app_name + "/app/app.js " + self.app_name + "/app/ios.js")
        run("cp " + self.app_name + "/app/app.js " + self.app_name + "/app/android.js")
        run("cp " + self.app_name + "/app/app.css " + self.app_name + "/app/app.ios.css")
        run("cp " + self.app_name + "/app/app.css " + self.app_name + "/app/app.android.css")
        run("mv " + self.app_name + "/app/app.js " + self.app_name + "/app/appNew.js")
        run("mv " + self.app_name + "/app/app.css " + self.app_name + "/app/appNew.css")

        Tns.prepare_android(attributes={"--path": self.app_name})
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.css')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/appandroid.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/appios.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/android.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/ios.js')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.ios.css')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.android.css')

    @unittest.skip("Ignored because of https://github.com/NativeScript/nativescript-cli/issues/2177")
    def test_310_prepare_should_flatten_scoped_dependencies(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

        Tns.plugin_add("nativescript-angular", attributes={"--path": self.app_name})
        Tns.prepare_android(attributes={"--path": self.app_name})

        # Verify scoped dependencies are flattened (see #1783)
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/@angular/core')

    def test_400_prepare_missing_platform(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.run_tns_command("prepare", attributes={"--path": self.app_name})
        assert "You need to provide all the required parameters." in output

    def test_401_prepare_invalid_platform(self):
        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.run_tns_command("prepare windows", attributes={"--path": self.app_name})
        assert "Invalid platform windows. Valid platforms are ios or android." in output
