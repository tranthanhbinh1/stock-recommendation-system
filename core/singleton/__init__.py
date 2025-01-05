from abc import ABCMeta


class SingletonWrapper(object):
    """Provide wrapper for Singleton pattern implementation."""

    _instance = None

    def __new__(cls, clz, *args, **kwargs):
        if cls._instance is None:
            cls._instance = clz(*args, **kwargs)
        return cls._instance


# TODO: research and do a Thread-safe Singleton pattern here
class SingletonMeta(ABCMeta):
    """Implement Singleton pattern."""

    _instances = {}

    def existed(cls) -> bool:
        return cls._instances.get(cls, False)

    def __call__(cls, *args, **kwargs):
        """
        For testing purposes, we need to instantiate multiple
        singleton objects to use in different test cases.
        """

        if kwargs.get("force_reload"):
            cls._instances[cls] = super().__call__(*args, **kwargs)
        elif cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    pass
