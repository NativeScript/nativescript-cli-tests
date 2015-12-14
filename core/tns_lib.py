'''
Created on Dec 14, 2015

A wrapper of the tns commands.

@author: vchimev
'''

import time
from core.constants import TNS_PATH

# TODO: remove this import
from helpers._os_lib import run_aut


def tns_livesync(platform=None, emulator=False, device=None, path=None):
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

#     if watch:
#         command += " --watch"

    if path is not None:
        command += " --path {0}".format(path)

#     if just_launch:
#         command += " --justlaunch"

    command += " --justlaunch --log trace"
    output = run_aut(command)

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
