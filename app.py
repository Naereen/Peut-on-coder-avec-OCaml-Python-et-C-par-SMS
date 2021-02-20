#!/usr/bin/env python3
# Flask server for the application
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

# Use to check if password file is present
import json
import os.path
# Use time get string for today current hour
import time
# to launch a random test
import random
# To parse the password from the message
import re
from pprint import pprint
from typing import Tuple

# Use base64 to not keep plaintext files of the number, username and password in your home
import base64

from flask import Flask, Response, request
from twilio import twiml

from safeExecuteCode import safe_execute_code, URL, SUPPORTED_LANGUAGES

# Turn to True if DEBUG mode
# DEBUG mode for a Flask app means that it automatically reloads when this file changes!
DEBUG = False
DEBUG = True

today = time.strftime("%H:%M:%S %Y-%m-%d")


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


PASSWORD_FILE = ".password.b64"
PASSWORD = "1234"
if not os.path.exists(PASSWORD_FILE):
    print(f"\nPassword file '{PASSWORD_FILE}' does not exist, please enter a password!")
    local_password = input("Password= ")
    # TODO real password input? Flemme! so not important
    with open(PASSWORD_FILE, "w") as file:
        print(base64.encodebytes(local_password.encode()), file=file, flush=True)

PASSWORD = read_b64_file(PASSWORD_FILE)
if PASSWORD is None:
    PASSWORD = "1234"

print(f"Using password = {PASSWORD}...")


def has_password(message: str) -> bool:
    """ Checks for presence of a password in message, in the form of `pw:SOMEPASSWORDNOSPACE`."""
    res = re.search("pw:([^ ]+)", message)
    return res is not None

def parse_password(message: str) -> str:
    """ Returns password in message, in the form of `pw:SOMEPASSWORDNOSPACE`."""
    res = re.search("pw:([^ ]+)", message)
    if res:
        password = res.group(0)
        password = password.replace("pw:", "", 1)
        return password
    return ""

def check_password(password: str) -> bool:
    """ Checks if password in message is correct."""
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

        first_result = json_result
        if "compile" in json_result \
            and "exitcode" in json_result["compile"] \
            and json_result["compile"]["exitcode"] > 0:
                compile_result = json_result["compile"]
                stdout = compile_result["stdout"]
                stderr = compile_result["stderr"]
                exitcode = compile_result["exitcode"]
        # Example of a reply of failed compilation:
        # {'compile': {'exitcode': 1,
        #         'meta': {'cg-mem': 8036,
        #                 'cg-oom-killed': 0,
        #                 'csw-forced': 12,
        #                 'csw-voluntary': 4,
        #                 'exitcode': 2,
        #                 'exitsig': 0,
        #                 'exitsig-message': None,
        #                 'killed': False,
        #                 'max-rss': 16532,
        #                 'message': 'Exited with error status 2',
        #                 'status': 'RUNTIME_ERROR',
        #                 'time': 0.014,
        #                 'wall-time': 0.027},
        #         'stderr': 'File "/box/source.ml", line 1, characters 74-77:\n'
        #                 'Error: This expression has type float but an '
        #                 'expression was expected of type\n'
        #                 '         int\n',
        #         'stdout': ''},
        # 'success': True}
        else:
            if "tests" in json_result:
                first_result = json_result["tests"][0]
            stdout = first_result["stdout"]
            stderr = first_result["stderr"]
            exitcode = first_result["exitcode"]
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
        stderr = f"Camisole VM was probably not available, check the configuration.\n$ curl {URL}/\n$ curl {URL}/system\n$ curl {URL}/languages"
        stderr += f"\n\nError: {e}"
        exitcode = 1
        # only for DEBUG, kill the server and print the calltrace
        if DEBUG:
            raise e

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
import first_tests

def test_backend() -> None:
    """ Test the API for two main languages."""
    for first_test in first_tests.FIRST_TESTS:
        print(f"\nDEBUG: trying to use this JSON request:\n{first_test}")
        inputcode = first_test["inputcode"]
        language = first_test["language"]
        print(f"\nDEBUG: trying to execute this code in language={language}:\n{inputcode}")
        stdout, stderr, exitcode = execute_code(inputcode, language=language)
        print(f"DEBUG: got an answer with stdout, stderr, exitcode:\n{stdout}\n{stderr}\n{exitcode}")
        reply = format_reply(language, stdout, stderr)
        print(f"DEBUG: got a reply:\n{reply}")
        # assert exitcode == 0

if __name__ == '__main__':
    test_backend()

# ================== now the Flask app ==================

app = Flask("Peut on coder avec OCaml Python et C par SMS ?")


