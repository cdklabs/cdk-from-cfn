#!/bin/bash
set -eu

echo "java setup"

echo "cdk synth"
npx cdk synth --no-version-reporting --no-path-metadata --app 'mvn -e -q compile exec:java'
