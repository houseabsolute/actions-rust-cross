#!/usr/bin/env python3

# Written by Claude.ai

import os
import json
from pathlib import Path
from typing import Dict, List, Union
import tempfile
import unittest

boolean_flags = {"cache_cross_binary", "force_use_cross", "strip", "use_rust_cache"}


class InputValidator:
    """Validate inputs for a GitHub Action."""

    def __init__(self, repo_root: Union[str, Path]):
        """
        Create a new InputValidator by collecting environment variables.

        Args:
            repo_root: Path to the repository root
        """
        self.repo_root = Path(repo_root)
        self.inputs: Dict[str, str] = {
            key.replace("INPUTS_", "").lower(): value
            for key, value in os.environ.items()
            if key.startswith("INPUTS_")
        }

    def validate(self) -> List[str]:
        """
        Validate all inputs according to specifications.

        Returns:
            List of validation errors. Empty list means all inputs are valid.
        """
        validation_errors: List[str] = []

        # Check for required 'target' parameter
        if "target" not in self.inputs:
            validation_errors.append("'target' is a required parameter")

        # Validate command if present
        if "command" in self.inputs:
            valid_commands = {"build", "test", "both", "bench"}
            if self.inputs["command"] not in valid_commands:
                validation_errors.append(
                    f"Invalid 'command'. Must be one of {sorted(valid_commands)}"
                )

        # Validate toolchain if present
        if "toolchain" in self.inputs:
            valid_toolchains = {"stable", "beta", "nightly"}
            if self.inputs["toolchain"] not in valid_toolchains:
                validation_errors.append(
                    f"Invalid 'toolchain'. Must be one of {sorted(valid_toolchains)}"
                )

        # Validate working directory if present
        if "working_directory" in self.inputs:
            path = Path(self.inputs["working_directory"])
            if not path.is_absolute():
                path = self.repo_root / path

            if not path.exists():
                validation_errors.append(
                    f"'working-directory' does not exist: {self.inputs['working_directory']}"
                )
            elif not path.is_dir():
                validation_errors.append(
                    f"'working-directory' is not a directory: {self.inputs['working_directory']}"
                )

        # Validate boolean flags
        for flag in boolean_flags:
            if flag in self.inputs and self.inputs[flag] not in {"true", "false"}:
                # Turn the underscores into dashes
                dashes = flag.replace("_", "-")
                validation_errors.append(f"'{dashes}' must be either 'true' or 'false'")

        # Validate rust-cache-parameters JSON if present
        if "rust_cache_parameters" in self.inputs:
            try:
                json.loads(self.inputs["rust_cache_parameters"])
            except json.JSONDecodeError:
                validation_errors.append("'rust-cache-parameters' must be valid JSON")

        return validation_errors


def main() -> None:
    """Main function for running the validator."""
    import sys

    validator = InputValidator(sys.argv[1])
    errors = validator.validate()

    if not errors:
        print("All inputs are valid.")
        sys.exit(0)
    else:
        for error in errors:
            print(error, file=sys.stderr)
        sys.exit(1)


