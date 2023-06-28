#!/bin/bash

cd $(dirname $(readlink -f $0))

if ! [ -d "venv" ]
then
    python3 -m venv venv
    . ./venv/bin/activate
    pip install -r requirements.txt
else
    . ./venv/bin/activate
fi

python .
