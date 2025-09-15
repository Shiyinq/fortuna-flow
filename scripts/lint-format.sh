#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src mcp-server --exclude=__init__.py,_example
isort src mcp-server --profile black
black src mcp-server