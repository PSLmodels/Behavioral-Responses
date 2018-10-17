"""
Partial-equilibrium elasticity-based Behavioral-Responses logic.
"""
# CODING-STYLE CHECKS:
# pycodestyle behavior.py
# pylint --disable=locally-disabled behavior.py

import copy
import numpy as np
import taxcalc as tc


def response(calc1, calc2, trace=False):
    """
    Implements TaxBrain "Partial Equilibrium Simulation" dynamic analysis.

    Modify calc2 records to account for behavioral responses that arise
      from the policy reform that involves moving from calc1 policy to
      calc2 policy.  Neither calc1 nor calc2 need to have had calc_all()
      executed before calling the response(calc1, calc2) function.
    Returns new Calculator object --- a deepcopy of calc2 --- that
      incorporates behavioral responses to the reform.
    Note: the use here of a dollar-change income elasticity (rather than
      a proportional-change elasticity) is consistent with Feldstein and
      Feenberg, "The Taxation of Two Earner Families", NBER Working Paper
      No. 5155 (June 1995).  A proportional-change elasticity was used by
      Gruber and Saez, "The elasticity of taxable income: evidence and
      implications", Journal of Public Economics 84:1-32 (2002) [see
      equation 2 on page 10].
    Note: the nature of the capital-gains elasticity used here is similar
      to that used in Joint Committee on Taxation, "New Evidence on the
      Tax Elasticity of Capital Gains: A Joint Working Paper of the Staff
      of the Joint Committee on Taxation and the Congressional Budget
      Office", (JCX-56-12), June 2012.  In particular, the elasticity
      use here is equivalent to the term inside the square brackets on
      the right-hand side of equation (4) on page 11 --- not the epsilon
      variable on the left-hand side of equation (4), which is equal to
      the elasticity used here times the weighted average marginal tax
      rate on long-term capital gains.  So, the JCT-CBO estimate of
      -0.792 for the epsilon elasticity (see JCT-CBO, Table 5) translates
      into a much larger absolute value for the _BE_cg semi-elasticity
      used by Tax-Calculator.
      To calculate the elasticity from a semi-elasticity, we multiply by
      MTRs from TC and weight by shares of taxable gains. To avoid those
      with zero MTRs, we restrict this to the top 40% of tax units by AGI.
      Using this function, a semi-elasticity of -3.45 corresponds to a tax
      rate elasticity of -0.792.
    """
    # pylint: disable=too-many-statements,too-many-locals,too-many-branches

    # nested function used only in response
    def trace_output(varname, variable, histbins, pweight, dweight):
        """
        Print trace output for specified variable.
        """
        print('*** TRACE for variable {}'.format(varname))
        hist = np.histogram(variable, bins=histbins)
        print('*** Histogram:')
        print(hist[0])
        print(hist[1])
        if pweight.sum() != 0:
            out = '*** Person-weighted mean= {:.2f}'
            mean = (variable * pweight).sum() / pweight.sum()
            print(out.format(mean))
        if dweight.sum() != 0:
            out = '*** Dollar-weighted mean= {:.2f}'
            mean = (variable * dweight).sum() / dweight.sum()
            print(out.format(mean))

    # begin main logic of response function
    assert calc1.array_len == calc2.array_len
    assert calc1.current_year == calc2.current_year
    mtr_cap = 0.99
    # calculate sum of substitution and income effects
    if calc2.behavior('BE_sub') == 0.0 and calc2.behavior('BE_inc') == 0.0:
        zero_sub_and_inc = True
    else:
        zero_sub_and_inc = False
        # calculate marginal combined tax rates on taxpayer wages+salary
        # (e00200p is taxpayer's wages+salary)
        wage_mtr1, wage_mtr2 = Behavior._mtr12(calc1, calc2,
                                               mtr_of='e00200p',
                                               tax_type='combined')
        # calculate magnitude of substitution effect
        if calc2.behavior('BE_sub') == 0.0:
            sub = np.zeros(calc1.array_len)
        else:
            # proportional change in marginal net-of-tax rates on earnings
            mtr1 = np.where(wage_mtr1 > mtr_cap, mtr_cap, wage_mtr1)
            mtr2 = np.where(wage_mtr2 > mtr_cap, mtr_cap, wage_mtr2)
            pch = ((1. - mtr2) / (1. - mtr1)) - 1.
            # Note: c04800 is filing unit's taxable income
            sub = (calc2.behavior('BE_sub') *
                   pch * calc1.array('c04800'))
            if trace:
                trace_output('wmtr1', wage_mtr1,
                             [-9e99, 0.00, 0.25, 0.50, 0.60,
                              0.70, 0.80, 0.90, 0.999999, 1.1,
                              1.2, 1.3, 9e99],
                             calc1.array('s006'),
                             np.zeros(calc1.array_len))
                print('high wage_mtr1:',
                      wage_mtr1[wage_mtr1 > 0.999999])
                print('wage_mtr2 them:',
                      wage_mtr2[wage_mtr1 > 0.999999])
                trace_output('pch', pch,
                             [-9e99, -1.00, -0.50, -0.20, -0.10,
                              -0.00001, 0.00001,
                              0.10, 0.20, 0.50, 1.00, 9e99],
                             calc1.array('s006'),
                             calc1.array('c04800'))
                trace_output('sub', sub,
                             [-9e99, -1e3,
                              -0.1, 0.1,
                              1e3, 1e4, 1e5, 1e6, 9e99],
                             calc1.array('s006'),
                             np.zeros(calc1.array_len))
        # calculate magnitude of income effect
        if calc2.behavior('BE_inc') == 0.0:
            inc = np.zeros(calc1.array_len)
        else:
            # dollar change in after-tax income
            # Note: combined is f.unit's income+payroll tax liability
            dch = calc1.array('combined') - calc2.array('combined')
            inc = calc2.behavior('BE_inc') * dch
        # calculate sum of substitution and income effects
        si_chg = sub + inc
    # calculate long-term capital-gains effect
    if calc2.behavior('BE_cg') == 0.0:
        ltcg_chg = np.zeros(calc1.array_len)
    else:
        # calculate marginal tax rates on long-term capital gains
        #  p23250 is filing units' long-term capital gains
        ltcg_mtr1, ltcg_mtr2 = Behavior._mtr12(calc1, calc2,
                                               mtr_of='p23250',
                                               tax_type='iitax')
        rch = ltcg_mtr2 - ltcg_mtr1
        exp_term = np.exp(calc2.behavior('BE_cg') * rch)
        new_ltcg = calc1.array('p23250') * exp_term
        ltcg_chg = new_ltcg - calc1.array('p23250')
    # Add behavioral-response changes to income sources
    calc2_behv = copy.deepcopy(calc2)
    if not zero_sub_and_inc:
        calc2_behv = Behavior._update_ordinary_income(si_chg,
                                                      calc2_behv)
    calc2_behv = Behavior._update_cap_gain_income(ltcg_chg,
                                                  calc2_behv)
    # Recalculate post-reform taxes incorporating behavioral responses
    calc2_behv.calc_all()
    calc2_behv.records_include_behavioral_responses()
    return calc2_behv


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
    check_years_return_first_year(year_n, start_year, use_puf_not_cps)
    calc1, calc2 = calculate(year_n, start_year,
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
