#!/usr/bin/env bash

cd $(dirname $0)
python3 -m venv .venv/
.venv/bin/python3 -m pip install -r requirements.txt
