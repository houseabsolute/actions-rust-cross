## 0.0.8

- For builds that need the `cross` binary, this binary is now cached. A cache
  hit saves about 20 seconds in my tests. Suggested by @timon-schelling. GH
  #4.

## 0.0.7 - 2023-04-21

- The toolchain argument was (probably) not being respected with cross builds,
  though it's hard to be sure since none of the output from past CI runs I've
  looked at it includes the toolchain version in the output. But now the
  toolchain version is explicitly passed to all `cargo` and `cross` commands.

## 0.0.6 - 2023-04-21

- When the `strip` parameter was true, stripping binaries could fail if there
  were both `target/*/debug` and `target/*/release` directories present and
  the `debug` directory didn't have a binary. Now it will strip all binaries
  it finds under `target`.

## 0.0.5 - 2023-03-19

- Fix use of `dtolnay/rust-toolchain` action to allow passing a `toolchain`
  input.

## 0.0.4 - 2023-03-19

- Added a new `toolchain` parameter to allow selecting a Rust toolchain other
  than stable. This supports picking on of "stable", "beta", or "nightly".
- Fixed binary stripping to work in more situations. Previously it depended on
  a very specific setup plus expected to be run in the context of the matrix I
  use for my own projects.
- Fixed a reference to a matrix variable that should have referenced an input
  variable.

## 0.0.3 - 2023-03-17

- This action now supports running the `build` and `test` commands, or both,
  with a new input parameter, `command`. The default is `build`.

## 0.0.2 - 2023-03-05

- Fixed some typos in the `README.md` documentation.

## 0.0.1 - 2023-03-05

- First release upon an unsuspecting world.
