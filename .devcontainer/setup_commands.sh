#!/bin/bash

install_deps() {
    pip install --upgrade pip && pip install uv
    uv sync && uv pip install -e .
}


FUNCTION_NAME=$1

if [ -z "$FUNCTION_NAME" ]; then
    echo "Error: Function name argument is missing."
    exit 1
fi

shift

if type -t "$FUNCTION_NAME" | grep -q 'function'; then
    "$FUNCTION_NAME" "$@"
else
    echo "Error: Function '$FUNCTION_NAME' not found."
    exit 1
fi
