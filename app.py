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
from typing import Tuple, Union

# Use base64 to not keep plaintext files of the number, username and password in your home
import base64

from flask import Flask, Response, request

# https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python
# this is the OLD API
# from twilio import twiml
from twilio.twiml.messaging_response import MessagingResponse

from safeExecuteCode import safe_execute_code, URL, SUPPORTED_LANGUAGES

# Turn to True if DEBUG mode
# DEBUG mode for a Flask app means that it automatically reloads when this file changes!
DEBUG = False
DEBUG = True

# To avoid risking a HUGE Twilio bill, by default the server stops as soon as one language has received more than MAX_SMSNUMBER requests by SMS.
MAX_SMSNUMBER = 100

def today():
    return time.strftime("%H:%M:%S %Y-%m-%d")


# DONE: read from .password.b64 file
def read_b64_file(name: str) -> Union[None, str]:
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
            content = content.replace('\n', '')
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
    print(f"DEBUG: message = '{message}'")
    print(f"DEBUG: and PASSWORD = '{PASSWORD}'")
    res = re.search("pw:([^ ]+) ", message)
    return res is not None

def parse_password(message: str) -> str:
    """ Returns password in message, in the form of `pw:SOMEPASSWORDNOSPACE`."""
    print(f"DEBUG: message = '{message}'")
    print(f"DEBUG: and PASSWORD = '{PASSWORD}'")
    res = re.search("pw:([^ ]+) ", message)
    if res:
        password = res.group(0)
        print(f"DEBUG: found a matching password = '{password}'")
        password = password.replace("pw:", "", 1)
        password = password.rstrip()
        print(f"DEBUG: cleaned to password = '{password}'")
        return password
    return ""

def check_password(password: str) -> bool:
    """ Checks if password in message is correct."""
    print(f"DEBUG: checking = '{password}'")
    print(f"DEBUG: and PASSWORD = '{PASSWORD}'")
    return password == PASSWORD


class FailedExecution(Exception):
    pass


# TODO: be able to really execute code
def execute_code(inputcode: str, language="python") -> Tuple[str, str, int, dict]:
    print(f"DEBUG: You sent me this {language} code:\n{inputcode}")
    stdout, stderr = "", ""
    exitcode = 0
    json_result = dict()
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
    return stdout, stderr, exitcode, json_result


from collections import defaultdict
cellnumbers = defaultdict(lambda: 0)
smsnumber = 0

def format_reply(language: str, stdout: str, stderr: str, exitcode=0, full_data=None) -> str:
    """ Format the reply to a nice message that can be printed or sent back by SMS."""
    global cellnumbers, smsnumber
    cellnumbers[language] += 1
    cellnumber = cellnumbers[language]
    smsnumber += 1
    assert smsnumber <= MAX_SMSNUMBER, f"Error: cell number for language='{language}' reached the maximum {MAX_SMSNUMBER}, so stopping the server.\nThis is NOT a bug, it's a feature, to avoid huge Twilio bills!"
    if stderr and stdout:
        reply = f"""Time: {today()}\nOut[{cellnumber}] {stdout}\nError[{cellnumber}] exitcode={exitcode} : {stderr}"""
    elif not stderr and stdout:
        reply = f"""Time: {today()}\nOut[{cellnumber}] {stdout}"""
    elif stderr and not stdout:
        reply = f"""Time: {today()}\nError[{cellnumber}] exitcode={exitcode} : {stderr}"""
    else:
        # TODO: print compiler error if something failed?
        # {'success': True,
        # 'tests': [{'exitcode': 1,
        #             'meta': {'cg-mem': 2492,
        #                     'cg-oom-killed': 0,
        #                     'csw-forced': 10,
        #                     'csw-voluntary': 66,
        #                     'exitcode': 0,
        #                     'exitsig': 0,
        #                     'exitsig-message': None,
        #                     'killed': True,
        #                     'max-rss': 7136,
        #                     'message': 'Time limit exceeded (wall clock)',
        #                     'status': 'TIMED_OUT',
        #                     'time': 0.017,
        #                     'wall-time': 60.116},
        #             'name': 'test000',
        #             'stderr': '',
        #             'stdout': ''}]
        if full_data and "tests" in full_data and "meta" in full_data["tests"][0]:
            warning_response = "(empty default warning response)"  # TODO:
            meta_data = full_data["tests"][0]["meta"]
            if "message" in meta_data:
                warning_response = meta_data["message"]
                if "(wall clock)" in warning_response and "wall-time" in meta_data:
                    wall_time = meta_data["wall-time"]
                    warning_response = warning_response.replace("(wall clock)", f"(wall clock) (time = {wall_time})")
                if "(time clock)" in warning_response and "time" in meta_data:
                    time_clock = meta_data["time"]
                    warning_response = warning_response.replace("(time clock)", f"(time clock) (time = {time_clock})")
            reply = f"""Time: {today()}\nFailed compilation or execution, got this reply for cell number {cellnumber}\n{warning_response}"""
        else:
            reply = f"""Time: {today()}\nNo output or error for cell number {cellnumber}"""
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
        stdout, stderr, exitcode, _ = execute_code(inputcode, language=language)
        print(f"DEBUG: got an answer with stdout, stderr, exitcode:\n{stdout}\n{stderr}\n{exitcode}")
        reply = format_reply(language, stdout, stderr, full_data=first_test)
        print(f"DEBUG: got a reply:\n{reply}")

        # TODO: when starting the server, it's expected that all tests should work!
        if not "What happens with a exitcode = 1 ?" in reply:
            assert exitcode == 0

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
    stdout, stderr, exitcode, _ = execute_code(random_test, language=language)
    reply = format_reply(language, stdout, stderr, exitcode=exitcode)
    return Response(reply), 200

