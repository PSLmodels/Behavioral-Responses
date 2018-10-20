#!/bin/bash
# USAGE: ./remove_local_behresp_package.sh
# ACTION: (1) uninstalls any installed behresp package (conda uninstall)
# NOTE: for those with experience working with compiled languages,
#       removing a local conda package is analogous to a "make clean" operation

# uninstall any existing behresp conda package
conda list behresp | awk '$1~/behresp/{rc=1}END{exit(rc)}'
if [ $? -eq 1 ]; then
    conda uninstall behresp --yes 2>&1 > /dev/null
fi

exit 0
