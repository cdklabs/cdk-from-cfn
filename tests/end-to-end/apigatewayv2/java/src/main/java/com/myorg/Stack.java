package com.myorg;

import software.constructs.Construct;

import java.util.*;
import software.amazon.awscdk.CfnMapping;
import software.amazon.awscdk.CfnTag;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;

import software.amazon.awscdk.*;
import software.amazon.awscdk.services.apigatewayv2.*;

class ApiGatewayV2Stack extends Stack {
    private Object apiEndpoint;

    public Object getApiEndpoint() {
        return this.apiEndpoint;
    }

    public ApiGatewayV2Stack(final Construct scope, final String id) {
        super(scope, id, null);
    }

    public ApiGatewayV2Stack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        CfnApi myApi = CfnApi.Builder.create(this, "MyApi")
                .name("MyHttpApi")
                .protocolType("HTTP")
                .description("My HTTP API")
                .build();

        CfnStage defaultStage = CfnStage.Builder.create(this, "DefaultStage")
                .apiId(myApi.getRef())
                .stageName("default")
                .autoDeploy(true)
                .build();

        CfnIntegration helloWorldIntegration = CfnIntegration.Builder.create(this, "HelloWorldIntegration")
                .apiId(myApi.getRef())
                .integrationType("HTTP_PROXY")
                .integrationUri("https://jsonplaceholder.typicode.com/posts/1")
                .integrationMethod("GET")
                .payloadFormatVersion("1.0")
                .build();

        CfnRoute helloWorldRoute = CfnRoute.Builder.create(this, "HelloWorldRoute")
                .apiId(myApi.getRef())
                .routeKey("GET /hello")
                .target(String.join("/",
                        "integrations",
                        helloWorldIntegration.getRef()))
                .build();

        this.apiEndpoint = "https://" + myApi.getRef() + ".execute-api." + this.getRegion() + ".amazonaws.com/default";
        CfnOutput.Builder.create(this, "CfnOutputApiEndpoint")
                .key("ApiEndpoint")
                .value(this.apiEndpoint.toString())
                .description("Endpoint for the HTTP API")
                .build();

    }
}
