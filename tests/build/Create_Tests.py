"""
Test for create command
"""
import os

from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.tns.tns import Tns


class CreateTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        super(CreateTests, cls).setUpClass()
        Folder.cleanup('folder')

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)
        Folder.cleanup(self.app_template)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)
        Folder.cleanup(self.app_template)

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup(cls.app_name_app)
        Folder.cleanup(cls.app_name_123)
        Folder.cleanup('folder')
        Folder.cleanup(cls.app_name_dash)
        Folder.cleanup(cls.app_name_space)

    def test_001_create_app(self):
        Tns.create_app(self.app_name, update_modules=False)
        assert Folder.is_empty(self.app_name + "/platforms")
        assert not Folder.exists(self.app_name + "/app/tns_modules")

        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        assert "\"tns-core-modules\": " in output

        assert File.exists(self.app_name + "/node_modules/tns-core-modules/package.json")
        assert File.exists(self.app_name + "/node_modules/tns-core-modules/LICENSE")
        assert File.exists(self.app_name + "/node_modules/tns-core-modules/xml/xml.js")

    def test_002_create_project_with_path(self):
        Tns.create_app(self.app_name, attributes={"--path": "folder/subfolder/"},
                       assert_success=False, update_modules=False)

        assert Folder.is_empty("folder/subfolder/" + self.app_name + "/platforms")
        assert not Folder.exists("folder/subfolder/" + self.app_name + "/app/tns_modules")

        output = File.read("folder/subfolder/" + self.app_name + "/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        assert "\"tns-core-modules\": " in output

        assert File.exists("folder/subfolder/" + self.app_name + "/node_modules/tns-core-modules/package.json")
        assert File.exists("folder/subfolder/" + self.app_name + "/node_modules/tns-core-modules/LICENSE")
        assert File.exists("folder/subfolder/" + self.app_name + "/node_modules/tns-core-modules/xml/xml.js")

    def test_003_create_project_with_appid(self):
        Tns.create_app(self.app_name, attributes={"--appid": "org.nativescript.MyApp"}, update_modules=False)
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.MyApp\"" in output

    def test_004_create_project_with_copyfrom(self):
        Tns.create_app(self.app_template, update_modules=False)
        File.replace(self.app_template + "/app/LICENSE", "Telerik", "T3l3r1k")
        Tns.create_app(self.app_name, attributes={"--copy-from": self.app_template + "/app"}, update_modules=False)
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        output = File.read(self.app_name + os.sep + "/app/LICENSE")
        assert "Telerik" not in output
        assert "T3l3r1k" in output

    def test_005_create_project_with_space(self):
        Tns.create_app(self.app_name_space, update_modules=False)
        output = File.read(self.app_name_space + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

    def test_006_create_project_with_dash(self):
        Tns.create_app(self.app_name_dash, assert_success=False, update_modules=False)
        output = File.read(self.app_name_dash + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.tnsapp\"" in output

    def test_007_create_project_named_123(self):
        output = Tns.create_app(self.app_name_123, attributes={"--force": ""}, update_modules=False)
        assert "Project " + self.app_name_123 + " was successfully created" in output

        output = File.read(self.app_name_123 + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.the123\"" in output

        output = Tns.create_app(self.app_name_123, assert_success=False, update_modules=False)
        assert "The project name does not start with letter and will fail to build for Android." in output

    def test_008_create_project_named_app(self):
        output = Tns.create_app(self.app_name_app, attributes={"--force": ""}, update_modules=False)
        assert "Project " + self.app_name_app + " was successfully created" in output

        output = File.read(self.app_name_app + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.app\"" in output

        output = Tns.create_app(self.app_name_app, assert_success=False, update_modules=False)
        assert "You cannot build applications named '" + self.app_name_app + "' in Xcode." in output

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
        Tns.create_app(self.app_name, attributes={"--template": template_source}, update_modules=False)
        assert Folder.is_empty(self.app_name + "/platforms")
        assert not Folder.is_empty(self.app_name + "/app")
        assert not Folder.exists(self.app_name + "/app/tns_modules")
        output = File.read(self.app_name + os.sep + "package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

    def test_400_create_project_with_copyfrom_wrong_path(self):
        output = Tns.create_app(self.app_name, attributes={"--copy-from": "invalidFolder"},
                                assert_success=False, update_modules=False)
        assert "successfully created" not in output
        assert "The specified path" in output
        assert "Check that you specified the path correctly and try again" in output

    def test_401_create_project_in_folder_with_existing_project(self):
        Tns.create_app(self.app_name, assert_success=False, update_modules=False)
        output = Tns.create_app(app_name=self.app_name, assert_success=False, update_modules=False)
        assert "successfully created" not in output
        assert "Path already exists and is not empty" in output

    def test_402_create_project_with_wrong_copy_from_command(self):
        Tns.create_app(self.app_template, update_modules=False)
        output = Tns.create_app(self.app_name, attributes={"-copy-from": self.app_template},
                                assert_success=False, update_modules=False)
        assert "successfully created" not in output
        assert "To see command's options, use '$ tns help create'" in output

    def test_403_create_project_with_no_name(self):
        output = Tns.run_tns_command("create ")
        assert "You need to provide all the required parameters." in output
        assert "# create" in output
