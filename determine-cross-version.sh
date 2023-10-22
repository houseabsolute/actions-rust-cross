set -e
set -x
set -o pipefail

VERSION=$1

if [ -z "$VERSION" ]; then
    JSON=$( curl \
                --request GET \
                --header "Authorization: Bearer $GITHUB_TOKEN" \
                https://api.github.com/repos/cross-rs/cross/releases/latest )
    VERSION=$( echo "$JSON" | jq -r ".tag_name")
fi

echo "cross-version=$VERSION" >> $GITHUB_OUTPUT
