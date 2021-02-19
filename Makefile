#!/usr/bin/env /usr/bin/make
# Makefile for Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
# Author: Lilian BESSON
# Email: lilian DOT besson AT crans D O T org
# Version: 1
# Date: 19-02-2021
# Web: https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
SHELL         = /usr/bin/env /bin/bash

PROTOCOL      = http
ADDRESS       = localhost
PORT          = 42920
URL           = $(PROTOCOL)://$(ADDRESS):$(PORT)

# ============== Rules for help ==============

all:	ngrok notify start test_hello_api
local:	notify start test_hello_api
total:	all clean

# ============== Rules for start server ==============

start:
	./venv3/bin/python3 ./app.py

ngrok:
	ngrok_and_text_address.sh $(PROTOCOL) $(PORT)

test_api:	test_hello_api test_python test_ocaml test_c
test_hello_api:	hello_api system_api languages_api
hello_api:
	curl --silent $(URL)
system_api:
	curl --silent $(URL)/system | python -m json.tool
languages_api:
	curl --silent $(URL)/languages | python -m json.tool

test_python:
	echo "TODO:"
	for f in json_tests/python/*.json; do printf "\n\nLoad ${f} - \n" && curl --silent -X POST -H "Content-Type: application/json" --data @${f} ${URL}; done

test_ocaml:
	echo "TODO:"
	for f in json_tests/python/*.json; do printf "\n\nLoad ${f} - \n" && curl --silent -X POST -H "Content-Type: application/json" --data @${f} ${URL}; done

test_c:
	echo "TODO:"
	for f in json_tests/python/*.json; do printf "\n\nLoad ${f} - \n" && curl --silent -X POST -H "Content-Type: application/json" --data @${f} ${URL}; done


#################################### Help #####################################

help:
	@echo "Help for utilities (by Lilian BESSON, https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git)"
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  setupvenv  to set-up and install requirements in a Python3 virtualenv"
	@echo "  total      to do everything"
	@echo "  local      to do local only"
	@echo "  test_hello_api connects and tests Camisole backend"
	@echo "  test_hello_api connects and tests Camisole backend"
	@echo "  notify     to notify that the server is ready"
	@echo "  clean      to COMPLETELY clean the temp files."
	@echo "  ngrok      if the local server is ready, open it to the world with https://ngrok.com"

# ============== Rules to send this online ==============

send:	send_zamok
send_zamok:	clean-temp
	CP --exclude=./.git/ ./ ${Szam}Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git/
send_local:	clean-temp
	CP --exclude=./.git/ ./ ~/Public/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git/

# ===================== Virtualenv =====================

setupvenv:	virtualenv install_requirements
virtualenv:
	virtualenv ./venv3/

install_requirements:
	. ./venv3/bin/activate
	./venv3/bin/pip3 install --upgrade --requirement=./requirements.txt

notify:
	notify-send "Local Peut-on-coder-avec-OCaml-Python-et-C-par-SMS ready\nGo to http://localhost:5000/"
	xdg-open http://localhost:5000/


# ===================== Cleaners =====================

clean:	clean-temp
clean-temp:
	-mv -vf ./*~ /tmp/
	# TODO: more

