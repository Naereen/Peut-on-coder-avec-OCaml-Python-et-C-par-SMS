#!/usr/bin/env bash
# Test the Camisole backend for https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS
# Author: Lilian BESSON
# Email: lilian DOT besson AT crans D O T org
# Version: 1
# Date: 19-02-2021
# Web: https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
#

URL="${1%/}"
FOLDER="${2%/}"

echo -e "\n\nReading JSON files from folder '${FOLDER}': \n"

for f in "$FOLDER"/*.json; do
    echo -e "\n\nLoad JSON file '${f}': \n"
    echo curl --silent \
        -X POST -H "Content-Type: application/json" \
        --data @"${f}" \
        "${URL}/run" \
        | cat
        # | python3 -m json.tool
done
