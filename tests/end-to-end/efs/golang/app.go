// auto-generated
package main
import (
    "github.com/aws/aws-cdk-go/awscdk/v2"
    "github.com/aws/jsii-runtime-go"
)
func main() {
    defer jsii.Close()
    app := awscdk.NewApp(&awscdk.AppProps{
        DefaultStackSynthesizer: awscdk.NewDefaultStackSynthesizer(&awscdk.DefaultStackSynthesizerProps{
            GenerateBootstrapVersionRule: jsii.Bool(false),
        }),
    })
    NewEfsStack(app, "Stack", nil)
    app.Synth(nil)
}
