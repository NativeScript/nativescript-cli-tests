import unittest, os, sys, platform, HTMLTestRunner
from _tns_lib import *
from _os_lib import *

class TNSSmokeTests(unittest.TestCase):
    
    tnsPath = os.path.join('node_modules', '.bin', 'tns');
    nativescriptPath = os.path.join('node_modules', '.bin', 'nativescript');
            
    def setUp(self):
        print self.id()

    def tearDown(self):
        pass

    def test_010_TNSHelp(self):
        command = self.tnsPath + " help"
        output = runAUT(command)
        CheckOutput(output, 'help_output.txt')
        assert not ("Error" in output)

    def test_011_NativescriptHelp(self):
        command = self.nativescriptPath + " help"
        output = runAUT(command)
        CheckOutput(output, 'help_output.txt')
        assert not ("Error" in output)
        
    def test_020_CreateProject(self):
        projName = "TNS_Javascript"
        CreateProject(projName)
        assert(CheckFilesExists(projName, 'template_javascript_files.txt'))
        
    def test_021_CreateProjectWithPath(self):
        projName = "TNS_Javascript"
        CleanupFolder('./folder');
        CreateProject(projName, 'folder/subfolder/')
        assert(CheckFilesExists('folder/subfolder/' + projName, 'template_javascript_files.txt'))        

def RunTests():
    print "Platform : ", platform.platform()
    suite = unittest.TestLoader().loadTestsFromTestCase(TNSSmokeTests)

    result = ""
    with open ("Report.html", "w") as f:
        descr = "Platform : {0};  nativescript-cli build version : {1}".format(platform.platform(), GetCLIBuildVersion())
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='TNS_CLI_smoke_tests', description=descr)
        # runner = unittest.runner.TextTestRunner()
        result = runner.run(suite)
    return result


if __name__ == '__main__':
    RunTests()
