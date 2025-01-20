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
        uses: actions/checkout@v4
      - name: Build binary
        uses: houseabsolute/actions-rust-cross@v1
        with:
          command: ${{ matrix.platform.command }}
          target: ${{ matrix.platform.target }}
          args: "--locked --release"
          strip: true
      - name: Publish artifacts and release
        uses: houseabsolute/actions-rust-release@v0
        with:
          executable-name: ubi
          target: ${{ matrix.platform.target }}
```

Note that for Linux or BSD targets, you should always set the `runs-on` key to a Linux x86-64
architecture runner.

If you _only_ want to do native ARM compilation, for example using the `ubuntu-latest-arm` runner,
then there's no need to use this action. However, if you want to compile for _many_ platforms,
including Linux ARM, using this action will simplify your config. This action is only tested on
Ubuntu x86-64, Windows, and macOS runners.

## Input Parameters

This action takes the following parameters:

| Key                     | Type                                                                 | Required? | Description                                                                                                                                                                                                                                                                                                                                   |
| ----------------------- | -------------------------------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command`               | string (one of `build`, `test`, `both` (build and test), or `bench`) | no        | The command(s) to run. The default is `build`. Running the `test` command will fail with \*BSD targets and non-x86 Windows.                                                                                                                                                                                                                   |
| `target`                | string                                                               | yes       | The target triple to compile for. This should be one of the targets found by running `rustup target list`.                                                                                                                                                                                                                                    |
| `working-directory`     | string                                                               | no        | The working directory in which to run the `cargo` or `cross` commands. Defaults to the current directory (`.`).                                                                                                                                                                                                                               |
| `toolchain`             | string (one of `stable`, `beta`, or `nightly`)                       | no        | The Rust toolchain version to install. The default is `stable`.                                                                                                                                                                                                                                                                               |
| `GITHUB_TOKEN`          | string                                                               | no        | Defaults to the value of `${{ github.token }}`.                                                                                                                                                                                                                                                                                               |
| `args`                  | string                                                               | no        | A string-separated list of arguments to be passed to `cross build`, like `--release --locked`.                                                                                                                                                                                                                                                |
| `strip`                 | boolean (`true` or `false`)                                          | no        | If this is true, then the resulting binaries will be stripped if possible. This is only possible for binaries which weren't cross-compiled.                                                                                                                                                                                                   |
| `cross-version`         | string                                                               | no        | This can be used to set the version of `cross` to use. If specified, it should be a specific `cross` release tag (like `v0.2.3`) or a git ref (commit hash, `HEAD`, etc.). If this is not set then the latest released version will always be used. If this is set to a git ref then the version corresponding to that ref will be installed. |
| `use-rust-cache`        | boolean                                                              | no        | Whether or not to use [the `Swatinem/rust-cache@v2` action](https://github.com/Swatinem/rust-cache). This defaults to true.                                                                                                                                                                                                                   |
| `rust-cache-parameters` | string (containing JSON)                                             | no        | This must be a string containing valid JSON. The JSON should be an object where the keys are the parameters for [the `Swatinem/rust-cache@v2` action](https://github.com/Swatinem/rust-cache).                                                                                                                                                |

### Setting Environment Variables

You can simply set an `env` key in the workflow step that uses this action, for example:

```
- name: Run build command
  uses: houseabsolute/actions-rust-cross@v1
  env:
    CARGO_LOG: debug
    RUSTFLAGS: "-g"
  with:
    command: build
```

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

When running `cargo` on a Linux system, it will also include the output of running
`lsb_release --short --description` in the cache key. This is important for crates that link against
system libraries. If those library versions change across OS versions (e.g. Ubuntu 20.04 to 22.04),
then the cache will be broken for these cases.

When running `cross`, the hash of the `cross` binary will be included in the cache key. This is done
because the Docker images that `cross` uses can change when `cross` is updated. We want to make sure
that we do not re-use the cache across changes when these images change.

Finally, it will run `strip` to strip the binaries it builds if the `strip` parameter is true. This
is only possible for builds that are not done via `cross`. In addition, Windows builds for `aarch64`
cannot be stripped either.

### Caching

By default, this action will use
[the `Swatinem/rust-cache@v2` action](https://github.com/Swatinem/rust-cache) to cache compiled
dependencies for a crate. Note that per the documentation for the `rust-cache` action, it has fairly
limited value for crates without a `Cargo.lock` file. The `key` parameter passed to this action will
always include the value of the `target` input. If you specify a `key` parameter in
`rust-cache-parameters`, then the `target` input will be appended to the value you specify.

#### Weird Caching Issue with Multiple Crates

In my testing, it seemed like in some cases restoring the cache would delete existing files in a
`target` directory. This manifested with this sequence of actions:

1. Run `actions-rust-cross` to compile a crate in a top-level directory.
2. Run `actions-rust-cross` to compile a crate in a subdirectory.

After step 2, the compiled binaries from step 1 were no longer present, _sometimes_. I'm not sure
exactly what's going on here, but my recommendation is to structure your workflows so that this
cannot affect you.

For example, if you have multiple crates, each of which builds a binary you want to release, then
you can avoid this issue by structuring your workflow as follows:

1. Run `actions-rust-cross` to compile crate A.
2. Run the release steps for crate A.
3. Run `actions-rust-cross` to compile crate B.
4. Run the release steps for crate B.

When structured this way, it does not matter if the output of crate A is deleted in step 3.
