import io as _io
import pathlib as _pathlib

class ClamFile:
    """Utility class to deal with files in a shell-y way"""

   def __init__(self, filename, cwd=""):
       if cwd is str:
          filename =
       self.filename = filename

    def __lshift__(self, other):
        if type(other) == str:
            self.write(other.encode("utf-8"))
        if isinstance(other, [_io.BufferedIOBase]):
            self.file.writelines(other.readlines())


if __name__ == '__main__':
    f = ClamFile("test.txt")
    f.write(b"test")
    f << "rshift"
