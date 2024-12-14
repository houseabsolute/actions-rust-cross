#!/usr/bin/env python3

# This code was mostly written by Claude.ai.

import os
import sys


def main() -> None:
    """
    Main entry point to create a pre-commit hook symlink.
    """
    symlink_hook("pre-commit")


def symlink_hook(hook: str) -> None:
    """
    Create a symlink for a Git hook if it doesn't already exist.

    Args:
        hook: Name of the Git hook (e.g., 'pre-commit')
    """
    # Path to the hook in .git/hooks
    dot_hook_path = os.path.join(".git", "hooks", hook)

    # Path to the actual hook script
    file_hook_path = os.path.join("git", "hooks", f"{hook}.sh")

    # Relative symlink path
    link_path = os.path.join("..", "..", file_hook_path)

    # Check if the hook already exists
    if os.path.exists(dot_hook_path):
        # If it's already a symlink, check if it points to the correct location
        if os.path.islink(dot_hook_path):
            # If the existing symlink is correct, do nothing
            if os.readlink(dot_hook_path) == link_path:
                return

        # If a hook exists and is not the expected symlink, warn and exit
        print(f"You already have a hook at {dot_hook_path}!", file=sys.stderr)
        return

    # Create the symlink
    try:
        os.symlink(link_path, dot_hook_path)
    except OSError as e:
        print(f"Error creating symlink: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
