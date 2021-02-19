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
from requests.api import post

# TODO: when importing the module, connect to VM, and list languages
SUPPORTED_LANGUAGES = [
    "python",
    "ocaml",
    "c",
]

PROTOCOL = "http"
ADDRESS = "localhost"
PORT = 42920
URL = f"{PROTOCOL}://{ADDRESS}:{PORT}"

def post_request_to_camisole(data,
        protocol=PROTOCOL,
        port=PORT,
        address=ADDRESS,
        endpoint="",
        url=None,
        use_json=True,
    ):
    """ Post data as a JSON object to the URL and returns JSON response."""
    if not url:
        if endpoint:
            endpoint = f"/{endpoint}"
        url = f"{protocol}://{address}:{port}{endpoint}"
    # TODO: use a real logger? Flemme
    print(f"DEBUG: using url = {url}")
    try:
        print(f"DEBUG: reading data = {data}")
        json_data = data
        if use_json:
            json_data = json.dumps(data)
            print(f"DEBUG: forcing data to be JSON: json_data = {json_data}")
        print(f"DEBUG: making this request...")
        result = requests.post(url=url, json=json_data)
        print(f"DEBUG: got a result from this request...")
        result_json = result.json()
        pprint(result_json)
        result_data = json.loads(result_json)
        print(f"DEBUG: result_data = {result_data}")
        return result_data

    except Exception as e:
        print(f"Error:\n{e}")
        return {
            "success": False,
        }

# TODO: try to discover the list of supported languages
try:
    data = ""
    result = post_request_to_camisole(data, use_json=False, endpoint="languages")
    json_languages = result["languages"]
    languages = list(d.keys())
    SUPPORTED_LANGUAGES = languages
except Exception as e:
    print(f"Error:\n{e}")
    raise e


def safe_execute_code(inputcode,
        language="python",
        protocol=PROTOCOL,
        port=PORT,
        address=ADDRESS,
        url=None
    ):
    """ Ask Camisole to execute the <inputcode> written in <language>, and returns the JSON result from Camisole."""
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
