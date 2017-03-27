from core.osutils.command import run
from core.osutils.command_log_level import CommandLogLevel


class Git(object):
    @staticmethod
    def clone_repo(repo_url, local_folder, branch=None):
        """Clone GitHub repo to local folder
        :param repo_url: GitHub repo URL
        :param branch: Branch
        :param local_folder: Local folder
        """
        command = 'git clone ' + repo_url + ' ' + local_folder
        if branch is not None:
            command = command + ' -b ' + branch
        output = run(command, log_level=CommandLogLevel.COMMAND_ONLY)
        assert not ("fatal" in output), "Failed to clone {0}".format(repo_url)
