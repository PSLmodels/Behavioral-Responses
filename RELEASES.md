BEHAVIORAL-RESPONSES RELEASE HISTORY
====================================
Go [here](https://github.com/PSLmodels/Behavioral-Responses/pulls?q=is%3Apr+is%3Aclosed)
for a complete commit history.


2019-03-xx Release 0.7.0
------------------------
(last merged pull request is
[#52](https://github.com/PSLmodels/Behavioral-Responses/pull/52))

**API Changes**
- Simplify elasticities argument of the `response` function
  [[#51](https://github.com/PSLmodels/Behavioral-Responses/pull/51)
  by Martin Holmer]

**New Features**
- None

**Bug Fixes**
- None


2019-02-22 Release 0.6.0
------------------------
(last merged pull request is
[#46](https://github.com/PSLmodels/Behavioral-Responses/pull/46))

**API Changes**
- Require taxcalc package for Tax-Calculator 1.0 or higher
  [[#46](https://github.com/PSLmodels/Behavioral-Responses/pull/46)
  by Martin Holmer]

**New Features**
- Add optional dump argument to the `response` function
  [[#39](https://github.com/PSLmodels/Behavioral-Responses/pull/39)
  by Martin Holmer responding to request by Matt Jensen and Anderson Frailey]
- Add `quantity_response` function that was formerly a Tax-Calculator utility function and that provides a lower-level behavioral response capability
  [[#43](https://github.com/PSLmodels/Behavioral-Responses/pull/43)
  by Martin Holmer responding to suggestion by Max Ghenis]

**Bug Fixes**
- None


2018-12-14 Release 0.5.0
------------------------
(last merged pull request is
[#35](https://github.com/PSLmodels/Behavioral-Responses/pull/35))

**API Changes**
- None

**New Features**
- Make behresp packages available for Python 3.7 as well as for Python 3.6
  [[#35](https://github.com/PSLmodels/Behavioral-Responses/pull/35)
  by Martin Holmer]

**Bug Fixes**
- None


2018-12-13 Release 0.4.1
------------------------
(last merged pull request is
[#33](https://github.com/PSLmodels/Behavioral-Responses/pull/33))

**API Changes**
- None

**New Features**
- Add GitHub Travis-CI testing under Python 3.7
  [[#33](https://github.com/PSLmodels/Behavioral-Responses/pull/33)
  by Martin Holmer]

**Bug Fixes**
- None


2018-11-13 Release 0.4.0
------------------------
(last merged pull request is
[#21](https://github.com/PSLmodels/Behavioral-Responses/pull/21))

**API Changes**
- Change documentation to state that Behavioral-Responses `behresp` packages are available **only** via the `PSLmodels` Anaconda Cloud channel
  [[#20](https://github.com/PSLmodels/Behavioral-Responses/pull/20)
  by Martin Holmer]
- Remove `versioneer.py` and `taxcalc/_version.py` and related code now that Package-Builder is handling version specification
  [[#21](https://github.com/PSLmodels/Behavioral-Responses/pull/21)
  by Martin Holmer]

**New Features**
- None

**Bug Fixes**
- None


2018-11-06 Release 0.3.0
------------------------
(last merged pull request is
[#18](https://github.com/PSLmodels/Behavioral-Responses/pull/18))

**API Changes**
- Simplify specification of package dependencies
  [[#18](https://github.com/PSLmodels/Behavioral-Responses/pull/18)
  by Martin Holmer]

**New Features**
- None

**Bug Fixes**
- None


2018-11-03 Release 0.2.0
------------------------
(last merged pull request is
[#15](https://github.com/PSLmodels/Behavioral-Responses/pull/15))

**API Changes**
- Make specification of required package versions comply with style in conda cheat sheet
  [[#15](https://github.com/PSLmodels/Behavioral-Responses/pull/15)
  by Martin Holmer]

**New Features**
- None

**Bug Fixes**
- None


2018-11-01 Release 0.1.0
------------------------
(last merged pull request is
[#11](https://github.com/PSLmodels/Behavioral-Responses/pull/11))

**API Changes**
- Copy Tax-Calculator top-level files to Behavioral-Responses repo
  [[#2](https://github.com/PSLmodels/Behavioral-Responses/pull/2)
  by Martin Holmer]
- Move Tax-Calculator Behavior class logic/tests to Behavioral-Responses repo
  [[#3](https://github.com/PSLmodels/Behavioral-Responses/pull/3)
  by Martin Holmer]
- Streamline tests to use less memory
  [[#8](https://github.com/PSLmodels/Behavioral-Responses/pull/8)
  by Martin Holmer with assistance from Matt Jensen]
- Add user documentation for Behavioral-Responses package
  [[#11](https://github.com/PSLmodels/Behavioral-Responses/pull/11)
  by Martin Holmer]

**New Features**
- None

**Bug Fixes**
- None
