#!/usr/bin/env python3

import json
import os
import sys

target = sys.argv[1]
build_command = sys.argv[2]

os_version = sys.argv[3]

parameters = json.loads(os.environ["RUST_CACHE_PARAMETERS"])
if "key" not in parameters:
    parameters["key"] = target
else:
    parameters["key"] = "{}-{}".format(parameters["key"], target)

# If we're running cargo, we need to add the OS version to the cache. Otherwise things that link
# against system packages, like openssl, can break when we use the same cache across different
# versions of the runner OS. For example, when going from Ubuntu 20.04 to 22.04, we move from
# OpenSSL 1.1.x to 3.x.
if build_command == "cargo":
    parameters["key"] = "{}-{}".format(parameters["key"], os_version)

file = os.environ["GITHUB_OUTPUT"]
with open(file, "w") as f:
    for key, value in parameters.items():
        f.write(f"{key}={value}")
