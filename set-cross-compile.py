#!/usr/bin/env python3

# Written mostly by Claude.ai based on my original bash script.

import sys
import platform
import re
import os
from subprocess import run, PIPE, CalledProcessError


def main() -> int:
    """
    Main function to determine cross-compilation requirements.

    Returns:
        Exit code (0 for success)
    """
    if len(sys.argv) < 3:
        print(
            "Error: Target architecture and force cross arguments are required",
            file=sys.stderr,
        )
        return 1

    target = sys.argv[1]
    force_use_cross = sys.argv[2]
    if force_use_cross == "true":
        needs_cross = True
    else:
        needs_cross = check_needs_cross(target)

    write_github_output(needs_cross)

    return 0


def check_needs_cross(target: str) -> bool:
    """
    Determine if cross-compilation is needed based on system and target.

    Args:
        target: Target architecture string

    Returns:
        Boolean indicating if cross-compilation is needed
    """
    system_info = get_uname_info().lower()

    # Check if we're on macOS or Windows
    if any(os in system_info for os in ["darwin", "msys", "windows"]):
        return False

    target = target.lower()

    # Check for x86_64 Linux targets on x86_64 Linux host. We always use cross for musl targets
    # because the Ubuntu runner lacks a C++ compiler for musl (musl-g++).
    if (
        re.search(r"x86_64.+linux-gnu", target)
        and "x86_64" in system_info
        and "linux" in system_info
    ):
        return False

    # It's tempting to not use cross when the host is Linux x86-64 and we're compiling for Linux
    # i586 or i686. This sort of works, but if there's any C being compiled, things get weird,
    # because then we need 32-bit C headers, 32-bit C libs to link to, etc.

    # Check if both host and target are ARM Linux. I'm assuming here that for things like
    # "arm-linux-androideabi" or "armv7-unknown-linux-ohos" we'd still need cross. We always use
    # cross for musl targets because the Ubuntu runner lacks a C++ compiler for musl (musl-g++).
    if (
        re.search(r"(?:aarch64|arm).+linux-gnu", target)
        and ("arm" in system_info or "aarch64" in system_info)
        and "linux" in system_info
    ):
        return False

    return True


def get_uname_info() -> str:
    """
    Get system information using uname command.

    Returns:
        String containing system information
    """
    try:
        result = run(["uname", "-a"], check=True, text=True, stdout=PIPE)
        return result.stdout
    except (CalledProcessError, FileNotFoundError):
        # Fallback to platform.platform() if uname is not available
        return platform.platform()


def write_github_output(needs_cross: bool) -> None:
    """
    Write the needs-cross output to GITHUB_OUTPUT environment variable file.

    Args:
        needs_cross: Boolean indicating if cross-compilation is needed
    """
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"needs-cross={str(needs_cross).lower()}\n")


if __name__ == "__main__":
    sys.exit(main())
