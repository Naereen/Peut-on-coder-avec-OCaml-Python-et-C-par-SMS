#!/usr/bin/env python3
# Flask server for https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS
# Author: Lilian BESSON
# Email: lilian DOT besson AT crans D O T org
# Version: 1
# Date: 19-02-2021
# Web: https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
#
# Source :
# https://www.fullstackpython.com/blog/respond-sms-text-messages-python-flask.html
# https://gist.github.com/mattmakai/8ab434ccb604d3ba5bde817a183e0bde
#

# Use time to sleep and get string for today current hour
import time
# To parse the password from the message
import re
from pprint import pprint
from typing import List, Tuple

# Use base64 to not keep plaintext files of the number, username and password in your home
import base64

from flask import Flask, Response, request
from twilio import twiml

from safeExecuteCode import safe_execute_code, URL, SUPPORTED_LANGUAGES


# DONE: read from .password.b64 file
def read_b64_file(name: str) -> str:
    """ Open the local file <name>, read and decode (base64) and return its content.
    """
    try:
        with open(name) as f:
            print(f"DEBUG: reading file '{name}'")
            content = base64.b64decode(f.readline()[:-1])
            while content[-1] == '\n':
                content = content[:-1]
            content = content.decode()
            print(f"DEBUG: content read is\n{content}")
            return content
    except OSError:
        print(f"Error: unable to read the file '{name}' ...")
        return None


PASSWORD = "1234"
PASSWORD = read_b64_file(".password.b64")
# TODO: create password file
if PASSWORD is None:
    PASSWORD = "1234"

print(f"Using password = {PASSWORD}...")



def has_password(message: str) -> bool:
    res = re.search("pw:([^ ]+)", message)
    return res is not None

def parse_password(message: str) -> str:
    res = re.search("pw:([^ ]+)", message)
    if res:
        password = res.group(0)
        password = password.replace("pw:", "", 1)
        return password
    # TODO: finish this function
    return ""

def check_password(password: str) -> bool:
    return password == PASSWORD


class FailedExecution(Exception):
    pass


# TODO: be able to really execute code
def execute_code(inputcode: str, language="python") -> Tuple[str, str, int]:
    print(f"DEBUG: You sent me this {language} code:\n{inputcode}")
    stdout, stderr = "", ""
    exitcode = 0
    stdout = f"You sent me this {language} code:\n{inputcode}"

    try:
        json_result = safe_execute_code(inputcode, language=language)
        print(f"DEBUG: I got back this JSON result:")
        pprint(json_result)  # DEBUG
        if not json_result["success"]:
            raise FailedExecution
        stdout = json_result["stdout"]
        stderr = json_result["stderr"]
        exitcode = json_result["exitcode"]
        # Example of a correct reply:
        # {
        #     "success": true,
        #     "tests": [
        #         {
        #             "exitcode": 0,
        #             "name": "test000",
        #             "stderr": "",
        #             "stdout": "42\n"
        #         }
        #     ]
        # }

    except Exception as e:
        print("Error:\n", e)
        stderr = f"Camisole VM was not probably available, check the configuration.\ncurl {URL}/\ncurl {URL}/system\ncurl {URL}/languages"
        stderr += f"\n\nError: {e}"
        exitcode = 1

    # now we are done, give this back to Flask API
    return stdout, stderr, exitcode


from collections import defaultdict
cellnumbers = defaultdict(lambda: 0)

def format_reply(language: str, stdout: str, stderr: str, exitcode=0) -> str:
    """ Format the reply to a nice message that can be printed or sent back by SMS."""
    global cellnumbers
    today = time.strftime("%H:%M:%S %Y-%m-%d")
    cellnumbers[language] += 1
    cellnumber = cellnumbers[language]
    if stderr and stdout:
        reply = f"""Time: {today}\nOut[{cellnumber}] {stdout}\nError[{cellnumber}] exitcode={exitcode} : {stderr}"""
    elif not stderr and stdout:
        reply = f"""Time: {today}\nOut[{cellnumber}] {stdout}"""
    elif stderr and not stdout:
        reply = f"""Time: {today}\nError[{cellnumber}] exitcode={exitcode} : {stderr}"""
    else:
        reply = f"""Time: {today}\nNo output or error for cell number {cellnumber}"""
    return reply


# ============== Test the API for two main languages ==============

FIRST_TESTS = [
    {
        "inputcode" : "print('Camisole backend works for Python!')",
        "language" : "python"
    },
    {
        "inputcode" : "print(f'The answer to life is = {4*10+2}')",
        "language" : "python"
    },
    {
        "inputcode": "print_endline 'Camisole backend works for OCaml!';;",
        "language": "ocaml",
    },
    {
        "inputcode": "Format.printf 'The answer to life is = %d' (4*10+2);;",
        "language": "ocaml",
    },
]

def test_backend() -> None:
    """ Test the API for two main languages."""
    for first_test in FIRST_TESTS:
        print(f"\nDEBUG: trying to use this JSON request:\n{first_test}")
        inputcode = first_test["inputcode"]
        language = first_test["language"]
        print(f"\nDEBUG: trying to execute this code in language={language}:\n{inputcode}")
        stdout, stderr, exitcode = execute_code(inputcode, language=language)
        print(f"DEBUG: got an answer with stdout, stderr, exitcode:\n{stdout}\n{stderr}\n{exitcode}")
        reply = format_reply(language, stdout, stderr)
        print(f"DEBUG: got a reply:\n{reply}")
        assert exitcode == 0

if __name__ == '__main__':
    test_backend()

# ================== now the Flask app ==================

app = Flask(__name__)


@app.route("/")
def check_app() -> Tuple[Response, int]:
    # returns a simple string stating the app is working
    return Response("It works! The local server is ready!\nNo, go to your Twilio page "), 200


@app.route("/twilio", methods=["POST"])
def inbound_sms() -> Tuple[Response, int]:
    response = twiml.Response()
    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = request.form.get("Body")
    # we can now use the incoming message text in our Python application

    # TODO: add a password
    if has_password(inbound_message):
        return Response("No password! Add a password by starting your SMS with pw:PASSWORD, with no space!"), 500
    password = parse_password(inbound_message)
    inbound_message = inbound_message.replace(f"pw:{password} ", "", 1)
    if not check_password(password):
        return Response("Wrong password! Hint: password might be 1234, if the developper was stupid!"), 500

    # test messages
    if inbound_message == "test":
        response.message("It works!")
    elif inbound_message == "Hello":
        response.message("Hello back to you from Python!")
    elif inbound_message == "Bonjour":
        response.message("Bien le bonjour depuis Python !")

    # return list of supported languages
    elif inbound_message == "Languages?":
        str_languages = ", ".join(SUPPORTED_LANGUAGES)
        response.message(f"List of supported languages are: {str_languages}")

    # return list of supported languages
    elif inbound_message == "Langages ?":
        str_languages = ", ".join(SUPPORTED_LANGUAGES)
        response.message(f"La liste des langues prises en charge est : {str_languages}")

    # now for languages
    else:
        for language in SUPPORTED_LANGUAGES:
            if inbound_message.startswith(f"{language}:"):

                inbound_message = inbound_message.replace("{language}:", "", 1).lstrip()
                stdout, stderr, exitcode = execute_code(inbound_message, language=language)
                reply = format_reply(language, stdout, stderr)

                response.message(reply)
                break
        # default response
        else:
            response.message("Hi! Not quite sure what you meant, but okay.\nSee https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS for more information!\n(C) Lilian Besson, 2021, MIT Licensed")

    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200


if __name__ == "__main__":
    app.run(debug=True)