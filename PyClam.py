import subprocess
import pathlib
import os

HOME = os.getenv("HOME")
PATH = os.getenv("PATH")


# A class wrapper which does system calls and handles errors
class Clam:
    # This will be used to buffer stdout from processes
    _result = b""

    def __init__(self, cwd="$HOME", err=None):
        self.handle = err if err else Clam.default_handler
        self.cwd = parse(cwd)

    # This is the default function called in case a command returns an error.
    @staticmethod
    def default_handler(caller, cmd):
        if input("{} was not successful, try again? [Y/n] ".format(cmd)).strip().lower() == "y":
            caller.call(cmd)
        else:
            exit(1)

    def call(self, *cmd):
        # Splits each argument into a list of strings separated by space,
        # then join each list into one big list.
        cmd = [x
               for arg in cmd
               for x in arg.split(" ")]

        # !TODO remove logging
        print("Running: {}".format(cmd))

        # As this class is designed to work like a safe shell,
        # most exceptions are just printed and the program goes on.
        try:
            # Runs cmd at the cwd 'self.cwd'
            process = subprocess.Popen(cmd, cwd=self.cwd, env={"PATH": PATH}, stdout=subprocess.PIPE)
            self._result = process.communicate()[0]
            process.wait()
        except subprocess.CalledProcessError:
            self.handle(cmd)
        except Exception as e:
            print(e)
        return self

    # Emulates the cd command from a shell
    def cd(self, cwd):
        self.cwd /= parse(cwd)
        return self

    # Sets the error handler function
    def set_handler(self, func):
        self.handle = func
        return self

    # Prints stdout
    def show(self):
        print(self._result.decode("utf-8"))
        return self


# Utility function to parse strings into paths
def parse(location):
    return pathlib.PosixPath(os.path.expandvars(location)).expanduser()
