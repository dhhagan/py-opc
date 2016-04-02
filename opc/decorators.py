"""
"""

from functools import wraps
from .exceptions import FirmwareVersionError

def requires_firmware(major):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if float(args[0].firmware['version']) < float(major):
                raise FirmwareVersionError("Testing decorator errors...")

            return f(*args, **kwargs)
        return decorated_function
    return decorator
