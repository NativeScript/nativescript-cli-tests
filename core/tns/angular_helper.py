from core.osutils.file import File
from core.osutils.folder import Folder

def assert_angular_project(app_name):
    output = File.read(app_name + "/package.json")
    assert "nativescript-angular" in output
    assert "tns-core-modules" in output
    assert "nativescript-dev-typescript" in output

    assert Folder.exists(app_name + "/node_modules/nativescript-angular")
    assert Folder.exists(app_name + "/node_modules/nativescript-dev-typescript")
    assert Folder.exists(app_name + "/node_modules/tns-core-modules")

    assert Folder.exists(app_name + "/hooks")
    assert Folder.exists(app_name + "/app/App_Resources")
