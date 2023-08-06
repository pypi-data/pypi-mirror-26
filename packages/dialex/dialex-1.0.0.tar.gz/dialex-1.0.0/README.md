# Dialex SDK for Python  
Python Client for HyperLab Dialex API  

[![Build Status](https://travis-ci.org/HyperLab-Solutions-Sdn-Bhd/dialex-sdk-python.svg?branch=master)](https://travis-ci.org/HyperLab-Solutions-Sdn-Bhd/dialex-sdk-python) [![Coverage Status](https://coveralls.io/repos/github/HyperLab-Solutions-Sdn-Bhd/dialex-sdk-python/badge.svg?branch=master)](https://coveralls.io/github/HyperLab-Solutions-Sdn-Bhd/dialex-sdk-python?branch=master) [![Known Vulnerabilities](https://snyk.io/test/github/hyperlab-solutions-sdn-bhd/dialex-sdk-python/badge.svg)](https://snyk.io/test/github/hyperlab-solutions-sdn-bhd/dialex-sdk-python)  

## Install

```bash
$ pip install -U dialex
```  

## Quick Start  

```python
from dialex import dialex
dial = dialex.Dialex('apiKey')
```  

## Developing  

Clone using git:  
`git clone git@github.com:HyperLab-Solutions-Sdn-Bhd/dialex-sdk-python.git`  

Install pipenv:  
`pip install -U pipenv`  

Install dependencies:  
`pipenv install --dev`  

Run tests:  
`python setup.py test`  
