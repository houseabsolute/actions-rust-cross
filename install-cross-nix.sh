set -e
set -x
set -o pipefail

CROSS_DIR="$1"
VERSION="$2"

VERSION_ARGS=""
if [ -n "$VERSION" ]; then
    VERSION_ARGS="--tag $VERSION"
fi

cd "$CROSS_DIR"
export TARGET=.
curl --silent --location \
     https://raw.githubusercontent.com/houseabsolute/ubi/master/bootstrap/bootstrap-ubi.sh |
    sh
./ubi --project cross-rs/cross --matching musl --in . $VERSION_ARGS
