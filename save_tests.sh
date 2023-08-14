#!/bin/bash

# Save the tests to the module dir
# Usage: save_tests.sh <module> <start..stop>

echo "Executing script"
python3 test.py --save=save_tests --$1 $2 2>&1> /dev/null
mv save_tests/* $1/
rm -rf save_tests
echo "Execution Complete"
