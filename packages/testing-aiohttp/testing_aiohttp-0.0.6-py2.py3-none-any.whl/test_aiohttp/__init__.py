_version = "0.0.6"
__version__ = VERSION = tuple(map(int, _version.split('.')))


from .rsps import RouteManager, RouteNotCalledError, RouteNotFoundError  # noqa
from .testcases import AioLoopTestCase  # noqa
