'''
Test for create command
'''
import unittest
import fileinput

from helpers._os_lib import cleanup_folder, check_file_exists, file_exists, folder_exists, \
    is_empty, run_aut
from helpers._tns_lib import create_project, TNSPATH

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=R0201, C0103, C0111, R0904
class Create(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cleanup_folder('./app')
        cleanup_folder('./123')
        cleanup_folder('./folder')
        cleanup_folder('./tns-app')
        cleanup_folder('./TNS App')

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')
        cleanup_folder('./template')

    def tearDown(self):
        cleanup_folder('./TNS_App')
        cleanup_folder('./template')

    @classmethod
    def tearDownClass(cls):
        cleanup_folder('./app')
        cleanup_folder('./123')
        cleanup_folder('./folder')
        cleanup_folder('./tns-app')
        cleanup_folder('./TNS App')

    def test_001_create_project(self):
        create_project(proj_name="TNS_App")

        assert is_empty("TNS_App/platforms")
        assert not folder_exists("TNS_App/app/tns_modules")

        output = run_aut("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        assert "\"tns-core-modules\": \"1." in output

        assert file_exists("TNS_App/node_modules/tns-core-modules/package.json")
        assert file_exists("TNS_App/node_modules/tns-core-modules/LICENSE")
        assert file_exists("TNS_App/node_modules/tns-core-modules/xml/xml.js")

        assert check_file_exists(
            "TNS_App", "template_javascript_files_1.2.0.txt")

    def test_002_create_project_with_path(self):
        create_project(proj_name="TNS_App", path='folder/subfolder/')

        assert is_empty("folder/subfolder/TNS_App/platforms")
        assert not folder_exists("folder/subfolder/TNS_App/app/tns_modules")

        output = run_aut("cat folder/subfolder/TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        assert "\"tns-core-modules\": \"1." in output

        assert file_exists(
            "folder/subfolder/TNS_App/node_modules/tns-core-modules/package.json")
        assert file_exists(
            "folder/subfolder/TNS_App/node_modules/tns-core-modules/LICENSE")
        assert file_exists(
            "folder/subfolder/TNS_App/node_modules/tns-core-modules/xml/xml.js")

        assert check_file_exists(
            'folder/subfolder/TNS_App',
            'template_javascript_files_1.2.0.txt')

    def test_003_create_project_with_appid(self):
        create_project(proj_name="TNS_App", app_id="org.nativescript.MyApp")
        output = run_aut("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.MyApp\"" in output

    def test_004_create_project_with_copyfrom(self):
        # Create initial template project
        create_project(proj_name="template")

        # Modify some files in template project
        for line in fileinput.input("template/app/LICENSE", inplace=1):
            print line.replace("Copyright (c) 2015, Telerik AD", "Copyright (c) 2015, Telerik A D"),

        # Create new project based on first one
        create_project(proj_name="TNS_App", copy_from="template/app")

        # Verify new project corresponds to name of the new project
        output = run_aut("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

        # Verify that content of the new project is based on first project
        output = run_aut("cat TNS_App/app/LICENSE")
        assert not "Copyright (c) 2015, Telerik AD" in output
        assert "Copyright (c) 2015, Telerik A D" in output

    def test_005_create_project_with_space(self):
        create_project(proj_name="\"TNS App\"")
        output = run_aut("cat \"TNS App/package.json\"")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

    def test_006_create_project_with_dash(self):
        create_project(proj_name="\"tns-app\"")
        output = run_aut("cat \"tns-app/package.json\"")
        assert "\"id\": \"org.nativescript.tnsapp\"" in output

    def test_007_create_project_named_123(self):
        create_project(proj_name="123")
        output = run_aut("cat 123/package.json")
        assert "\"id\": \"org.nativescript.the123\"" in output

    def test_008_create_project_named_app(self):
        output = create_project(proj_name="app")
        assert "You cannot build applications named 'app' in Xcode." in output

        output = run_aut("cat app/package.json")
        assert "\"id\": \"org.nativescript.app\"" in output

    def test_400_create_project_with_copyfrom_wrong_path(self):
        output = run_aut(TNSPATH + " create TNS_App --copy-from invalidFolder")
        assert not "successfully created" in output

        assert "The specified path" in output
        assert "doesn't exist. Check that you specified the path correctly and try again" in output

    def test_401_create_project_in_folder_with_existing_project(self):
        create_project(proj_name="TNS_App")
        output = run_aut(TNSPATH + " create TNS_App")
        assert not "successfully created" in output
        assert "Path already exists and is not empty" in output

    def test_402_create_project_with_wrong_copyfrom_command(self):
        # Create initial template project
        create_project(proj_name="template")

        output = run_aut(TNSPATH + " create TNS_App -copy-from template")
        assert not "successfully created" in output
        assert "To see command's options, use '$ tns help create'" in output

    def test_403_create_project_with_no_name(self):
        output = run_aut(TNSPATH + " create")
        assert "You need to provide all the required parameters." in output
        assert "# create" in output
