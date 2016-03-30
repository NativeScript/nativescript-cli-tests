import unittest

from nose_parameterized import parameterized

from core.osutils.command import run
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH
from core.tns.tns import Tns


class CreateNG(unittest.TestCase):

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        Folder.cleanup('./TNS_App')

    def assert_angular_project(self):
        output = run("cat TNS_App/package.json")
        assert "nativescript-angular" in output
        assert "tns-core-modules" in output
        assert "nativescript-dev-typescript" in output

        assert Folder.exists("TNS_App/node_modules/angular2")
        assert Folder.exists("TNS_App/node_modules/nativescript-angular")
        assert Folder.exists("TNS_App/node_modules/nativescript-dev-typescript")
        assert Folder.exists("TNS_App/node_modules/tns-core-modules")

        assert Folder.exists("TNS_App/hooks")
        assert Folder.exists("TNS_App/app/App_Resources")

    def test_101_create_ng_project(self):
        output = run(TNS_PATH + " create TNS_App --ng")
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
        Tns.create_app(app_name="TNS_App", template=template_source)
        self.assert_angular_project()

    def test_401_create_project_with_template_no_value(self):
        output = run(TNS_PATH + " create TNS_App --template")
        assert "successfully created" not in output
        assert "requires non-empty value" in output

    def test_402_create_project_with_template_and_ng(self):
        output = run(TNS_PATH + " create TNS_App --template --ng")
        assert "successfully created" not in output
        assert "requires non-empty value" in output
