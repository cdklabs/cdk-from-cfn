npm remove node_modules
npx --yes cdk@latest synth --no-version-reporting --no-path-metadata --app 'go mod download && go run stack.go app.go'
