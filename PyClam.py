import subprocess as _subprocess
import shlex as _shlex
from ClamPath import ClamPath
import os as _os
HOME = ClamPath("$HOME")
PATH = _os.environ["PATH"]

# !TODO finish adding comments


class Clam:
    """Thin wrapper around Popen which aims to resemble a shell.

    
    """
    # This will be used to buffer stdout from processes
    _result = b""

    def __init__(self, cwd="$HOME"):
        self.handle = Clam.default_handler
        self.cwd = ClamPath(cwd)

    # This is the default function called in case a command returns an error.
    @staticmethod
    def default_handler(clam, cmd):
        """A callback function to handle process' non 0 exits.

        Parameters
        ----------
        clam: Clam
            The caller instance
        cmd: list[str]
            The list used by Popen
        """
        if input("{} was not successful, try again? [Y/n] ".format(cmd)).strip().lower() == "y":
            clam.call(cmd)
        else:
            exit(1)

    def call(self, *cmd):
        # Splits each argument into a list of strings separated by space,
        # then join each list into one big list.
        cmd = _shlex.split(_shlex.join(cmd))

        # !TODO remove logging
        print("Running: {}".format(cmd))

        # As this class is designed to work like a shell,
        # most exceptions are just printed and the program goes on.
        try:
            # Runs cmd at the cwd 'self.cwd'
            process = _subprocess.Popen(cmd, cwd=self.cwd, env={"PATH": PATH}, stdout=_subprocess.PIPE)
            self._result = process.communicate()[0]
            process.wait()
        except _subprocess.CalledProcessError:
            self.handle(cmd)
        except Exception as e:
            print(e)
        return self

    def source(self, file):
        self.call("env -i bash 'source {} && env'".format(str(self.cwd/file)))
        for line in self._result.split("\n"):
            key, value = line.split("=")
            if key != "PWD" or key != "PATH":
                _os.environ[key] = value

    def cd(self, cwd):
        self.cwd.join(cwd)
        return self

    def cat(self, file):
        return self.cwd / file

    def set_handler(self, func):
        self.handle = func
        return self

    def show(self):
        print(self._result.decode("utf-8"))
        return self
