#!/bin/bash

set -e
set -x
set -o pipefail

TARGET=$1
did_strip=""

strip_binary() {
    if [[ $(uname -s) =~ "Darwin" ]]; then
        stripped=$(
            find "$1" -maxdepth 1 -type f -perm +111 | while read -r exe; do
                strip "$exe"
                echo "stripped $exe"
            done
        )
    else
        stripped=$(
            find "$1" -maxdepth 1 -type f -executable | while read -r exe; do
                strip "$exe"
                echo "stripped $exe"
            done
        )
    fi

    if [ -z "$stripped" ]; then
        echo "Could not find any binaries to strip in $1"
    else
        did_strip="true"
    fi
}

for type in debug release; do
    if [ -d "target/$TARGET/$type" ]; then
        strip_binary "target/$TARGET/$type"
    elif [ -d "target/$type" ]; then
        strip_binary "target/$type"
    fi
done

if [ -z "$did_strip" ]; then
    echo "No binaries were stripped"
    exit 1
fi
