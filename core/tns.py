'''
Created on Dec 14, 2015

A wrapper of the tns commands.

@author: vchimev
'''


# C0111 - Missing docstring
# pylint: disable=C0111

import time
from core.constants import TNS_PATH
from core.commons import run


class Tns(object):

    @classmethod
    def tns_version(cls):
        '''
        Return {N} CLI version.
        '''

        command = TNS_PATH + "--version"
        output = run(command)
        return output

    @classmethod
    def tns_create_app(cls, app_name, path=None, app_id=None, copy_from=None):
        '''
        Create {N} project.
        '''

        command = TNS_PATH + " create {0}".format(app_name)

        if path is not None:
            command += " --path " + path

        if app_id is not None:
            command += " --appid " + app_id

        # By default --copy-from template-hello-world
        if copy_from is not None:
            command += " --copy-from " + copy_from
        else:
            command += " --copy-from  template-hello-world"

        command += " --log trace"
        output = run(command)

        assert "Project {0} was successfully created".format(app_name.replace("\"", "")) in output
        return output

    @classmethod
    def tns_create_app_from_template(cls, app_name, path=None, app_id=None, template=None):
        '''
        Create {N} project.
        '''

        command = TNS_PATH + " create {0}".format(app_name)

        if path is not None:
            command += " --path " + path

        if app_id is not None:
            command += " --appid " + app_id

        if template is not None:
            command += " --template " + path

        command += " --log trace"
        output = run(command)

        assert "Project {0} was successfully created".format(app_name.replace("\"", "")) in output
        return output

    @classmethod
    def tns_platform_add(cls, platform=None, framework_path=None, path=None, symlink=False):
        '''
        Add target platform.
        '''

        command = TNS_PATH + " platform add"

        if platform is not None:
            command += " {0}".format(platform)

        if framework_path is not None:
            command += " --framework-path {0}".format(framework_path)

        if path is not None:
            command += " --path {0}".format(path)

        if symlink is True:
            command += " --symlink"

        command += " --log trace"
        output = run(command)

        assert "Copying template files..." in output
        assert "Project successfully created." in output
        return output

    @classmethod
    def tns_prepare(cls, platform=None, path=None):
        '''
        Prepare target platform.
        '''

        command = TNS_PATH + " prepare"

        if platform is not None:
            command += " {0}".format(platform)

        if path is not None:
            command += " --path {0}".format(path)

        command += " --log trace"
        output = run(command)

        assert "Project successfully prepared" in output
        return output

    @classmethod
    def tns_plugin_add(cls, plugin=None, path=None):
        '''
        Install {N} plugin.
        '''

        command = TNS_PATH + " plugin add"

        if plugin is not None:
            command += " {0}".format(plugin)

        if path is not None:
            command += " --path {0}".format(path)

        command += " --log trace"
        output = run(command)

        assert "Successfully installed plugin {0}".format(plugin) in output
        return output

    @classmethod
    def tns_build(cls, platform=None, mode=None, for_device=False, path=None):
        '''
        Build {N} project.
        '''

        command = TNS_PATH + " build"

        if platform is not None:
            command += " {0}".format(platform)

        if mode is not None:
            command += " --{0}".format(mode)

        if for_device:
            command += " --for-device"

        if path is not None:
            command += " --path {0}".format(path)

        command += " --log trace"
        output = run(command)

        assert "Project successfully prepared" in output
        if platform is "android":
            assert "BUILD SUCCESSFUL" in output
        elif platform is "ios":
            assert "BUILD SUCCEEDED" in output
        assert "Project successfully built" in output
        assert "ERROR" not in output
        return output

    @classmethod
    def tns_run(cls, platform=None, emulator=False, device=None, path=None):
        '''
        Run {N} project.
        '''

        command = TNS_PATH + " run"

        if platform is not None:
            command += " {0}".format(platform)

        if emulator:
            command += " --emulator"

        if device is not None:
            command += " --device {0}".format(device)

        if path is not None:
            command += " --path {0}".format(path)

        command += " --justlaunch --log trace"
        output = run(command)

        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        if platform is "android":
            assert "Successfully deployed on device with identifier" in output
        elif platform is "ios":
            if emulator:
                assert "Starting iOS Simulator" in output
            else:
                assert "Successfully deployed on device" in output
                assert "Successfully run application org.nativescript." in output
        return output

    @classmethod
    def tns_livesync(cls, platform=None, emulator=False, device=None, path=None):
        '''
        The livesync command.

        Parameters:
            - android: --device, -- watch
            - iOS: --emulator, -- device, --watch
        '''

        command = TNS_PATH + " livesync"

        if platform is not None:
            command += " {0}".format(platform)

        if emulator:
            command += " --emulator"

        if device is not None:
            command += " --device {0}".format(device)

        if path is not None:
            command += " --path {0}".format(path)

        command += " --justlaunch --log trace"
        output = run(command)

        assert "Project successfully prepared" in output
        if platform is "android":
            assert "Start syncing application" in output
            assert "Transferring project files..." in output
            assert "Successfully transferred all project files." in output
            assert "Applying changes..." in output
            assert "Successfully synced application" in output
            time.sleep(10)
        elif platform is "ios":
            assert "Project successfully prepared" in output
        return output

    @classmethod
    def tns_create_app_platform_add(cls, app_name, platform=None, framework_path=None, \
                                    symlink=False):
        '''
        Create {N} project and add target platform.
        '''

        cls.tns_create_app(app_name)
        cls.tns_platform_add(platform, framework_path, app_name, symlink)
