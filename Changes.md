## 0.0.14 - 2024-08-25

- When the given `target` includes the string `musl`, this action will install the `musl-tools`
  package. This allows crates with C or C++ code to compile properly. Fixes #20. Reported by Matteo
  Pietro Dazzi (@ilteoood).

## 0.0.13 - 2024-05-18

- It's now possible to set `cross-version` to a git ref like a commit hash or `HEAD`. This will
  install `cross` from its git repo.

## 0.0.12 - 2024-02-25

- Bumped the version of `actions/cache` used in this action to v4. The v3 version uses Node 16,
  which causes warnings when run. Implemented by @hms5232. GH #13.

## 0.0.11 - 2023-12-17

- Use `cross` when compiling for 32-bit Linux targets. While in theory this should work without
  `cross`, compiling `openssl` with the `vendored` feature fails when we run
  `cargo build --target i686-unknown-linux-musl`.

## 0.0.10 - 2023-12-10

- Fixed handling of crates with multiple binaries. Attempting to strip binaries for such a crate
  caused the build to fail. Reported by Tomaž Hribernik. GH #8
- Added a new `cross-version` parameter. This can be specified to make this action use a specific
  version of `cross`. If this is not specified, the latest version will be used.

## 0.0.9 - 2023-09-10

- Added a `working-directory` parameter. By default this is the current directory (`.`) but you can
  set it to something else to compile a single crate or workspace in a subdirectory of the repo.
  This allows you to use this action with monorepos with multiple crates. Based on GH #7 by
  @aaronvg.

## 0.0.8 - 2023-07-22

- For builds that need the `cross` binary, this binary is now cached. A cache hit saves about 20
  seconds in my tests. Suggested by @timon-schelling. GH #4.

## 0.0.7 - 2023-04-21

- The toolchain argument was (probably) not being respected with cross builds, though it's hard to
  be sure since none of the output from past CI runs I've looked at it includes the toolchain
  version in the output. But now the toolchain version is explicitly passed to all `cargo` and
  `cross` commands.

## 0.0.6 - 2023-04-21

- When the `strip` parameter was true, stripping binaries could fail if there were both
  `target/*/debug` and `target/*/release` directories present and the `debug` directory didn't have
  a binary. Now it will strip all binaries it finds under `target`.

## 0.0.5 - 2023-03-19

- Fix use of `dtolnay/rust-toolchain` action to allow passing a `toolchain` input.

## 0.0.4 - 2023-03-19

- Added a new `toolchain` parameter to allow selecting a Rust toolchain other than stable. This
  supports picking on of "stable", "beta", or "nightly".
- Fixed binary stripping to work in more situations. Previously it depended on a very specific setup
  plus expected to be run in the context of the matrix I use for my own projects.
- Fixed a reference to a matrix variable that should have referenced an input variable.

## 0.0.3 - 2023-03-17

- This action now supports running the `build` and `test` commands, or both, with a new input
  parameter, `command`. The default is `build`.

## 0.0.2 - 2023-03-05

- Fixed some typos in the `README.md` documentation.

## 0.0.1 - 2023-03-05

- First release upon an unsuspecting world.
