import os
import pickle
import functools

import constants


def file_cache():
    def decorator(method):
        if not os.path.exists(constants.CACHE_DIR):
            os.mkdir(constants.CACHE_DIR)

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            filename = os.path.join(
                constants.CACHE_DIR, f"{self.__class__.__name__}_{method.__name__}.pkl"
            )

            if os.path.exists(filename):
                with open(filename, "rb") as f:
                    result = pickle.load(f)

                return result
            else:
                result = method(self, *args, **kwargs)

                with open(filename, "wb") as f:
                    pickle.dump(result, f)

                return result

        return wrapper

    return decorator
