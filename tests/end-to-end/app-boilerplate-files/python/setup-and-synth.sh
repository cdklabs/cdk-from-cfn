#!/bin/bash
set -eu

echo "create venv"
python3 -m venv .venv

echo "source venv"
source .venv/bin/activate

echo "pip install"
pip install --disable-pip-version-check -q -r requirements.txt

echo "cdk synth"
npx cdk synth --no-version-reporting --no-path-metadata --app 'python3 app.py'