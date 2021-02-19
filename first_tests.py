
TESTS_PYTHON = [
    {
        "inputcode" : "print(\"Camisole backend works for Python!\"a)",
        "language" : "python"
    },
    {
        "inputcode" : "print(f\"The answer to life is = {4*10+2}\"a)",
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
        "inputcode": "#include <stdio.h>;\n/* Say hello */\nint main(int argc, char** argv) {\nprintf(\"Camisole backend works for Python!\");\nreturn 0;\n}",
        "language": "C",
    },
    {
        "inputcode": "#include <stdio.h>;\n/* Print 42 */\nint main(int argc, char** argv) {\nint answer_to_life = 42;\nprintf(\"The answer to life is =%d\", answer_to_life);\nreturn 0;\n}",
        "language": "C",
    },
]

FIRST_TESTS = TESTS_PYTHON + TESTS_OCAML + TESTS_C