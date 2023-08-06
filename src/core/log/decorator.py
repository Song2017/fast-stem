import functools
import os
import time

DEBUG = bool(os.getenv("DEBUG") or "")


def req_log(show_req=False, show_resp=True):
    def decorator(caller: callable):
        @functools.wraps(caller)
        def inner_call(*args, **kwargs):
            print(f"begin time: {time.ctime()}, func {caller.__name__}")
            if show_req or DEBUG:
                print(f"parameter: {args, kwargs}")

            result = caller(*args, **kwargs)

            if show_resp or DEBUG:
                print(f"end time: {time.ctime()}, result {str(result)[:10]}")
            return result

        return inner_call

    return decorator


if __name__ == '__main__':
    @req_log(show_resp=False)
    def test(arg1, arg2, arg3):
        print("tests function", arg1, arg2, arg3)


    test('arg1', 2, arg3=3)
