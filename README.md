[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Build Status](https://travis-ci.org/open-source-economics/Behavioral-Responses.svg?branch=master)](https://travis-ci.org/open-source-economics/Behavioral-Responses)
[![Codecov](https://codecov.io/gh/open-source-economics/Behavioral-Responses/branch/master/graph/badge.svg)](https://codecov.io/gh/open-source-economics/Behavioral-Responses)


Developing Behavioral-Responses
===============================

This document tells you how to begin contributing to
Behavioral-Responses by reporting a bug, improving the documentation,
or making an enhancement to the Python source code.  If you only want
to **use** Behavioral-Responses, you should begin by reading the [user
documentation](https://open-source-economics.github.io/Behavioral-Responses/)
that describes how to write Python scripts that use
Behavioral-Responses on your own computer.


What is Behavioral-Responses?
-----------------------------

Behavioral-Responses, which is part of the Policy Simulation Library (PSL)
collection of USA tax models, estimates partial-equilibrium behavioral
responses to changes in the US federal individual income and payroll
tax system as simulated by
[Tax-Calculator](https://github.com/open-source-economics/Tax-Calculator)


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
[here](https://github.com/open-source-economics/Behavioral-Responses/issues)
providing details on what you think is wrong with Behavioral-Responses.

If you want to **request an enhancement**, create a new issue
[here](https://github.com/open-source-economics/Behavioral-Responses/issues)
providing details on what you think should be added to Behavioral-Responses.

If you want to **propose code changes**, follow the directions in the
[Tax-Calculator Contributor
Guide](https://taxcalc.readthedocs.io/en/latest/contributor_guide.html)
on how to fork and clone the Behavioral-Responses git repository.
Before developing any code changes be sure to read completely the
Tax-Calculator Contributor Guide and then read about the
[Tax-Calculator pull-request
workflow](https://github.com/open-source-economics/Tax-Calculator/blob/master/WORKFLOW.md#tax-calculator-pull-request-workflow).
When reading both documents, be sure to mentally substitute
Behavioral-Response for Tax-Calculator and behresp for taxcalc.

The Behavioral-Responses [release
history](https://github.com/open-source-economics/Behavioral-Responses/blob/master/RELEASES.md#tax-calculator-release-history)
provides a high-level summary of past pull requests and access to a
complete list of merged, closed, and pending pull requests.


Citing Behavioral-Responses
---------------------------

Please cite the source of your analysis as "Behavioral-Responses
release #.#.#, author's calculations." If you wish to link to
Behavioral-Responses,
https://open-source-economics.github.io/Behavioral-Responses/ is
preferred.  Additionally, we strongly recommend that you describe the
elasticity assumptions used, and provide a link to the materials
required to replicate your analysis or, at least, note that those
materials are available upon request.