@app.route("/")
def check_app() -> Tuple[Response, int]:
    # returns a detailed documentation of the app!
    str_languages = ", ".join(SUPPORTED_LANGUAGES)
    return Response("""
<h1>« Peut on coder avec OCaml Python et C par SMS ? »</h1>
It works! The local server is ready!
TODO: test the SMS part now, when Twilio will give me my number!
<h2>Documentation of this API</h2>
This API has the following end-points, please try them!
<ul>
<li><a href="http://localhost:5000/languages">Lists available programming languages</a> : """ + str_languages + """ ;</li>
<li><a href="http://localhost:5000/langages">Liste les langages de programmation supporté</a> : """ + str_languages + """ ;</li>
<li>And to test one of the main three supported languages, use:<ul>
    <li><a href="http://localhost:5000/test/python">Test Python language (random test)</a> ;</li>
    <li><a href="http://localhost:5000/test/ocaml">Test OCaml language (random test)</a> ;</li>
    <li><a href="http://localhost:5000/test/c">Test C language (random test)</a> ;</li>
    </ul></li>
</ul>
Now, <a href="https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git">go read the documentation to conclude your setup</a> (in French, so far).
Enjoy!
<br>
If all the API end-points work, and if you have a Twilio account, then start "ngrok" for HTTP tunneling, add the ngrok proxy address to your Twilio dashboard, and try to send some code to your Twilio phone number (using your own phone).
<br>
<h2>Format of SMS messages</h2>
<ul>
<li><code>pw:PASSWORD python: print("Hello world from Python!")</code></li>
<li><code>pw:PASSWORD ocaml: print_endline "Hello world from OCaml!"</code></li>
<li><code>pw:PASSWORD c: #include <stdio.h>;\n/* Say hello */\nint main(void) {\nprintf("Hello world from C!");\nreturn 0;\n}"</code></li>
</ul>
<b>Be aware that each SMS costs around 0.07€!</b>
<hr>
<h2>About this project</h2>
Flask app started at """ + str(today) + """.
<br>
This script and this documentation are distributed in open access according to the conditions of the <a href="https://lbesson.mit-license.org/">licence MIT</a>.
© <a href="https://GitHub.com/Naereen">Lilian Besson</a>, 2021.
"""), 200

# return list of supported languages
@app.route("/languages")
def app_route_language() -> Tuple[Response, int]:
    str_languages = ", ".join(SUPPORTED_LANGUAGES)
    return Response(f"List of supported languages are: {str_languages}"), 200

@app.route("/langages")
def app_route_langage() -> Tuple[Response, int]:
    str_languages = ", ".join(SUPPORTED_LANGUAGES)
    return Response(f"La liste des langues prises en charge est : {str_languages}"), 200

@app.route("/test")
def app_route_test() -> Tuple[Response, int]:
    return Response(f"""Open one of these links to test the code execution API:
<ul>
    <li><a href="http://localhost:5000/test/python">Test Python language (random test)</a> ;</li>
    <li><a href="http://localhost:5000/test/ocaml">Test OCaml language (random test)</a> ;</li>
    <li><a href="http://localhost:5000/test/c">Test C language (random test)</a> ;</li>
</ul>
"""), 200

# TODO factor these /test/XXX endpints

@app.route("/test/python")
def app_route_testpython() -> Tuple[Response, int]:
    language = "python"
    random_test = random.choice(first_tests.TESTS_PYTHON)["inputcode"]
    stdout, stderr, exitcode = execute_code(random_test, language=language)
    reply = format_reply(language, stdout, stderr, exitcode=exitcode)
    return Response(reply), 200

@app.route("/test/ocaml")
def app_route_testocaml() -> Tuple[Response, int]:
    language = "ocaml"
    random_test = random.choice(first_tests.TESTS_OCAML)["inputcode"]
    stdout, stderr, exitcode = execute_code(random_test, language=language)
    reply = format_reply(language, stdout, stderr, exitcode=exitcode)
    return Response(reply), 200

@app.route("/test/c")
def app_route_testc() -> Tuple[Response, int]:
    language = "c"
    random_test = random.choice(first_tests.TESTS_C)["inputcode"]
    stdout, stderr, exitcode = execute_code(random_test, language=language)
    reply = format_reply(language, stdout, stderr, exitcode=exitcode)
    return Response(reply), 200


# ============ now the Twilio part ============

@app.route("/twilio", methods=["POST"])
def inbound_sms() -> Tuple[Response, int]:
    response = twiml.Response()
    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = request.form.get("Body")
    # we can now use the incoming message text in our Python application

    # DONE add a password
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
                reply = format_reply(language, stdout, stderr, exitcode=exitcode)

                response.message(reply)
                break
        # default response
        else:
            response.message("Hi! Not quite sure what you meant, but okay.\nSee https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS for more information!\n(C) Lilian Besson, 2021, MIT Licensed")

    # we return back the mimetype because Twilio needs an XML response
    return Response(str(response), mimetype="application/xml"), 200


if __name__ == "__main__":
    app.run(debug=DEBUG)