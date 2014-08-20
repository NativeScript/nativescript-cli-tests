import unittest, os, sys, platform, HTMLTestRunner
from _tns_lib import *

class TNSSmokeTests(unittest.TestCase):
    def setUp(self):
        print self.id()

    def tearDown(self):
        pass

    def test_010_Help(self):
        command="tns help"
        output=runAUT(command)
        assert("Usage" in output)
        assert not ("Error" in output)

    def test_020_CreateProject(self):
        projName="TNS_Javascript"
        CreateProject_CheckFiles(projName,'template_javascript_files.txt')



def RunTests():
    print "Platform : ", platform.platform()
    suite = unittest.TestLoader().loadTestsFromTestCase(TNSSmokeTests)

    result =""
    with open ("Report.html", "w") as f:
        descr= "Platform : {0};  nativescript-cli build version : {1}".format(platform.platform(),GetCLIBuildVersion())
        runner = HTMLTestRunner.HTMLTestRunner(stream=f, title='TNS_CLI_smoke_tests', description = descr)
        #runner = unittest.runner.TextTestRunner()
        result= runner.run(suite)
    return result


if __name__ == '__main__':
    RunTests()