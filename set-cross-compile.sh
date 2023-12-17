set -e
set -x

TARGET="$1"

# On macOS and Windows, we can cross-compile to all possible targets without
# using cross.
if uname -a | grep --quiet --extended-regexp -i "darwin|msys|windows"; then
    echo "needs-cross=false" >> $GITHUB_OUTPUT
    exit 0
fi

# On Linux, we should be able to cross-compile to i586 and i686, but in
# practice this fails with some crates, notably openssl with the "vendored"
# feature. This feature makes it compile openssl itself, which fails without
# cross.
if echo "$TARGET" | grep --quiet --extended-regexp -i 'x86_64.+linux-(gnu|musl)'; then
    echo "needs-cross=false" >> $GITHUB_OUTPUT
    exit 0
fi

echo "needs-cross=true" >> $GITHUB_OUTPUT
