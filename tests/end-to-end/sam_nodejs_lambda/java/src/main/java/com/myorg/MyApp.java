//auto-generated
package com.myorg;
import software.amazon.awscdk.App;
import software.amazon.awscdk.AppProps;
import software.amazon.awscdk.DefaultStackSynthesizer;
import software.amazon.awscdk.StackProps;
public class MyApp {
    public static void main(final String[] args) {
        App app = new App(AppProps.builder()
            .defaultStackSynthesizer(DefaultStackSynthesizer.Builder.create()
                .generateBootstrapVersionRule(false)
                .build())
            .build());
            new SAMNodeJSLambda(app, "Stack", StackProps.builder()
                .build());
            app.synth();

    }
}
