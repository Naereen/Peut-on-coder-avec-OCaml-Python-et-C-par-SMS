#!/usr/bin/env bash
# Test the Camisole backend for https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS
# For all the ./json_tests/LANGUAGE/*.json files, the expected output is ONE line printing 42
#
# TODO: automatically produce the .json files if it's not present? flemme
#
# Author: Lilian BESSON
# Email: lilian DOT besson AT crans D O T org
# Version: 1
# Date: 19-02-2021
# Web: https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
#

# http://redsymbol.net/articles/unofficial-bash-strict-mode/
set -euo pipefail

URL="${1%/}"
FOLDER="${2%/}"

echo -e "\n\nReading JSON files from folder '${FOLDER}':"

for f in "$FOLDER"/*.json; do
    echo -e "\nLoad JSON file '${f}':"
    echo curl --silent \
        -X POST -H "Content-Type: application/json" \
        --data @"${f}" \
        "${URL}/run"
    curl --silent \
        -X POST -H "Content-Type: application/json" \
        --data @"${f}" \
        "${URL}/run" \
        | python -m json.tool \
        | grep -o '"stdout": "42\(\\n\)\?"'
        # | cat
done
