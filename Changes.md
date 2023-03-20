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
