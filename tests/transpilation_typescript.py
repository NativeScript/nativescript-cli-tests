'''
Tests for transpilation of typescript in context
'''

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0111, R0201

import platform, unittest

from helpers._os_lib import cleanup_folder, \
    file_exists, file_with_extension_exists, is_empty, run_aut
from helpers._tns_lib import ANDROID_RUNTIME_PATH, IOS_RUNTIME_SYMLINK_PATH, \
    TNS_PATH, build, create_project, platform_add, prepare


class TranspilationTypeScript(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('TNS_App')

    def tearDown(self):
        cleanup_folder('TNS_App')

    def test_001_transpilation_ts(self):
        create_project(proj_name="TNS_App", copy_from="template-hello-world-ts")
        platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path="TNS_App")

        assert file_with_extension_exists(
            "TNS_App/node_modules/tns-core-modules", ".ts")

        output = run_aut(TNS_PATH + " install typescript --path TNS_App")
        assert "TNS_App/node_modules/nativescript-dev-typescript" in output
        assert "nativescript-hook@" in output

        assert file_exists("TNS_App/tsconfig.json")
        assert file_exists("TNS_App/node_modules/typescript/bin/tsc")
        assert not is_empty("TNS_App/node_modules/nativescript-dev-typescript")
        assert file_exists("TNS_App/hooks/before-prepare/nativescript-dev-typescript.js")
        assert file_exists("TNS_App/hooks/before-watch/nativescript-dev-typescript.js")

        output = run_aut("cat TNS_App/package.json")
        assert "devDependencies" in output
        assert "nativescript-dev-typescript" in output

        output = prepare(path="TNS_App", platform="android")
        assert "Executing before-prepare hook" in output
        assert "Found peer TypeScript" in output
        assert not "error" in output

        assert file_with_extension_exists("TNS_App/app", ".js")
        assert file_with_extension_exists("TNS_App/app", ".ts")

        assert file_with_extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".js")
        assert not file_with_extension_exists(
            "TNS_App/platforms/android/src/main/assets/app", ".ts")
        assert not file_with_extension_exists(
            "TNS_App/platforms/android/src/main/assets/app/tns_modules", ".ts")
        build(platform="android", path="TNS_App")

        if 'Darwin' in platform.platform():
            platform_add(
                platform="ios",
                framework_path=IOS_RUNTIME_SYMLINK_PATH,
                path="TNS_App",
                symlink=True)

            output = prepare(platform="ios", path="TNS_App")
            assert "Executing before-prepare hook" in output
            assert "Found peer TypeScript" in output
            assert not "error" in output

            assert file_with_extension_exists("TNS_App/app", ".js")
            assert file_with_extension_exists("TNS_App/app", ".ts")

            assert file_with_extension_exists(
                "TNS_App/platforms/ios/TNSApp/app", ".js")
            assert not file_with_extension_exists(
                "TNS_App/platforms/ios/TNSApp/app", ".ts")
            assert not file_with_extension_exists(
                "TNS_App/platforms/ios/TNSApp/app/tns_modules", ".ts")
            build(platform="ios", path="TNS_App")

