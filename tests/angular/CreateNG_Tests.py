from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.osutils.folder import Folder
from core.tns.tns import Tns


class CreateNGTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)

    def assert_angular_project(self):
        output = File.read(self.app_name + "/package.json")
        assert "nativescript-angular" in output
        assert "tns-core-modules" in output
        assert "nativescript-dev-typescript" in output

        assert Folder.exists(self.app_name + "/node_modules/nativescript-angular")
        assert Folder.exists(self.app_name + "/node_modules/nativescript-dev-typescript")
        assert Folder.exists(self.app_name + "/node_modules/tns-core-modules")

        assert Folder.exists(self.app_name + "/hooks")
        assert Folder.exists(self.app_name + "/app/App_Resources")

    def test_101_create_ng_project(self):
        output = Tns.create_app_ng(self.app_name, update_modules=False)
        assert "successfully created" in output
        self.assert_angular_project()
        assert not File.exists("TNS_App/app/LICENSE")

    @parameterized.expand([
        "tns-template-hello-world-ng",
        "https://github.com/NativeScript/template-hello-world-ng.git",
        "angular",
        "ng",
    ])
    def test_102_create_project_with_template_ng(self, template_source):
        Tns.create_app(self.app_name, attributes={"--template": template_source}, assert_success=False,
                       update_modules=False)
        self.assert_angular_project()

    def test_401_create_project_with_template_no_value(self):
        output = Tns.create_app(self.app_name, attributes={"--template": ""}, assert_success=False,
                                update_modules=False)
        assert "successfully created" not in output
        assert "requires non-empty value" in output

    def test_402_create_project_with_template_and_ng(self):
        output = Tns.create_app(self.app_name, attributes={"--template": "--ng"}, assert_success=False,
                                update_modules=False)
        assert "successfully created" not in output
        assert "requires non-empty value" in output
