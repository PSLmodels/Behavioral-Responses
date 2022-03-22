try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    longdesc = f.read()

version = '0.0.0'

config = {
    'description': 'Behavioral Responses',
    'url': 'https://github.com/PSLmodels/Behavioral-Responses',
    'download_url': 'https://github.com/PSLmodels/Behavioral-Responses',
    'description': 'behresp',
    'long_description': longdesc,
    'version': version,
    'license': 'CC0 1.0 Universal public domain dedication',
    'packages': ['behresp'],
    'include_package_data': True,
    'name': 'behresp',
    'install_requires': ['numpy', 'pandas', 'taxcalc'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    'tests_require': ['pytest']
}

setup(**config)
