#!/bin/bash

mypy cli_pipeline/__init__.py

pip uninstall .

pip install --ignore-installed --no-cache -U -e .

pipeline version
