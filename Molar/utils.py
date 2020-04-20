import subprocess
from pathlib import PurePosixPath as Path
import os.path
import os

HOME = os.getenv("HOME")
PATH = os.getenv("PATH")
# !
async_off = True


# A class wrapper which does system calls and handles errors
class SafeCaller:
    def __init__(self, cwd="$HOME", err=None):
        self.err = err if err else SafeCaller.default_handler
        self.cwd = parse(cwd)

    # This is the default function called in case a call returns an error.
    @staticmethod
    def default_handler(caller, cmd):
        if input("{} was not successful, try again? [Y/n] ".format(cmd)).strip().lowercase() == "y":
            caller.call(cmd)
        else:
            exit(1)

    # The function which actually does everything.
    def call(self, *cmd):
        # This splits each argument into a list of strings separated by space,
        # then join each list into one big list.
        cmd = [x
               for arg in cmd
               for x in arg.split(" ")]

        # !TODO remove logging
        print("Running: {}".format(cmd))
        try:
            # Runs cmd at the cwd 'self.cwd'
            process = subprocess.Popen(cmd, cwd=self.cwd, env={"PATH": PATH})
            if async_off:
                process.wait()
        except subprocess.CalledProcessError:
            self.err(cmd)
        except Exception as e:
            print(e)
        return self

    # Emulates the cd command from a shell.
    def cd(self, cwd):
        self.cwd /= parse(cwd)
        return self

    # Set the error handler function
    def set_error(self, func):
        self.err = func
        return self


# Utility function to parse strings into os path
def parse(location):
    return Path(os.path.expandvars(location))


# If you need something like "echo 'thing' >> .bashrc"
def append(filepath, *args, end="\n"):
    args = [x+end for x in args]
    with open(parse(filepath), "a") as file:
        file.writelines(args)


# If you find yourself wanting to use something like "cat example >> .bashrc"
def append_from(source, target):
    source = parse(source)
    target = parse(target)
    with open(source, "r") as file:
        append(target, *file.readlines(), end="")

def setenv(key, val):
    os.environ[key] = val

