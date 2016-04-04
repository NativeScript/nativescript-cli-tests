"""
Test for create command
"""
import unittest

from nose_parameterized import parameterized

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH
from core.tns.tns import Tns


class Create(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Folder.cleanup('./app')
        Folder.cleanup('./123')
        Folder.cleanup('./folder')
        Folder.cleanup('./tns-app')
        Folder.cleanup('./TNS App')

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')
        Folder.cleanup('./template')

    def tearDown(self):
        Folder.cleanup('./TNS_App')
        Folder.cleanup('./template')

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./app')
        Folder.cleanup('./123')
        Folder.cleanup('./folder')
        Folder.cleanup('./tns-app')
        Folder.cleanup('./TNS App')

    def test_001_create_app(self):
        Tns.create_app(app_name="TNS_App")

        assert Folder.is_empty("TNS_App/platforms")
        assert not Folder.exists("TNS_App/app/tns_modules")

        output = run("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        assert "\"tns-core-modules\": " in output

        assert File.exists("TNS_App/node_modules/tns-core-modules/package.json")
        assert File.exists("TNS_App/node_modules/tns-core-modules/LICENSE")
        assert File.exists("TNS_App/node_modules/tns-core-modules/xml/xml.js")

        assert File.list_of_files_exists("TNS_App", "template_javascript_files_1.2.0.txt")

    def test_002_create_project_with_path(self):
        Tns.create_app(app_name="TNS_App", path='folder/subfolder/', assert_success=False, update_modules=False)

        assert Folder.is_empty("folder/subfolder/TNS_App/platforms")
        assert not Folder.exists("folder/subfolder/TNS_App/app/tns_modules")

        output = run("cat folder/subfolder/TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        assert "\"tns-core-modules\": " in output

        assert File.exists(
                "folder/subfolder/TNS_App/node_modules/tns-core-modules/package.json")
        assert File.exists(
                "folder/subfolder/TNS_App/node_modules/tns-core-modules/LICENSE")
        assert File.exists(
                "folder/subfolder/TNS_App/node_modules/tns-core-modules/xml/xml.js")

        assert File.list_of_files_exists(
                'folder/subfolder/TNS_App',
                'template_javascript_files_1.2.0.txt')

    def test_003_create_project_with_appid(self):
        Tns.create_app(app_name="TNS_App", app_id="org.nativescript.MyApp")
        output = run("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.MyApp\"" in output

    def test_004_create_project_with_copyfrom(self):
        # Create initial template project
        Tns.create_app(app_name="template")

        # Modify some files in template project
        File.replace("template/app/LICENSE", "Telerik", "T3l3r1k")

        # Create new project based on first one
        Tns.create_app(app_name="TNS_App", copy_from="template/app")

        # Verify new project corresponds to name of the new project
        output = run("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

        # Verify that content of the new project is based on first project
        output = run("cat TNS_App/app/LICENSE")
        assert "Telerik" not in output
        assert "T3l3r1k" in output

    def test_005_create_project_with_space(self):
        Tns.create_app(app_name="\"TNS App\"")
        output = run("cat \"TNS App/package.json\"")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

    def test_006_create_project_with_dash(self):
        Tns.create_app(app_name="tns-app", assert_success=False)
        output = run("cat \"tns-app/package.json\"")
        assert "\"id\": \"org.nativescript.tnsapp\"" in output

    def test_007_create_project_named_123(self):
        output = run(TNS_PATH + " create 123 --force")
        assert "Project 123 was successfully created" in output

        output = run("cat 123/package.json")
        assert "\"id\": \"org.nativescript.the123\"" in output

    def test_008_create_project_named_app(self):
        output = run(TNS_PATH + " create app --force")
        assert "Project app was successfully created" in output

        output = run("cat app/package.json")
        assert "\"id\": \"org.nativescript.app\"" in output

    @parameterized.expand([
        "tns-template-hello-world",
        "tns-template-hello-world-ts",
        "https://github.com/NativeScript/template-hello-world-ts/tarball/master",
        "https://github.com/NativeScript/template-hello-world-ts.git",
        "https://github.com/NativeScript/template-hello-world-ts.git#master",
        "typescript",
        "tsc",
    ])
    def test_100_create_project_with_template(self, template_source):
        Tns.create_app(app_name="TNS_App", template=template_source)
        assert Folder.is_empty("TNS_App/platforms")
        assert not Folder.is_empty("TNS_App/app")
        assert not Folder.exists("TNS_App/app/tns_modules")
        output = run("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

    def test_400_create_project_with_copyfrom_wrong_path(self):
        output = run(TNS_PATH + " create TNS_App --copy-from invalidFolder")
        assert "successfully created" not in output

        assert "The specified path" in output
        assert "doesn't exist. Check that you specified the path correctly and try again" in output

    def test_401_create_project_in_folder_with_existing_project(self):
        Tns.create_app(app_name="TNS_App")
        output = run(TNS_PATH + " create TNS_App")
        assert "successfully created" not in output
        assert "Path already exists and is not empty" in output

    def test_402_create_project_with_wrong_copy_from_command(self):
        # Create initial template project
        Tns.create_app(app_name="template")

        output = run(TNS_PATH + " create TNS_App -copy-from template")
        assert "successfully created" not in output
        assert "To see command's options, use '$ tns help create'" in output

    def test_403_create_project_with_no_name(self):
        output = run(TNS_PATH + " create")
        assert "You need to provide all the required parameters." in output
        assert "# create" in output
