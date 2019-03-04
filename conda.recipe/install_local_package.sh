#!/bin/bash
# USAGE: ./install_local_package.sh
# ACTION: (1) uninstall _ANY_ installed package (remove_local_package.sh)
#         (2) execute "conda install conda-build" (if necessary)
#         (3) build local behresp=0.0.0 package (conda build)
#         (4) install local behresp=0.0.0 package (conda install), which
#               requires EITHER
#               (a) prior install of taxcalc package as follows:
#                   $ conda install -c PSLmodels --yes taxcalc
#               OR
#               (b) prior one-time execution of the following command:
#                   $ conda config --add channels PSLmodels
# NOTE: for those with experience working with compiled languages,
#       building a local conda package is analogous to compiling an executable

echo "STARTING : `date`"

echo "BUILD-PREP..."

# uninstall _ANY_ installed package
./remove_local_package.sh

# check version of conda package
conda list conda | awk '$1=="conda"{v=$2;gsub(/\./,"",v);nv=v+0;if(nv<444)rc=1}END{exit(rc)}'
if [[ $? -eq 1 ]]; then
    echo "==> Installing conda 4.4.4+"
    conda install conda>=4.4.4 --yes 2>&1 > /dev/null
    echo "==> Continuing to build new behresp package"
fi

# install conda-build package if not present
conda list build | awk '$1~/conda-build/{rc=1}END{exit(rc)}'
if [[ $? -eq 0 ]]; then
    echo "==> Installing conda-build package"
    conda install conda-build --yes 2>&1 > /dev/null
    echo "==> Continuing to build new behresp package"
fi

# build behresp conda package for this version of Python
OPTIONS="--old-build-string --no-anaconda-upload -c PSLmodels --python 3.6"
conda build $OPTIONS . 2>&1 | awk '$1~/BUILD/||$1~/TEST/'

# install behresp conda package, which requires prior install of taxcalc
echo "INSTALLATION..."
conda install --yes -c local behresp=0.0.0 2>&1 > /dev/null

# clean-up after package build
echo "CLEAN-UP..."
conda build purge 2> /dev/null
topdir=$(git rev-parse --show-toplevel)
pushd $topdir > /dev/null
rm -rf build/*
rmdir build/
rm -rf dist/*
rmdir dist/
rm -rf behresp.egg-info/*
rmdir behresp.egg-info/
popd > /dev/null

echo "FINISHED : `date`"
exit 0
