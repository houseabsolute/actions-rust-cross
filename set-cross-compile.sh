set -e
set -x

TARGET="$1"

# On macOS and Windows, we can cross-compile to all possible targets without
# using cross.
if uname -a | grep --quiet --extended-regexp -i "darwin|msys|windows"; then
    echo "needs-cross=false" >> $GITHUB_OUTPUT
    exit 0
fi

if echo "$TARGET" | grep --quiet --extended-regexp -i '(x86_64|586|686).+linux-(gnu|musl)'; then
    echo "needs-cross=false" >> $GITHUB_OUTPUT
    exit 0
fi

echo "needs-cross=true" >> $GITHUB_OUTPUT
