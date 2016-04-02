from functools import wraps
from .exceptions import FirmwareVersionError

def requires_firmware(major):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if float(args[0].firmware['version']) < float(major):
                msg = """Your current firmware ({}) does not support this method.
                    Firmware v{} is required.""".format(args[0].firmware['version'], major)

                raise FirmwareVersionError(msg)

            return f(*args, **kwargs)
        return decorated_function
    return decorator
