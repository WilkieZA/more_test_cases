# AMPL Testing Scripts

![Header Image](https://repository-images.githubusercontent.com/678396879/33ab37e9-c433-4848-b67a-8f535c5bcb8c)

**WARNING**: The validity of these tests is not guaranteed.

## Setup

### Requirements

System Requirements:
- Python 3
- GCC
- Make

```bash
sudo apt install gcc make python3 python3-pip
```

Additional python requirements can be installed with:
```bash
python3 -m pip install -r requirements.txt
```

## Repository Structure

The test scripts should be placed along side the `src/` directory of the `AMPL` compiler in the `test/` directory.

Follow the directory structure below:
```
ampl/
    src/
        test{module}.c
        {requirements}.c
        {requirements}.h
        Makefile
    test/
        test.py
        tests/
            0.ampl
            ...
        {module}/
            0.out
            ...
    bin/
        test{module}
```

## Scripts

**Note**: All test scripts should be run from the `test/` directory.

### Running Tests


The `test.py` script will run the tests, see:
```bash
python3 test.py --help
```

For the purposes of the scanner run:
```bash
# Run all tests
python3 test.py --scanner 0..30
```

### Style Checking

The `styletest.py` and `style_checker.py` scripts will run a style checker, see:
```bash
# Grep based style checker
python3 styletest.py
# Py regex based style checker
# This script has a --help flag for more information
python3 style_checker.py
```

The `style_checker.py` script will continually be improved upon, the `styletest.py` script is a depreciated solution.

### Auto-Formatt using clang-format

**Disclaimer**: Use auto-formatting at your own risk, it may break your code style.

You can set up automatic formatting using clang-format by running the following command:
```bash
python3 -m pip install clang-format && echo 'export PATH="$PATH'":$(python3 -m site --user-base)/bin\"" >> ~/.bashrc
```

This will install clang-format using pip, this is allowed in NARGA. Then it will add the path to the binary to your PATH variable.

You must then restart your terminal or run the following command:
```bash
source ~/.bashrc
```

You then need to copy or create a `.clang-format` file to the base directory of the project.

You may then run the following command to format your code:
```bash
clang-format -i src/*.c
```

**Note**: This will overwrite the files, so make sure you have committed your changes.
Run `git diff` to see changes.

### Creating tests for a module

*NB*: This script should only be used by people contributing to the test suite.

The `create_test_cases.sh` script saves the executed code to the module direcory, effectively overwriting the "expected out".

## Contributing

Please fork the repository and checkout a resonable branch name and submit a pull request to merge your changes.

> Do not commit directly to the `master` branch

## Acknowledgments

| Name              | Student Number |
| ----------------- | -------------- |
| Dylan Kirby       | 25853805       |
| Zander Von Ludwig | 25870963       |
| Michael van Zyl   | 22604731       |
| Matthew Stein     | 25400800       |
| Louis Wilkinson   | 25948873       |