@app.route("/test/ocaml")
def app_route_testocaml() -> Tuple[Response, int]:
    language = "ocaml"
    random_test = random.choice(first_tests.TESTS_OCAML)["inputcode"]
    stdout, stderr, exitcode, _ = execute_code(random_test, language=language)
    reply = format_reply(language, stdout, stderr, exitcode=exitcode)
    return Response(reply), 200

@app.route("/test/c")
def app_route_testc() -> Tuple[Response, int]:
    language = "c"
    random_test = random.choice(first_tests.TESTS_C)["inputcode"]
    stdout, stderr, exitcode, _ = execute_code(random_test, language=language)
    reply = format_reply(language, stdout, stderr, exitcode=exitcode)
    return Response(reply), 200


# ============ now the Twilio part ============

# def inbound_sms() -> str:
@app.route("/twilio", methods=["POST"])
def inbound_sms() -> Tuple[Response, int]:
    response = MessagingResponse()
    # we get the SMS message from the request. we could also get the
    # "To" and the "From" phone number as well
    inbound_message = request.form.get("Body")
    print(f"DEBUG: {today()} received a new message:\n{inbound_message}")
    # we can now use the incoming message text in our Python application

    # test messages
    # TODO: remove when DEBUG is done (https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS/issues/1)
    if inbound_message == "test":
        # DONE it works! 2021-02-21 04:33:03
        print(f"DEBUG: sending back\nIt works!")
        response.message("It works!")
    elif inbound_message == "Hello":
        # DONE it works! 2021-02-21 04:33:03
        print(f"DEBUG: sending back\nHello back to you from Python!")
        response.message("Hello back to you from Python!")
    elif inbound_message == "Bonjour":
        # DONE it works! 2021-02-21 04:33:03
        print(f"DEBUG: sending back\nBien le bonjour depuis Python !")
        response.message("Bien le bonjour depuis Python !")

    # return list of supported languages
    elif inbound_message == "Languages?":
        # DONE it works! 2021-02-21 04:33:03
        str_languages = ", ".join(SUPPORTED_LANGUAGES)
        print(f"DEBUG: sending back\nList of supported languages are: {str_languages}")
        response.message(f"List of supported languages are: {str_languages}")

    # return list of supported languages
    elif inbound_message == "Langages ?":
        # DONE it works! 2021-02-21 04:33:03
        str_languages = ", ".join(SUPPORTED_LANGUAGES)
        print(f"DEBUG: sending back\nLa liste des langues prises en charge est : {str_languages}")
        response.message(f"La liste des langues prises en charge est : {str_languages}")

    # now for languages
    else:
        # DONE add a password
        if not has_password(inbound_message):
            print("ERROR: No password! Add a password by starting your SMS with pw:PASSWORD, with no space!")  # DEBUG
            return Response("No password! Add a password by starting your SMS with pw:PASSWORD, with no space!"), 500
        password = parse_password(inbound_message)
        print(f"DEBUG: extracted password to be: '{password}'")
        inbound_message = inbound_message.replace(f"pw:{password} ", "", 1)
        if not check_password(password):
            print("ERROR: Wrong password! Hint: password might be 1234, if the developper was stupid!")  # DEBUG
            return Response("Wrong password! Hint: password might be 1234, if the developper was stupid!"), 500
        for language in SUPPORTED_LANGUAGES:
            if inbound_message.startswith(f"{language}:"):
                print(f"\nDEBUG: ==> detected that the message uses language = {language}")
                inbound_message = inbound_message.replace(f"{language}:\n", "", 1).lstrip()
                print(f"DEBUG: cleaned inbound_message:\n{inbound_message}")
                inbound_message = inbound_message.replace(f"{language}:", "", 1).lstrip()
                print(f"DEBUG: cleaned inbound_message:\n{inbound_message}")
                stdout, stderr, exitcode, full_data = execute_code(inbound_message, language=language)
                print(f"DEBUG: code stdout:\n{stdout}")
                print(f"DEBUG: code stderr:\n{stderr}")
                print(f"DEBUG: code exitcode = {exitcode}")

                reply = format_reply(language, stdout, stderr, exitcode=exitcode, full_data=full_data)
                print(f"DEBUG: giving back this reply:\n{reply}")

                response.message(reply)
                break
        # default response
        else:
            response.message("Hi! Not quite sure what you meant, but okay.\nLanguage not recognized maybe?\nSent 'Languages?' to get list of languages\nSee https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS for more information!\n(C) Lilian Besson, 2021, MIT Licensed")

    print(f"DEBUG: done for the reply, sending back with code=200 (success), this text:\n{str(response)}")
    return Response(str(response)), 200


if __name__ == "__main__":
    app.run(debug=DEBUG)