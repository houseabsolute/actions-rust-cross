set -e
set -x

TARGET=$1

DIR=""
for type in debug release; do
    if [ -d "target/$TARGET/$type" ]; then
        DIR="target/$TARGET/$type"
        break
    elif [ -d "target/$type" ]; then
        DIR="target/$type"
        break
    fi
done

if [ -z "$DIR" ]; then
    echo "Could not find directory with binary in it under target/"
    exit 1
fi

if [[ $( uname -s ) =~ "Darwin" ]]; then
    EXE=$( find "$DIR" -maxdepth 1 -type f -perm +111 )
else
    EXE=$( find "$DIR" -maxdepth 1 -type f -executable )
fi

if [ -z "$EXE" ]; then
    echo "Could not find a binary to strip in $DIR"
    exit 2
fi

strip "$EXE"
