"""
Tests for functions in tbi.py file.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_tbi.py
# pylint --disable=locally-disabled test_tbi.py

import numpy as np
import pandas as pd
import pytest
import taxcalc as tc
from behresp import assumption_errors, run_nth_year_behresp_model, response


def test_assumption_errors():
    """
    Test assumption_error function.
    """
    behv_json = '{"BE_sub": {"2018": -0.25}}'
    behv_dict = tc.Calculator.read_json_assumptions(behv_json)
    errmsg = assumption_errors(behv_dict, 2013, 10)
    assert errmsg


def test_behavioral_response(cps_subsample):
    """
    Test that behavioral-response results are the same
    when generated from standard Behavioral-Response calls and
    when generated from tbi.run_nth_year_behresp_model() calls
    """
    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    # specify policy reform and behavioral assumptions
    reform_json = '{"policy": {"_II_em": {"2020": [1500]}}}'
    params = tc.Calculator.read_json_param_objects(reform_json, None)
    beh_json = '{"BE_sub": {"2013": 0.25}}'
    beh_dict = tc.Calculator.read_json_assumptions(beh_json)
    # specify keyword arguments used in tbi function call
    kwargs = {
        'start_year': 2019,
        'year_n': 0,
        'use_puf_not_cps': False,
        'use_full_sample': False,
        'user_mods': {
            'policy': params['policy'],
            'behavior': dict(),
            'growdiff_baseline': params['growdiff_baseline'],
            'growdiff_response': params['growdiff_response'],
            'consumption': params['consumption'],
            'growmodel': params['growmodel']
        },
        'behavior': beh_dict,
        'return_dict': False
    }
    # generate aggregate results two ways: using tbi and standard calls
    num_years = 3
    std_res = dict()
    tbi_res = dict()
    rec = tc.Records.cps_constructor(data=cps_subsample)
    for using_tbi in [True, False]:
        for year in range(0, num_years):
            cyr = year + kwargs['start_year']
            if using_tbi:
                kwargs['year_n'] = year
                tables = run_nth_year_behresp_model(**kwargs)
                tbi_res[cyr] = dict()
                for tbl in ['aggr_1', 'aggr_2', 'aggr_d']:
                    tbi_res[cyr][tbl] = tables[tbl]
            else:
                pol = tc.Policy()
                calc1 = tc.Calculator(policy=pol, records=rec)
                pol.implement_reform(params['policy'])
                assert not pol.parameter_errors
                calc2 = tc.Calculator(policy=pol, records=rec)
                calc1.advance_to_year(cyr)
                calc2.advance_to_year(cyr)
                df1, df2 = response(calc1, calc2, beh_dict)
                del calc1
                del calc2
                std_res[cyr] = dict()
                wgt = df1['s006']
                for tbl in ['aggr_1', 'aggr_2', 'aggr_d']:
                    if tbl.endswith('_1'):
                        itax = (df1['iitax'] * wgt).sum()
                        ptax = (df1['payrolltax'] * wgt).sum()
                        ctax = (df1['combined'] * wgt).sum()
                    elif tbl.endswith('_2'):
                        itax = (df2['iitax'] * wgt).sum()
                        ptax = (df2['payrolltax'] * wgt).sum()
                        ctax = (df2['combined'] * wgt).sum()
                    elif tbl.endswith('_d'):
                        itax = ((df2['iitax'] * wgt).sum() -
                                (df1['iitax'] * wgt).sum())
                        ptax = ((df2['payrolltax'] * wgt).sum() -
                                (df1['payrolltax'] * wgt).sum())
                        ctax = ((df2['combined'] * wgt).sum() -
                                (df1['combined'] * wgt).sum())
                    cols = ['0_{}'.format(year)]
                    rows = ['ind_tax', 'payroll_tax', 'combined_tax']
                    datalist = [itax, ptax, ctax]
                    std_res[cyr][tbl] = pd.DataFrame(data=datalist,
                                                     index=rows,
                                                     columns=cols)
                    for col in std_res[cyr][tbl].columns:
                        val = std_res[cyr][tbl][col] * 1e-9
                        std_res[cyr][tbl][col] = round(val, 3)
    # compare the two sets of results
    no_diffs = True
    dumping = False  # setting to True produces dump output and test failure
    reltol = 1e-9  # std and tbi should be virtually identical
    for year in range(0, num_years):
        cyr = year + kwargs['start_year']
        do_dump = bool(dumping and cyr >= 2019 and cyr <= 2020)
        col = '0_{}'.format(year)
        for tbl in ['aggr_1', 'aggr_2', 'aggr_d']:
            tbi = tbi_res[cyr][tbl][col]
            if do_dump:
                txt = 'DUMP of CPS {} table for year {}:'
                print(txt.format(tbl, cyr))
                print(tbi)
            std = std_res[cyr][tbl][col]
            if not np.allclose(tbi, std, atol=0.0, rtol=reltol):
                no_diffs = False
                txt = '***** CPS diff in {} table for year {} (year_n={}):'
                print(txt.format(tbl, cyr, year))
                print('TBI RESULTS:')
                print(tbi)
                print('STD RESULTS:')
                print(std)
    assert no_diffs
    assert not dumping


@pytest.mark.requires_pufcsv
def test_fuzzing_and_returning_dict():
    """
    Test returning of non-JSON PUF results from run_nth_year_behresp_model().
    """
    # specify policy reform and behavioral assumptions
    reform_json = '{"policy": {"_II_em": {"2020": [1500]}}}'
    params = tc.Calculator.read_json_param_objects(reform_json, None)
    beh_json = '{"BE_sub": {"2013": 0.25}}'
    beh_dict = tc.Calculator.read_json_assumptions(beh_json)
    # specify keyword arguments used in tbi function call
    kwargs = {
        'start_year': 2020,
        'year_n': 0,
        'use_puf_not_cps': True,
        'use_full_sample': False,
        'user_mods': {
            'policy': params['policy'],
            'behavior': dict(),
            'growdiff_baseline': params['growdiff_baseline'],
            'growdiff_response': params['growdiff_response'],
            'consumption': params['consumption'],
            'growmodel': params['growmodel']
        },
        'behavior': beh_dict,
        'return_dict': True
    }
    # call run_nth_year_behresp_model function
    tables = run_nth_year_behresp_model(**kwargs)
    assert isinstance(tables, dict)
