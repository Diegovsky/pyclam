import pathlib as _pathlib


class ClamPath(_pathlib.PosixPath):
    """Utility class to deal with files in a shell-y way."""
    def __rrshift__(self, other) -> int:
        self.write(other, "ab")

    def __lshift__(self, other) -> int:
        self.write(other, "ab")

    def __rshift__(self, other) -> int:
        self.write_to(other, "ab")

    def __gt__(self, other) -> int:
        self.write_to(other, "wb")

    def __lt__(self, other) -> int:
        return self.write(other, "wb")

    def write_to(self, other, mode) -> int:
        """Takes content from self and writes to other.

        Parameters
        ----------
        other : ClamPath
        mode : str

        Returns
        -------
        int
            The number of bytes written.
        """
        with self.open("rb") as src:
            with other.open(mode) as target:
                return target.writelines(src.readlines())

    def write(self, other, mode) -> int:
        """Writes data to self.

        Parameters
        ----------
        other : str, ClamFile
            The value to be written.
        mode : str
            The mode used by open().

        Returns
        -------
        int
            The number of bytes written.
        """
        with self.open(mode) as file:
            if type(other) is not ClamPath:
                other = str(other).encode("utf-8")
                return file.write(other)
            else:
                return other.write_to(self, mode)

    def __new__(cls, *args, **kwargs):
        self = cls._from_parts(args, init=False)
        self._init()
        return self



