class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


if __name__ == '__main__':
    class Test(metaclass=Singleton):
        val = 1


    class Test3(Test):
        val = 1


    class Test2(metaclass=Singleton):
        val = 1


    test1 = Test()
    test12 = Test()
    test2 = Test2()
    test3 = Test3()
    print(id(test1), id(test12), id(test2), id(test3))
