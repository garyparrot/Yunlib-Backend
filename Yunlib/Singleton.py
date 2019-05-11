import functools
import threading

lock = threading.Lock()

def synchronized(lock):
    def wrapper(f):
        @functools.wraps(f)
        def inner_wrapper(*args, **kwargs):
            with lock:
                return f(*args,**kwargs)
        return inner_wrapper
    return  wrapper

class Singleton(type):
    _instances = {}

    @synchronized(lock)
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


