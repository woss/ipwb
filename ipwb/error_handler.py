import functools
import logging
from typing import Callable

logger = logging.getLogger('ipwb')


def exception_logger(catch=True, exception_class=Exception):
    """Decorator which catches exceptions in the function and logs them."""

    def decorator(f: Callable):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)

            except exception_class as err:
                if catch:
                    logger.critical(str(err))

                else:
                    raise

        return wrapper

    return decorator
