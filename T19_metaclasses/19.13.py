import random
import time


def catch_exception(f):
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            with open('exception1.txt', "w", encoding="utf-8") as f1:
                f1.write(
                    f'Exception {e.__class__.__name__} was caught in method \"{f.__name__}\" with paremeters {args}')
    return func


class ErrorCatcher(type):
    def __new__(cls, name, bases, dct):
        for m in dct:
            if hasattr(dct[m], '__call__'):
                dct[m] = catch_exception(dct[m])
        return type.__new__(cls, name, bases, dct)


class QueueEmptyError(Exception):
    def __init__(self, pname):
        self.pname = pname

    def __str__(self):

        return repr(self.pname) + ".Черга порожня."


class Queue(metaclass=ErrorCatcher):

    def __init__(self):
        self.x2 = 2
        self._lst = []

    def isempty(self):
        return len(self._lst) == 0


    def add(self, data):
        self._lst.append(data)

    def take(self):
        if self.isempty():
            raise QueueEmptyError('Take')
        data = self._lst.pop(0)
        return data

    def __del__(self):
        del self._lst



q = Queue()
m = 0
z = 5
k = 0
t1 = 5
t2 = 3
T = 6
b = 0

for i in range(m):
    k += 1
    q.add(k)


for i in range(z):
    a = random.randint(0, t2)
    time.sleep(a)
    b += a
    j = q.take()
    print(f'Покупця обслуговано {j} {time.ctime(b)}')
    c = random.randint(0, t1)
    time.sleep(c)
    b += c
    if b >= T:
        break
    k = k+1
    q.add(k)
    print(f'Додано в чергу покупця {k} {time.ctime(b)}')


print('Залишок черги')
n = 0
while not q.isempty():
    h = q.take()
    n += 1
    print(f'{n} покупців')


