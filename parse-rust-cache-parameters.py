#!/usr/bin/env python3

import json
import os
import sys

parameters = json.loads(os.environ["RUST_CACHE_PARAMETERS"])
if "key" not in parameters:
    parameters["key"] = sys.argv[1]
else:
    parameters["key"] = "{}-{}".format(parameters["key"], sys.argv[1])

file = os.environ["GITHUB_OUTPUT"]
with open(file, "w") as f:
    for key, value in parameters.items():
        f.write(f"{key}={value}")
