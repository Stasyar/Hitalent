import asyncio
import inspect
from datetime import datetime
from functools import wraps


def decorator(count):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            start = datetime.now()
            for _ in range(count):
                res = func(*args, **kwargs)
            time_res = datetime.now() - start
            print(f"func name: {func.__name__}, time: {time_res}")
            return res

        @wraps(func)
        async def async_wrapped(*args, **kwargs):
            start = datetime.now()
            for _ in range(count):
                res = await func(*args, **kwargs)
            time_res = datetime.now() - start
            print(f"func name: {func.__name__}, time: {time_res}")
            return res

        if inspect.iscoroutinefunction(func):
            return async_wrapped
        else:
            return wrapped

    return wrapper


@decorator(count=3)
def foo(x, y):
    return x ** y


@decorator(count=3)
async def async_foo(x, y):
    return x ** y


print(foo.__name__)
print(foo(5, 5))

print(async_foo.__name__)
print(asyncio.run(async_foo(5, 5)))