# -*- coding: utf-8 -*-
"""singleton.py

This module is only used by Context to ensure the uniqueness of the global context state.
"""

class Singleton(type):
    """
    Restricts the instantiation of a class to one single instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
