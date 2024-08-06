#!/bin/bash

cat <<EOF > app/.env
# this is secret stuff. When you change it don't commit it to the remote
# an initial version of this file is provided on purpose to establish a VERSION
VERSION=0.0.0
TOP_SECRET_MESSAGE="This is another secret message"
EOF

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

python3 bootstrap.py

python3 set_repo_secrets.py