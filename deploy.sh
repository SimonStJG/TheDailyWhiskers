#!/usr/bin/env bash

set -euo pipefail

ENVIRONMENT=$1

rm -rf virtualenv
python -m venv virtualenv
source virtualenv/bin/activate
trap "rm -rf virtualenv" EXIT

mkdir -p target
TARGET="$(pwd)/target/target-$(date '+%Y%m%d-%H%M%S').zip"

pip install -r requirements.txt

zip "${TARGET}" dailywhiskers/*.py config.json

tmp_dir=$(mktemp -d)
trap "rm -rf $tmp_dir" EXIT
cp $ENVIRONMENT-config.json  ${tmp_dir}/config.json
pushd $tmp_dir
zip "${TARGET}" config.json
popd

pushd $VIRTUAL_ENV/lib/python3.6/site-packages
zip -r "${TARGET}" .
popd

pushd infra
terraform init
terraform workspace select $ENVIRONMENT
terraform apply -var "lambda_code_zip=${TARGET}"
popd
