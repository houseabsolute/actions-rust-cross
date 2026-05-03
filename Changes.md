## 1.0.8

- This action now always uses `cross` for `musl` targets on Linux, even when the host architecture
  matches the target. This fixes C++ compilation failures caused by the lack of `musl-g++` on Ubuntu
  runners. Reported by @RaulTrombin (Raul Victor Trombin). GH #22.

## 1.0.7 - 2026-05-02

- Fixed a bug in calculating the `cross` binary's hash.
- Fixed cache key handling to deal with spaces in cache key elements, for example in the OS version.
  Reported by @gdubicki (Greg Dubicki). GH #50. Fixes #51.

## 1.0.6 - 2026-03-15

- Updated various actions used by this action so that it no longer triggers warnings about Node.js
  20 deprecation.
- Added a section to the docs about dealing with a failure to link `-lexecinfo` on NetBSD.

## 1.0.5 - 2025-07-20

- Fixed a bug in the handling of the `rust-cache-parameters` input. If anything was specified for
  this, it would end up providing a broken config to the `Swatinem/rust-cache` action. Reported by
  @SinTan1729 (Sayantan Santra). GH #46.

## 1.0.4 - 2025-04-12

- Removed validation for the `toolchain` input. The
  [dtolnay/rust-toolchain](https://github.com/dtolnay/rust-toolchain) accepts a lot of different
  options that this action wasn't allowing. It's simpler and more flexible to just let that action
  handle validation. Requested by @axos88 (Akos Vandra-Meyer). GH #42.
- Removed validation for the `command` input. This allows you to use this action with any `cargo`
  extension command, like `cargo-deb`. Setting `command` to `both` is still supported and will run
  the `build` and `test` commands. Requested by @bvaisvil (Benjamin Vaisvil). GH #43.

## 1.0.3 - 2025-02-17

- Fixed a bug when running with a Linux ARM host where the action would use a cached `cross`
  download for x86-64 Linux (or vice versa). Now the cache key for the `cross` binary includes the
  runner's architecture in addition to its OS.
- This release partially support running on Linxu ARM, but see the `README.md` file for details on
  this.

## 1.0.2 - 2025-02-16

- Added a new `force-use-cross` input, which does what it says. It will force the use of `cross`
  even when it is not required for given platform/target combination. Note that this only works on
  Linux hosts.

## 1.0.1 - 2025-01-20

- Fixed a bug where this action would attempt to use `cross` when compiling for an ARM Linux target
  on an ARM Linux host.

## 1.0.0 - 2025-01-11

The addition of caching is a significant behavior change for this action, so the version has been
bumped to v1.0.0 because of this change.

- This action will now configure and use `Swatinem/rust-cache` by default for you. It will include
  the `target` parameter as part of the cache key automatically, as well as the OS version when
  using `cargo` on Linux. Suggested by @jennydaman (Jennings Zhang). GH #23.
- This action now validates its input and will exit early if they are not valid. GH #35.
- When compiling for `musl` targets, this action will not try to reinstall the `musl-tools` package
  if it's already installed.

The following changes were made since the 1.0.0-beta1 release:

- The cache key includes information that causes the cache to not be re-used when the system running
  `cargo` or `cross` changes. When using `cargo` on Linux, this is the OS version, like "Ubuntu
  22.04". When using `cross`, this is the hash of the `cross` binary itself. This is needed because
  the Docker images that `cross` uses can change when the binary is updated. This can include
  changing the underlying Docker image base OS, in which case it's quite likely the old cache
  contents would be incompatible with the the new image.

## 1.0.0-beta1 - 2024-12-21

The addition of caching is a significant behavior change for this action, so the version has been
bumped to v1.0.0 because of this change.

- This action will now configure and use `Swatinem/rust-cache` by default for you. It will include
  the `target` parameter as part of the cache key automatically. Suggested by @jennydaman (Jennings
  Zhang). GH #23.
- This action now validates its inputs and will exit early if they are not valid. GH #35.

## 0.0.17 - 2024-11-23

- Added support for running `cargo bench` or `cross bench`. Implemented by @RaulTrombin (Raul Victor
  Trombin). GH #32.

## 0.0.16 - 2024-11-17

- Arguments passed in the `args` parameter are now always last when executing `cargo`. This lets you
  pass arguments to test binaries like `-- --something`. First reported by @mateocabanal (Mateo
  Cabanal) as GH #12 and fully fixed by @donatello (Aditya Manthramurthy) in GH #30.

## 0.0.15 - 2024-09-21

- The `musl` packages are only installed when not cross-compiling.

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
