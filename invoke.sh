#!/usr/bin/env bash
set -euxo pipefail

ENVIRONMENT=$1

# Setup some temporary directories
TMP_DIR=$(mktemp -d)
trap "rm -rf ${TMP_DIR}" EXIT

pushd $TMP_DIR
aws lambda invoke --function-name dailywhiskers-$ENVIRONMENT out --log-type Tail --query 'LogResult' --output text |  base64 -d
cat out
popd
