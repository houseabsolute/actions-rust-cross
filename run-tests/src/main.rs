// Mostly written by Claude.ai.

use clap::Parser;
use is_executable::is_executable;
use regex::Regex;
use std::{
    env,
    path::{Path, PathBuf},
    process::Command,
};

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(long)]
    checkout_root: String,
    #[arg(long)]
    target: String,
    #[arg(long)]
    expect_file_re: Option<String>,
    #[arg(long)]
    expect_cross: bool,
    #[arg(long)]
    expect_cross_version: Option<String>,
    #[arg(long)]
    expect_stripped: bool,
    #[arg(long)]
    is_subcrate: bool,
}

fn main() {
    let args = Args::parse();

    let runner_temp = env::var("RUNNER_TEMP").expect("RUNNER_TEMP is not set");
    let runner_temp_path = PathBuf::from(runner_temp);

    check_cross(
        &runner_temp_path,
        args.expect_cross,
        args.expect_cross_version.as_deref(),
    );

    let checkout_root_path = PathBuf::from(args.checkout_root);
    let bin_paths = if args.is_subcrate {
        vec![checkout_root_path
            .join("subcrate")
            .join("target")
            .join(&args.target)
            .join("debug")
            .join("subcrate")]
    } else {
        vec![
            checkout_root_path
                .join("target")
                .join(&args.target)
                .join("debug")
                .join("bin1"),
            checkout_root_path
                .join("target")
                .join(&args.target)
                .join("debug")
                .join("bin2"),
        ]
    };

    for mut bin_path in bin_paths {
        if cfg!(windows) {
            bin_path.set_extension("exe");
        }
        check_binary(
            &bin_path,
            args.expect_file_re.as_deref(),
            args.expect_stripped,
        );
    }
}

fn check_cross(bin_dir: &Path, expect_cross: bool, expect_cross_version: Option<&str>) {
    let cross_path = bin_dir.join("cross");

    if expect_cross {
        assert!(cross_path.is_file(), "`cross` exists");

        if let Some(expected_version) = expect_cross_version {
            let output = Command::new(&cross_path)
                .arg("--version")
                .output()
                .expect("Failed to execute `cross` command");
            let version = String::from_utf8(output.stdout)
                .expect("`cross --version` stdout was not valid UTF-8");
            assert!(
                version.contains(expected_version),
                "`cross` version matches expected version"
            );
        }
    } else {
        assert!(!cross_path.exists(), "`cross` was not downloaded");
    }
}

fn check_binary(bin_path: &PathBuf, expect_file_re: Option<&str>, expect_stripped: bool) {
    assert!(bin_path.exists(), "Binary at {} exists", bin_path.display());
    assert!(
        bin_path.is_file(),
        "Binary at {} is a file",
        bin_path.display()
    );

    assert!(
        is_executable(bin_path),
        "Binary at {} is executable",
        bin_path.display()
    );

    let output = Command::new("file")
        .arg("--brief")
        .arg(bin_path)
        .output()
        .expect("Failed to execute `file` command");
    let file_output = String::from_utf8_lossy(&output.stdout);

    if let Some(file_re) = expect_file_re {
        let re = Regex::new(file_re).expect("Invalid regex");
        assert!(
            re.is_match(&file_output),
            "`file` output for {} matches expected output",
            bin_path.display(),
        );
    }

    // `file` on macOS doesn't report if the binary is stripped.
    if cfg!(target_os = "macos") {
        return;
    }

    if expect_stripped {
        assert!(
            !file_output.contains("not stripped"),
            "`file` does not report {} as not stripped",
            bin_path.display(),
        );
        assert!(
            file_output.contains("stripped"),
            "`file` reports {} as stripped",
            bin_path.display(),
        );
    } else if cfg!(windows) {
        assert!(
            !file_output.contains("stripped"),
            "`file` does not report {} as stripped",
            bin_path.display(),
        );
    } else {
        assert!(
            file_output.contains("not stripped"),
            "`file` reports {} as not stripped",
            bin_path.display(),
        );
    }
}
