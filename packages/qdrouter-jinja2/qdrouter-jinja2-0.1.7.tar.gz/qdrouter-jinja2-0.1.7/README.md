# Qdrouter-jinja2
Generate jinja2 config template from installed qpid-dispatch

## Build/Test Status
[![Build Status](https://travis-ci.org/rh-messaging-qe/qdrouterd-jinja2.svg?branch=master)](https://travis-ci.org/rh-messaging-qe/qdrouterd-jinja2)
[![GitHub Issues](https://img.shields.io/github/issues/rh-messaging-qe/qdrouterd-jinja2.svg)](https://github.com/rh-messaging-qe/qdrouterd-jinja2/issues)
[![GitHub Issues](https://img.shields.io/github/issues-pr/rh-messaging-qe/qdrouterd-jinja2.svg)](https://github.com/rh-messaging-qe/qdrouterd-jinja2/pulls)
[![pypi](https://img.shields.io/pypi/v/qdrouter-jinja2.svg)](https://github.com/rh-messaging-qe/qdrouter-jinja2)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


## Summary
This python package can generate a dispatch template for a config file based on the current version of Qpid-dispatch installed on machine.

## Requirements
Qpid-dispatch
Python >= 2.7

## Install & Run
```bash
$ pip install qdrouter-jinja2
```

```bash
$ qdrouterJinja2 -o <OUTPUT_FILE>
```

## Tests
(no tests implemented!)

### Requirements
[tox](https://tox.readthedocs.io/en/latest/)

### How to run tests
```bash
$ tox
```

## License
Apache 2.0

## Author Information
Messaging QE team @ redhat.com