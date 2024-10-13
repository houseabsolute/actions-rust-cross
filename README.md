# GitHub Action to Cross Compile Rust Projects

This action lets you easily cross-compile Rust projects using
[cross](https://github.com/cross-rs/cross).

Here's a simplified example from the test and release workflow for
[my tool `ubi`](https://github.com/houseabsolute/ubi):

```yaml
jobs:
  release:
    name: Release - ${{ matrix.platform.os-name }}
    strategy:
      matrix:
        platform:
          - os-name: FreeBSD-x86_64
            runs-on: ubuntu-20.04
            target: x86_64-unknown-freebsd
            skip_tests: true

          - os-name: Linux-x86_64
            runs-on: ubuntu-20.04
            target: x86_64-unknown-linux-musl

          - os-name: Linux-aarch64
            runs-on: ubuntu-20.04
            target: aarch64-unknown-linux-musl

          - os-name: Linux-riscv64
            runs-on: ubuntu-20.04
            target: riscv64gc-unknown-linux-gnu

          - os-name: Windows-x86_64
            runs-on: windows-latest
            target: x86_64-pc-windows-msvc

          - os-name: macOS-x86_64
            runs-on: macOS-latest
            target: x86_64-apple-darwin

          # more targets here ...

    runs-on: ${{ matrix.platform.runs-on }}
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Build binary
        uses: houseabsolute/actions-rust-cross@v0
        with:
          command: ${{ matrix.platform.command }}
          target: ${{ matrix.platform.target }}
          args: "--locked --release"
          strip: true
      - name: Publish artifacts and release
        uses: houseabsolute/actions-rust-release@v0
        with:
          binary-name: ubi
          target: ${{ matrix.platform.target }}
```

Note that for Linux or BSD targets, you should always set the `runs-on` key to an x86-64
architecture runner. If you want to do native ARM compilation, for example using
`ubuntu-latest-arm`, then there's no point in using this action. This action is only tested on
Ubuntu x86-64, Windows, and macOS runners.

## Input Parameters

This action takes the following parameters:

| Key                 | Type                                           | Required? | Description                                                                                                                                                                                                                                                                                                                                   |
| ------------------- | ---------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command`           | string (one of `build`, `test`, or `both`)     | no        | The command(s) to run. The default is `build`. Running the `test` command will fail with \*BSD targets and non-x86 Windows.                                                                                                                                                                                                                   |
| `target`            | string                                         | yes       | The target triple to compile for. This should be one of the targets found by running `rustup target list`.                                                                                                                                                                                                                                    |
| `working-directory` | string                                         | no        | The working directory in which to run the `cargo` or `cross` commands. Defaults to the current directory (`.`).                                                                                                                                                                                                                               |
| `toolchain`         | string (one of `stable`, `beta`, or `nightly`) | no        | The Rust toolchain version to install. The default is `stable`.                                                                                                                                                                                                                                                                               |
| `GITHUB_TOKEN`      | string                                         | no        | Defaults to the value of `${{ github.token }}`.                                                                                                                                                                                                                                                                                               |
| `args`              | string                                         | no        | A string-separated list of arguments to be passed to `cross build`, like `--release --locked`.                                                                                                                                                                                                                                                |
| `strip`             | boolean (`true` or `false`)                    | no        | If this is true, then the resulting binaries will be stripped if possible. This is only possible for binaries which weren't cross-compiled.                                                                                                                                                                                                   |
| `cross-version`     | string                                         | no        | This can be used to set the version of `cross` to use. If specified, it should be a specific `cross` release tag (like `v0.2.3`) or a git ref (commit hash, `HEAD`, etc.). If this is not set then the latest released version will always be used. If this is set to a git ref then the version corresponding to that ref will be installed. |

## How it Works

Under the hood, this action will compile your binaries with either `cargo` or `cross`, depending on
the host machine and target. For Linux builds, it will always use `cross` except for builds
targeting an x86 architecture like `x86_64` or `i686`.

On Windows and macOS, it's possible to compile for all supported targets out of the box, so `cross`
will not be used on those platforms.

If it needs to install `cross`, it will install the latest version by downloading a release using
[my tool `ubi`](https://github.com/houseabsolute/ubi). This is much faster than using `cargo` to
build `cross`.

When compiling on Windows, it will do so in a Powershell environment, which can matter in some
corner cases, like compiling the `openssl` crate with the `vendored` feature.

Finally, it will run `strip` to strip the binaries if the `strip` parameter is true. This is only
possible for builds that are not done via `cross`. In addition, Windows builds for `aarch64` cannot
be stripped either.

## Caching Rust Compilation Output

You can use the [Swatinem/rust-cache](https://github.com/Swatinem/rust-cache) action with this one
seamlessly, whether or not a specific build target needs `cross`. There is no special configuration
that you need for this. It just works.
