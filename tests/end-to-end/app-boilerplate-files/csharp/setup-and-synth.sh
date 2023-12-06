#!/bin/bash
set -eu

npx cdk synth --no-version-reporting --no-path-metadata --app 'dotnet run --project ./CSharp.csproj'
