# tmpld
[![Build Status](https://travis-ci.org/telephoneorg/debian.svg?branch=master)](https://travis-ci.org/telephoneorg/tmpld) [![Github Repo](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/telephoneorg/tmpld) [![Pypi Version](https://img.shields.io/pypi/v/tmpld.svg)](https://pypi.python.org/pypi/tmpld) [![Pypi License](https://img.shields.io/pypi/l/tmpld.svg)](https://pypi.python.org/pypi/tmpld) [![Pypi Wheel](https://img.shields.io/pypi/wheel/tmpld.svg)](https://pypi.python.org/pypi/tmpld) [![Pypi Versions](https://img.shields.io/pypi/pyversions/tmpld.svg)](https://pypi.python.org/pypi/tmpld) [![Docker Pulls](https://img.shields.io/docker/pulls/telephoneorg/tmpld.svg)](https://hub.docker.com/r/telephoneorg/tmpld/)


## Maintainer
Joe Black | <me@joeblack.nyc> | [github](https://github.com/joeblackwaslike)


## Introduction
CLI tool combining jinja2 with parsers and other objects including Kubernetes
API objects and linux capabilities objects.


## Usage
```
usage: tmpld (sub-commands ...) [options ...] {arguments ...}

Base Controller

positional arguments:
  templates             template files to render

optional arguments:
  -h, --help            show this help message and exit
  --debug               toggle debug output
  --quiet               suppress all output
  -d DATA, --data DATA  file(s) containing context data
  -s, --strict          Raise an exception if a variable is not defined
```
