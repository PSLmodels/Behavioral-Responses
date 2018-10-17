"""
Specify what is available to import from the behavioral-responses package.
"""
from behavioral-responses.behavior import *

from behavioral-responses._version import get_versions
__version__ = get_versions()['version']
del get_versions
