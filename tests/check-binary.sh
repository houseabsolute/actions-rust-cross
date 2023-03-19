set -e
set -x

TARGET=$1
EXPECT_CROSS=$2
EXPECT_FILE_RE=$3
EXPECT_STRIPPED=$4

if [ "$EXPECT_CROSS" == "true" ]; then
    if [ ! -f "$RUNNER_TEMP/cross" ]; then
        echo "Could not find cross in path: $PATH"
        exit 1
    fi
else
    if [ -f "$RUNNER_TEMP/cross" ]; then
        echo "Found cross in path: $PATH"
        exit 1
    fi
fi

FILE=$(file --brief ./target/$TARGET/debug/test-project)
if [[ "$FILE" =~ $EXPECT_FILE_RE ]]; then
    echo "file output matches $EXPECT_FILE_RE"
else
    echo "file output does not match $EXPECT_FILE_RE"
    exit 2
fi

if [[ $( uname -s ) =~ "Darwin" ]]; then
    # File on macOS doesn't report whether the binary is stripped or not.
    exit 0
fi

if [[ "$FILE" =~ "not stripped" ]]; then
    echo "binary was not stripped"
    GOT_STRIPPED="false"
elif [[ "$FILE" =~ "stripped" ]]; then
    echo "binary was stripped"
    GOT_STRIPPED="true"
else
    # On Windows the aarch64 binary's file info doesn't include the word
    # "stripped" at all.
    echo "binary was not stripped"
    GOT_STRIPPED="false"
fi

if [ "$EXPECT_STRIPPED" != "$GOT_STRIPPED" ]; then
    exit 3
fi
