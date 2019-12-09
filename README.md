# youtube-lecture-parser

This repository pulls down and processes YouTube lectures that have captions.  It is intended to facilitate processing of posted lectures.

## Usage

For help on cli parameters:

```bash
python main.py --help
```

Example use case:

```bash
python main.py www.youtube.com -o ./output_directory
```

Microservice

```bash
python server_main.py
```

## Installation

### Install Tesseract

If on ubuntu or debian based you can run the bash script `install_tesseract.sh`.

If on windows reference the tesseract website instructions.

<https://github.com/tesseract-ocr/tesseract/wiki>

### Install Conda

https://docs.conda.io/projects/conda/en/latest/user-guide/install/

Once installed create the environment from the yaml file.

```bash
conda env create -f conda_env.yml
```

## Development Setup

Depending on your environment you will need git and some sort of shell script to run the helpers.

### Precommit setup

This should be installed as part of the conda environment
```
pre-commit install
```

Once installed you should be able to run the `precommit_check.sh` to see the stat of the checks.

### Running tests

There are 3 test bash scripts, but the cli should be the same between OS.

* `test_all.sh`
* `test_int.sh`
* `test_unit.sh`

These are relatively straight forward to running all or a subset of tests.  For clarity, `test_int.sh` is all of the integration tests that hit outside resources.  `test_unit.sh` only does unit tests and should be quick.
