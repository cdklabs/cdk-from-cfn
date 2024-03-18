//Auto-generated
using Amazon.CDK;
sealed class Program
{
    public static void Main(string[] args)
    {
        var app = new App(new AppProps
        {
            DefaultStackSynthesizer = new DefaultStackSynthesizer(new DefaultStackSynthesizerProps
            {
                GenerateBootstrapVersionRule = false,
            }),
        });
        new Ec2Stack.Ec2Stack(app, "Stack");
        app.Synth();
    }
}
