#!/bin/bash

set -e
set -x
set -o pipefail

CROSS_DIR="$1"
VERSION="$2"

cd "$CROSS_DIR"

if [[ -n $VERSION ]] && ! [[ $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    cargo install cross --git https://github.com/cross-rs/cross --rev "$VERSION" --force
    mv "$HOME/.cargo/bin/cross" .
    CROSS_NO_WARNINGS=0 ./cross --version
    exit 0
fi

VERSION_ARGS=""
if [ -n "$VERSION" ]; then
    VERSION_ARGS="--tag $VERSION"
fi

export TARGET=.
curl --silent --location \
    https://raw.githubusercontent.com/houseabsolute/ubi/master/bootstrap/bootstrap-ubi.sh |
    sh
# shellcheck disable=SC2086
./ubi --project cross-rs/cross --matching musl --in . $VERSION_ARGS
CROSS_NO_WARNINGS=0 ./cross --version
