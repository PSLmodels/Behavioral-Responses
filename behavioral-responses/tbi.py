"""
Partial-equilibrium elasticity-based Behavioral-Responses results
returned as expected by TaxBrain.
"""
# CODING-STYLE CHECKS:
# pycodestyle tbi.py
# pylint --disable=locally-disabled tbi.py

import copy
import numpy as np
import taxcalc as tc
from behavioral-response.behavior import response


def run_nth_year_behresp_model(year_n, start_year,
                               use_puf_not_cps,
                               use_full_sample,
                               elasticity,
                               return_dict=True):
    """
    Returns behavioral-response results as expected by TaxBrain.

    The run_nth_year_behresp_model function assumes elasticity is a dictionary
      containing the assumed values of the behavioral-responses elasticities.
    Setting use_puf_not_cps=True implies use puf.csv input file;
      otherwise, use cps.csv input file.
    Setting use_full_sample=False implies use sub-sample of input file;
      otherwsie, use the complete sample.
    """
    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches

    start_time = time.time()

    # create calc1 and calc2 calculated for year_n
    check_years(year_n, start_year, use_puf_not_cps)
    calc1, calc2 = calculator_objects(year_n, start_year,
                                      use_puf_not_cps, use_full_sample,
                                      user_mods,
                                      behavior_allowed=True)

    # extract unfuzzed raw results from calc1 and calc2
    dv1 = calc1.distribution_table_dataframe()
    dv2 = calc2.distribution_table_dataframe()

    # delete calc1 and calc2 now that raw results have been extracted
    del calc1
    del calc2

    # construct TaxBrain summary results from raw results
    sres = dict()
    fuzzing = use_puf_not_cps
    if fuzzing:
        # seed random number generator with a seed value based on user_mods
        # (reform-specific seed is used to choose whose results are fuzzed)
        seed = random_seed(user_mods)
        print('fuzzing_seed={}'.format(seed))
        np.random.seed(seed)  # pylint: disable=no-member
        # make bool array marking which filing units are affected by the reform
        reform_affected = np.logical_not(  # pylint: disable=no-member
            np.isclose(dv1['combined'], dv2['combined'], atol=0.01, rtol=0.0)
        )
        agg1, agg2 = fuzzed(dv1, dv2, reform_affected, 'aggr')
        sres = summary_aggregate(sres, agg1, agg2)
        del agg1
        del agg2
        dv1b, dv2b = fuzzed(dv1, dv2, reform_affected, 'xbin')
        sres = summary_dist_xbin(sres, dv1b, dv2b)
        sres = summary_diff_xbin(sres, dv1b, dv2b)
        del dv1b
        del dv2b
        dv1d, dv2d = fuzzed(dv1, dv2, reform_affected, 'xdec')
        sres = summary_dist_xdec(sres, dv1d, dv2d)
        sres = summary_diff_xdec(sres, dv1d, dv2d)
        del dv1d
        del dv2d
        del reform_affected
    else:
        sres = summary_aggregate(sres, dv1, dv2)
        sres = summary_dist_xbin(sres, dv1, dv2)
        sres = summary_diff_xbin(sres, dv1, dv2)
        sres = summary_dist_xdec(sres, dv1, dv2)
        sres = summary_diff_xdec(sres, dv1, dv2)

    # nested function used below
    def append_year(dframe):
        """
        append_year embedded function revises all column names in dframe
        """
        dframe.columns = [str(col) + '_{}'.format(year_n)
                          for col in dframe.columns]
        return dframe

    # optionally return non-JSON-like results
    if not return_dict:
        res = dict()
        for tbl in sres:
            res[tbl] = append_year(sres[tbl])
        elapsed_time = time.time() - start_time
        print('elapsed time for this run: {:.1f}'.format(elapsed_time))
        return res

    # optionally construct JSON-like results dictionaries for year n
    dec_rownames = list(sres['diff_comb_xdec'].index.values)
    dec_row_names_n = [x + '_' + str(year_n) for x in dec_rownames]
    bin_rownames = list(sres['diff_comb_xbin'].index.values)
    bin_row_names_n = [x + '_' + str(year_n) for x in bin_rownames]
    agg_row_names_n = [x + '_' + str(year_n) for x in AGG_ROW_NAMES]
    dist_column_types = [float] * len(DIST_TABLE_LABELS)
    diff_column_types = [float] * len(DIFF_TABLE_LABELS)
    info = dict()
    for tbl in sres:
        info[tbl] = {'row_names': [], 'col_types': []}
        if 'dec' in tbl:
            info[tbl]['row_names'] = dec_row_names_n
        elif 'bin' in tbl:
            info[tbl]['row_names'] = bin_row_names_n
        else:
            info[tbl]['row_names'] = agg_row_names_n
        if 'dist' in tbl:
            info[tbl]['col_types'] = dist_column_types
        elif 'diff' in tbl:
            info[tbl]['col_types'] = diff_column_types
    res = dict()
    for tbl in sres:
        if 'aggr' in tbl:
            res_table = create_dict_table(sres[tbl],
                                          row_names=info[tbl]['row_names'])
            res[tbl] = dict((k, v[0]) for k, v in res_table.items())
        else:
            res[tbl] = create_dict_table(sres[tbl],
                                         row_names=info[tbl]['row_names'],
                                         column_types=info[tbl]['col_types'])

    elapsed_time = time.time() - start_time
    print('elapsed time for this run: {:.1f}'.format(elapsed_time))

    return res


