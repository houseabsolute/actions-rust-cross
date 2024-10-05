#!/usr/bin/env bash

# This script was copied from the https://github.com/cross-rs/cross project at commit
# ac4c11cedc97cd7c27faed36e55377a90e6ed618. The license for that project in its `Cargo.toml` file is
# "MIT OR Apache-2.0". The copyright in the MIT license says:
#
# Copyright (c) 2017-2022 by the respective authors
# Copyright (c) 2016 Jorge Aparicio
#
# The script was adjusted to get rid of the sysroot and arch parameters in favor of hardcoding the
# paths for Ubuntu 22.04 and the x86-64 arch.

# Create necessary symlinks for musl images to run
# dynamically-linked binaries.
# Just to be careful, we need this in a few locations,
# relative to the musl sysroot.
#   /lib/ld-musl-armhf.so
#   /lib/ld-musl-armhf.so.1
#   /usr/lib/ld.so
#   /usr/lib/ld.so.1
#   /usr/lib/libc.so
#   /usr/lib/libc.so.1

set -x
set -euo pipefail

main() {
    apt-get --yes install libboost-dev

    local src
    local dst
    local dsts
    local libstdcpp_path
    local libstdcpp_basename

    # ignore any failures here
    src="/usr/lib/x86_64-linux-musl/libc.so"
    dsts=(
        "/usr/lib/ld-musl-x86_64.so"
        "/usr/lib/ld-musl-x86_64.so.1"
        "/usr/lib/ld.so"
        "/usr/lib/ld.so.6"
        "/usr/lib/libc.so"
        "/usr/lib/libc.so.6"
    )
    for dst in "${dsts[@]}"; do
        # force a link if the dst does not exist or is broken
        if [[ -L ${dst} ]] && [[ ! -e ${dst} ]]; then
            ln -sf "${src}" "${dst}"
        elif [[ ! -f ${dst} ]]; then
            ln -s "${src}" "${dst}"
        fi
    done

    libstdcpp_path=$(find /usr/lib/x86_64-linux-gnu/ -name 'libstdc++.so.6.0.*')
    libstdcpp_basename=$(basename "$libstdcpp_path")

    # ensure we statically link libstdc++, so avoid segfaults with c++
    # https://github.com/cross-rs/cross/issues/902
    find /usr -name 'libstdc++.so*' -exec rm -f {} \;

    # now, we create a linker script that adds all the required dependencies
    # because we link to a static libstdc++ to avoid runtime issues and
    # with the shared libstdc++, we can have missing symbols that are referenced
    # in libstdc++, such as those from libc like `setlocale` and `__cxa_atexit`,
    # as well as those from libgcc, like `__extendsftf2`. all musl targets
    # can require symbols from libc, however, only the following are known
    # to require symbols from libgcc:
    #   - aarch64-unknown-linux-musl
    #   - mips64-unknown-linux-muslabi64
    #   - mips64el-unknown-linux-muslabi64
    echo '/* cross-rs linker script
 * this allows us to statically link libstdc++ to avoid segfaults
 * https://github.com/cross-rs/cross/issues/902
 */
GROUP ( libstdc++.a AS_NEEDED( -lgcc -lc -lm ) )
' >"$libstdcpp_path"
    ln -s "$libstdcpp_basename" /usr/lib/x86_64-linux-gnu/libstdc++.so.6
    ln -s "$libstdcpp_basename" /usr/lib/x86_64-linux-gnu/libstdc++.so

    echo /usr/lib/x86_64-linux-gnu >>/etc/ld-musl-x86_64.path

    ln -s /usr/bin/musl-gcc /usr/bin/musl-g++
}

main
