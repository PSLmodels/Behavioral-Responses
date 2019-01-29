"""
Tests for functions in behavior.py file.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_behavior.py
# pylint --disable=locally-disabled test_behavior.py

import numpy as np
import pandas as pd
import taxcalc as tc
from behresp import PARAM_INFO, response


def test_param_info():
    """
    Test structure and content of PARAM_INFO dictionary.
    """
    # ensure PARAM_INFO has correct keys
    actkeys = set(PARAM_INFO.keys())
    expkeys = set(['BE_sub', 'BE_inc', 'BE_cg'])
    assert actkeys == expkeys
    for pname in PARAM_INFO:
        pdict = PARAM_INFO[pname]
        # ensure that minimum_value no less than maximum_value
        assert pdict['minimum_value'] <= pdict['maximum_value']
        # ensure that default_value is in [minimum_value,maximum_value] range
        assert pdict['default_value'] >= pdict['minimum_value']
        assert pdict['default_value'] <= pdict['maximum_value']


def test_response_function(cps_subsample):
    """
    Test response function.
    """
    # pylint: disable=too-many-locals,too-many-statements

    rec = tc.Records.cps_constructor(data=cps_subsample)

    refyear = 2020
    reform = {refyear: {'_II_em': [1500]}}

    behx_json = """{
    "BE_sub": {"2018": 0.25},
    "BE_inc": {"2018": -0.1},
    "BE_cg": {"2018": -0.79}
    }"""
    behy_json = """{
    "_BE_sub": {"2018": [0.25]},
    "_BE_inc": {"2018": [-0.1]},
    "_BE_cg": {"2018": [-0.79]}
    }"""

    # use new behresp response function for x results
    behx_dict = tc.Calculator.read_json_assumptions(behx_json)
    pol = tc.Policy()
    calc1x = tc.Calculator(records=rec, policy=pol)
    pol.implement_reform(reform)
    calc2x = tc.Calculator(records=rec, policy=pol)
    del pol
    calc1x.advance_to_year(refyear)
    calc2x.advance_to_year(refyear)
    df1, df2 = response(calc1x, calc2x, behx_dict, trace=True)
    del calc1x
    del calc2x
    itax1x = round((df1['iitax'] * df1['s006']).sum() * 1e-9, 3)
    itax2x = round((df2['iitax'] * df2['s006']).sum() * 1e-9, 3)
    del df1
    del df2
    assert np.allclose([itax1x, itax2x], [1422.156, 1368.489])

    # use old taxcalc Behavior class for y results
    behy_dict = tc.Calculator.read_json_assumptions(behy_json)
    behy_obj = tc.Behavior()
    behy_obj.update_behavior(behy_dict)
    pol = tc.Policy()
    calc1y = tc.Calculator(records=rec, policy=pol)
    pol.implement_reform(reform)
    calc2y = tc.Calculator(records=rec, policy=pol, behavior=behy_obj)
    del pol
    calc1y.advance_to_year(refyear)
    calc2y.advance_to_year(refyear)
    calc2y_behv = tc.Behavior.response(calc1y, calc2y, trace=True)
    itax1y = round(calc1y.weighted_total('iitax') * 1e-9, 3)
    itax2y = round(calc2y_behv.weighted_total('iitax') * 1e-9, 3)
    del calc1y
    del calc2y
    assert np.allclose([itax1y, itax2y], [itax1x, itax2x])

    # test that default behavioral parameters produce static results
    beh_dict = tc.Calculator.read_json_assumptions('{}')
    pol = tc.Policy()
    calc1x = tc.Calculator(records=rec, policy=pol)
    pol.implement_reform(reform)
    calc2x = tc.Calculator(records=rec, policy=pol)
    calc1x.advance_to_year(refyear)
    calc2x.advance_to_year(refyear)
    df1, df2 = response(calc1x, calc2x, beh_dict)
    del calc1x
    del calc2x
    itax1n = round((df1['iitax'] * df1['s006']).sum() * 1e-9, 3)
    itax2n = round((df2['iitax'] * df2['s006']).sum() * 1e-9, 3)
    del df1
    del df2
    calc2s = tc.Calculator(records=rec, policy=pol)
    del pol
    calc2s.advance_to_year(refyear)
    calc2s.calc_all()
    itax2s = round(calc2s.weighted_total('iitax') * 1e-9, 3)
    del calc2s
    assert np.allclose([itax1n, itax2n], [itax1x, itax2s])

    # different behavior parameters to improve code coverage
    beh_dict = tc.Calculator.read_json_assumptions(
        '{"BE_inc": {"2018": -0.10}}'
    )
    pol = tc.Policy()
    calc1x = tc.Calculator(records=rec, policy=pol)
    pol.implement_reform(reform)
    calc2x = tc.Calculator(records=rec, policy=pol)
    del pol
    calc1x.advance_to_year(refyear)
    calc2x.advance_to_year(refyear)
    df1, df2 = response(calc1x, calc2x, beh_dict, trace=True)
    del calc1x
    del calc2x
    assert isinstance(df1, pd.DataFrame)
    assert isinstance(df2, pd.DataFrame)
    del df1
    del df2