# ----- begin private functions -----


def _update_ordinary_income(taxinc_change, calc):
    """
    Implement total taxable income change induced by behavioral response.
    """
    # compute AGI minus itemized deductions, agi_m_ided
    agi = calc.array('c00100')
    ided = np.where(calc.array('c04470') < calc.array('standard'),
                    0., calc.array('c04470'))
    agi_m_ided = agi - ided
    # assume behv response only for filing units with positive agi_m_ided
    pos = np.array(agi_m_ided > 0., dtype=bool)
    delta_income = np.where(pos, taxinc_change, 0.)
    # allocate delta_income into three parts
    winc = calc.array('e00200')
    delta_winc = np.zeros_like(agi)
    delta_winc[pos] = delta_income[pos] * winc[pos] / agi_m_ided[pos]
    oinc = agi - winc
    delta_oinc = np.zeros_like(agi)
    delta_oinc[pos] = delta_income[pos] * oinc[pos] / agi_m_ided[pos]
    delta_ided = np.zeros_like(agi)
    delta_ided[pos] = delta_income[pos] * ided[pos] / agi_m_ided[pos]
    # confirm that the three parts are consistent with delta_income
    assert np.allclose(delta_income, delta_winc + delta_oinc - delta_ided)
    # add the three parts to different records variables embedded in calc
    calc.incarray('e00200', delta_winc)
    calc.incarray('e00200p', delta_winc)
    calc.incarray('e00300', delta_oinc)
    calc.incarray('e19200', delta_ided)
    return calc


def _update_cap_gain_income(cap_gain_change, calc):
    """
    Implement capital gain change induced by behavioral responses.
    """
    calc.incarray('p23250', cap_gain_change)
    return calc


def _mtr12(calc1, calc2, mtr_of='e00200p', tax_type='combined'):
    """
    Computes marginal tax rates for Calculator objects calc1 and calc2
    for specified mtr_of income type and specified tax_type.
    """
    _, iitax1, combined1 = calc1.mtr(mtr_of, wrt_full_compensation=True)
    _, iitax2, combined2 = calc2.mtr(mtr_of, wrt_full_compensation=True)
    if tax_type == 'combined':
        return (combined1, combined2)
    elif tax_type == 'iitax':
        return (iitax1, iitax2)
    else:
        raise ValueError('tax_type must be "combined" or "iitax"')
