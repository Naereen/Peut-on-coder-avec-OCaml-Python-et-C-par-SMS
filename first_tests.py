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
    {
        "inputcode" : "print(f\"Did you know floating points are WEIRD? 0.1+0.1+0.1 = {0.1+0.1+0.1}\")",
        "language" : "python"
    },
    {
        "inputcode" : "print(\"Printing 1000 lines like these!\\n\"*1000)",
        "language" : "python"
    },
    {
        "inputcode" : "print(\"Testing HTML markup in reply:<ul>\"+\"<li>Printing 10 lines like these!\\n</li>\"*10+\"</ul>End of list!\")",
        "language" : "python"
    },
    {
        "inputcode" : "import sys; print(\"What happens with a exitcode = 1 ?\"); sys.exit(1)",
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
    {
        "inputcode": "Format.printf \"Did you know floating points are WEIRD? (0.1+0.1+0.1)-0.3 = %g\" ((0.1 +. 0.1 +. 0.1) -. 0.3);;",
        "language": "ocaml",
    },
    {
        "inputcode": "print_endline (String.concat \"\" (Array.to_list (Array.make 1000 \"Printing 1000 lines like these!\\n\")));;",
        "language": "ocaml",
    },
    {
        "inputcode": "print_endline (\"Testing HTML markup in reply:<ul>\" ^ (String.concat \"\" (Array.to_list (Array.make 10 \"<li>Printing 10 lines like these!\\n</li>\"))) ^ \"</ul>End of list!\");;",
        "language": "ocaml",
    },
    {
        "inputcode": "print_endline \"Camisole backend works for OCaml!\";; exit 1;;",
        "language": "ocaml",
    },
]
TESTS_C = [
    {
        "inputcode": "#include <stdio.h>;\n/* Say hello */\nint main(void) {\nprintf(\"Camisole backend works for C!\");\nreturn 0;\n}",
        "language": "C",
    },
    {
        "inputcode": "#include <stdio.h>;\n/* Print 42 */\nint main(void) {\nint answer_to_life = 42;\nprintf(\"The answer to life is = %d\", answer_to_life);\nreturn 0;\n}",
        "language": "C",
    },
    {
        "inputcode": "#include <stdio.h>;\n/* Print ((1+(1e20-1e20))-(((1+1e20)-1e20))) */\nint main(void) {\nprintf(\"Did you know floating points are WEIRD? ((1+(1e20-1e20))-(((1+1e20)-1e20))) = %f\", ((1+(1e20-1e20))-(((1+1e20)-1e20))));\nreturn 0;\n}",
        "language": "C",
    },
    {
        "inputcode": "#include <stdio.h>;\n/* Say hello 1000 lines! */\nint main(void) {\nfor(int i=1;i<=1000;i++){\nprintf(\"Printing 1000 lines like these!\\n\");\n}\nreturn 0;\n}",
        "language": "C",
    },
    {
        "inputcode": "#include <stdio.h>;\n/* Test HTML in the output (not for SMS) */\nint main(void) {\nprintf(\"Testing HTML markup in reply:<ul>\");\nfor(int i=1;i<=10;i++){\nprintf(\"Printing 10 lines like these!\\n\");\n}\nprintf(\"</ul>End of list!\");\nreturn 0;\n}",
        "language": "C",
    },
    {
        "inputcode": "#include <stdio.h>;\n/* Say hello */\nint main(void) {\nprintf(\"What happens with a exitcode = 1 ?\");\nreturn 1;\n}",
        "language": "C",
    },
]

FIRST_TESTS = TESTS_PYTHON + TESTS_OCAML + TESTS_C

__all__ = [
    "TESTS_PYTHON", "TESTS_OCAML", "TESTS_C",
    "FIRST_TESTS",
]
