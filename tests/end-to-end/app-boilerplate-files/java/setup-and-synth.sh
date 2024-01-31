#!/bin/bash
set -eu

echo "java setup"

echo "cdk synth"
npx --yes cdk@latest synth --no-version-reporting --no-path-metadata --app 'mvn -e -q package'
