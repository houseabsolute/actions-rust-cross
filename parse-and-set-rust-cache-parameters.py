#!/usr/bin/env python3

import json
import os
import sys
import hashlib
import re
import unittest


def build_parameters(
    raw_parameters, target, build_command, os_version, working_directory
):
    parameters = json.loads(raw_parameters)
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

    parameters["key"] = sanitize_key(parameters["key"])

    # When the cargo project lives in a subdirectory, the user passes `working-directory`. We need
    # to forward that to `Swatinem/rust-cache` as `workspaces` so that it runs `cargo metadata` in
    # the right place instead of failing at the repo root. See
    # https://github.com/houseabsolute/actions-rust-cross/issues/53. We don't clobber a `workspaces`
    # value that the user supplied explicitly via `rust-cache-parameters`.
    if working_directory and "workspaces" not in parameters:
        # Normalize so that `./rust`, `rust/`, and `rust` all map to the same value, and so that
        # `./` collapses to `.` and is treated as the (skipped) default. Absolute paths, such as
        # the `${{ github.workspace }}/rust` form from the issue, are cleaned but preserved.
        working_directory = os.path.normpath(working_directory)
        if working_directory != ".":
            parameters["workspaces"] = working_directory

    return parameters


def main():
    target = sys.argv[1]
    build_command = sys.argv[2]
    os_version = sys.argv[3]
    working_directory = sys.argv[4]

    parameters = build_parameters(
        os.environ["RUST_CACHE_PARAMETERS"],
        target,
        build_command,
        os_version,
        working_directory,
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


def sanitize_key(key):
    # cache key cannot contain any whitespace
    return re.sub(r"\s+", "-", key)


class TestBuildParameters(unittest.TestCase):
    def test_workspaces_set_from_working_directory(self):
        # See https://github.com/houseabsolute/actions-rust-cross/issues/53. When the cargo
        # project lives in a subdirectory, `Swatinem/rust-cache` runs `cargo metadata` from the
        # repo root and fails to find a `Cargo.toml`, so it silently does no caching. We need to
        # pass the `working-directory` through as the rust-cache `workspaces` parameter.
        parameters = build_parameters(
            "{}", "x86_64-unknown-linux-gnu", "cargo", "Ubuntu 24.04", "rust"
        )
        self.assertEqual(parameters["workspaces"], "rust")

    def test_workspaces_not_set_for_default_working_directory(self):
        # When the working directory is the default (the repo root), we should not set
        # `workspaces` so that existing behavior is unchanged.
        parameters = build_parameters(
            "{}", "x86_64-unknown-linux-gnu", "cargo", "Ubuntu 24.04", "."
        )
        self.assertNotIn("workspaces", parameters)

    def test_workspaces_not_set_for_empty_working_directory(self):
        # An explicitly-cleared working directory should behave like the default.
        parameters = build_parameters(
            "{}", "x86_64-unknown-linux-gnu", "cargo", "Ubuntu 24.04", ""
        )
        self.assertNotIn("workspaces", parameters)

    def test_working_directory_is_normalized(self):
        # `./rust` and `rust/` should map to the same value as `rust`, and `./` should collapse
        # to the (skipped) default.
        for working_directory in ("./rust", "rust/", "rust/."):
            parameters = build_parameters(
                "{}",
                "x86_64-unknown-linux-gnu",
                "cargo",
                "Ubuntu 24.04",
                working_directory,
            )
            self.assertEqual(parameters["workspaces"], "rust", working_directory)

        parameters = build_parameters(
            "{}", "x86_64-unknown-linux-gnu", "cargo", "Ubuntu 24.04", "./"
        )
        self.assertNotIn("workspaces", parameters)

    def test_absolute_working_directory_is_preserved(self):
        # The `${{ github.workspace }}/rust` form from the issue expands to an absolute path,
        # which should be passed through (cleaned but not made relative).
        parameters = build_parameters(
            "{}",
            "x86_64-unknown-linux-gnu",
            "cargo",
            "Ubuntu 24.04",
            "/home/runner/work/repo/rust",
        )
        self.assertEqual(parameters["workspaces"], "/home/runner/work/repo/rust")

    def test_user_supplied_workspaces_is_preserved(self):
        # If the user explicitly passes `workspaces` in `rust-cache-parameters`, we must not
        # clobber it with `working-directory`.
        parameters = build_parameters(
            '{ "workspaces": "custom -> custom/target" }',
            "x86_64-unknown-linux-gnu",
            "cargo",
            "Ubuntu 24.04",
            "rust",
        )
        self.assertEqual(parameters["workspaces"], "custom -> custom/target")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        unittest.main(argv=["unittest"])
    else:
        main()
