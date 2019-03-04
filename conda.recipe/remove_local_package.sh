#!/bin/bash
# USAGE: ./remove_local_package.sh
# ACTION: (1) uninstalls _ANY_ installed behresp package (conda uninstall)
# NOTE: for those with experience working with compiled languages,
#       removing a local conda package is analogous to a "make clean" operation

# uninstall _ANY_ existing behresp conda package
conda list behresp | awk '$1=="behresp"{rc=1}END{exit(rc)}'
if [[ $? -eq 1 ]]; then
    conda uninstall --yes behresp 2>&1 > /dev/null
fi

exit 0
