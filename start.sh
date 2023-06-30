#!/bin/bash

cd $(dirname $(readlink -f $0))

if ! [ -d "venv" ]
then
    pip3 install virtualenv
    virtualenv venv
    . ./venv/bin/activate
    pip install -r requirements.txt
else
    . ./venv/bin/activate
fi

python .
