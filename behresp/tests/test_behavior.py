"""
Tests for functions in behavior.py file.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_behavior.py
# pylint --disable=locally-disabled test_behavior.py

from io import StringIO
import numpy as np
import pandas as pd
import taxcalc as tc
from behresp import PARAM_INFO, response, quantity_response


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


def test_default_response_function(cps_subsample):
    """
    Test that default behavior parameters produce static results.
    """
    # ... specify Records object and policy reform
    rec = tc.Records.cps_constructor(data=cps_subsample)
    refyear = 2020
    assert refyear >= 2018
    reform = {refyear: {'_II_em': [1500]}}
    # ... construct pre-reform calculator
    pol = tc.Policy()
    calc1 = tc.Calculator(records=rec, policy=pol)
    calc1.advance_to_year(refyear)
    # ... construct two post-reform calculators
    pol.implement_reform(reform)
    calc2s = tc.Calculator(records=rec, policy=pol)  # for static assumptions
    calc2s.advance_to_year(refyear)
    calc2d = tc.Calculator(records=rec, policy=pol)  # for default behavior
    calc2d.advance_to_year(refyear)
    del pol
    # ... calculate aggregate inctax using static assumptions
    calc2s.calc_all()
    df2s = calc2s.dataframe(['iitax', 's006'])
    itax2s = round((df2s['iitax'] * df2s['s006']).sum() * 1e-9, 3)
    # ... calculate aggregate inctax using default behavior assumptions
    default_beh_dict = tc.Calculator.read_json_assumptions('{}')
    _, df2d = response(calc1, calc2d, default_beh_dict, dump=True)
    itax2d = round((df2d['iitax'] * df2d['s006']).sum() * 1e-9, 3)
    assert np.allclose(itax2d, itax2s)
    # ... clean up
    del calc1
    del calc2s
    del calc2d
    del df2s
    del df2d


def test_nondefault_response_function(cps_subsample):
    """
    Test that non-default behavior parameters produce expected results.
    """
    # ... specify Records object and policy reform
    rec = tc.Records.cps_constructor(data=cps_subsample)
    refyear = 2020
    assert refyear >= 2018
    reform = {refyear: {'_II_em': [1500]}}
    # ... specify non-default behavior assumptions
    beh_json = """{
    "BE_sub": {"2018": 0.25},
    "BE_inc": {"2018": -0.1},
    "BE_cg": {"2018": -0.79}
    }"""
    beh_dict = tc.Calculator.read_json_assumptions(beh_json)
    # ... calculate behavioral response to reform
    pol = tc.Policy()
    calc1 = tc.Calculator(records=rec, policy=pol)
    pol.implement_reform(reform)
    calc2 = tc.Calculator(records=rec, policy=pol)
    del pol
    calc1.advance_to_year(refyear)
    calc2.advance_to_year(refyear)
    df1, df2 = response(calc1, calc2, beh_dict)
    del calc1
    del calc2
    itax1 = round((df1['iitax'] * df1['s006']).sum() * 1e-9, 3)
    itax2 = round((df2['iitax'] * df2['s006']).sum() * 1e-9, 3)
    del df1
    del df2
    assert np.allclose([itax1, itax2], [1422.156, 1368.489])


def test_alternative_behavior_parameters(cps_subsample):
    """
    Test alternative behavior parameters to improve code coverage.
    Also, test response function's dump argument.
    """
    # ... specify Records object and policy reform
    rec = tc.Records.cps_constructor(data=cps_subsample)
    refyear = 2020
    assert refyear >= 2018
    reform = {refyear: {'_II_em': [1500]}}
    # ... specify alternative set of behavior parameters
    beh_dict = tc.Calculator.read_json_assumptions(
        '{"BE_inc": {"2018": -0.10}}'
    )
    # ... use the alternative behavior parameters and dump option
    pol = tc.Policy()
    calc1 = tc.Calculator(records=rec, policy=pol)
    pol.implement_reform(reform)
    calc2 = tc.Calculator(records=rec, policy=pol)
    del pol
    calc1.advance_to_year(refyear)
    calc2.advance_to_year(refyear)
    df1, df2 = response(calc1, calc2, beh_dict, dump=True)
    del calc1
    del calc2
    assert isinstance(df1, pd.DataFrame)
    assert isinstance(df2, pd.DataFrame)
    assert len(df1.index) == len(df2.index)
    assert len(df1.index) > len(tc.DIST_VARIABLES)
    del df1
    del df2


def test_sub_effect_independence():
    """
    Ensure that LTCG amount does not affect magnitude of substitution effect.
    """
    # specify reform that raises top-bracket marginal tax rate
    refyear = 2020
    reform = {refyear: {'_II_rt7': [0.70]}}
    # specify a substitution effect behavioral response
    beh_json = """{
    "BE_sub": {"2013": 0.25}
    }"""
    # specify input consisting of two filing units with high earnings, but
    # with one having large long-term capital gains and the other having
    # no long-term capital gains
    input_csv = (u'RECID,MARS,e00200,e00200p,p23250\n'
                 u'1,1,1000000,1000000,500000\n'
                 u'2,1,1000000,1000000,0\n')
    recs = tc.Records(data=pd.read_csv(StringIO(input_csv)),
                      start_year=refyear,
                      gfactors=None, weights=None)
    beh_dict = tc.Calculator.read_json_assumptions(beh_json)
    pol = tc.Policy()
    calc1 = tc.Calculator(records=recs, policy=pol)
    assert calc1.current_year == refyear
    pol.implement_reform(reform)
    calc2 = tc.Calculator(records=recs, policy=pol)
    assert calc2.current_year == refyear
    del pol
    df1, df2 = response(calc1, calc2, beh_dict)
    del calc1
    del calc2
    # compute change in taxable income for each of the two filing units
    chg_funit1 = df2['c04800'][0] - df1['c04800'][0]  # funit with RECID=1
    chg_funit2 = df2['c04800'][1] - df1['c04800'][1]  # funit with RECID=2
    del df1
    del df2
    # confirm reform reduces taxable income when assuming substitution effect
    assert chg_funit1 < 0
    assert chg_funit2 < 0
    # confirm change in taxable income is same for the two filing units
    assert np.allclose(chg_funit1, chg_funit2)
    del chg_funit1
    del chg_funit2


def test_quantity_response():
    """
    Test quantity_response function.
    """
    quantity = np.array([1.0] * 10)
    res = quantity_response(quantity,
                            price_elasticity=0,
                            aftertax_price1=None,
                            aftertax_price2=None,
                            income_elasticity=0,
                            aftertax_income1=None,
                            aftertax_income2=None)
    assert np.allclose(res, np.zeros(quantity.shape))
    one = np.ones(quantity.shape)
    res = quantity_response(quantity,
                            price_elasticity=-0.2,
                            aftertax_price1=one,
                            aftertax_price2=one,
                            income_elasticity=0.1,
                            aftertax_income1=one,
                            aftertax_income2=(one + one))
    assert not np.allclose(res, np.zeros(quantity.shape))
