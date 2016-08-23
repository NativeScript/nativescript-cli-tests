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
    app_name = "TNS_App"

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./' + self.app_name)

    def tearDown(self):
        Folder.cleanup('./' + self.app_name)

    def test_001_prepare_android(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-view-model.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                           'application/application.js')
        assert not File.exists(self.app_name + "/platforms/android/src/main/assets/app/tns_modules/"
                                               "application/application.android.js")
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                               'application/application.ios.js')

    def test_002_prepare_android_inside_project(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, self.app_name))
        output = Tns.run_tns_command("prepare android", tns_path=os.path.join("..", TNS_PATH))
        os.chdir(current_dir)
        assert "Project successfully prepared" in output

        # Verify app and modules are processed and available in platform folder
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-view-model.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                           'application/application.js')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                               'application/application.android.js')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/'
                                               'application/application.ios.js')

    def test_010_prepare_android_ng_project(self):
        output = Tns.create_app(self.app_name, attributes={"--ng": ""}, assert_success=False)
        assert "successfully created" in output
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.prepare_android(attributes={"--path": self.app_name})

        assert Folder.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/@angular')
        assert Folder.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/nativescript-angular')

    def test_200_prepare_android_patform_not_added(self):
        Tns.create_app(self.app_name)
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/tns_modules/xml/xml.js')

    def test_201_prepare_xml_error(self):
        Tns.create_app(self.app_name)
        File.replace(self.app_name + "/app/main-page.xml", "</Page>", "</Page")
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "main-page.xml has syntax errors." in output
        assert "unclosed xml attribute" in output

    def test_210_prepare_android_tns_core_modules(self):
        Tns.create_app(self.app_name, attributes={"--copy-from": SUT_ROOT_FOLDER + "/QA-TestApps/tns-modules-app/app"})
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

        # Make a change in tns-core-modules to verify they are not overwritten.
        File.replace(self.app_name + "/node_modules/tns-core-modules/application/application-common.js",
                     "(\"globals\");",
                     "(\"globals\"); // test")

        # Verify tns-core-modules are copied to the native project, not app's
        # tns_modules.
        for i in range(1, 3):
            print "prepare number: " + str(i)

            output = Tns.prepare_android(attributes={"--path": self.app_name})
            assert "You have tns_modules dir in your app folder" in output
            assert "Project successfully prepared" in output

            output = run("cat " + self.app_name + "/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," in output

            output = run(
                "cat " + self.app_name + "/node_modules/tns-core-modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = run(
                "cat " + self.app_name + "/node_modules/tns-core-modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

            output = run(
                "cat " + self.app_name + "/platforms/android/src/main/assets/app/tns_modules/package.json")
            assert "\"version\": \"1.2.1\"," not in output
            output = run(
                "cat " + self.app_name + "/platforms/android/src/main/assets/app/" +
                "tns_modules/application/application-common.js")
            assert "require(\"globals\"); // test" in output

    def test_300_prepare_android_remove_old_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })

        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output

        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.css')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-page.xml')

        run("mv " + self.app_name + "/app/app.js " + self.app_name + "/app/app-new.js")
        run("mv " + self.app_name + "/app/app.css " + self.app_name + "/app/app-new.css")
        run("mv " + self.app_name + "/app/main-page.xml " + self.app_name + "/app/main-page-new.xml")

        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app-new.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app-new.css')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-page-new.xml')

        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.js')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.css')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/main-page.xml')

    def test_301_prepare_android_platform_specific_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output
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

        output = Tns.prepare_android(attributes={"--path": self.app_name})
        assert "Project successfully prepared" in output
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.css')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/appandroid.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/appios.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/android.js')
        assert File.exists(self.app_name + '/platforms/android/src/main/assets/app/ios.js')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.ios.css')
        assert not File.exists(self.app_name + '/platforms/android/src/main/assets/app/app.android.css')

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
        Tns.create_app(self.app_name)
        output = Tns.run_tns_command("prepare", attributes={"--path": self.app_name})
        assert "You need to provide all the required parameters." in output

    def test_401_prepare_invalid_platform(self):
        Tns.create_app(self.app_name)
        output = Tns.run_tns_command("prepare windows", attributes={"--path": self.app_name})
        assert "Invalid platform windows. Valid platforms are ios or android." in output
