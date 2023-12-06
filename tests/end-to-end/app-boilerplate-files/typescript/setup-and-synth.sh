#!/bin/bash
set -eu

echo "npm install"
npm install --no-package-lock

echo "cdk synth"
npx cdk synth --no-version-reporting --no-path-metadata --app 'npx ts-node ./app.ts'
