
def log(func):
    def wrapper(*args, **kwargs):
        print(args)
        return func(*args, **kwargs)
    return wrapper()

class t:
    def __init__(self, i):
        self.i = i

    def __rshift__(self, l):
        print("rshift")
        self.i = l
        return l

    def __str__(self):
        return "{{i:{}}}".format(self.i)

    def __rrshift__(self, other):
        print("rrshift")
        return 0

    def __int__(self):
        return int(self.i)

    def __gt__(self, other):
        pass

    def __lt__(self, other):
        pass


if __name__ == '__main__':
    l = t(90)
    l >> t(80)

