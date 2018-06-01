import errno
import os
import signal
from time import sleep


class subprocess_utils(object):
    @staticmethod
    def cancelTimeout(prevAlarmHandler):
        """Cancel the SIGALRM timeout when
           the child is finished, and restore the previous SIGALRM handler"""
        signal.alarm(0)
        signal.signal(signal.SIGALRM, prevAlarmHandler)
        pass
        return

    @staticmethod
    def wait_process(subprocess, prevAlarmHandler):
        """Wait for the child process to exit, or the timeout to expire,
            whichever comes first.
            This function returns the same thing as Python's
            subprocess.wait(). That is, this function returns the exit status of
            the child process; if the return value is -N, it indicates that the
            child was killed by signal N. """

        try:
            subprocess.wait()
        except OSError, e:

            # If the child times out, the wait() syscall can get
            # interrupted by the SIGALRM. We should then only need to
            # wait() once more for the child to actually exit.

            if e.errno == errno.EINTR:
                subprocess.wait()
            else:
                raise e
            pass

        subprocess_utils.cancelTimeout(prevAlarmHandler)

        assert subprocess.poll() is not None
        return subprocess.poll()

    @staticmethod
    def kill(pgid, prevAlarmHandler, deathsig=signal.SIGKILL):
        """Kill the child process. Optionally specify the signal to be used
        (default: SIGKILL)"""
        try:
            os.killpg(pgid, deathsig)
        except OSError, e:
            if e.errno == errno.ESRCH:
                # We end up here if the process group has already exited, so it's safe to
                # ignore the error
                pass
            else:
                sleep(20)
                try:
                    os.killpg(pgid, deathsig)
                except OSError, e:

                    if e.errno == errno.ESRCH:
                        # We end up here if the process group has already exited, so it's safe to
                        # ignore the error
                        pass
                    else:
                        raise e
                    pass
            pass

        subprocess_utils.cancelTimeout(prevAlarmHandler)
