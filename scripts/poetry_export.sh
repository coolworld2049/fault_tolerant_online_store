#!/usr/bin/env bash

set -eou

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if command -v poetry &> /dev/null; then
  poetry export --without-hashes --format=requirements.txt > ${SCRIPT_DIR}/../requirements.txt
  git add ${SCRIPT_DIR}/../requirements.txt
else
    echo "Poetry is not installed. Please install it from https://python-poetry.org/docs/."
fi