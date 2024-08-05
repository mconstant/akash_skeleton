#!/bin/bash

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 bootstrap.py

python3 set_repo_secrets.py