#!/usr/bin/env python3

import json
import os
import sys
import hashlib


def main():
    target = sys.argv[1]
    build_command = sys.argv[2]

    os_version = sys.argv[3]

    parameters = json.loads(os.environ["RUST_CACHE_PARAMETERS"])
    if "key" not in parameters:
        parameters["key"] = target
    else:
        parameters["key"] += "-{}".format(target)

    if build_command == "cargo":
        # If we're running cargo, we need to add the OS version to the cache. Otherwise things that link
        # against system packages, like openssl, can break when we use the same cache across different
        # versions of the runner OS. For example, when going from Ubuntu 20.04 to 22.04, we move from
        # OpenSSL 1.1.x to 3.x.
        parameters["key"] += "-{}".format(os_version)
    else:
        # Otherwise we want to include the `cross` binary's hash. The Docker images that `cross`
        # uses can change when the binary is updated. This protects us from using the same cache
        # inside containers that have changed.
        parameters["key"] += "-cross-binary-hash-{}".format(
            get_file_hash(build_command)
        )

    file = os.environ["GITHUB_OUTPUT"]
    with open(file, "w") as f:
        for key, value in parameters.items():
            f.write(f"{key}={value}\n")


def get_file_hash(build_command):
    with open(build_command, "rb") as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(65536):
            file_hash.update(chunk)
            return file_hash.hexdigest()


main()
