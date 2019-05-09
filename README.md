[![PSL cataloged](https://img.shields.io/badge/PSL-cataloged-a0a0a0.svg)](https://www.PSLmodels.org)
[![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Build Status](https://travis-ci.org/PSLmodels/Behavioral-Responses.svg?branch=master)](https://travis-ci.org/PSLmodels/Behavioral-Responses)
[![Codecov](https://codecov.io/gh/PSLmodels/Behavioral-Responses/branch/master/graph/badge.svg)](https://codecov.io/gh/PSLmodels/Behavioral-Responses)


Behavioral-Responses
====================

This document tells you how to begin using or contributing to
Behavioral-Responses.  Begin by reading the [Tax-Calculator
documentation](https://PSLmodels.github.io/Tax-Calculator/) and then
the [Behavioral-Responses user
guide](https://PSLmodels.github.io/Behavioral-Responses/) that
describes how to write Python programs that use Behavioral-Responses
together with Tax-Calculator on your own computer.


What is Behavioral-Responses?
-----------------------------

Behavioral-Responses, which is part of the Policy Simulation Library
(PSL) collection of USA tax models, estimates partial-equilibrium
behavioral responses to changes in the US federal individual income
and payroll tax system as simulated by Tax-Calculator.  It provides
two ways of doing this: (1) the `response` function, which contains
higher-level logic that supports the Tax-Brain "Partial Equilibrium
Simulation" capability and requires specification of only the
elasticities, and (2) the `quantity_response` function, which contains
lower-level logic that requires specification of the quantity whose
response is to be estimated, requires specification of the marginal
tax rates and elasticities to be used in the response calculation, and
allows the response estimation to be conducted by subgroup with
different elasticities for each subgroup.


Disclaimer
----------

Results will change as the underlying models improve. A fundamental
reason for adopting open source methods in this project is so that
people from all backgrounds can contribute to the models that our
society uses to assess economic policy; when community-contributed
improvements are incorporated, the model will produce different
results.


Getting Started
---------------

If you want to **report a bug**, create a new issue
[here](https://github.com/PSLmodels/Behavioral-Responses/issues)
providing details on what you think is wrong with Behavioral-Responses.

If you want to **request an enhancement**, create a new issue
[here](https://github.com/PSLmodels/Behavioral-Responses/issues)
providing details on what you think should be added to Behavioral-Responses.

If you want to **propose code changes**, follow the directions in the
[Tax-Calculator contributor
guide](https://github.com/PSLmodels/Tax-Calculator/blob/master/CONTRIBUTING.md#tax-calculator-contributor-guide)
on how to fork and clone the Behavioral-Responses git repository.
Before developing any code changes be sure to read completely the
Tax-Calculator contributor guide and then read about the
[Tax-Calculator pull-request
workflow](https://github.com/PSLmodels/Tax-Calculator/blob/master/WORKFLOW.md#tax-calculator-pull-request-workflow).
When reading both documents, be sure to mentally substitute
Behavioral-Response for Tax-Calculator and behresp for taxcalc.

The Behavioral-Responses [release
history](https://github.com/PSLmodels/Behavioral-Responses/blob/master/RELEASES.md#tax-calculator-release-history)
provides a high-level summary of past pull requests and access to a
complete list of merged, closed, and pending pull requests.


Citing Behavioral-Responses
---------------------------

Please cite the source of your analysis as "Behavioral-Responses
release #.#.#, author's calculations." If you wish to link to
Behavioral-Responses,
https://PSLmodels.github.io/Behavioral-Responses/ is preferred.
Additionally, we strongly recommend that you describe the
elasticity parameters used, and provide a link to the materials
required to replicate your analysis or, at least, note that those
materials are available upon request.
