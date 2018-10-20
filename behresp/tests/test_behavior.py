"""
Tests for functions in behavior.py file.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_behavior.py
# pylint --disable=locally-disabled test_behavior.py

import os
import json
import numpy as np
import pytest
# TODO: import taxcalc as tc
from behresp import PARAM_INFO, response

@pytest.mark.one
def test_param_info():
    """
    Test structure and content of PARAM_INFO dictionary.
    """
    # ensure PARAM_INFO has correct keys
    actkeys = set(PARAM_INFO.keys())
    expkeys = set(['BE_sub', 'BE_inc', 'BE_cg'])
    assert actkeys == expkeys
    for pname in PARAM_INFO.keys():
        pdict = PARAM_INFO[pname]
        # ensure that minimum_value no less than maximum_value
        assert pdict['minimum_value'] <= pdict['maximum_value']
        # ensure that default_value is in [minimum_value,maximum_value] range
        assert pdict['default_value'] >= pdict['minimum_value']
        assert pdict['default_value'] <= pdict['maximum_value']
