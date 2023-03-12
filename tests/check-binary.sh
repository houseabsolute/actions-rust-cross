set -e
set -x

TARGET=$1
EXPECT_CROSS=$2
EXPECT_FILE_RE=$3

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
