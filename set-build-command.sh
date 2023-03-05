set -e
set -x

if [ -f "$RUNNER_TEMP/cross" ]; then
    echo "build-command=$RUNNER_TEMP/cross" >> $GITHUB_OUTPUT
else
    echo "build-command=cargo" >> $GITHUB_OUTPUT
fi
