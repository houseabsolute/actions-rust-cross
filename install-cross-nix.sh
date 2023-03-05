set -e
set -x

cd "$RUNNER_TEMP"
export TARGET=.
curl --silent --location \
     https://raw.githubusercontent.com/houseabsolute/ubi/master/bootstrap/bootstrap-ubi.sh |
    sh
./ubi --project cross-rs/cross --matching musl --in .
