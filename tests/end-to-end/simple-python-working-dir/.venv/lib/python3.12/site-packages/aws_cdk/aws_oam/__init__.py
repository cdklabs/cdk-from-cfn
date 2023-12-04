'''
# AWS::Oam Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_oam as oam
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Oam construct libraries](https://constructs.dev/search?q=oam)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Oam resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Oam.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Oam](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Oam.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_9df397a6,
    IInspectable as _IInspectable_c2943556,
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)


@jsii.implements(_IInspectable_c2943556)
class CfnLink(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_oam.CfnLink",
):
    '''A CloudFormation ``AWS::Oam::Link``.

    Creates a link between a source account and a sink that you have created in a monitoring account.

    Before you create a link, you must create a sink in the monitoring account. The sink must have a sink policy that permits the source account to link to it. You can grant permission to source accounts by granting permission to an entire organization, an organizational unit, or to individual accounts.

    For more information, see `CreateSink <https://docs.aws.amazon.com/OAM/latest/APIReference/API_CreateSink.html>`_ and `PutSinkPolicy <https://docs.aws.amazon.com/OAM/latest/APIReference/API_PutSinkPolicy.html>`_ .

    Each monitoring account can be linked to as many as 100,000 source accounts.

    Each source account can be linked to as many as five monitoring accounts.

    :cloudformationResource: AWS::Oam::Link
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_oam as oam
        
        cfn_link = oam.CfnLink(self, "MyCfnLink",
            label_template="labelTemplate",
            resource_types=["resourceTypes"],
            sink_identifier="sinkIdentifier",
        
            # the properties below are optional
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        label_template: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        sink_identifier: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Oam::Link``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param label_template: Specify a friendly human-readable name to use to identify this source account when you are viewing data from it in the monitoring account. You can include the following variables in your template: - ``$AccountName`` is the name of the account - ``$AccountEmail`` is a globally-unique email address, which includes the email domain, such as ``mariagarcia@example.com`` - ``$AccountEmailNoDomain`` is an email address without the domain name, such as ``mariagarcia``
        :param resource_types: An array of strings that define which types of data that the source account shares with the monitoring account. Valid values are ``AWS::CloudWatch::Metric | AWS::Logs::LogGroup | AWS::XRay::Trace`` .
        :param sink_identifier: The ARN of the sink in the monitoring account that you want to link to. You can use `ListSinks <https://docs.aws.amazon.com/OAM/latest/APIReference/API_ListSinks.html>`_ to find the ARNs of sinks.
        :param tags: An array of key-value pairs to apply to the link. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffbd6521de55eb2e3d4f2bc8edac2d144f850a53dbdfd3dac4b1591612aaeac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLinkProps(
            label_template=label_template,
            resource_types=resource_types,
            sink_identifier=sink_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c070a52405d10c02ca36373c6f7099717b46c4eeb9b9100704beaaf1d2c1ed20)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a5a72fcba4df99c0a38699a0ae8d36072c85020c3e6c48585ff388860d46dd9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The ARN of the link.

        For example, ``arn:aws:oam:us-west-1:111111111111:link:abcd1234-a123-456a-a12b-a123b456c789``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLabel")
    def attr_label(self) -> builtins.str:
        '''The friendly human-readable name used to identify this source account when it is viewed from the monitoring account.

        For example, ``my-account1`` .

        :cloudformationAttribute: Label
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLabel"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''An array of key-value pairs to apply to the link.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="labelTemplate")
    def label_template(self) -> builtins.str:
        '''Specify a friendly human-readable name to use to identify this source account when you are viewing data from it in the monitoring account.

        You can include the following variables in your template:

        - ``$AccountName`` is the name of the account
        - ``$AccountEmail`` is a globally-unique email address, which includes the email domain, such as ``mariagarcia@example.com``
        - ``$AccountEmailNoDomain`` is an email address without the domain name, such as ``mariagarcia``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-labeltemplate
        '''
        return typing.cast(builtins.str, jsii.get(self, "labelTemplate"))

    @label_template.setter
    def label_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997e0a25bd896cf32312772dad16f8a1714d949b05e540d8b70c8452ec128d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labelTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        '''An array of strings that define which types of data that the source account shares with the monitoring account.

        Valid values are ``AWS::CloudWatch::Metric | AWS::Logs::LogGroup | AWS::XRay::Trace`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-resourcetypes
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @resource_types.setter
    def resource_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0132bd2ba8eaa5be7ac98303f37a6cd4af3e395ff83ff41a4b1d603604e6616)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypes", value)

    @builtins.property
    @jsii.member(jsii_name="sinkIdentifier")
    def sink_identifier(self) -> builtins.str:
        '''The ARN of the sink in the monitoring account that you want to link to.

        You can use `ListSinks <https://docs.aws.amazon.com/OAM/latest/APIReference/API_ListSinks.html>`_ to find the ARNs of sinks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-sinkidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "sinkIdentifier"))

    @sink_identifier.setter
    def sink_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333f53159fc6c2c5a53817b12e42df1c0c36eb1c4ce8b2f5ac882088416ddefb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sinkIdentifier", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_oam.CfnLinkProps",
    jsii_struct_bases=[],
    name_mapping={
        "label_template": "labelTemplate",
        "resource_types": "resourceTypes",
        "sink_identifier": "sinkIdentifier",
        "tags": "tags",
    },
)
class CfnLinkProps:
    def __init__(
        self,
        *,
        label_template: builtins.str,
        resource_types: typing.Sequence[builtins.str],
        sink_identifier: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLink``.

        :param label_template: Specify a friendly human-readable name to use to identify this source account when you are viewing data from it in the monitoring account. You can include the following variables in your template: - ``$AccountName`` is the name of the account - ``$AccountEmail`` is a globally-unique email address, which includes the email domain, such as ``mariagarcia@example.com`` - ``$AccountEmailNoDomain`` is an email address without the domain name, such as ``mariagarcia``
        :param resource_types: An array of strings that define which types of data that the source account shares with the monitoring account. Valid values are ``AWS::CloudWatch::Metric | AWS::Logs::LogGroup | AWS::XRay::Trace`` .
        :param sink_identifier: The ARN of the sink in the monitoring account that you want to link to. You can use `ListSinks <https://docs.aws.amazon.com/OAM/latest/APIReference/API_ListSinks.html>`_ to find the ARNs of sinks.
        :param tags: An array of key-value pairs to apply to the link. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_oam as oam
            
            cfn_link_props = oam.CfnLinkProps(
                label_template="labelTemplate",
                resource_types=["resourceTypes"],
                sink_identifier="sinkIdentifier",
            
                # the properties below are optional
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debdd90801a5b490b9ec98da9bb17f5329c1db3816f558321a3ce7bdfb7aab12)
            check_type(argname="argument label_template", value=label_template, expected_type=type_hints["label_template"])
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
            check_type(argname="argument sink_identifier", value=sink_identifier, expected_type=type_hints["sink_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "label_template": label_template,
            "resource_types": resource_types,
            "sink_identifier": sink_identifier,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def label_template(self) -> builtins.str:
        '''Specify a friendly human-readable name to use to identify this source account when you are viewing data from it in the monitoring account.

        You can include the following variables in your template:

        - ``$AccountName`` is the name of the account
        - ``$AccountEmail`` is a globally-unique email address, which includes the email domain, such as ``mariagarcia@example.com``
        - ``$AccountEmailNoDomain`` is an email address without the domain name, such as ``mariagarcia``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-labeltemplate
        '''
        result = self._values.get("label_template")
        assert result is not None, "Required property 'label_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_types(self) -> typing.List[builtins.str]:
        '''An array of strings that define which types of data that the source account shares with the monitoring account.

        Valid values are ``AWS::CloudWatch::Metric | AWS::Logs::LogGroup | AWS::XRay::Trace`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-resourcetypes
        '''
        result = self._values.get("resource_types")
        assert result is not None, "Required property 'resource_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def sink_identifier(self) -> builtins.str:
        '''The ARN of the sink in the monitoring account that you want to link to.

        You can use `ListSinks <https://docs.aws.amazon.com/OAM/latest/APIReference/API_ListSinks.html>`_ to find the ARNs of sinks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-sinkidentifier
        '''
        result = self._values.get("sink_identifier")
        assert result is not None, "Required property 'sink_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to the link.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-link.html#cfn-oam-link-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnSink(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_oam.CfnSink",
):
    '''A CloudFormation ``AWS::Oam::Sink``.

    Creates or updates a *sink* in the current account, so that it can be used as a monitoring account in CloudWatch cross-account observability. A sink is a resource that represents an attachment point in a monitoring account, which source accounts can link to to be able to send observability data.

    After you create a sink, you must create a sink policy that allows source accounts to attach to it. For more information, see `PutSinkPolicy <https://docs.aws.amazon.com/OAM/latest/APIReference/API_PutSinkPolicy.html>`_ .

    An account can have one sink.

    :cloudformationResource: AWS::Oam::Sink
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_oam as oam
        
        # policy: Any
        
        cfn_sink = oam.CfnSink(self, "MyCfnSink",
            name="name",
        
            # the properties below are optional
            policy=policy,
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        policy: typing.Any = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Oam::Sink``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the sink.
        :param policy: The IAM policy that grants permissions to source accounts to link to this sink. The policy can grant permission in the following ways: - Include organization IDs or organization paths to permit all accounts in an organization - Include account IDs to permit the specified accounts
        :param tags: An array of key-value pairs to apply to the sink. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc6909cf2fa64c817adc7144cbdc866a604a4bcf1e0859e6a2301142ad88158)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSinkProps(name=name, policy=policy, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7efaf81f7f46e186f80b4548e1a30d7c79c4496664ca70dfb24821523ef350bb)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4098b4b70e3b0125490695575d8b1c7e159ae8c920aaff402f579550bfa07ca2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The ARN of the sink.

        For example, ``arn:aws:oam:us-west-1:111111111111:sink:abcd1234-a123-456a-a12b-a123b456c789``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''An array of key-value pairs to apply to the sink.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the sink.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c4525dee6f8a7375f1f7a92c71b0244885baf54d86723e2e625b150bee5f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''The IAM policy that grants permissions to source accounts to link to this sink.

        The policy can grant permission in the following ways:

        - Include organization IDs or organization paths to permit all accounts in an organization
        - Include account IDs to permit the specified accounts

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b105d896dac211275e0427a07a7c1ef0096d9d405b1f2c26c9622c36b574a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_oam.CfnSinkProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "policy": "policy", "tags": "tags"},
)
class CfnSinkProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        policy: typing.Any = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSink``.

        :param name: A name for the sink.
        :param policy: The IAM policy that grants permissions to source accounts to link to this sink. The policy can grant permission in the following ways: - Include organization IDs or organization paths to permit all accounts in an organization - Include account IDs to permit the specified accounts
        :param tags: An array of key-value pairs to apply to the sink. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_oam as oam
            
            # policy: Any
            
            cfn_sink_props = oam.CfnSinkProps(
                name="name",
            
                # the properties below are optional
                policy=policy,
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd29c4cd77d22ee5292aed2b76dafa78094044e68522a05f311c0ee028231e47)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if policy is not None:
            self._values["policy"] = policy
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the sink.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''The IAM policy that grants permissions to source accounts to link to this sink.

        The policy can grant permission in the following ways:

        - Include organization IDs or organization paths to permit all accounts in an organization
        - Include account IDs to permit the specified accounts

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to the sink.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-oam-sink.html#cfn-oam-sink-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSinkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLink",
    "CfnLinkProps",
    "CfnSink",
    "CfnSinkProps",
]

publication.publish()

def _typecheckingstub__2ffbd6521de55eb2e3d4f2bc8edac2d144f850a53dbdfd3dac4b1591612aaeac(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    label_template: builtins.str,
    resource_types: typing.Sequence[builtins.str],
    sink_identifier: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c070a52405d10c02ca36373c6f7099717b46c4eeb9b9100704beaaf1d2c1ed20(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a5a72fcba4df99c0a38699a0ae8d36072c85020c3e6c48585ff388860d46dd9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997e0a25bd896cf32312772dad16f8a1714d949b05e540d8b70c8452ec128d2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0132bd2ba8eaa5be7ac98303f37a6cd4af3e395ff83ff41a4b1d603604e6616(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333f53159fc6c2c5a53817b12e42df1c0c36eb1c4ce8b2f5ac882088416ddefb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debdd90801a5b490b9ec98da9bb17f5329c1db3816f558321a3ce7bdfb7aab12(
    *,
    label_template: builtins.str,
    resource_types: typing.Sequence[builtins.str],
    sink_identifier: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc6909cf2fa64c817adc7144cbdc866a604a4bcf1e0859e6a2301142ad88158(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    policy: typing.Any = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7efaf81f7f46e186f80b4548e1a30d7c79c4496664ca70dfb24821523ef350bb(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4098b4b70e3b0125490695575d8b1c7e159ae8c920aaff402f579550bfa07ca2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c4525dee6f8a7375f1f7a92c71b0244885baf54d86723e2e625b150bee5f2c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b105d896dac211275e0427a07a7c1ef0096d9d405b1f2c26c9622c36b574a5(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd29c4cd77d22ee5292aed2b76dafa78094044e68522a05f311c0ee028231e47(
    *,
    name: builtins.str,
    policy: typing.Any = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
