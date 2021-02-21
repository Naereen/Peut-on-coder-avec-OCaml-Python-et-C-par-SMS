#!/usr/bin/env python3
# Configure the limited ressources of Camisole execution/compilation for all process
# Author: Lilian BESSON
# Email: lilian DOT besson AT crans D O T org
# Version: 1
# Date: 19-02-2021
# Web: https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
#
# See https://camisole.prologin.org/usage.html#adding-limits-and-quotas

# Documentation:
# time: limit the user time of the program (seconds)
# wall-time: limit the wall time of the program (seconds)
# extra-time: grace period before killing a program after it exceeded a time limit (seconds)
# mem: limit the available memory of each process (kilobytes)
# virt-mem: limit the address space of each process (kilobytes)
# fsize: limit the size of files created by the program (kilobytes)
# processes: limit the number of processes and/or threads
# quota: limit the disk quota to a number of blocks and inodes (separate both numbers by a comma, eg. 10,30)
# stack: limit the stack size of each process (kilobytes)
#

camisole_limited_ressources_conf = {
    "compile": {
        "time": 60,
        "wall-time": 60,
        "extra-time": 15,
        "processes": 64,
        # "quota": "50,3",
        "fsize": 10_000,
        "stack": 10_000,
        "mem": 100_000,
    },
    "execute": {
        "time": 30,
        "wall-time": 30,
        "extra-time": 30,
        "processes": 64,
        # "quota": "50,3",
        "fsize": 10_000,
        "stack": 10_000,
        "mem": 100_000,
    }
}
