#!/bin/bash

# $1 = .env file name

if [ -f "$1" ]; then
    export $(cat "$1" | sed 's/#.*//g' | xargs)
fi

export PYTHONPATH=$PYTHONPATH:nucleus

./venv/bin/python nucleus/main.py
