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
ERROR_REGEXES = {
    # Logical Statements
    "no_if_space": re.compile(r"if\("),
    "no_for_space": re.compile(r"for\("),
    "no_while_space": re.compile(r"while\("),
    "no_switch_space": re.compile(r"switch\("),
    "no_case_space": re.compile(r"case\w"),
    "no_space_around_else": re.compile(r"(\}else)|(else\{)"),

    # Braces
    "parenthesis_with_space": re.compile(r"(\(\s)|(\s\))"),
    "bracket_with_space": re.compile(r"(\[\s)|(\s\])"),
    
    # Function Calls
    "function_with_space": re.compile(r"\b(?!(if|for|while|switch|else|return|void|int|char|double)\b)[a-z]+\s\("),
    
    # Comments
    "single_line_comment": re.compile(r"//"),

    # Lines
    "line_ends_in_space": re.compile(r"\s\n$"),
    "line_longer_80_chars": re.compile(r"^.{81,}$"),

}

WARNING_REGEXES = {
    "spaces_around_additive_op_in_array_access": re.compile(r"\w\[\s*\w(\s+[+-]\s*)|(\s*[+-]\s+)\w\s*\]"),
}

COMMENT_CHECKS = [
    "line_longer_80_chars"
]

IS_PRINT_RE = re.compile(r"\w*print\w*\s*\(")


ERR_LEVELS = {
    "ERROR": "red",
    "WARNING": "yellow",
    "POTENTIAL ERROR": "magenta"
}
def errprint(level, rule, file_name, line_num, line):
    """
    Prints an error message to the console.
    
    :param level: The level of the error (0 = error, 1 = warning, 2 = potential error)
    :param rule: The rule that was broken
    :param file_name: The name of the file that the error occured in
    :param line_num: The line number that the error occured on
    :param line: The line that the error occured on
    """

    color = ERR_LEVELS.get(level, "red")

    cprint(f"{level}: <{rule}> on line {line_num + 1} of {file_name}", color)
    print(">", line)
    print()

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
    warnings = 0
    for file in c_files:
        with open(file, "r") as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines):
            for rule, regex in ERROR_REGEXES.items():

                strp_line = line.strip()
                is_comment = strp_line.startswith(("/*", "*"), 0, 2)
                # Skip checks on comments unless it is a comment check
                if is_comment and rule not in COMMENT_CHECKS:
                    continue

                re_match = regex.search(line)
                if re_match:
                    # Check for print statements
                    is_print = IS_PRINT_RE.search(line)
                    if is_print and is_print.start() < re_match.start():
                        errprint("POTENTIAL ERROR", rule, file, line_num, strp_line)
                    else:
                        errprint("ERROR", rule, file, line_num, strp_line)
                        errors += 1

            for rule, regex in WARNING_REGEXES.items():

                strp_line = line.strip()
                is_comment = strp_line.startswith("//") or strp_line.startswith("/*")
                # Skip checks on comments unless it is a comment check
                if is_comment and rule not in COMMENT_CHECKS:
                    continue

                if regex.search(line):
                    errprint("WARNING", rule, file, line_num, strp_line)
                    warnings += 1

        # make sure eof is on a newline
        if lines[-1] != "\n":
            cprint(f"ERROR: <eof_not_on_newline> on line {len(lines)} of {file}", "red")
            print(">", lines[-1].strip())
            print()
            errors += 1

    cprint(f"Check finished with {errors} errors and {warnings} warnings.", "red" if errors else "yellow" if warnings else "green")

    if errors:
        sys.exit(1)

    sys.exit(0)