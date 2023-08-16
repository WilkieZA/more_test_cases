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

Usage:
    style_checker.py [options]
    style_checker.py [options] <file>...

Options:
    -h, --help      Show this help message and exit
    -v, --verbose   Print verbose output

@author: Dylan Kirby - 25853805
@date: 2023-08-15
@version: 1.0
"""

import os
import re
import sys

from docopt import docopt
from termcolor import cprint
from pprint import pprint

# Precompile regexes
ERROR_REGEXES = {
    # Logical Statements
    "no_if_space": re.compile(r"if\("),
    "no_for_space": re.compile(r"for\("),
    "no_while_space": re.compile(r"while\("),
    "no_switch_space": re.compile(r"switch\("),
    "no_case_space": re.compile(r"case\w"),
    "no_space_around_else": re.compile(r"(\}else)|(else\{)"),
    "else_on_newline": re.compile(r"^\s*else"),

    # Operators
    "multiplicative_with_only_one_space": re.compile(r"(([a-z0-9().]+\s+[*/][a-z0-9().]+)|([a-z0-9().]+[*/]\s+[a-z0-9().]+))"),
    "additive_with_only_one_space": re.compile(r"(([a-z0-9().]+\s+[+-][a-z0-9().]+)|([a-z0-9().]+[+-]\s+[a-z0-9().]+))"),
    "preprocessor_not_flush_with_left": re.compile(r"^\s+#"),

    # Delimmiters
    "no_space_after_comma": re.compile(r",\w"),
    "no_space_after_semicolon": re.compile(r";\w"),

    # Braces
    "paren_with_space": re.compile(r"(\(\s)|(\s\))"),
    "bracket_with_space": re.compile(r"(\[\s)|(\s\])"),
    "paren_and_curly_without_space": re.compile(r"\)\{"),
    
    # Function Calls
    "function_with_space": re.compile(r"\b(?!(if|for|while|switch|else|return|void|int|char|double)\b)[a-z]+\s\("),
    
    # Comments
    "single_line_comment": re.compile(r"//"),

    # Lines
    "line_ends_in_space": re.compile(r"\s\n$"),
    "line_longer_80_chars": re.compile(r"^.{81,}$"),

}

WARNING_REGEXES = {
    "spaces_around_additive_op_in_array_access": re.compile(r"\\w+\[\s*[a-z0-9]+(\s+[+-]\s*)|(\s*[+-]\s+)[a-z0-9]+\s*\]", re.IGNORECASE),
}

COMMENT_CHECKS = [
    "line_longer_80_chars",
    "line_ends_in_space",
    "single_line_comment"
]

IS_STRING_RE = re.compile(r"([\'\"])(.*?)\1")
IS_POINTER_RE = re.compile(r"(\b(void|int|char|double|[A-Z]\w+)\s*\*[),]*\s*\w*)")

ERR_LEVELS = {
    "ERROR": "red",
    "WARNING": "yellow",
    "POTENTIAL ERROR": "magenta"
}
def errprint(level, rule, file_name, line_num, line, match_group=None):
    """
    Prints an error message to the console.
    :param level: The level of the error (0 = error, 1 = warning, 2 = potential error)
    :param rule: The rule that was broken
    :param file_name: The name of the file that the error occured in
    :param line_num: The line number that the error occured on
    :param line: The line that the error occured on
    """

    color = ERR_LEVELS.get(level, "red")

    if match_group:
        line = line.replace(match_group, f"\033[1m{match_group}\033[0m")

    cprint(f"{level}: <{rule}> on line {line_num + 1} of {file_name}", color)
    print(">", line)
    print()

def get_files():
    c_files = []
    for root, dirs, files in os.walk("../src"):
        for file in files:
            if file.endswith(".c"):
                c_files.append(os.path.join(root, file))

    return c_files

def check_lines():

    errors = 0
    warnings = 0
    for line_num, line in enumerate(lines):

        # Precompute certain checks
        strp_line = line.strip()
        is_comment = strp_line.startswith(("/*", "*"), 0, 2)
        is_print = IS_STRING_RE.search(line)
        is_pointer = IS_POINTER_RE.search(line)

        for rule, regex in ERROR_REGEXES.items():

            if is_comment and rule not in COMMENT_CHECKS:
                continue

            re_match = regex.search(line)
            if not re_match:
                continue

            if is_pointer and rule == "multiplicative_with_only_one_space":
                errprint("POTENTIAL ERROR", rule, file, line_num, strp_line, re_match.group()) if is_verbose else None
                continue
            
            if is_print and is_print.start() < re_match.start():
                errprint("POTENTIAL ERROR", rule, file, line_num, strp_line, re_match.group())
                continue
                
            errprint("ERROR", rule, file, line_num, strp_line, re_match.group())
            errors += 1

        for rule, regex in WARNING_REGEXES.items():

            if is_comment and rule not in COMMENT_CHECKS:
                continue

            re_match = regex.search(line)
            if not re_match:
                continue

            errprint("WARNING", rule, file, line_num, strp_line, re_match.group())
            warnings += 1

    # make sure eof is on a newline
    if lines[-1] != "\n":
        errprint("ERROR", "eof_not_on_newline", file, len(lines), lines[-1].strip())
        errors += 1

    return (errors, warnings)

if __name__ == "__main__":

    args = docopt(__doc__)
    is_verbose = args["--verbose"]

    cprint("Starting style check...", "blue")

    c_files = get_files() if not args["<file>"] else args["<file>"]

    if is_verbose:
        cprint(f"Checking files:", "blue")
        pprint(c_files, indent=4)
        cprint(f"Rules:", "blue")
        pprint(ERROR_REGEXES, indent=2)
        cprint(f"Warnings:", "blue")
        pprint(WARNING_REGEXES, indent=2)
        print()

    total_errors = 0
    total_warnings = 0
    for file in c_files:
        with open(file, "r") as f:
            lines = f.readlines()

        e, w = check_lines()
        total_errors += e
        total_warnings += w

    c = "red" if total_errors else "yellow" if total_warnings else "green"
    cprint(f"Check finished with {total_errors} errors and {total_warnings} warnings.", c)

    if total_errors:
        sys.exit(1)

    sys.exit(0)