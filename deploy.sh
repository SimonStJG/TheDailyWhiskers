#!/usr/bin/env bash

set -euxo pipefail

ENVIRONMENT=$1
LOCAL_DIR=$(pwd)

# Setup some temporary directories
TMP_DIR=$(mktemp -d)
CONTENT_DIR="${TMP_DIR}/content"
trap "rm -rf ${TMP_DIR}" EXIT

TARGET="${TMP_DIR}/target-$(date '+%Y%m%d-%H%M%S').zip"

# Zip up everything we need
mkdir -p "${CONTENT_DIR}"
pip install -t "${CONTENT_DIR}" .
pushd "${CONTENT_DIR}"
cp "${LOCAL_DIR}/${ENVIRONMENT}-config.json" ./config.json
zip -r "${TARGET}" .
popd

# Deploy it
pushd infra
terraform init
terraform workspace select $ENVIRONMENT
terraform apply -var "lambda_code_zip=${TARGET}"
popd
