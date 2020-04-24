import pathlib as _pathlib
import os as _os


class ClamPath(_pathlib.PosixPath):
    """Utility class to deal with files in a shell-y way"""
    def __rrshift__(self, other):
        self._write(other, "ab")

    def __lshift__(self, other):
        self.__rrshift__(other)

    # def __rshift__(self, other):
    #     self._write_to(other, "ab")

    def __gt__(self, other):
        self._write_to(other, "wb")

    def __lt__(self, other):
        return self._write(other, "wb")

    def _write_to(self, other, mode):
        if not issubclass(tp := type(other), ClamPath):
            raise TypeError("Did not expect", tp)
        with self.open("rb") as src:
            with other.open(mode) as target:
                return target.writelines(src.readlines())

    def _write(self, other, mode):
        if self.is_file():
            with self.open(mode) as file:
                if type(other) is not ClamPath:
                    other = str(other).encode("utf-8")
                    return file.write(other)
                else:
                    other._write_to(other, mode)
        else:
            raise IOError("The path '{}' is not a file!".format(self.__str__()))

    def __new__(cls, *args, **kwargs):
        print(args)
        self = cls._from_parts(args, init=False)
        self._init()
        return self
        # super().__init__(_os.path.expandvars(filepath))
        # self = self.expanduser()

    def __init__(self, cu):
        print(cu)


if __name__ == '__main__':
    f1 = ClamPath("test.txt")
    f2 = ClamPath("res.txt")
    f1 >> f2
