from nose_parameterized import parameterized

from core.base_class.BaseClass import BaseClass
from core.osutils.folder import Folder
from core.tns.tns import Tns
from core.tns import angular_helper as angular

class CreateNGTests(BaseClass):
    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup(self.app_name)


    @parameterized.expand([
        "tns-template-hello-world-ng",
        "https://github.com/NativeScript/template-hello-world-ng.git",
        "angular",
        "ng",
    ])
    def test_100_create_project_with_template_ng(self, template_source):
        Tns.create_app(self.app_name, attributes={"--template": template_source}, assert_success=False,
                       update_modules=False)
        angular.assert_angular_project(self.app_name)

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
