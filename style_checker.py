"""
A style checker for C files.
It will automatically scan the `src/` directory, and should be executed from a sibling of `src/`.

The following will be checked:
| Requirement | Description                                    | Example        |
| ----------- | ---------------------------------------------- | -------------- |
| Required    | Indentation using tabs                         |                |
| Required    | Spaces between logical statements and braces   | if (           |
| Required    | Spaces in additive logical operators           | (x + 1)        |
| Required    | No spaces in additive operators in []          | x[a + b]       |
| Required    | Spaces between braces and statements           | } else {       |
| Optional    | Spaces in multiplicative operators             | x*y OR x + y   |
| Required    | Spaces between function calls and braces       | function (x) { |
| Required    | Spaces between braces and logical statements   | } (            |
| Required    | sizeof must be treated as a function           | sizeof (x)     |
| Required    | EOF must be on a newline                       | \\nEOF          |
| Required    | No sinle line comments                         | //             |
| Required    | No spaces after opening parenthesis            | ( x            |
| Required    | No lines containing only spaces or tabs        |                |
| Required    | No lines ending in spaces                      |                |

Usage: python3 style_checker.py

@author: Dylan Kirby - 25853805
@date: 2023-08-15
@version: 1.0
"""

import os
import re
from termcolor import cprint

# Precompile regexes
DISALLOWED_REGEXES = {
    "single_line_comment": re.compile(r"//"),
    "sizeof_with_space": re.compile(r"sizeof \("),
    "opening_parenthesis_space": re.compile(r"\(\s"),
    "closing_parenthesis_space": re.compile(r"\s\)"),
    "opening_bracket_space": re.compile(r"\[\s"),
    "closing_bracket_space": re.compile(r"\s\]"),
    "no_if_space": re.compile(r"if\("),
    "no_for_space": re.compile(r"for\("),
    "no_while_space": re.compile(r"while\("),
    "no_switch_space": re.compile(r"switch\("),
    "no_case_space": re.compile(r"case\("),
    "no_space_before_else": re.compile(r"\}else"),
    "no_space_after_else": re.compile(r"else\{"),
    "no_space_between_else_if": re.compile(r"elseif"),
    "no_newline_eof": re.compile(r"\nEOF"),
    "line_ends_in_space": re.compile(r"\s\n$"),
}


if __name__ == "__main__":

    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(__doc__)
            sys.exit(0)
        
        print("Usage: python3 style_checker.py")
        sys.exit(1)

    cprint("Starting style check...", "blue")

    # get all of the c files in the src directory
    c_files = []
    for root, dirs, files in os.walk("../src"):
        for file in files:
            if file.endswith(".c"):
                c_files.append(os.path.join(root, file))

    # check each file
    errors = 0
    for file in c_files:
        with open(file, "r") as f:
            lines = f.readlines()

        for rule, regex in DISALLOWED_REGEXES.items():
            for line_num, line in enumerate(lines):
                if regex.search(line):
                    print(f"ERROR: {rule} on line {line_num + 1} of {file}")
                    print(">", line.strip())
                    print()
                    errors += 1

    cprint(f"Check finished with {errors} errors.", "red" if errors else "green")