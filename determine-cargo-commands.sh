#!/bin/bash

set -e
set -x
set -o pipefail

COMMAND="$1"
if [ "$COMMAND" == 'both' ]; then
    echo "build=true" >>"$GITHUB_OUTPUT"
    echo "test=true" >>"$GITHUB_OUTPUT"
else
    echo "command=$COMMAND" >>"$GITHUB_OUTPUT"
fi
