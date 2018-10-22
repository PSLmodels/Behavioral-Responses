"""
Specify what is available to import from the behresp package.
"""
from behresp.behavior import PARAM_INFO, response
from behresp.tbi import run_nth_year_behresp_model

from behresp._version import get_versions
__version__ = get_versions()['version']
del get_versions
