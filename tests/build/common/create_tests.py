"""
Test for create command
"""
import os
import unittest

from nose_parameterized import parameterized
from core.git.git import Git
from core.base_class.BaseClass import BaseClass
from core.npm.npm import Npm
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.os_type import OSType
from core.settings.settings import TEST_RUN_HOME
from core.tns.tns import Tns
from core.tns.tns_verifications import TnsAsserts
from core.settings.settings import CURRENT_OS


class CreateTests(BaseClass):
    app_name_dash = "tns-app"
    app_name_space = "TNS App"
    app_name_123 = "123"
    app_name_app = "app"

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)
        Folder.cleanup('folder')
        Folder.cleanup(cls.app_name)

    def setUp(self):
        BaseClass.setUp(self)

    def tearDown(self):
        BaseClass.tearDown(self)

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup(cls.app_name_app)
        Folder.cleanup(cls.app_name_123)
        Folder.cleanup('folder')
        Folder.cleanup(cls.app_name_dash)
        Folder.cleanup(cls.app_name_space)
        Folder.cleanup(cls.app_name)

    def test_000_create_app_like_real_user(self):
        """Create app like real user."""

        # Tns.create_app use --template internally.
        # This test case cover the real user scenario.
        output = Tns.run_tns_command("create " + self.app_name)
        TnsAsserts.created(self.app_name, output=output)
        assert "Now you can navigate to your project with $ cd {0}".format(self.app_name) in output
        assert "After that you can run it on device/emulator by executing $ tns run <platform>" in output

    def test_001_create_app(self):
        """Create app with --template and update modules"""
        output = Tns.create_app(self.app_name, update_modules=True)
        TnsAsserts.created(self.app_name, output=output)

    def test_002_create_project_with_path(self):
        """Create project with --path option"""

        output = Tns.create_app(self.app_name, attributes={"--path": "folder/subfolder/"},
                                assert_success=False, update_modules=False)
        app_folder = "folder/subfolder/" + self.app_name
        TnsAsserts.created(app_folder, output=output)

    def test_003_create_project_with_appid(self):
        """Create project with --appid option"""

        output = Tns.create_app(self.app_name, attributes={"--appid": "org.nativescript.MyApp"}, update_modules=False,
                                assert_success=False)
        TnsAsserts.created(app_name=self.app_name, output=output, full_check=False)
        strings = ["\"id\": \"org.nativescript.MyApp\""]
        TnsAsserts.package_json_contains(self.app_name, string_list=strings)

    def test_005_create_project_with_space(self):
        """ Create project with space is possible, but packageId will skip the space symbol"""

        output = Tns.create_app(self.app_name_space, update_modules=True)
        TnsAsserts.created(self.app_name_space, output=output)

    def test_006_create_project_with_dash(self):
        """ Create project with dash is possible, but packageId will skip the dash symbol"""

        output = Tns.create_app(self.app_name_dash, update_modules=True)
        TnsAsserts.created(self.app_name_dash, output=output)

    def test_007_create_project_named_123(self):
        """Create app starting with digits should not be possible without --force option"""

        # --force will allow user to create app named '123', but packageID will be 'org.nativescript.the123'
        output = Tns.create_app(self.app_name_123, attributes={"--force": ""}, update_modules=False,
                                assert_success=False)
        TnsAsserts.created(app_name=self.app_name_123, output=output, full_check=False)
        strings = ["\"id\": \"org.nativescript.the123\""]
        TnsAsserts.package_json_contains(self.app_name_123, string_list=strings)

        # Create project should fail without --force
        output = Tns.create_app(self.app_name_123, assert_success=False, update_modules=False)
        assert "The project name does not start with letter and will fail to build for Android." in output

    def test_008_create_project_named_app(self):
        """Create app named 'app' should not be possible without --force option"""

        # --force will allow user to create app named 'app'
        Tns.create_app(self.app_name_app, attributes={"--force": ""}, update_modules=False)
        strings = ["\"id\": \"org.nativescript.app\""]
        TnsAsserts.package_json_contains(self.app_name_app, string_list=strings)

        # Create project should fail without --force
        output = Tns.create_app(self.app_name_app, assert_success=False, update_modules=False)
        assert "You cannot build applications named '" + self.app_name_app + "' in Xcode." in output

    def test_009_create_app_default(self):
        Folder.cleanup(self.app_name)
        output = Tns.create_app(self.app_name, attributes={"--default": ""}, update_modules=False)
        TnsAsserts.created(self.app_name, output=output)
        assert "Now you can navigate to your project with $ cd {0}".format(self.app_name) in output
        assert "After that you can run it on device/emulator by executing $ tns run <platform>" in output

    @unittest.skipIf(CURRENT_OS == OSType.WINDOWS, "Skip on Windows temporary")
    def test_010_create_app_remove_app_resources(self):
        #creates valid project from local directory template
        Folder.cleanup("template-hello-world")
        Folder.cleanup(self.app_name)
        Git.clone_repo(repo_url='git@github.com:NativeScript/template-hello-world.git',
                       local_folder="template-hello-world")
        Folder.cleanup(os.path.join(TEST_RUN_HOME + '/template-hello-world/App_Resources'))
        File.replace(file_path=TEST_RUN_HOME + "/template-hello-world/package.json",
                     str1="tns-template-hello-world", str2="test-tns-template-hello-world")
        path = os.path.join(TEST_RUN_HOME, 'template-hello-world')
        output = Tns.run_tns_command("create " + self.app_name, attributes={"--template": path})
        TnsAsserts.created(self.app_name, output=output)
        Folder.cleanup("template-hello-world")

    @parameterized.expand([
        "tns-template-hello-world",
        "https://github.com/NativeScript/template-hello-world.git",
        "https://github.com/NativeScript/template-hello-world-ts/tarball/master",
        "https://github.com/NativeScript/template-hello-world-ts.git#master",
        "https://github.com/NativeScript/template-hello-world-ng.git#master",
        "typescript",
        "tsc",
        "ng",
        "angular",
        "default",
        "default@4.0.0"
    ])
    def test_200_create_project_with_template(self, template_source):
        """Create app should be possible with --template and npm packages, git repos and aliases"""

        output = Tns.create_app(self.app_name, attributes={"--template": template_source}, update_modules=True)
        TnsAsserts.created(self.app_name, output=output)
        if 'ts' in template_source and '#master' in template_source:
            TnsAsserts.created_ts(self.app_name, output=output)
        if 'ng' in template_source and '#master' in template_source:
            TnsAsserts.created_ng(self.app_name, output=output)

    @unittest.skipIf(Npm.version() > 4, "This is not supported with npm5!")
    def test_201_create_project_with_local_directory_template(self):
        """--template should install all packages from package.json"""

        output = Tns.create_app(self.app_name, attributes={"--template": "./data/templates/myCustomTemplate/"},
                                update_modules=False)
        TnsAsserts.created(self.app_name, output=output)
        assert not Folder.is_empty(self.app_name + "/node_modules/lodash")
        assert not Folder.is_empty(self.app_name + "/node_modules/minimist")
        assert not Folder.is_empty(self.app_name + "/node_modules/tns-core-modules")
        assert not Folder.is_empty(self.app_name + "/node_modules/tns-core-modules-widgets")

        strings = ["\"tns-core-modules\":", "\"lodash\": \"3.10.1\"", "\"minimist\": \"1.2.0\""]
        TnsAsserts.package_json_contains(self.app_name, string_list=strings)

    def test_300_create_project_with_no_app_resoruces(self):
        """--template should not create project if value is no npm installable"""

        Tns.create_app(self.app_name, attributes={"--template": "tns-template-hello-world-ts@2.0.0"},
                       assert_success=False)
        res_path = os.path.join(self.app_name, 'app', 'App_Resources')
        assert File.exists(res_path), "App Resouces not added by {N} CLI if missing in template"

    def test_400_create_project_with_wrong_template_path(self):
        """--template should not create project if value is no npm installable"""

        output = Tns.create_app(self.app_name, attributes={"--template": "invalidEntry"},
                                assert_success=False, update_modules=False)
        assert "successfully created" not in output
        assert "npm ERR!" in output
        assert "404" in output

    def test_401_create_project_with_empty_template_path(self):
        output = Tns.create_app(self.app_name, attributes={"--template": ""}, assert_success=False,
                                update_modules=False)
        assert "successfully created" not in output
        assert "requires non-empty value" in output

    def test_402_create_project_in_folder_with_existing_project(self):
        """Create project with name that already exist should show friendly error message"""

        Tns.create_app(self.app_name, update_modules=False)
        output = Tns.create_app(app_name=self.app_name, assert_success=False, update_modules=False, force_clean=False)
        assert "successfully created" not in output
        assert "Path already exists and is not empty" in output

    def test_403_create_project_with_no_name(self):
        """Create project without name should show friendly error message"""

        output = Tns.run_tns_command("create ")
        assert "You need to provide all the required parameters." in output
        assert "# tns create" in output

    def test_404_create_project_with_template_and_ng(self):
        output = Tns.create_app(self.app_name, attributes={"--template": "--ng"}, assert_success=False,
                                update_modules=False)
        assert "successfully created" not in output
        assert "requires non-empty value" in output

    def test_405_create_app_with_space_without_quotes(self):
        """Create project with space without quotes."""

        # Test for https://github.com/NativeScript/nativescript-cli/issues/2727
        output = Tns.run_tns_command("create fake fake")
        assert "The parameter fake is not valid for this command" in output
        assert "# tns create" in output
