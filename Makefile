#!/usr/bin/env /usr/bin/make
# Makefile for Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
# Author: Lilian BESSON
# Email: lilian DOT besson AT crans D O T org
# Version: 1
# Date: 19-02-2021
# Web: https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
SHELL         = /usr/bin/env /bin/bash
ADDRESS       = 127.0.0.1
PORT          = 12345

# ============== Rules for help ==============

all:	ngrok notify start
local:	notify start
total:	all clean

# ============== Rules for start server ==============

start:
	./venv3/bin/python3 ./app.py $(ADDRESS) $(PORT)

ngrok:
	ngrok_and_text_address.sh http $(PORT)


#################################### Help #####################################

help:
	@echo "Help for utilities (by Lilian BESSON, https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git)"
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  total      to do everything"
	@echo "  local      to do local only"
	@echo "  notify     to notify that the server is ready"
	@echo "  clean      to COMPLETELY clean the temp files."
	@echo "  ngrok      if the local server is ready, open it to the world with https://ngrok.io"

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
	notify-send "Local Peut-on-coder-avec-OCaml-Python-et-C-par-SMS ready!"


# ===================== Cleaners =====================

clean:	clean-temp
clean-temp:
	-mv -vf ./*~ /tmp/
	# TODO: more

