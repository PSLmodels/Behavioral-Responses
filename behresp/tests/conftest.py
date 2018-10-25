import os
import numpy
import pandas as pd
import pytest
import taxcalc as tc


# convert all numpy warnings into errors so they can be detected in tests
numpy.seterr(all='raise')


@pytest.fixture(scope='session')
def tests_path():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture(scope='session')
def cps_fullsample():
    return tc.Records.read_cps_data()


@pytest.fixture(scope='session')
def cps_subsample(cps_fullsample):
    # draw same subsample as used in taxcalc.tbi.calculators()
    return cps_fullsample.sample(frac=0.03, random_state=180)
