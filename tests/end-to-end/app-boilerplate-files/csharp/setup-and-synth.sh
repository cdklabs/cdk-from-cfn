#!/bin/bash
set -eu

npx --yes cdk@latest synth --no-version-reporting --no-path-metadata --app 'dotnet run --project ./CSharp.csproj'
