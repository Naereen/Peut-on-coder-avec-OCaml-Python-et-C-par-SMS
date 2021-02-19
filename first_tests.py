#!/usr/bin/env python3
# Define some basic test for the Camisole backend
# Email: lilian DOT besson AT crans D O T org
# Version: 1
# Date: 19-02-2021
# Web: https://github.com/Naereen/Peut-on-coder-avec-OCaml-Python-et-C-par-SMS.git
#

TESTS_PYTHON = [
    {
        "inputcode" : "print(\"Camisole backend works for Python!\")",
        "language" : "python"
    },
    {
        "inputcode" : "print(f\"The answer to life is = {4*10+2}\")",
        "language" : "python"
    },
]
TESTS_OCAML = [
    {
        "inputcode": "print_endline \"Camisole backend works for OCaml!\";;",
        "language": "ocaml",
    },
    {
        "inputcode": "Format.printf \"The answer to life is = %d\" (4*10+2);;",
        "language": "ocaml",
    },
]
TESTS_C = [
    {
        "inputcode": "#include <stdio.h>;\n/* Say hello */\nint main(void) {\nprintf(\"Camisole backend works for C!\");\nreturn 0;\n}",
        "language": "C",
    },
    {
        "inputcode": "#include <stdio.h>;\n/* Print 42 */\nint main(void) {\nint answer_to_life = 42;\nprintf(\"The answer to life is =%d\", answer_to_life);\nreturn 0;\n}",
        "language": "C",
    },
]

FIRST_TESTS = TESTS_PYTHON + TESTS_OCAML + TESTS_C

__all__ = [
    "TESTS_PYTHON", "TESTS_OCAML", "TESTS_C",
    "FIRST_TESTS",
]
