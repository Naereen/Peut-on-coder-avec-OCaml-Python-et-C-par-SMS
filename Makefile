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
PORT_BACKEND  = 42920
URL_BACKEND   = $(PROTOCOL)://$(ADDRESS):$(PORT_BACKEND)
PORT          = 5000
URL           = $(PROTOCOL)://$(ADDRESS):$(PORT)

# ============== Rules for help ==============

local:	notify start
server:	ngrok notify start
all:	server clean

# ============== Rules for start server ==============

start: test_api
	./venv3/bin/python3 ./app.py

ngrok:
	# TODO: don't use my script, just use ngrok?
	./start-ngrok.sh $(PROTOCOL) $(PORT) &

test_api:	test_hello_api test_python test_ocaml test_c
test_hello_api:	hello_api system_api languages_api
hello_api:
	curl --silent $(URL_BACKEND)
system_api:
	curl --silent $(URL_BACKEND)/system | python -m json.tool
languages_api:
	curl --silent $(URL_BACKEND)/languages | python -m json.tool

test_python:
	echo "TODO: complete and add more examples!"
	./test-backend.sh $(URL_BACKEND) ./json_tests/python/

test_ocaml:
	echo "TODO: complete and add more examples!"
	./test-backend.sh $(URL_BACKEND) ./json_tests/ocaml/

test_c:
	echo "TODO: complete and add more examples!"
	./test-backend.sh $(URL_BACKEND) ./json_tests/c/


#################################### Help #####################################

help:
	@echo "Help for utilities (by Lilian BESSON, https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git)"
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  setupvenv  to set-up and install requirements in a Python3 virtualenv"
	@echo "  server     to do everything"
	@echo "  local      to do local only"
	@echo "  test_hello_api connects and tests Camisole backend"
	@echo "  test_api   connects and tests Camisole backend"
	@echo "  notify     to notify that the server is ready"
	@echo "  clean      to clean the temp files."
	@echo "  ngrok      if the local server is ready, open it to the world with https://ngrok.com"

# ============== Rules to send this online ==============

send:	send_zamok
send_zamok:	clean-temp
	CP --exclude-from=.gitignore . ${Szam}publis/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git/
send_local:	clean-temp
	CP --exclude-from=.gitignore . ~/Public/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git/

# ===================== Virtualenv =====================

setupvenv:	virtualenv install_requirements
virtualenv:
	virtualenv ./venv3/

install_requirements:
	. ./venv3/bin/activate
	./venv3/bin/pip3 install --upgrade --requirement=./requirements.txt

notify:
	notify-send "Local Peut-on-coder-avec-OCaml-Python-et-C-par-SMS ready\nGo to $(URL)"
	xdg-open $(URL) &


# ===================== Cleaners =====================

clean:	clean-temp
# TODO: more
clean-temp:
	-mv -vf ./*~ /tmp/