#         output = run_aut(TNS_PATH + " prepare android --path TNS_App")
#         assert "Project successfully prepared" in output
# 
#         # Verify app and modules are processed and available in platform folder
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/main-view-model.js')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.js')
#         assert not file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
#         "application/application.android.js')
#         assert not file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/tns_modules/" + \
#         "application/application.ios.js')
# 
#     def test_002_prepare_android_inside_project(self):
#         create_project_add_platform(
#             proj_name="TNS_App",
#             platform="android",
#             framework_path=ANDROID_RUNTIME_PATH)
#         current_dir = os.getcwd()
#         os.chdir(os.path.join(current_dir, "TNS_App"))
#         output = run_aut(os.path.join("..", TNS_PATH) + " prepare android")
#         os.chdir(current_dir)
#         assert "Project successfully prepared" in output
# 
#         # Verify app and modules are processed and available in platform folder
#         assert file_exists(
#         'TNS_App/platforms/android/src/main/assets/app/main-view-model.js')
#         assert file_exists(
#         'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.js')
#         assert not file_exists(
#         'TNS_App/platforms/android/src/main/assets/app/tns_modules/' + \
#         'application/application.android.js')
#         assert not file_exists(
#         'TNS_App/platforms/android/src/main/assets/app/tns_modules/application/application.ios.js')
# 
#     def test_010_prepare_android_tns_core_modules(self):
#         create_project(
#             proj_name="TNS_App",
#             copy_from="QA-TestApps/tns-modules-app/app")
#         platform_add(
#             platform="android",
#             path="TNS_App",
#             framework_path=ANDROID_RUNTIME_PATH)
# 
#         # Make a change in tns-core-modules to verify they are not overwritten.
#         replace(
#             "TNS_App/node_modules/tns-core-modules/application/application-common.js",
#             "(\"globals\");",
#             "(\"globals\"); // test")
# 
#         # Verify tns-core-modules are copied to the native project, not app's
#         # tns_modules.
#         for i in range(1, 3):
#             print "prepare number: " + str(i)
# 
#             output = run_aut(TNS_PATH + " prepare android --path TNS_App")
#             assert "You have tns_modules dir in your app folder" in output
#             assert "Project successfully prepared" in output
# 
#             output = run_aut("cat TNS_App/app/tns_modules/package.json")
#             assert "\"version\": \"1.2.1\"," in output
# 
#             output = run_aut(
#                 "cat TNS_App/node_modules/tns-core-modules/package.json")
#             assert "\"version\": \"1.2.1\"," not in output
#             output = run_aut(
#                 "cat TNS_App/node_modules/tns-core-modules/application/application-common.js")
#             assert "require(\"globals\"); // test" in output
# 
#             output = run_aut(
#                 "cat TNS_App/platforms/android/src/main/assets/app/tns_modules/package.json")
#             assert "\"version\": \"1.2.1\"," not in output
#             output = run_aut(
#                 "cat TNS_App/platforms/android/src/main/assets/app/" + \
#                 "tns_modules/application/application-common.js")
#             assert "require(\"globals\"); // test" in output
# 
#     def test_210_prepare_android_patform_not_added(self):
#         create_project(proj_name="TNS_App")
#         output = run_aut(TNS_PATH + " prepare android --path TNS_App")
#         assert "Copying template files..." in output
#         assert "Project successfully created." in output
#         assert "Project successfully prepared" in output
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/tns_modules/xml/xml.js')
# 
#     def test_300_prepare_android_remove_old_files(self):
#         create_project_add_platform(
#             proj_name="TNS_App",
#             platform="android",
#             framework_path=ANDROID_RUNTIME_PATH)
#         output = run_aut(TNS_PATH + " prepare android --path TNS_App")
#         assert "Project successfully prepared" in output
# 
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.js')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.css')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/main-page.xml')
# 
#         run_aut("mv TNS_App/app/app.js TNS_App/app/app-new.js")
#         run_aut("mv TNS_App/app/app.css TNS_App/app/app-new.css")
#         run_aut("mv TNS_App/app/main-page.xml TNS_App/app/main-page-new.xml")
# 
#         output = run_aut(TNS_PATH + " prepare android --path TNS_App")
#         assert "Project successfully prepared" in output
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app-new.js')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app-new.css')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/main-page-new.xml')
# 
#         assert not file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.js')
#         assert not file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.css')
#         assert not file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/main-page.xml')
# 
#     def test_301_prepare_android_platform_specific_files(self):
#         create_project_add_platform(
#             proj_name="TNS_App",
#             platform="android",
#             framework_path=ANDROID_RUNTIME_PATH)
#         output = run_aut(TNS_PATH + " prepare android --path TNS_App")
#         assert "Project successfully prepared" in output
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.css')
# 
#         run_aut("cp TNS_App/app/app.js TNS_App/app/app.ios.js")
#         run_aut("cp TNS_App/app/app.js TNS_App/app/app.android.js")
#         run_aut("cp TNS_App/app/app.js TNS_App/app/appios.js")
#         run_aut("cp TNS_App/app/app.js TNS_App/app/appandroid.js")
#         run_aut("cp TNS_App/app/app.js TNS_App/app/ios.js")
#         run_aut("cp TNS_App/app/app.js TNS_App/app/android.js")
#         run_aut("cp TNS_App/app/app.css TNS_App/app/app.ios.css")
#         run_aut("cp TNS_App/app/app.css TNS_App/app/app.android.css")
#         run_aut("mv TNS_App/app/app.js TNS_App/app/appNew.js")
#         run_aut("mv TNS_App/app/app.css TNS_App/app/appNew.css")
# 
#         output = run_aut(TNS_PATH + " prepare android --path TNS_App")
#         assert "Project successfully prepared" in output
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.css')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.js')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/appandroid.js')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/appios.js')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/android.js')
#         assert file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/ios.js')
#         assert not file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.ios.css')
#         assert not file_exists(
#             'TNS_App/platforms/android/src/main/assets/app/app.android.css')
# 
#     def test_400_prepare_missing_platform(self):
#         create_project(proj_name="TNS_App")
#         output = run_aut(TNS_PATH + " prepare --path TNS_App")
#         assert "You need to provide all the required parameters." in output
# 
#     def test_401_prepare_invalid_platform(self):
#         create_project(proj_name="TNS_App")
#         output = run_aut(TNS_PATH + " prepare windows --path TNS_App")
#         assert "Invalid platform windows. Valid platforms are ios or android." in output
