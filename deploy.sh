#!/usr/bin/env bash

source virtualenv/bin/activate

set -euo pipefail

mkdir -p target
TARGET="$(pwd)/target/target-$(date '+%Y%m%d-%H%M%S').zip"

pip install -r requirements.txt

zip "${TARGET}" dailywhiskers/*.py config.json

pushd $VIRTUAL_ENV/lib/python3.5/site-packages
zip -r "${TARGET}" .
popd

pushd infra > /dev/null
terraform init
terraform apply -var "lambda_code_zip=${TARGET}"
popd > /dev/null