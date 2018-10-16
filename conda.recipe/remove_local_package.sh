#!/bin/bash
# USAGE: ./remove_local_behavioral-responses_package.sh
# ACTION: (1) uninstalls any installed beh-resp package (conda uninstall)
# NOTE: for those with experience working with compiled languages,
#       removing a local conda package is analogous to a "make clean" operation

# uninstall any existing behavioral-responses conda package
conda list behavioral-responses | awk '$1~/behavioral-responses/{rc=1}END{exit(rc)}'
if [ $? -eq 1 ]; then
    conda uninstall behavioral-responses --yes 2>&1 > /dev/null
fi

exit 0
