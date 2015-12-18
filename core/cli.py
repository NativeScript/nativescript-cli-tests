'''
Created on Dec 14, 2015

A wrapper of the NativeScript CLI.

@author: vchimev
'''


# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0111

import os, shutil
from core.commons import run
from core.file import File


# class Cli(object):

#     TODO: Verify all needed environs
#       if 'CLI_PATH' in os.environ:


def install():
    location = os.path.join(os.environ['CLI_PATH'], "nativescript.tgz")
    shutil.copy2(location.strip(), os.path.join(os.getcwd(), "nativescript.tgz"))

    output = run("npm i nativescript.tgz")
    message = "NativeScript CLI installation failed - \"{e}\" found in output."
    assert "ERR" not in output, message.format(e="ERR")
    assert "Error" not in output, message.format(e="Error")
    assert "error" not in output, message.format(e="error")
    assert "FiberFuture" not in output, message.format(e="FiberFuture")
    assert "dev-post-install" not in output, message.format(e="dev-post-install")
    assert File.exists("node_modules/.bin/tns"), \
        "NativeScript CLI installation failed - tns does not exist."
    print output

def uninstall():
    output = run("npm uninstall nativescript")
    print output
