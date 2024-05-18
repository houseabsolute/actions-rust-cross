#!/bin/bash

set -eo pipefail
set -x

function run() {
    echo "$1"
    eval "$1"
}

function install_tools() {
    curl --silent --location \
        https://raw.githubusercontent.com/houseabsolute/ubi/master/bootstrap/bootstrap-ubi.sh |
        sh
    run "ubi --project houseabsolute/precious --in $HOME/bin"
    run "ubi --project houseabsolute/omegasort --in $HOME/bin"
    run "ubi --project koalaman/shellcheck --in $HOME/bin"
    run "ubi --project mvdan/sh --in $HOME/bin --exe shfmt"
    run "ubi --project crate-ci/typos --in $HOME/bin"
    run "npm install prettier"
    run "curl -L https://cpanmin.us/ -o $HOME/bin/cpanm"
    run "chmod 0755 $HOME/bin/cpanm"
    run "$HOME/bin/cpanm --sudo --notest Perl::Tidy"
}

if [ "$1" == "-v" ]; then
    set -x
fi

mkdir -p "$HOME"/bin

set +e
echo ":$PATH:" | grep --extended-regexp ":$HOME/bin:" >&/dev/null
# shellcheck disable=SC2181
if [ "$?" -eq "0" ]; then
    path_has_home_bin=1
fi
set -e

if [ -z "$path_has_home_bin" ]; then
    PATH=$HOME/bin:$PATH
fi

install_tools

echo "Tools were installed into $HOME/bin."
if [ -z "$path_has_home_bin" ]; then
    echo "You should add $HOME/bin to your PATH."
fi

exit 0
