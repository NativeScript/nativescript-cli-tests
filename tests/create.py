import unittest
import fileinput

from helpers._os_lib import CleanupFolder, CheckFilesExists, FileExists, FolderExists, \
    IsEmpty, runAUT
from helpers._tns_lib import CreateProject, tnsPath

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=R0201, C0111, R0904


class Create(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanupFolder('./app')
        CleanupFolder('./123')
        CleanupFolder('./folder')
        CleanupFolder('./tns-app')
        CleanupFolder('./TNS App')

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')
        CleanupFolder('./template')

    def tearDown(self):
        CleanupFolder('./TNS_App')
        CleanupFolder('./template')

    @classmethod
    def tearDownClass(cls):
        CleanupFolder('./app')
        CleanupFolder('./123')
        CleanupFolder('./folder')
        CleanupFolder('./tns-app')
        CleanupFolder('./TNS App')

    def test_001_create_project(self):
        CreateProject(projName="TNS_App")

        assert IsEmpty("TNS_App/platforms")
        assert not FolderExists("TNS_App/app/tns_modules")

        output = runAUT("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        assert "\"tns-core-modules\": \"1." in output

        assert FileExists("TNS_App/node_modules/tns-core-modules/package.json")
        assert FileExists("TNS_App/node_modules/tns-core-modules/LICENSE")
        assert FileExists("TNS_App/node_modules/tns-core-modules/xml/xml.js")

        assert CheckFilesExists(
            "TNS_App", "template_javascript_files_1.2.0.txt")

    def test_002_create_project_with_path(self):
        CreateProject(projName="TNS_App", path='folder/subfolder/')

        assert IsEmpty("folder/subfolder/TNS_App/platforms")
        assert not FolderExists("folder/subfolder/TNS_App/app/tns_modules")

        output = runAUT("cat folder/subfolder/TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output
        assert "\"tns-core-modules\": \"1." in output

        assert FileExists(
            "folder/subfolder/TNS_App/node_modules/tns-core-modules/package.json")
        assert FileExists(
            "folder/subfolder/TNS_App/node_modules/tns-core-modules/LICENSE")
        assert FileExists(
            "folder/subfolder/TNS_App/node_modules/tns-core-modules/xml/xml.js")

        assert CheckFilesExists(
            'folder/subfolder/TNS_App',
            'template_javascript_files_1.2.0.txt')

    def test_003_create_project_with_appid(self):
        CreateProject(projName="TNS_App", appId="org.nativescript.MyApp")
        output = runAUT("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.MyApp\"" in output

    def test_004_create_project_with_copyfrom(self):
        # Create initial template project
        CreateProject(projName="template")

        # Modify some files in template project
        for line in fileinput.input("template/app/LICENSE", inplace=1):
            print line.replace("Copyright (c) 2015, Telerik AD", "Copyright (c) 2015, Telerik A D"),

        # Create new project based on first one
        CreateProject(projName="TNS_App", copyFrom="template/app")

        # Verify new project corresponds to name of the new project
        output = runAUT("cat TNS_App/package.json")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

        # Verify that content of the new project is based on first project
        output = runAUT("cat TNS_App/app/LICENSE")
        assert not "Copyright (c) 2015, Telerik AD" in output
        assert "Copyright (c) 2015, Telerik A D" in output

    def test_005_create_project_with_space(self):
        CreateProject(projName="\"TNS App\"")
        output = runAUT("cat \"TNS App/package.json\"")
        assert "\"id\": \"org.nativescript.TNSApp\"" in output

    def test_006_create_project_with_dash(self):
        CreateProject(projName="\"tns-app\"")
        output = runAUT("cat \"tns-app/package.json\"")
        assert "\"id\": \"org.nativescript.tnsapp\"" in output

    def test_007_create_project_named_123(self):
        CreateProject(projName="123")
        output = runAUT("cat 123/package.json")
        assert "\"id\": \"org.nativescript.the123\"" in output

    def test_008_create_project_named_app(self):
        output = CreateProject(projName="app")
        assert "You cannot build applications named 'app' in Xcode. Consider creating a project with different name." in output

        output = runAUT("cat app/package.json")
        assert "\"id\": \"org.nativescript.app\"" in output

    def test_400_create_project_with_copyfrom_wrong_path(self):
        output = runAUT(tnsPath + " create TNS_App --copy-from invalidFolder")
        assert not "successfully created" in output

        assert "The specified path" in output
        assert "doesn't exist. Check that you specified the path correctly and try again." in output

    def test_401_create_project_in_folder_with_existing_project(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " create TNS_App")
        assert not "successfully created" in output
        assert "Path already exists and is not empty" in output

    def test_402_create_project_with_wrong_copyfrom_command(self):
        # Create initial template project
        CreateProject(projName="template")

        output = runAUT(tnsPath + " create TNS_App -copy-from template")
        assert not "successfully created" in output
        assert "To see command's options, use '$ tns help create'" in output

    def test_403_create_project_with_no_name(self):
        output = runAUT(tnsPath + " create")
        assert "You need to provide all the required parameters." in output
        assert "# create" in output
