set -e
set -x

CROSS_DIR="$1"
if [ -f "$CROSS_DIR/cross" ]; then
    echo "build-command=$CROSS_DIR/cross" >> $GITHUB_OUTPUT
else
    echo "build-command=cargo" >> $GITHUB_OUTPUT
fi
