#!/usr/bin/env python3
# Link between python API/code to a Camisole server running in a VM, accessible by "http://localhost:42920/"
# for https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS
# Author: Lilian BESSON
# Email: lilian DOT besson AT crans D O T org
# Version: 1
# Date: 19-02-2021
# Web: https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
#

# See https://www.geeksforgeeks.org/get-post-requests-using-python/ for help on this HTTP client using a POST request
import json
import requests

PROTOCOL = "http"
ADDRESS = "localhost"
PORT = 42920
URL = f"{PROTOCOL}://{ADDRESS}:{PORT}"

def post_request_to_camisole(data,
        protocol=PROTOCOL,
        port=PORT,
        address=ADDRESS,
        url=None,
    ):
    if not url:
        url = f"{protocol}://{address}:{port}"
    try:
        json_data = json.dumps(data)
        result = requests.post(url=url, json=json_data)
        return result.json()
    except Exception as e:
        print(f"Error:\n{e}")
        return {
            "success": False,
        }

def safe_execute_code(inputcode,
        language="python",
        protocol=PROTOCOL,
        port=PORT,
        address=ADDRESS,
        url=None
    ):
    data = {
        "lang": str(language),
        "source": str(inputcode)
    }
    return post_request_to_camisole(data,
        protocol=protocol,
        port=port,
        address=address,
        url=url,
    )
