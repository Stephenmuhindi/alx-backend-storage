#!/usr/bin/env python3
"""
redis cache
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    amount of func calls
    Args:
        method: func to work on
    Returns:
        worked on func
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        rapper function
        Args:
            self: The object instantiantion
            *args: first thing to write dynamically
            **kwargs: second thing to write dynamically
        Returns:
            rapper
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Number of func calls
    Args:
        method: func
    Returns:
        smart func dazzle
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        decorated function rapper
        Args:
            self: object part 1
            *args: data first one
            **kwargs: data last one
        Returns:
            decorated function value data
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    function history(lovelife)
    Args:
        method: decorated func
    Returns:
        nothing
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    """
    actual methods told to code down
    """
    def __init__(self) -> None:
        """
        redis client init
        Attributes:
            self._redis (redis.Redis): clientelle
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store redis cache data
        Args:
            data (dict): store the f*ckn data
        Returns:
            str: str()
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
        """
        Get redis cache data method
        """
        data = self._redis.get(key)
        if data is not None and fn is not None and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Get redis cache as string
        Args:
            key (str): string
        Returns:
            str: self.get()
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Get redis cache data as int
        Args:
            key (str): string
        Returns:
            int: self
        """
        data = self