class TestInputValidator(unittest.TestCase):
    """Unit tests for the InputValidator."""

    def setUp(self) -> None:
        """Set up test environment."""
        # Clear existing INPUTS_ environment variables
        for key in list(os.environ.keys()):
            if key.startswith("INPUTS_"):
                del os.environ[key]

    def setup_env(self, inputs: Dict[str, str]) -> None:
        """Helper function to set up environment variables for testing."""
        for key, value in inputs.items():
            env_key = f"INPUTS_{key.upper().replace('-', '_')}"
            os.environ[env_key] = value

    def test_get_inputs_from_env(self) -> None:
        """Test getting inputs from environment variables."""
        inputs = {
            "target": "x86_64-unknown-linux-gnu",
            "command": "build",
            "toolchain": "stable",
            "use-rust-cache": "true",
        }
        self.setup_env(inputs)

        validator = InputValidator("/root")
        for key, value in validator.inputs.items():
            self.assertEqual(value, inputs[key.replace("_", "-")])

    def test_validate_missing_target(self) -> None:
        """Test validation with missing target."""
        self.setup_env({})
        validator = InputValidator("/root")
        errors = validator.validate()
        self.assertTrue(errors)

    def test_validate_valid_command(self) -> None:
        """Test validation of valid commands."""
        valid_commands = ["build", "test", "both", "bench"]

        for command in valid_commands:
            self.setup_env({"target": "x86_64-unknown-linux-gnu", "command": command})
            validator = InputValidator("/root")
            errors = validator.validate()
            self.assertFalse(errors, f"Command '{command}' should be valid")

    def test_validate_invalid_command(self) -> None:
        """Test validation of invalid command."""
        self.setup_env({"target": "x86_64-unknown-linux-gnu", "command": "invalid"})
        validator = InputValidator("/root")
        errors = validator.validate()
        self.assertTrue(errors)

    def test_validate_valid_toolchain(self) -> None:
        """Test validation of valid toolchains."""
        valid_toolchains = ["stable", "beta", "nightly"]

        for toolchain in valid_toolchains:
            self.setup_env(
                {"target": "x86_64-unknown-linux-gnu", "toolchain": toolchain}
            )
            validator = InputValidator("/root")
            errors = validator.validate()
            self.assertFalse(errors, f"Toolchain '{toolchain}' should be valid")

    def test_validate_invalid_toolchain(self) -> None:
        """Test validation of invalid toolchain."""
        self.setup_env({"target": "x86_64-unknown-linux-gnu", "toolchain": "unknown"})
        validator = InputValidator("/root")
        errors = validator.validate()
        self.assertTrue(errors)

    def test_validate_working_directory(self) -> None:
        """Test validation of working directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test with valid directory
            self.setup_env(
                {"target": "x86_64-unknown-linux-gnu", "working-directory": temp_dir}
            )
            validator = InputValidator("/root")
            errors = validator.validate()
            self.assertFalse(errors)

            # Test with non-existent directory
            self.setup_env(
                {
                    "target": "x86_64-unknown-linux-gnu",
                    "working-directory": "/path/to/nonexistent/directory",
                }
            )
            validator = InputValidator("/root")
            errors = validator.validate()
            self.assertTrue(errors)

            # Test with file instead of directory
            with tempfile.NamedTemporaryFile() as temp_file:
                self.setup_env(
                    {
                        "target": "x86_64-unknown-linux-gnu",
                        "working-directory": temp_file.name,
                    }
                )
                validator = InputValidator("/root")
                errors = validator.validate()
                self.assertTrue(errors)

    def test_validate_boolean_flags(self) -> None:
        """Test validation of boolean flags."""

        # Test valid boolean values
        for flag in boolean_flags:
            for value in ["true", "false"]:
                self.setup_env({"target": "x86_64-unknown-linux-gnu", flag: value})
                validator = InputValidator("/root")
                errors = validator.validate()
                self.assertFalse(errors, f"'{flag}' with '{value}' should be valid")

        # Test invalid boolean values
        for flag in boolean_flags:
            self.setup_env({"target": "x86_64-unknown-linux-gnu", flag: "invalid"})
            validator = InputValidator("/root")
            errors = validator.validate()
            self.assertTrue(errors, f"'{flag}' with 'invalid' should be invalid")

    def test_validate_rust_cache_parameters(self) -> None:
        """Test validation of rust cache parameters."""
        # Valid JSON
        self.setup_env(
            {
                "target": "x86_64-unknown-linux-gnu",
                "rust-cache-parameters": '{"key1":"value1","key2":"value2"}',
            }
        )
        validator = InputValidator("/root")
        errors = validator.validate()
        self.assertFalse(errors)

        # Invalid JSON
        self.setup_env(
            {
                "target": "x86_64-unknown-linux-gnu",
                "rust-cache-parameters": "{invalid json",
            }
        )
        validator = InputValidator("/root")
        errors = validator.validate()
        self.assertTrue(errors)


if __name__ == "__main__":
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "--test":
        unittest.main(argv=["unittest"])
    else:
        main()
