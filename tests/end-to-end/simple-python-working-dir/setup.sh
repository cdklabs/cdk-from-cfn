#!/bin/bash
set -eu

echo "create venv"
python3 -m venv .venv

echo "source venv"
source .venv/bin/activate

echo "pip install"
pip install -r requirements.txt

echo "run the app"
python3 app.py

echo "synth"
npx cdk synth --no-version-reporting --no-path-metadata --app python3 app.py