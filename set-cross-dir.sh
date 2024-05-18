#!/bin/bash

set -e
set -x
set -o pipefail

echo "cross-dir=$RUNNER_TEMP" >>"$GITHUB_OUTPUT"
