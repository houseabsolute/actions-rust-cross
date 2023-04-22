set -e
set -x

TARGET=$1
stripped=""

strip_binary () {
    if [[ $( uname -s ) =~ "Darwin" ]]; then
        EXE=$( find "$1" -maxdepth 1 -type f -perm +111 )
    else
        EXE=$( find "$1" -maxdepth 1 -type f -executable )
    fi

    if [ -z "$EXE" ]; then
        echo "Could not find a binary to strip in $1"
    else
        strip "$EXE"
        stripped="$EXE"
    fi
}

for type in debug release; do
    if [ -d "target/$TARGET/$type" ]; then
        strip_binary "target/$TARGET/$type"
    elif [ -d "target/$type" ]; then
        strip_binary "target/$type"
    fi
done

if [ -z "$stripped" ]; then
    echo "No binaries were stripped"
    exit 1
fi
