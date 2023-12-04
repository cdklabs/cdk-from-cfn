'''
# AWS::Connect Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_connect as connect
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Connect construct libraries](https://constructs.dev/search?q=connect)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Connect resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Connect.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Connect](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Connect.html).

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
    CfnTag as _CfnTag_f6864754,
    IInspectable as _IInspectable_c2943556,
    IResolvable as _IResolvable_da3f097b,
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)


@jsii.implements(_IInspectable_c2943556)
class CfnApprovedOrigin(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnApprovedOrigin",
):
    '''A CloudFormation ``AWS::Connect::ApprovedOrigin``.

    The approved origin for the instance.

    :cloudformationResource: AWS::Connect::ApprovedOrigin
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_approved_origin = connect.CfnApprovedOrigin(self, "MyCfnApprovedOrigin",
            instance_id="instanceId",
            origin="origin"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_id: builtins.str,
        origin: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Connect::ApprovedOrigin``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param origin: Domain name to be added to the allow-list of the instance. *Maximum* : ``267``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44955422cb4c00b338f45e52a0d4136fdcdb94c8e433595b636f468d589e514a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApprovedOriginProps(instance_id=instance_id, origin=origin)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b611bd9c5a92c253c2e2b0cba97b9f73bad0cfc8494953acb694fda143bba2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc2ef7b8d5a06b007fe66bb9f5b0208e869ed47a6e5af0d6bf354f4df2d4d6c8)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html#cfn-connect-approvedorigin-instanceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd219e5b157d40fbc4254297a9308245796269c824a72c0b9db3bad7013261c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value)

    @builtins.property
    @jsii.member(jsii_name="origin")
    def origin(self) -> builtins.str:
        '''Domain name to be added to the allow-list of the instance.

        *Maximum* : ``267``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html#cfn-connect-approvedorigin-origin
        '''
        return typing.cast(builtins.str, jsii.get(self, "origin"))

    @origin.setter
    def origin(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49fb9b02cf4a1b22d6433eac9cb35377d1877512b477dbf9c030fec47fb54f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "origin", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnApprovedOriginProps",
    jsii_struct_bases=[],
    name_mapping={"instance_id": "instanceId", "origin": "origin"},
)
class CfnApprovedOriginProps:
    def __init__(self, *, instance_id: builtins.str, origin: builtins.str) -> None:
        '''Properties for defining a ``CfnApprovedOrigin``.

        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param origin: Domain name to be added to the allow-list of the instance. *Maximum* : ``267``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_approved_origin_props = connect.CfnApprovedOriginProps(
                instance_id="instanceId",
                origin="origin"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437fb8bad3e7665288233ec7ee3b4db6669d85ab53efddb888b5d729979a4e2f)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_id": instance_id,
            "origin": origin,
        }

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html#cfn-connect-approvedorigin-instanceid
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(self) -> builtins.str:
        '''Domain name to be added to the allow-list of the instance.

        *Maximum* : ``267``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html#cfn-connect-approvedorigin-origin
        '''
        result = self._values.get("origin")
        assert result is not None, "Required property 'origin' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApprovedOriginProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnContactFlow(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnContactFlow",
):
    '''A CloudFormation ``AWS::Connect::ContactFlow``.

    Specifies a flow for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::ContactFlow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_contact_flow = connect.CfnContactFlow(self, "MyCfnContactFlow",
            content="content",
            instance_arn="instanceArn",
            name="name",
            type="type",
        
            # the properties below are optional
            description="description",
            state="state",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::ContactFlow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: The content of the flow. For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow.
        :param type: The type of the flow. For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .
        :param description: The description of the flow.
        :param state: The state of the flow.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bacec198fd7006a7e922c6b62694383eb7200d23c3f8da491f520191bdc8353f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactFlowProps(
            content=content,
            instance_arn=instance_arn,
            name=name,
            type=type,
            description=description,
            state=state,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aca14ea5542ff9acc3dc06746c7580c88c1e0b75d66bf0ac0a8cd785404cc173)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4b3abb60d405603981215ec7d659c3d8939dbf9b5de879c8d56dfd0631f9d5b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrContactFlowArn")
    def attr_contact_flow_arn(self) -> builtins.str:
        '''``Ref`` returns the Amazon Resource Name (ARN) of the flow. For example:.

        ``{ "Ref": "myFlowArn" }``

        :cloudformationAttribute: ContactFlowArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrContactFlowArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        '''The content of the flow.

        For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-content
        '''
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a517102f202efaced50f937df38d5374d2d8ae33c5659296852d677cbe73e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20f6a7aacca6b49f3791bf907484b7af427677a1079ea79db9a45489b963b9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f576a62faffae972ec30039ac3019bddb9b613e8dd2dce2b52723ba8a64dbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of the flow.

        For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__213719edbc55495f331c0d1f51b7ab8a359f2c5cc563f3fa97077760121c6aa9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4573df3b75ab7b2ea3d0cba32ff3c515f11f6cbec43c0885d9ee30d25616a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b6f72cf71dca93b2b2baae1d002d73d66de8e16bec7709efdb45c4bb811336)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)


@jsii.implements(_IInspectable_c2943556)
class CfnContactFlowModule(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnContactFlowModule",
):
    '''A CloudFormation ``AWS::Connect::ContactFlowModule``.

    Specifies a flow module for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::ContactFlowModule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_contact_flow_module = connect.CfnContactFlowModule(self, "MyCfnContactFlowModule",
            content="content",
            instance_arn="instanceArn",
            name="name",
        
            # the properties below are optional
            description="description",
            state="state",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::ContactFlowModule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content: The content of the flow module.
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow module.
        :param description: The description of the flow module.
        :param state: The state of the flow module.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__008a6ee0ce6447d7f5f7c62774a959e253bc4a69cef26848e6d3f74cf2381193)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactFlowModuleProps(
            content=content,
            instance_arn=instance_arn,
            name=name,
            description=description,
            state=state,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82176173dbe238b7a4715d8a94792d3696ada52a4372f823ab10f4c590c6193f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f3e317a83e30b22f766c5d65c8451e4d9e5ffcd6510573aa22d0063860e7b99)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrContactFlowModuleArn")
    def attr_contact_flow_module_arn(self) -> builtins.str:
        '''``Ref`` returns the Amazon Resource Name (ARN) of the flow module. For example:.

        ``{ "Ref": "myFlowModuleArn" }``

        :cloudformationAttribute: ContactFlowModuleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrContactFlowModuleArn"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        '''The content of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-content
        '''
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1701812aa93a58317265edab1cd66b5a843fc9845a1aed0b81f83c4f738b5b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68b9231af4bcfc40233b3b8fbbd6acd02fe21a59b2f962738d2ce93d6ffa7fa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e18e7239d9aefba3afcb9b93bf7f3ec9f6e4f173d51f91e93f5543efe25658a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c1841af03e44ad4a3c471a24f30aa57c457ec766515db087b0745fb9a6a68d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25db523d57560a8813a16f507ae8c09c28625a53b6a24b5744ca978282ff51a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnContactFlowModuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "instance_arn": "instanceArn",
        "name": "name",
        "description": "description",
        "state": "state",
        "tags": "tags",
    },
)
class CfnContactFlowModuleProps:
    def __init__(
        self,
        *,
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContactFlowModule``.

        :param content: The content of the flow module.
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow module.
        :param description: The description of the flow module.
        :param state: The state of the flow module.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_contact_flow_module_props = connect.CfnContactFlowModuleProps(
                content="content",
                instance_arn="instanceArn",
                name="name",
            
                # the properties below are optional
                description="description",
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84f0f2ba3fd7010e7e0bb6aaa71b591e31e6d4c4ad736e9c4e08be6f11de0102)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "instance_arn": instance_arn,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-content
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow module.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowModuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnContactFlowProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "instance_arn": "instanceArn",
        "name": "name",
        "type": "type",
        "description": "description",
        "state": "state",
        "tags": "tags",
    },
)
class CfnContactFlowProps:
    def __init__(
        self,
        *,
        content: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContactFlow``.

        :param content: The content of the flow. For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow.
        :param type: The type of the flow. For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .
        :param description: The description of the flow.
        :param state: The state of the flow.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_contact_flow_props = connect.CfnContactFlowProps(
                content="content",
                instance_arn="instanceArn",
                name="name",
                type="type",
            
                # the properties below are optional
                description="description",
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0555b19a226cc1a8bd054951921ffd23e0c635fe29a3d69a330d8262710a7d8)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content": content,
            "instance_arn": instance_arn,
            "name": name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the flow.

        For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-content
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the flow.

        For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnHoursOfOperation(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnHoursOfOperation",
):
    '''A CloudFormation ``AWS::Connect::HoursOfOperation``.

    Specifies hours of operation.

    :cloudformationResource: AWS::Connect::HoursOfOperation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_hours_of_operation = connect.CfnHoursOfOperation(self, "MyCfnHoursOfOperation",
            config=[connect.CfnHoursOfOperation.HoursOfOperationConfigProperty(
                day="day",
                end_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                ),
                start_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                )
            )],
            instance_arn="instanceArn",
            name="name",
            time_zone="timeZone",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        config: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]],
        instance_arn: builtins.str,
        name: builtins.str,
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::HoursOfOperation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param config: Configuration information for the hours of operation.
        :param instance_arn: The Amazon Resource Name (ARN) for the instance.
        :param name: The name for the hours of operation.
        :param time_zone: The time zone for the hours of operation.
        :param description: The description for the hours of operation.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9a7b2f06b8b2d053fcfa26018be9202b48193f9ffb7fc1d9518391cd9b5afe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHoursOfOperationProps(
            config=config,
            instance_arn=instance_arn,
            name=name,
            time_zone=time_zone,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1892c64bc10c89577bb1c7c1cbafe5e7256d59298765e4d13fa8bc792aff27cb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1be399a62772419844397558be775450dd4c2dc740a8864f61b03b483610073)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrHoursOfOperationArn")
    def attr_hours_of_operation_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the hours of operation.

        :cloudformationAttribute: HoursOfOperationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHoursOfOperationArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _IResolvable_da3f097b]]]:
        '''Configuration information for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-config
        '''
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _IResolvable_da3f097b]]], jsii.get(self, "config"))

    @config.setter
    def config(
        self,
        value: typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnHoursOfOperation.HoursOfOperationConfigProperty", _IResolvable_da3f097b]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390986701d928ed3f41379b144a434426999d52505eaf487d066a0865f299c42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff371c180e62831feb4bd92859ad779161086fed20f40c5fcaec70aedbd1d950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314c5f51a2268bd65be9864b4a46c3d2279936b4a2675b16522bc736ba5fb373)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        '''The time zone for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-timezone
        '''
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__442605da8563582cbafb26c421377e100eaf1791f47f7f84657994d9d7347b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224611189f5992474af63688324a9a850ba31b7aad01b0eaae5a8fd63f4ea172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnHoursOfOperation.HoursOfOperationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"day": "day", "end_time": "endTime", "start_time": "startTime"},
    )
    class HoursOfOperationConfigProperty:
        def __init__(
            self,
            *,
            day: builtins.str,
            end_time: typing.Union[typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
            start_time: typing.Union[typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        ) -> None:
            '''Contains information about the hours of operation.

            :param day: The day that the hours of operation applies to.
            :param end_time: The end time that your contact center closes.
            :param start_time: The start time that your contact center opens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                hours_of_operation_config_property = connect.CfnHoursOfOperation.HoursOfOperationConfigProperty(
                    day="day",
                    end_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    ),
                    start_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ef26f457a53e548698c50361c4e334e5f633638af5ae2b9230dccc5fd5c1dd3)
                check_type(argname="argument day", value=day, expected_type=type_hints["day"])
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "day": day,
                "end_time": end_time,
                "start_time": start_time,
            }

        @builtins.property
        def day(self) -> builtins.str:
            '''The day that the hours of operation applies to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-day
            '''
            result = self._values.get("day")
            assert result is not None, "Required property 'day' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def end_time(
            self,
        ) -> typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", _IResolvable_da3f097b]:
            '''The end time that your contact center closes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-endtime
            '''
            result = self._values.get("end_time")
            assert result is not None, "Required property 'end_time' is missing"
            return typing.cast(typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def start_time(
            self,
        ) -> typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", _IResolvable_da3f097b]:
            '''The start time that your contact center opens.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-starttime
            '''
            result = self._values.get("start_time")
            assert result is not None, "Required property 'start_time' is missing"
            return typing.cast(typing.Union["CfnHoursOfOperation.HoursOfOperationTimeSliceProperty", _IResolvable_da3f097b], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty",
        jsii_struct_bases=[],
        name_mapping={"hours": "hours", "minutes": "minutes"},
    )
    class HoursOfOperationTimeSliceProperty:
        def __init__(self, *, hours: jsii.Number, minutes: jsii.Number) -> None:
            '''The start time or end time for an hours of operation.

            :param hours: The hours.
            :param minutes: The minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                hours_of_operation_time_slice_property = connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca5c5b128d189787db53fa22c88668d84b3efd31f5b54320dcda0838372db008)
                check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
                check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "hours": hours,
                "minutes": minutes,
            }

        @builtins.property
        def hours(self) -> jsii.Number:
            '''The hours.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html#cfn-connect-hoursofoperation-hoursofoperationtimeslice-hours
            '''
            result = self._values.get("hours")
            assert result is not None, "Required property 'hours' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def minutes(self) -> jsii.Number:
            '''The minutes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html#cfn-connect-hoursofoperation-hoursofoperationtimeslice-minutes
            '''
            result = self._values.get("minutes")
            assert result is not None, "Required property 'minutes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationTimeSliceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnHoursOfOperationProps",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "instance_arn": "instanceArn",
        "name": "name",
        "time_zone": "timeZone",
        "description": "description",
        "tags": "tags",
    },
)
class CfnHoursOfOperationProps:
    def __init__(
        self,
        *,
        config: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]],
        instance_arn: builtins.str,
        name: builtins.str,
        time_zone: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnHoursOfOperation``.

        :param config: Configuration information for the hours of operation.
        :param instance_arn: The Amazon Resource Name (ARN) for the instance.
        :param name: The name for the hours of operation.
        :param time_zone: The time zone for the hours of operation.
        :param description: The description for the hours of operation.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_hours_of_operation_props = connect.CfnHoursOfOperationProps(
                config=[connect.CfnHoursOfOperation.HoursOfOperationConfigProperty(
                    day="day",
                    end_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    ),
                    start_time=connect.CfnHoursOfOperation.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    )
                )],
                instance_arn="instanceArn",
                name="name",
                time_zone="timeZone",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66cef12b59765322de54d22fe6de568f262a635899fc46cbe6a5f5a97b848467)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
            "instance_arn": instance_arn,
            "name": name,
            "time_zone": time_zone,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def config(
        self,
    ) -> typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _IResolvable_da3f097b]]]:
        '''Configuration information for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-config
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _IResolvable_da3f097b]]], result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-timezone
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the hours of operation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHoursOfOperationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnInstance(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnInstance",
):
    '''A CloudFormation ``AWS::Connect::Instance``.

    *This is a preview release for Amazon Connect . It is subject to change.*

    Initiates an Amazon Connect instance with all the supported channels enabled. It does not attach any storage, such as Amazon Simple Storage Service (Amazon S3) or Amazon Kinesis.

    Amazon Connect enforces a limit on the total number of instances that you can create or delete in 30 days. If you exceed this limit, you will get an error message indicating there has been an excessive number of attempts at creating or deleting instances. You must wait 30 days before you can restart creating and deleting instances in your account.

    :cloudformationResource: AWS::Connect::Instance
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_instance = connect.CfnInstance(self, "MyCfnInstance",
            attributes=connect.CfnInstance.AttributesProperty(
                inbound_calls=False,
                outbound_calls=False,
        
                # the properties below are optional
                auto_resolve_best_voices=False,
                contactflow_logs=False,
                contact_lens=False,
                early_media=False,
                use_custom_tts_voices=False
            ),
            identity_management_type="identityManagementType",
        
            # the properties below are optional
            directory_id="directoryId",
            instance_alias="instanceAlias"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        attributes: typing.Union[typing.Union["CfnInstance.AttributesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        identity_management_type: builtins.str,
        directory_id: typing.Optional[builtins.str] = None,
        instance_alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::Instance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param attributes: A toggle for an individual feature at the instance level.
        :param identity_management_type: The identity management type.
        :param directory_id: The identifier for the directory.
        :param instance_alias: The alias of instance. ``InstanceAlias`` is only required when ``IdentityManagementType`` is ``CONNECT_MANAGED`` or ``SAML`` . ``InstanceAlias`` is not required when ``IdentityManagementType`` is ``EXISTING_DIRECTORY`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f291b6bb708a40e1a35dc95de4a38d5f9d8117683bed082183bd387f4848fef9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInstanceProps(
            attributes=attributes,
            identity_management_type=identity_management_type,
            directory_id=directory_id,
            instance_alias=instance_alias,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e4dee5bd55d2c2f964814ca3e2747955315fb5bc8f0a80efc7cbad1ed39cbdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__023c45bbafb1abf38373b2528d8531c6e7048604e4fabca7c6a4684feb4413d6)
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
        '''The Amazon Resource Name (ARN) of the instance.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedTime")
    def attr_created_time(self) -> builtins.str:
        '''When the instance was created.

        :cloudformationAttribute: CreatedTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedTime"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier of the Amazon Connect instance.

        You can find the instanceId in the ARN of the instance.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrInstanceStatus")
    def attr_instance_status(self) -> builtins.str:
        '''The state of the instance.

        :cloudformationAttribute: InstanceStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrInstanceStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceRole")
    def attr_service_role(self) -> builtins.str:
        '''The service role of the instance.

        :cloudformationAttribute: ServiceRole
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceRole"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Union["CfnInstance.AttributesProperty", _IResolvable_da3f097b]:
        '''A toggle for an individual feature at the instance level.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-attributes
        '''
        return typing.cast(typing.Union["CfnInstance.AttributesProperty", _IResolvable_da3f097b], jsii.get(self, "attributes"))

    @attributes.setter
    def attributes(
        self,
        value: typing.Union["CfnInstance.AttributesProperty", _IResolvable_da3f097b],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b81c5f62ba93ec0d3e48188cccf781d5861eac87dc5aa4a4038e6d2176145e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attributes", value)

    @builtins.property
    @jsii.member(jsii_name="identityManagementType")
    def identity_management_type(self) -> builtins.str:
        '''The identity management type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-identitymanagementtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "identityManagementType"))

    @identity_management_type.setter
    def identity_management_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1723398c06ebefeb9e3f4e11e08b8929e713cae56a36abf11fae424fa1c0cea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityManagementType", value)

    @builtins.property
    @jsii.member(jsii_name="directoryId")
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the directory.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-directoryid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryId"))

    @directory_id.setter
    def directory_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a002f21d50b37114edc464bd9143a0e1abc1702e5ff455644179b2ac7acbfbdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryId", value)

    @builtins.property
    @jsii.member(jsii_name="instanceAlias")
    def instance_alias(self) -> typing.Optional[builtins.str]:
        '''The alias of instance.

        ``InstanceAlias`` is only required when ``IdentityManagementType`` is ``CONNECT_MANAGED`` or ``SAML`` . ``InstanceAlias`` is not required when ``IdentityManagementType`` is ``EXISTING_DIRECTORY`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-instancealias
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceAlias"))

    @instance_alias.setter
    def instance_alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225190f7b3c1545c436fe6b710e05a3a5b7d256f1ece21dcb8ad6ba49cf45c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceAlias", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnInstance.AttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "inbound_calls": "inboundCalls",
            "outbound_calls": "outboundCalls",
            "auto_resolve_best_voices": "autoResolveBestVoices",
            "contactflow_logs": "contactflowLogs",
            "contact_lens": "contactLens",
            "early_media": "earlyMedia",
            "use_custom_tts_voices": "useCustomTtsVoices",
        },
    )
    class AttributesProperty:
        def __init__(
            self,
            *,
            inbound_calls: typing.Union[builtins.bool, _IResolvable_da3f097b],
            outbound_calls: typing.Union[builtins.bool, _IResolvable_da3f097b],
            auto_resolve_best_voices: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            contactflow_logs: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            contact_lens: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            early_media: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            use_custom_tts_voices: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''*This is a preview release for Amazon Connect .

            It is subject to change.*

            :param inbound_calls: ``CfnInstance.AttributesProperty.InboundCalls``.
            :param outbound_calls: ``CfnInstance.AttributesProperty.OutboundCalls``.
            :param auto_resolve_best_voices: ``CfnInstance.AttributesProperty.AutoResolveBestVoices``.
            :param contactflow_logs: ``CfnInstance.AttributesProperty.ContactflowLogs``.
            :param contact_lens: ``CfnInstance.AttributesProperty.ContactLens``.
            :param early_media: ``CfnInstance.AttributesProperty.EarlyMedia``.
            :param use_custom_tts_voices: ``CfnInstance.AttributesProperty.UseCustomTTSVoices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                attributes_property = connect.CfnInstance.AttributesProperty(
                    inbound_calls=False,
                    outbound_calls=False,
                
                    # the properties below are optional
                    auto_resolve_best_voices=False,
                    contactflow_logs=False,
                    contact_lens=False,
                    early_media=False,
                    use_custom_tts_voices=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c40aedafdc4ea4fb2b717cc5c6ef0e2db4eb7490be99c35b78dc90f18526d068)
                check_type(argname="argument inbound_calls", value=inbound_calls, expected_type=type_hints["inbound_calls"])
                check_type(argname="argument outbound_calls", value=outbound_calls, expected_type=type_hints["outbound_calls"])
                check_type(argname="argument auto_resolve_best_voices", value=auto_resolve_best_voices, expected_type=type_hints["auto_resolve_best_voices"])
                check_type(argname="argument contactflow_logs", value=contactflow_logs, expected_type=type_hints["contactflow_logs"])
                check_type(argname="argument contact_lens", value=contact_lens, expected_type=type_hints["contact_lens"])
                check_type(argname="argument early_media", value=early_media, expected_type=type_hints["early_media"])
                check_type(argname="argument use_custom_tts_voices", value=use_custom_tts_voices, expected_type=type_hints["use_custom_tts_voices"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "inbound_calls": inbound_calls,
                "outbound_calls": outbound_calls,
            }
            if auto_resolve_best_voices is not None:
                self._values["auto_resolve_best_voices"] = auto_resolve_best_voices
            if contactflow_logs is not None:
                self._values["contactflow_logs"] = contactflow_logs
            if contact_lens is not None:
                self._values["contact_lens"] = contact_lens
            if early_media is not None:
                self._values["early_media"] = early_media
            if use_custom_tts_voices is not None:
                self._values["use_custom_tts_voices"] = use_custom_tts_voices

        @builtins.property
        def inbound_calls(self) -> typing.Union[builtins.bool, _IResolvable_da3f097b]:
            '''``CfnInstance.AttributesProperty.InboundCalls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-inboundcalls
            '''
            result = self._values.get("inbound_calls")
            assert result is not None, "Required property 'inbound_calls' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_da3f097b], result)

        @builtins.property
        def outbound_calls(self) -> typing.Union[builtins.bool, _IResolvable_da3f097b]:
            '''``CfnInstance.AttributesProperty.OutboundCalls``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-outboundcalls
            '''
            result = self._values.get("outbound_calls")
            assert result is not None, "Required property 'outbound_calls' is missing"
            return typing.cast(typing.Union[builtins.bool, _IResolvable_da3f097b], result)

        @builtins.property
        def auto_resolve_best_voices(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnInstance.AttributesProperty.AutoResolveBestVoices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-autoresolvebestvoices
            '''
            result = self._values.get("auto_resolve_best_voices")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def contactflow_logs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnInstance.AttributesProperty.ContactflowLogs``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-contactflowlogs
            '''
            result = self._values.get("contactflow_logs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def contact_lens(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnInstance.AttributesProperty.ContactLens``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-contactlens
            '''
            result = self._values.get("contact_lens")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def early_media(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnInstance.AttributesProperty.EarlyMedia``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-earlymedia
            '''
            result = self._values.get("early_media")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def use_custom_tts_voices(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnInstance.AttributesProperty.UseCustomTTSVoices``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-usecustomttsvoices
            '''
            result = self._values.get("use_custom_tts_voices")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "identity_management_type": "identityManagementType",
        "directory_id": "directoryId",
        "instance_alias": "instanceAlias",
    },
)
class CfnInstanceProps:
    def __init__(
        self,
        *,
        attributes: typing.Union[typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        identity_management_type: builtins.str,
        directory_id: typing.Optional[builtins.str] = None,
        instance_alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnInstance``.

        :param attributes: A toggle for an individual feature at the instance level.
        :param identity_management_type: The identity management type.
        :param directory_id: The identifier for the directory.
        :param instance_alias: The alias of instance. ``InstanceAlias`` is only required when ``IdentityManagementType`` is ``CONNECT_MANAGED`` or ``SAML`` . ``InstanceAlias`` is not required when ``IdentityManagementType`` is ``EXISTING_DIRECTORY`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_instance_props = connect.CfnInstanceProps(
                attributes=connect.CfnInstance.AttributesProperty(
                    inbound_calls=False,
                    outbound_calls=False,
            
                    # the properties below are optional
                    auto_resolve_best_voices=False,
                    contactflow_logs=False,
                    contact_lens=False,
                    early_media=False,
                    use_custom_tts_voices=False
                ),
                identity_management_type="identityManagementType",
            
                # the properties below are optional
                directory_id="directoryId",
                instance_alias="instanceAlias"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67fdacfbc8ac4206df45637f43843e90e644b42387d3af9173f714ef095953b4)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument identity_management_type", value=identity_management_type, expected_type=type_hints["identity_management_type"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument instance_alias", value=instance_alias, expected_type=type_hints["instance_alias"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attributes": attributes,
            "identity_management_type": identity_management_type,
        }
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if instance_alias is not None:
            self._values["instance_alias"] = instance_alias

    @builtins.property
    def attributes(
        self,
    ) -> typing.Union[CfnInstance.AttributesProperty, _IResolvable_da3f097b]:
        '''A toggle for an individual feature at the instance level.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-attributes
        '''
        result = self._values.get("attributes")
        assert result is not None, "Required property 'attributes' is missing"
        return typing.cast(typing.Union[CfnInstance.AttributesProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def identity_management_type(self) -> builtins.str:
        '''The identity management type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-identitymanagementtype
        '''
        result = self._values.get("identity_management_type")
        assert result is not None, "Required property 'identity_management_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the directory.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-directoryid
        '''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_alias(self) -> typing.Optional[builtins.str]:
        '''The alias of instance.

        ``InstanceAlias`` is only required when ``IdentityManagementType`` is ``CONNECT_MANAGED`` or ``SAML`` . ``InstanceAlias`` is not required when ``IdentityManagementType`` is ``EXISTING_DIRECTORY`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-instancealias
        '''
        result = self._values.get("instance_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnInstanceStorageConfig(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnInstanceStorageConfig",
):
    '''A CloudFormation ``AWS::Connect::InstanceStorageConfig``.

    The storage configuration for the instance.

    :cloudformationResource: AWS::Connect::InstanceStorageConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_instance_storage_config = connect.CfnInstanceStorageConfig(self, "MyCfnInstanceStorageConfig",
            instance_arn="instanceArn",
            resource_type="resourceType",
            storage_type="storageType",
        
            # the properties below are optional
            kinesis_firehose_config=connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty(
                firehose_arn="firehoseArn"
            ),
            kinesis_stream_config=connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty(
                stream_arn="streamArn"
            ),
            kinesis_video_stream_config=connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty(
                prefix="prefix",
                retention_period_hours=123,
        
                # the properties below are optional
                encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            ),
            s3_config=connect.CfnInstanceStorageConfig.S3ConfigProperty(
                bucket_name="bucketName",
                bucket_prefix="bucketPrefix",
        
                # the properties below are optional
                encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        resource_type: builtins.str,
        storage_type: builtins.str,
        kinesis_firehose_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        kinesis_stream_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        kinesis_video_stream_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        s3_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::InstanceStorageConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param resource_type: A valid resource type. Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``
        :param storage_type: A valid storage type.
        :param kinesis_firehose_config: The configuration of the Kinesis Firehose delivery stream.
        :param kinesis_stream_config: The configuration of the Kinesis data stream.
        :param kinesis_video_stream_config: The configuration of the Kinesis video stream.
        :param s3_config: The S3 bucket configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c8e9e3ad538fac1acafd66e46e4e7a4f3893f93a8c6bb42ba1525f14973522)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInstanceStorageConfigProps(
            instance_arn=instance_arn,
            resource_type=resource_type,
            storage_type=storage_type,
            kinesis_firehose_config=kinesis_firehose_config,
            kinesis_stream_config=kinesis_stream_config,
            kinesis_video_stream_config=kinesis_video_stream_config,
            s3_config=s3_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047b8a3f497a61ecbf349954496260297e95ce2a4561a42f301589ab2cee4b2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64e208c0e80a04bb7be2d96f8d6f17f40b00cfff9d7822b7f4ecb07751859062)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationId")
    def attr_association_id(self) -> builtins.str:
        '''The existing association identifier that uniquely identifies the resource type and storage config for the given instance ID.

        :cloudformationAttribute: AssociationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb171c6a585c549bf0fad4d15990fc6ee838655cd803c3fd46739aba98a2a1d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        '''A valid resource type.

        Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-resourcetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae5f517bee9d34ee21bd11e2d5f0247d46092ae2f3deb37dcf2893b2f798f14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> builtins.str:
        '''A valid storage type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-storagetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "storageType"))

    @storage_type.setter
    def storage_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e576862f1e107b0e3735b4d183525ba16593162db67ddb46e8ca789a1af5850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageType", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisFirehoseConfig")
    def kinesis_firehose_config(
        self,
    ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", _IResolvable_da3f097b]]:
        '''The configuration of the Kinesis Firehose delivery stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", _IResolvable_da3f097b]], jsii.get(self, "kinesisFirehoseConfig"))

    @kinesis_firehose_config.setter
    def kinesis_firehose_config(
        self,
        value: typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisFirehoseConfigProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c82cfbbde3b0d4520ea2bf1db2e6d9a0262e0c56473bd9769a65fc32f975a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisFirehoseConfig", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisStreamConfig")
    def kinesis_stream_config(
        self,
    ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", _IResolvable_da3f097b]]:
        '''The configuration of the Kinesis data stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", _IResolvable_da3f097b]], jsii.get(self, "kinesisStreamConfig"))

    @kinesis_stream_config.setter
    def kinesis_stream_config(
        self,
        value: typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisStreamConfigProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a364c6eb62a091d24f417f496838aa90b1e63e040b4dad6e12dd8288568f014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisStreamConfig", value)

    @builtins.property
    @jsii.member(jsii_name="kinesisVideoStreamConfig")
    def kinesis_video_stream_config(
        self,
    ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", _IResolvable_da3f097b]]:
        '''The configuration of the Kinesis video stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", _IResolvable_da3f097b]], jsii.get(self, "kinesisVideoStreamConfig"))

    @kinesis_video_stream_config.setter
    def kinesis_video_stream_config(
        self,
        value: typing.Optional[typing.Union["CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43628a93b9adb2e5341b48d5f226f90e92dc0574e63f1fabc8616c9c49b35ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kinesisVideoStreamConfig", value)

    @builtins.property
    @jsii.member(jsii_name="s3Config")
    def s3_config(
        self,
    ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", _IResolvable_da3f097b]]:
        '''The S3 bucket configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-s3config
        '''
        return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", _IResolvable_da3f097b]], jsii.get(self, "s3Config"))

    @s3_config.setter
    def s3_config(
        self,
        value: typing.Optional[typing.Union["CfnInstanceStorageConfig.S3ConfigProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e076b90fc0b5155e89233d8d5afcf24aea56049cea6a67a56da67867dd963c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Config", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnInstanceStorageConfig.EncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "key_id": "keyId"},
    )
    class EncryptionConfigProperty:
        def __init__(
            self,
            *,
            encryption_type: builtins.str,
            key_id: builtins.str,
        ) -> None:
            '''The encryption configuration.

            :param encryption_type: The type of encryption.
            :param key_id: The full ARN of the encryption key. .. epigraph:: Be sure to provide the full ARN of the encryption key, not just the ID. Amazon Connect supports only KMS keys with the default key spec of ```SYMMETRIC_DEFAULT`` <https://docs.aws.amazon.com/kms/latest/developerguide/asymmetric-key-specs.html#key-spec-symmetric-default>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                encryption_config_property = connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc46269845c7184ad0679658c798d342839ec1fbf50541709790ef0d801dd540)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "encryption_type": encryption_type,
                "key_id": key_id,
            }

        @builtins.property
        def encryption_type(self) -> builtins.str:
            '''The type of encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html#cfn-connect-instancestorageconfig-encryptionconfig-encryptiontype
            '''
            result = self._values.get("encryption_type")
            assert result is not None, "Required property 'encryption_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_id(self) -> builtins.str:
            '''The full ARN of the encryption key.

            .. epigraph::

               Be sure to provide the full ARN of the encryption key, not just the ID.

               Amazon Connect supports only KMS keys with the default key spec of ```SYMMETRIC_DEFAULT`` <https://docs.aws.amazon.com/kms/latest/developerguide/asymmetric-key-specs.html#key-spec-symmetric-default>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html#cfn-connect-instancestorageconfig-encryptionconfig-keyid
            '''
            result = self._values.get("key_id")
            assert result is not None, "Required property 'key_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"firehose_arn": "firehoseArn"},
    )
    class KinesisFirehoseConfigProperty:
        def __init__(self, *, firehose_arn: builtins.str) -> None:
            '''Configuration information of a Kinesis Data Firehose delivery stream.

            :param firehose_arn: The Amazon Resource Name (ARN) of the delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisfirehoseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                kinesis_firehose_config_property = connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty(
                    firehose_arn="firehoseArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a572a34b9441880677e439712bb7b9dbc0a79fc55daf5839857f2041774e7c99)
                check_type(argname="argument firehose_arn", value=firehose_arn, expected_type=type_hints["firehose_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "firehose_arn": firehose_arn,
            }

        @builtins.property
        def firehose_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisfirehoseconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig-firehosearn
            '''
            result = self._values.get("firehose_arn")
            assert result is not None, "Required property 'firehose_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_arn": "streamArn"},
    )
    class KinesisStreamConfigProperty:
        def __init__(self, *, stream_arn: builtins.str) -> None:
            '''Configuration information of a Kinesis data stream.

            :param stream_arn: The Amazon Resource Name (ARN) of the data stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisstreamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                kinesis_stream_config_property = connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty(
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__198e237e2c62ec06cc78609686ceeb43aaecd21ba79e09b267cdd8be2c3743a1)
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stream_arn": stream_arn,
            }

        @builtins.property
        def stream_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the data stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisstreamconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig-streamarn
            '''
            result = self._values.get("stream_arn")
            assert result is not None, "Required property 'stream_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "prefix": "prefix",
            "retention_period_hours": "retentionPeriodHours",
            "encryption_config": "encryptionConfig",
        },
    )
    class KinesisVideoStreamConfigProperty:
        def __init__(
            self,
            *,
            prefix: builtins.str,
            retention_period_hours: jsii.Number,
            encryption_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Configuration information of a Kinesis video stream.

            :param prefix: The prefix of the video stream.
            :param retention_period_hours: The number of hours data is retained in the stream. Kinesis Video Streams retains the data in a data store that is associated with the stream. The default value is 0, indicating that the stream does not persist data.
            :param encryption_config: The encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                kinesis_video_stream_config_property = connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty(
                    prefix="prefix",
                    retention_period_hours=123,
                
                    # the properties below are optional
                    encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__52c9485c197abc64e1dbe93a9ffbdf11fda8b3df13bc67381180643da843a5b8)
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument retention_period_hours", value=retention_period_hours, expected_type=type_hints["retention_period_hours"])
                check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "prefix": prefix,
                "retention_period_hours": retention_period_hours,
            }
            if encryption_config is not None:
                self._values["encryption_config"] = encryption_config

        @builtins.property
        def prefix(self) -> builtins.str:
            '''The prefix of the video stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-prefix
            '''
            result = self._values.get("prefix")
            assert result is not None, "Required property 'prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def retention_period_hours(self) -> jsii.Number:
            '''The number of hours data is retained in the stream.

            Kinesis Video Streams retains the data in a data store that is associated with the stream.

            The default value is 0, indicating that the stream does not persist data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-retentionperiodhours
            '''
            result = self._values.get("retention_period_hours")
            assert result is not None, "Required property 'retention_period_hours' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def encryption_config(
            self,
        ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", _IResolvable_da3f097b]]:
            '''The encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-encryptionconfig
            '''
            result = self._values.get("encryption_config")
            return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisVideoStreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnInstanceStorageConfig.S3ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "encryption_config": "encryptionConfig",
        },
    )
    class S3ConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            bucket_prefix: builtins.str,
            encryption_config: typing.Optional[typing.Union[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Information about the Amazon Simple Storage Service (Amazon S3) storage type.

            :param bucket_name: The S3 bucket name.
            :param bucket_prefix: The S3 bucket prefix.
            :param encryption_config: The Amazon S3 encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                s3_config_property = connect.CfnInstanceStorageConfig.S3ConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                
                    # the properties below are optional
                    encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7296a98085d62b3fe09acddef52fca10fedbaae666bc4512bfa543fd1ddcccab)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
                "bucket_prefix": bucket_prefix,
            }
            if encryption_config is not None:
                self._values["encryption_config"] = encryption_config

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The S3 bucket name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def bucket_prefix(self) -> builtins.str:
            '''The S3 bucket prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            assert result is not None, "Required property 'bucket_prefix' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def encryption_config(
            self,
        ) -> typing.Optional[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", _IResolvable_da3f097b]]:
            '''The Amazon S3 encryption configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-encryptionconfig
            '''
            result = self._values.get("encryption_config")
            return typing.cast(typing.Optional[typing.Union["CfnInstanceStorageConfig.EncryptionConfigProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnInstanceStorageConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "resource_type": "resourceType",
        "storage_type": "storageType",
        "kinesis_firehose_config": "kinesisFirehoseConfig",
        "kinesis_stream_config": "kinesisStreamConfig",
        "kinesis_video_stream_config": "kinesisVideoStreamConfig",
        "s3_config": "s3Config",
    },
)
class CfnInstanceStorageConfigProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        resource_type: builtins.str,
        storage_type: builtins.str,
        kinesis_firehose_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        kinesis_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        kinesis_video_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        s3_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    ) -> None:
        '''Properties for defining a ``CfnInstanceStorageConfig``.

        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param resource_type: A valid resource type. Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``
        :param storage_type: A valid storage type.
        :param kinesis_firehose_config: The configuration of the Kinesis Firehose delivery stream.
        :param kinesis_stream_config: The configuration of the Kinesis data stream.
        :param kinesis_video_stream_config: The configuration of the Kinesis video stream.
        :param s3_config: The S3 bucket configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_instance_storage_config_props = connect.CfnInstanceStorageConfigProps(
                instance_arn="instanceArn",
                resource_type="resourceType",
                storage_type="storageType",
            
                # the properties below are optional
                kinesis_firehose_config=connect.CfnInstanceStorageConfig.KinesisFirehoseConfigProperty(
                    firehose_arn="firehoseArn"
                ),
                kinesis_stream_config=connect.CfnInstanceStorageConfig.KinesisStreamConfigProperty(
                    stream_arn="streamArn"
                ),
                kinesis_video_stream_config=connect.CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty(
                    prefix="prefix",
                    retention_period_hours=123,
            
                    # the properties below are optional
                    encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                ),
                s3_config=connect.CfnInstanceStorageConfig.S3ConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
            
                    # the properties below are optional
                    encryption_config=connect.CfnInstanceStorageConfig.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__220fe9c269db6e3bcb651e492fae1b71e17d6b254dfd6b60c71dc0cda259419b)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument kinesis_firehose_config", value=kinesis_firehose_config, expected_type=type_hints["kinesis_firehose_config"])
            check_type(argname="argument kinesis_stream_config", value=kinesis_stream_config, expected_type=type_hints["kinesis_stream_config"])
            check_type(argname="argument kinesis_video_stream_config", value=kinesis_video_stream_config, expected_type=type_hints["kinesis_video_stream_config"])
            check_type(argname="argument s3_config", value=s3_config, expected_type=type_hints["s3_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "resource_type": resource_type,
            "storage_type": storage_type,
        }
        if kinesis_firehose_config is not None:
            self._values["kinesis_firehose_config"] = kinesis_firehose_config
        if kinesis_stream_config is not None:
            self._values["kinesis_stream_config"] = kinesis_stream_config
        if kinesis_video_stream_config is not None:
            self._values["kinesis_video_stream_config"] = kinesis_video_stream_config
        if s3_config is not None:
            self._values["s3_config"] = s3_config

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type(self) -> builtins.str:
        '''A valid resource type.

        Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-resourcetype
        '''
        result = self._values.get("resource_type")
        assert result is not None, "Required property 'resource_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_type(self) -> builtins.str:
        '''A valid storage type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-storagetype
        '''
        result = self._values.get("storage_type")
        assert result is not None, "Required property 'storage_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kinesis_firehose_config(
        self,
    ) -> typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, _IResolvable_da3f097b]]:
        '''The configuration of the Kinesis Firehose delivery stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig
        '''
        result = self._values.get("kinesis_firehose_config")
        return typing.cast(typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def kinesis_stream_config(
        self,
    ) -> typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, _IResolvable_da3f097b]]:
        '''The configuration of the Kinesis data stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig
        '''
        result = self._values.get("kinesis_stream_config")
        return typing.cast(typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def kinesis_video_stream_config(
        self,
    ) -> typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, _IResolvable_da3f097b]]:
        '''The configuration of the Kinesis video stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig
        '''
        result = self._values.get("kinesis_video_stream_config")
        return typing.cast(typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def s3_config(
        self,
    ) -> typing.Optional[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, _IResolvable_da3f097b]]:
        '''The S3 bucket configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-s3config
        '''
        result = self._values.get("s3_config")
        return typing.cast(typing.Optional[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, _IResolvable_da3f097b]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceStorageConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnIntegrationAssociation(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnIntegrationAssociation",
):
    '''A CloudFormation ``AWS::Connect::IntegrationAssociation``.

    Specifies the association of an AWS resource such as Lex bot (both v1 and v2) and Lambda function with an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::IntegrationAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_integration_association = connect.CfnIntegrationAssociation(self, "MyCfnIntegrationAssociation",
            instance_id="instanceId",
            integration_arn="integrationArn",
            integration_type="integrationType"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_id: builtins.str,
        integration_arn: builtins.str,
        integration_type: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Connect::IntegrationAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param integration_arn: ARN of the integration being associated with the instance. *Minimum* : ``1`` *Maximum* : ``140``
        :param integration_type: Specifies the integration type to be associated with the instance. *Allowed Values* : ``LEX_BOT`` | ``LAMBDA_FUNCTION``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0623057688349069456f9eae4995faa9cd189f98024c1f76262706d5734b311e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIntegrationAssociationProps(
            instance_id=instance_id,
            integration_arn=integration_arn,
            integration_type=integration_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb2bfc240169367a312e392a1f57215cf8d8c8079407283c69a1ce7b13f7f09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3d2595ec7f89aa2a00d106ed9c54cd5cee3b8f448483b246b960847d1347cd0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrIntegrationAssociationId")
    def attr_integration_association_id(self) -> builtins.str:
        '''Identifier of the association with an Amazon Connect instance.

        :cloudformationAttribute: IntegrationAssociationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIntegrationAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-instanceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7925af3a6409e56b03183e28600488914d5fe9b4e7accd90ff869ac4ba2618e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value)

    @builtins.property
    @jsii.member(jsii_name="integrationArn")
    def integration_arn(self) -> builtins.str:
        '''ARN of the integration being associated with the instance.

        *Minimum* : ``1``

        *Maximum* : ``140``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-integrationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "integrationArn"))

    @integration_arn.setter
    def integration_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cc0c68d9b0ec88ff8644cffd658aa26a913dcd92e1fc6ea4af9e71598d78538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationArn", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def integration_type(self) -> builtins.str:
        '''Specifies the integration type to be associated with the instance.

        *Allowed Values* : ``LEX_BOT`` | ``LAMBDA_FUNCTION``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-integrationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "integrationType"))

    @integration_type.setter
    def integration_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb9a11163321e5e540a87e2baf965475a45e960cf9aa4a424acc86dcad3feef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnIntegrationAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_id": "instanceId",
        "integration_arn": "integrationArn",
        "integration_type": "integrationType",
    },
)
class CfnIntegrationAssociationProps:
    def __init__(
        self,
        *,
        instance_id: builtins.str,
        integration_arn: builtins.str,
        integration_type: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnIntegrationAssociation``.

        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param integration_arn: ARN of the integration being associated with the instance. *Minimum* : ``1`` *Maximum* : ``140``
        :param integration_type: Specifies the integration type to be associated with the instance. *Allowed Values* : ``LEX_BOT`` | ``LAMBDA_FUNCTION``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_integration_association_props = connect.CfnIntegrationAssociationProps(
                instance_id="instanceId",
                integration_arn="integrationArn",
                integration_type="integrationType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe194aedf3230ea702915cbc89ea1228fbcd7507b4352cd6ca6f2c8b3d412d21)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument integration_arn", value=integration_arn, expected_type=type_hints["integration_arn"])
            check_type(argname="argument integration_type", value=integration_type, expected_type=type_hints["integration_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_id": instance_id,
            "integration_arn": integration_arn,
            "integration_type": integration_type,
        }

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-instanceid
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_arn(self) -> builtins.str:
        '''ARN of the integration being associated with the instance.

        *Minimum* : ``1``

        *Maximum* : ``140``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-integrationarn
        '''
        result = self._values.get("integration_arn")
        assert result is not None, "Required property 'integration_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def integration_type(self) -> builtins.str:
        '''Specifies the integration type to be associated with the instance.

        *Allowed Values* : ``LEX_BOT`` | ``LAMBDA_FUNCTION``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-integrationtype
        '''
        result = self._values.get("integration_type")
        assert result is not None, "Required property 'integration_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnPhoneNumber(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnPhoneNumber",
):
    '''A CloudFormation ``AWS::Connect::PhoneNumber``.

    Claims a phone number to the specified Amazon Connect instance or traffic distribution group.

    :cloudformationResource: AWS::Connect::PhoneNumber
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_phone_number = connect.CfnPhoneNumber(self, "MyCfnPhoneNumber",
            country_code="countryCode",
            target_arn="targetArn",
            type="type",
        
            # the properties below are optional
            description="description",
            prefix="prefix",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        country_code: builtins.str,
        target_arn: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::PhoneNumber``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param country_code: The ISO country code.
        :param target_arn: The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.
        :param type: The type of phone number.
        :param description: The description of the phone number.
        :param prefix: The prefix of the phone number. If provided, it must contain ``+`` as part of the country code. *Pattern* : ``^\\\\+[0-9]{1,15}``
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ec70d84fd2bda163d290722acbb6feca633b4ee134732d8b720c0b96701cb7b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPhoneNumberProps(
            country_code=country_code,
            target_arn=target_arn,
            type=type,
            description=description,
            prefix=prefix,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccee69f4a06306d444592cd5cf9588d2bb31a952c87c3487ff8ad82fc8c8cf94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b523ee72d695f2e00f7a42b04d5ef172e9c4c9f850d546d7d54f31058efcbf64)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAddress")
    def attr_address(self) -> builtins.str:
        '''The phone number, in E.164 format.

        :cloudformationAttribute: Address
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAddress"))

    @builtins.property
    @jsii.member(jsii_name="attrPhoneNumberArn")
    def attr_phone_number_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the phone number.

        :cloudformationAttribute: PhoneNumberArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPhoneNumberArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        '''The ISO country code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-countrycode
        '''
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @country_code.setter
    def country_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e8049a6bcb60451cb780647e8cad2360b140018c95db8d6b0e339ed0524e56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "countryCode", value)

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-targetarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aee914dbb9c13734690f391827e9cd37ca89f521141f3de61e900bfbbd902752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of phone number.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0868299e1426aef01fcea4843c3c28737fa3b7614cce2aa77e978bfa8976f8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the phone number.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9949958c848f257cc25ceae67fe2e9cee4b1972f09d90ea4ed667dac758be40e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix of the phone number. If provided, it must contain ``+`` as part of the country code.

        *Pattern* : ``^\\\\+[0-9]{1,15}``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-prefix
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572d2dd079d87f4a7578acddb0bc7dbcca5ec4c2fecd370ff662ac4d429ea5b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnPhoneNumberProps",
    jsii_struct_bases=[],
    name_mapping={
        "country_code": "countryCode",
        "target_arn": "targetArn",
        "type": "type",
        "description": "description",
        "prefix": "prefix",
        "tags": "tags",
    },
)
class CfnPhoneNumberProps:
    def __init__(
        self,
        *,
        country_code: builtins.str,
        target_arn: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPhoneNumber``.

        :param country_code: The ISO country code.
        :param target_arn: The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.
        :param type: The type of phone number.
        :param description: The description of the phone number.
        :param prefix: The prefix of the phone number. If provided, it must contain ``+`` as part of the country code. *Pattern* : ``^\\\\+[0-9]{1,15}``
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_phone_number_props = connect.CfnPhoneNumberProps(
                country_code="countryCode",
                target_arn="targetArn",
                type="type",
            
                # the properties below are optional
                description="description",
                prefix="prefix",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b6cbf832a5409fafc1645b1b1a1567ef5e6d173dfed6d56cae08b977fd4b95)
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "country_code": country_code,
            "target_arn": target_arn,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if prefix is not None:
            self._values["prefix"] = prefix
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def country_code(self) -> builtins.str:
        '''The ISO country code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-countrycode
        '''
        result = self._values.get("country_code")
        assert result is not None, "Required property 'country_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-targetarn
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of phone number.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the phone number.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix of the phone number. If provided, it must contain ``+`` as part of the country code.

        *Pattern* : ``^\\\\+[0-9]{1,15}``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-prefix
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPhoneNumberProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnQuickConnect(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnQuickConnect",
):
    '''A CloudFormation ``AWS::Connect::QuickConnect``.

    Specifies a quick connect for an Amazon Connect instance.

    :cloudformationResource: AWS::Connect::QuickConnect
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_quick_connect = connect.CfnQuickConnect(self, "MyCfnQuickConnect",
            instance_arn="instanceArn",
            name="name",
            quick_connect_config=connect.CfnQuickConnect.QuickConnectConfigProperty(
                quick_connect_type="quickConnectType",
        
                # the properties below are optional
                phone_config=connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                    phone_number="phoneNumber"
                ),
                queue_config=connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    queue_arn="queueArn"
                ),
                user_config=connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    user_arn="userArn"
                )
            ),
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        quick_connect_config: typing.Union[typing.Union["CfnQuickConnect.QuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::QuickConnect``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the quick connect.
        :param quick_connect_config: Contains information about the quick connect.
        :param description: The description of the quick connect.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44121049328c061f99076678805110a34e47bc31097d43b030f388eca53234e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnQuickConnectProps(
            instance_arn=instance_arn,
            name=name,
            quick_connect_config=quick_connect_config,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac17b042f7cf408478c49ac00f219efb0ede78bbe556a5ec55b66c5025bf6198)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a25858c0bb7501da609f58db5989e1c4593c28fa68b47618b9ed5533379f506)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrQuickConnectArn")
    def attr_quick_connect_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the quick connect.

        :cloudformationAttribute: QuickConnectArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrQuickConnectArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4d649c9007065ac09a0caa875fd618788a773aab62e76f33a48ae54d5284ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d7d088ec5e9e804f349ff7c9f716ab0de501abdb1561144e8cba5e16ae351d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="quickConnectConfig")
    def quick_connect_config(
        self,
    ) -> typing.Union["CfnQuickConnect.QuickConnectConfigProperty", _IResolvable_da3f097b]:
        '''Contains information about the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-quickconnectconfig
        '''
        return typing.cast(typing.Union["CfnQuickConnect.QuickConnectConfigProperty", _IResolvable_da3f097b], jsii.get(self, "quickConnectConfig"))

    @quick_connect_config.setter
    def quick_connect_config(
        self,
        value: typing.Union["CfnQuickConnect.QuickConnectConfigProperty", _IResolvable_da3f097b],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf95cf02ae05236caa122a481ca15ec758f528b67ca083a27c0d64c2c3c7f4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "quickConnectConfig", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f4633c9c2a7464e4f507d168aa19eee91126aef113fdfcb12ab23fe37d443cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"phone_number": "phoneNumber"},
    )
    class PhoneNumberQuickConnectConfigProperty:
        def __init__(self, *, phone_number: builtins.str) -> None:
            '''Contains information about a phone number for a quick connect.

            :param phone_number: The phone number in E.164 format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-phonenumberquickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                phone_number_quick_connect_config_property = connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                    phone_number="phoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c594b9d59e37b885f89d8bea8817c96760d7982a4ec30c3cec4c9d6620f0690)
                check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "phone_number": phone_number,
            }

        @builtins.property
        def phone_number(self) -> builtins.str:
            '''The phone number in E.164 format.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-phonenumberquickconnectconfig.html#cfn-connect-quickconnect-phonenumberquickconnectconfig-phonenumber
            '''
            result = self._values.get("phone_number")
            assert result is not None, "Required property 'phone_number' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PhoneNumberQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnQuickConnect.QueueQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_flow_arn": "contactFlowArn", "queue_arn": "queueArn"},
    )
    class QueueQuickConnectConfigProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: builtins.str,
            queue_arn: builtins.str,
        ) -> None:
            '''Contains information about a queue for a quick connect.

            The flow must be of type Transfer to Queue.

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param queue_arn: The Amazon Resource Name (ARN) of the queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                queue_quick_connect_config_property = connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    queue_arn="queueArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7632a33b2bc55f259222d21532508c7c3f8f6ef77e1098e16a144fdb3514616)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_flow_arn": contact_flow_arn,
                "queue_arn": queue_arn,
            }

        @builtins.property
        def contact_flow_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html#cfn-connect-quickconnect-queuequickconnectconfig-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            assert result is not None, "Required property 'contact_flow_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def queue_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html#cfn-connect-quickconnect-queuequickconnectconfig-queuearn
            '''
            result = self._values.get("queue_arn")
            assert result is not None, "Required property 'queue_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnQuickConnect.QuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "quick_connect_type": "quickConnectType",
            "phone_config": "phoneConfig",
            "queue_config": "queueConfig",
            "user_config": "userConfig",
        },
    )
    class QuickConnectConfigProperty:
        def __init__(
            self,
            *,
            quick_connect_type: builtins.str,
            phone_config: typing.Optional[typing.Union[typing.Union["CfnQuickConnect.PhoneNumberQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            queue_config: typing.Optional[typing.Union[typing.Union["CfnQuickConnect.QueueQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            user_config: typing.Optional[typing.Union[typing.Union["CfnQuickConnect.UserQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Contains configuration settings for a quick connect.

            :param quick_connect_type: The type of quick connect. In the Amazon Connect console, when you create a quick connect, you are prompted to assign one of the following types: Agent (USER), External (PHONE_NUMBER), or Queue (QUEUE).
            :param phone_config: The phone configuration. This is required only if QuickConnectType is PHONE_NUMBER.
            :param queue_config: The queue configuration. This is required only if QuickConnectType is QUEUE.
            :param user_config: The user configuration. This is required only if QuickConnectType is USER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                quick_connect_config_property = connect.CfnQuickConnect.QuickConnectConfigProperty(
                    quick_connect_type="quickConnectType",
                
                    # the properties below are optional
                    phone_config=connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                        phone_number="phoneNumber"
                    ),
                    queue_config=connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        queue_arn="queueArn"
                    ),
                    user_config=connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        user_arn="userArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5a5ffbc184bff7cbc8cc0dd5bf20c11b8676ca18d518a33d4b7ae2d76891f05d)
                check_type(argname="argument quick_connect_type", value=quick_connect_type, expected_type=type_hints["quick_connect_type"])
                check_type(argname="argument phone_config", value=phone_config, expected_type=type_hints["phone_config"])
                check_type(argname="argument queue_config", value=queue_config, expected_type=type_hints["queue_config"])
                check_type(argname="argument user_config", value=user_config, expected_type=type_hints["user_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "quick_connect_type": quick_connect_type,
            }
            if phone_config is not None:
                self._values["phone_config"] = phone_config
            if queue_config is not None:
                self._values["queue_config"] = queue_config
            if user_config is not None:
                self._values["user_config"] = user_config

        @builtins.property
        def quick_connect_type(self) -> builtins.str:
            '''The type of quick connect.

            In the Amazon Connect console, when you create a quick connect, you are prompted to assign one of the following types: Agent (USER), External (PHONE_NUMBER), or Queue (QUEUE).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-quickconnecttype
            '''
            result = self._values.get("quick_connect_type")
            assert result is not None, "Required property 'quick_connect_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def phone_config(
            self,
        ) -> typing.Optional[typing.Union["CfnQuickConnect.PhoneNumberQuickConnectConfigProperty", _IResolvable_da3f097b]]:
            '''The phone configuration.

            This is required only if QuickConnectType is PHONE_NUMBER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-phoneconfig
            '''
            result = self._values.get("phone_config")
            return typing.cast(typing.Optional[typing.Union["CfnQuickConnect.PhoneNumberQuickConnectConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def queue_config(
            self,
        ) -> typing.Optional[typing.Union["CfnQuickConnect.QueueQuickConnectConfigProperty", _IResolvable_da3f097b]]:
            '''The queue configuration.

            This is required only if QuickConnectType is QUEUE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-queueconfig
            '''
            result = self._values.get("queue_config")
            return typing.cast(typing.Optional[typing.Union["CfnQuickConnect.QueueQuickConnectConfigProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def user_config(
            self,
        ) -> typing.Optional[typing.Union["CfnQuickConnect.UserQuickConnectConfigProperty", _IResolvable_da3f097b]]:
            '''The user configuration.

            This is required only if QuickConnectType is USER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-userconfig
            '''
            result = self._values.get("user_config")
            return typing.cast(typing.Optional[typing.Union["CfnQuickConnect.UserQuickConnectConfigProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnQuickConnect.UserQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_flow_arn": "contactFlowArn", "user_arn": "userArn"},
    )
    class UserQuickConnectConfigProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: builtins.str,
            user_arn: builtins.str,
        ) -> None:
            '''Contains information about the quick connect configuration settings for a user.

            The contact flow must be of type Transfer to Agent.

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param user_arn: The Amazon Resource Name (ARN) of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                user_quick_connect_config_property = connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    user_arn="userArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7730396d4c494428f6ddd636283d9d5c17ba3fbc6013f1c545a8788d686e0fc1)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument user_arn", value=user_arn, expected_type=type_hints["user_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_flow_arn": contact_flow_arn,
                "user_arn": user_arn,
            }

        @builtins.property
        def contact_flow_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html#cfn-connect-quickconnect-userquickconnectconfig-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            assert result is not None, "Required property 'contact_flow_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html#cfn-connect-quickconnect-userquickconnectconfig-userarn
            '''
            result = self._values.get("user_arn")
            assert result is not None, "Required property 'user_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnQuickConnectProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "name": "name",
        "quick_connect_config": "quickConnectConfig",
        "description": "description",
        "tags": "tags",
    },
)
class CfnQuickConnectProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        quick_connect_config: typing.Union[typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnQuickConnect``.

        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the quick connect.
        :param quick_connect_config: Contains information about the quick connect.
        :param description: The description of the quick connect.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_quick_connect_props = connect.CfnQuickConnectProps(
                instance_arn="instanceArn",
                name="name",
                quick_connect_config=connect.CfnQuickConnect.QuickConnectConfigProperty(
                    quick_connect_type="quickConnectType",
            
                    # the properties below are optional
                    phone_config=connect.CfnQuickConnect.PhoneNumberQuickConnectConfigProperty(
                        phone_number="phoneNumber"
                    ),
                    queue_config=connect.CfnQuickConnect.QueueQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        queue_arn="queueArn"
                    ),
                    user_config=connect.CfnQuickConnect.UserQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        user_arn="userArn"
                    )
                ),
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d4ffda8775de853a0509cc15bc43b59e37fc8f6d1d2c110c1202c4192841fbd)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument quick_connect_config", value=quick_connect_config, expected_type=type_hints["quick_connect_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "name": name,
            "quick_connect_config": quick_connect_config,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def quick_connect_config(
        self,
    ) -> typing.Union[CfnQuickConnect.QuickConnectConfigProperty, _IResolvable_da3f097b]:
        '''Contains information about the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-quickconnectconfig
        '''
        result = self._values.get("quick_connect_config")
        assert result is not None, "Required property 'quick_connect_config' is missing"
        return typing.cast(typing.Union[CfnQuickConnect.QuickConnectConfigProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the quick connect.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQuickConnectProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnRule(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnRule",
):
    '''A CloudFormation ``AWS::Connect::Rule``.

    Creates a rule for the specified Amazon Connect instance.

    :cloudformationResource: AWS::Connect::Rule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        # assign_contact_category_actions: Any
        
        cfn_rule = connect.CfnRule(self, "MyCfnRule",
            actions=connect.CfnRule.ActionsProperty(
                assign_contact_category_actions=[assign_contact_category_actions],
                event_bridge_actions=[connect.CfnRule.EventBridgeActionProperty(
                    name="name"
                )],
                send_notification_actions=[connect.CfnRule.SendNotificationActionProperty(
                    content="content",
                    content_type="contentType",
                    delivery_method="deliveryMethod",
                    recipient=connect.CfnRule.NotificationRecipientTypeProperty(
                        user_arns=["userArns"],
                        user_tags={
                            "user_tags_key": "userTags"
                        }
                    ),
        
                    # the properties below are optional
                    subject="subject"
                )],
                task_actions=[connect.CfnRule.TaskActionProperty(
                    contact_flow_arn="contactFlowArn",
                    name="name",
        
                    # the properties below are optional
                    description="description",
                    references={
                        "references_key": connect.CfnRule.ReferenceProperty(
                            type="type",
                            value="value"
                        )
                    }
                )]
            ),
            function="function",
            instance_arn="instanceArn",
            name="name",
            publish_status="publishStatus",
            trigger_event_source=connect.CfnRule.RuleTriggerEventSourceProperty(
                event_source_name="eventSourceName",
        
                # the properties below are optional
                integration_association_arn="integrationAssociationArn"
            ),
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        actions: typing.Union[typing.Union["CfnRule.ActionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        function: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        publish_status: builtins.str,
        trigger_event_source: typing.Union[typing.Union["CfnRule.RuleTriggerEventSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param actions: A list of actions to be run when the rule is triggered.
        :param function: The conditions of the rule.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the rule.
        :param publish_status: The publish status of the rule. *Allowed values* : ``DRAFT`` | ``PUBLISHED``
        :param trigger_event_source: The event source to trigger the rule.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999d5f7971fc0ea0f693e0f9a61faf62317d493403a6d249ca1db6bc52d61e6f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleProps(
            actions=actions,
            function=function,
            instance_arn=instance_arn,
            name=name,
            publish_status=publish_status,
            trigger_event_source=trigger_event_source,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa852f8205e0acaca3e6361c61c512ea090fe504a708495d2b5bdadc81b30809)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8f82a813645b192cb4d0a6df6a35e9ffe4fe072375390e4d29ebb42555752ad)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleArn")
    def attr_rule_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the rule.

        :cloudformationAttribute: RuleArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.Union["CfnRule.ActionsProperty", _IResolvable_da3f097b]:
        '''A list of actions to be run when the rule is triggered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-actions
        '''
        return typing.cast(typing.Union["CfnRule.ActionsProperty", _IResolvable_da3f097b], jsii.get(self, "actions"))

    @actions.setter
    def actions(
        self,
        value: typing.Union["CfnRule.ActionsProperty", _IResolvable_da3f097b],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bdf3e9c3a73f02992b32c967f3457b7eeade7d3dfa554da9d661f54924ad9a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value)

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        '''The conditions of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-function
        '''
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85af4feedf296e30da787ccf9bc61e248b9a97c21a29fd8fbf38621d5d654fdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec5da44206c20fbb184f7443ea185123d28ab75d447650604f654e3fe336b233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6699a016b8fc3ffcc40b2227c32c82c77dcef5f7a74d28bea7e181707fb33bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="publishStatus")
    def publish_status(self) -> builtins.str:
        '''The publish status of the rule.

        *Allowed values* : ``DRAFT`` | ``PUBLISHED``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-publishstatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "publishStatus"))

    @publish_status.setter
    def publish_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__464a87f0223cf9d2bd4ca32eeb79cbb74d44d9fead6bf2a81a1db65870834bf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publishStatus", value)

    @builtins.property
    @jsii.member(jsii_name="triggerEventSource")
    def trigger_event_source(
        self,
    ) -> typing.Union["CfnRule.RuleTriggerEventSourceProperty", _IResolvable_da3f097b]:
        '''The event source to trigger the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-triggereventsource
        '''
        return typing.cast(typing.Union["CfnRule.RuleTriggerEventSourceProperty", _IResolvable_da3f097b], jsii.get(self, "triggerEventSource"))

    @trigger_event_source.setter
    def trigger_event_source(
        self,
        value: typing.Union["CfnRule.RuleTriggerEventSourceProperty", _IResolvable_da3f097b],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a752b13b9a86d9caa3ed642e2b19a8ac6db9d24515c76f729c8ad704d664388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerEventSource", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnRule.ActionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "assign_contact_category_actions": "assignContactCategoryActions",
            "event_bridge_actions": "eventBridgeActions",
            "send_notification_actions": "sendNotificationActions",
            "task_actions": "taskActions",
        },
    )
    class ActionsProperty:
        def __init__(
            self,
            *,
            assign_contact_category_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_da3f097b]] = None,
            event_bridge_actions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnRule.EventBridgeActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            send_notification_actions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnRule.SendNotificationActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            task_actions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnRule.TaskActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''A list of actions to be run when the rule is triggered.

            :param assign_contact_category_actions: Information about the contact category action. The syntax can be empty, for example, ``{}`` .
            :param event_bridge_actions: Information about the EventBridge action.
            :param send_notification_actions: Information about the send notification action.
            :param task_actions: Information about the task action. This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                # assign_contact_category_actions: Any
                
                actions_property = connect.CfnRule.ActionsProperty(
                    assign_contact_category_actions=[assign_contact_category_actions],
                    event_bridge_actions=[connect.CfnRule.EventBridgeActionProperty(
                        name="name"
                    )],
                    send_notification_actions=[connect.CfnRule.SendNotificationActionProperty(
                        content="content",
                        content_type="contentType",
                        delivery_method="deliveryMethod",
                        recipient=connect.CfnRule.NotificationRecipientTypeProperty(
                            user_arns=["userArns"],
                            user_tags={
                                "user_tags_key": "userTags"
                            }
                        ),
                
                        # the properties below are optional
                        subject="subject"
                    )],
                    task_actions=[connect.CfnRule.TaskActionProperty(
                        contact_flow_arn="contactFlowArn",
                        name="name",
                
                        # the properties below are optional
                        description="description",
                        references={
                            "references_key": connect.CfnRule.ReferenceProperty(
                                type="type",
                                value="value"
                            )
                        }
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ef20a75dbfc13161d3fff13ec1c4969adde44c34f62addd27e480514ce92395)
                check_type(argname="argument assign_contact_category_actions", value=assign_contact_category_actions, expected_type=type_hints["assign_contact_category_actions"])
                check_type(argname="argument event_bridge_actions", value=event_bridge_actions, expected_type=type_hints["event_bridge_actions"])
                check_type(argname="argument send_notification_actions", value=send_notification_actions, expected_type=type_hints["send_notification_actions"])
                check_type(argname="argument task_actions", value=task_actions, expected_type=type_hints["task_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assign_contact_category_actions is not None:
                self._values["assign_contact_category_actions"] = assign_contact_category_actions
            if event_bridge_actions is not None:
                self._values["event_bridge_actions"] = event_bridge_actions
            if send_notification_actions is not None:
                self._values["send_notification_actions"] = send_notification_actions
            if task_actions is not None:
                self._values["task_actions"] = task_actions

        @builtins.property
        def assign_contact_category_actions(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_da3f097b]]:
            '''Information about the contact category action.

            The syntax can be empty, for example, ``{}`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-assigncontactcategoryactions
            '''
            result = self._values.get("assign_contact_category_actions")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _IResolvable_da3f097b]], result)

        @builtins.property
        def event_bridge_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnRule.EventBridgeActionProperty", _IResolvable_da3f097b]]]]:
            '''Information about the EventBridge action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-eventbridgeactions
            '''
            result = self._values.get("event_bridge_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnRule.EventBridgeActionProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def send_notification_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnRule.SendNotificationActionProperty", _IResolvable_da3f097b]]]]:
            '''Information about the send notification action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-sendnotificationactions
            '''
            result = self._values.get("send_notification_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnRule.SendNotificationActionProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def task_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnRule.TaskActionProperty", _IResolvable_da3f097b]]]]:
            '''Information about the task action.

            This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-taskactions
            '''
            result = self._values.get("task_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnRule.TaskActionProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnRule.EventBridgeActionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class EventBridgeActionProperty:
        def __init__(self, *, name: builtins.str) -> None:
            '''The EventBridge action definition.

            :param name: The name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-eventbridgeaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                event_bridge_action_property = connect.CfnRule.EventBridgeActionProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__037f7c36eff1515bc6e2d8e67f9b2bac8beade9773e2103dd3b8b5ca5405e447)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-eventbridgeaction.html#cfn-connect-rule-eventbridgeaction-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnRule.NotificationRecipientTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"user_arns": "userArns", "user_tags": "userTags"},
    )
    class NotificationRecipientTypeProperty:
        def __init__(
            self,
            *,
            user_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            user_tags: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''The type of notification recipient.

            :param user_arns: The Amazon Resource Name (ARN) of the user account.
            :param user_tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }. Amazon Connect users with the specified tags will be notified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                notification_recipient_type_property = connect.CfnRule.NotificationRecipientTypeProperty(
                    user_arns=["userArns"],
                    user_tags={
                        "user_tags_key": "userTags"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d577395a2866fe40fdf75bbcc932da0701cd7985bbb4de4e2ef65243ba9d387)
                check_type(argname="argument user_arns", value=user_arns, expected_type=type_hints["user_arns"])
                check_type(argname="argument user_tags", value=user_tags, expected_type=type_hints["user_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if user_arns is not None:
                self._values["user_arns"] = user_arns
            if user_tags is not None:
                self._values["user_tags"] = user_tags

        @builtins.property
        def user_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Name (ARN) of the user account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html#cfn-connect-rule-notificationrecipienttype-userarns
            '''
            result = self._values.get("user_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def user_tags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
            '''The tags used to organize, track, or control access for this resource.

            For example, { "tags": {"key1":"value1", "key2":"value2"} }. Amazon Connect users with the specified tags will be notified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html#cfn-connect-rule-notificationrecipienttype-usertags
            '''
            result = self._values.get("user_tags")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationRecipientTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnRule.ReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ReferenceProperty:
        def __init__(self, *, type: builtins.str, value: builtins.str) -> None:
            '''Information about the reference when the ``referenceType`` is ``URL`` .

            Otherwise, null. (Supports variable injection in the ``Value`` field.)

            :param type: The type of the reference. ``DATE`` must be of type Epoch timestamp. *Allowed values* : ``URL`` | ``ATTACHMENT`` | ``NUMBER`` | ``STRING`` | ``DATE`` | ``EMAIL``
            :param value: A valid value for the reference. For example, for a URL reference, a formatted URL that is displayed to an agent in the Contact Control Panel (CCP).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                reference_property = connect.CfnRule.ReferenceProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6a9deeefd8de7f6bdabd5dee0827f879a4b6911d8516976e0492403b3a4724a)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
                "value": value,
            }

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of the reference. ``DATE`` must be of type Epoch timestamp.

            *Allowed values* : ``URL`` | ``ATTACHMENT`` | ``NUMBER`` | ``STRING`` | ``DATE`` | ``EMAIL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html#cfn-connect-rule-reference-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''A valid value for the reference.

            For example, for a URL reference, a formatted URL that is displayed to an agent in the Contact Control Panel (CCP).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html#cfn-connect-rule-reference-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnRule.RuleTriggerEventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_source_name": "eventSourceName",
            "integration_association_arn": "integrationAssociationArn",
        },
    )
    class RuleTriggerEventSourceProperty:
        def __init__(
            self,
            *,
            event_source_name: builtins.str,
            integration_association_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the event source.

            :param event_source_name: The name of the event source. *Allowed values* : ``OnPostCallAnalysisAvailable`` | ``OnRealTimeCallAnalysisAvailable`` | ``OnPostChatAnalysisAvailable`` | ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``
            :param integration_association_arn: The Amazon Resource Name (ARN) for the integration association. ``IntegrationAssociationArn`` is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                rule_trigger_event_source_property = connect.CfnRule.RuleTriggerEventSourceProperty(
                    event_source_name="eventSourceName",
                
                    # the properties below are optional
                    integration_association_arn="integrationAssociationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16bc3686835833422d3f82ede42c0b9acf288c30c14f9b3b761db32339bbd1f5)
                check_type(argname="argument event_source_name", value=event_source_name, expected_type=type_hints["event_source_name"])
                check_type(argname="argument integration_association_arn", value=integration_association_arn, expected_type=type_hints["integration_association_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "event_source_name": event_source_name,
            }
            if integration_association_arn is not None:
                self._values["integration_association_arn"] = integration_association_arn

        @builtins.property
        def event_source_name(self) -> builtins.str:
            '''The name of the event source.

            *Allowed values* : ``OnPostCallAnalysisAvailable`` | ``OnRealTimeCallAnalysisAvailable`` | ``OnPostChatAnalysisAvailable`` | ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html#cfn-connect-rule-ruletriggereventsource-eventsourcename
            '''
            result = self._values.get("event_source_name")
            assert result is not None, "Required property 'event_source_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def integration_association_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the integration association.

            ``IntegrationAssociationArn`` is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html#cfn-connect-rule-ruletriggereventsource-integrationassociationarn
            '''
            result = self._values.get("integration_association_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleTriggerEventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnRule.SendNotificationActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content": "content",
            "content_type": "contentType",
            "delivery_method": "deliveryMethod",
            "recipient": "recipient",
            "subject": "subject",
        },
    )
    class SendNotificationActionProperty:
        def __init__(
            self,
            *,
            content: builtins.str,
            content_type: builtins.str,
            delivery_method: builtins.str,
            recipient: typing.Union[typing.Union["CfnRule.NotificationRecipientTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
            subject: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the send notification action.

            :param content: Notification content. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param content_type: Content type format. *Allowed value* : ``PLAIN_TEXT``
            :param delivery_method: Notification delivery method. *Allowed value* : ``EMAIL``
            :param recipient: Notification recipient.
            :param subject: The subject of the email if the delivery method is ``EMAIL`` . Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                send_notification_action_property = connect.CfnRule.SendNotificationActionProperty(
                    content="content",
                    content_type="contentType",
                    delivery_method="deliveryMethod",
                    recipient=connect.CfnRule.NotificationRecipientTypeProperty(
                        user_arns=["userArns"],
                        user_tags={
                            "user_tags_key": "userTags"
                        }
                    ),
                
                    # the properties below are optional
                    subject="subject"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__199075d61da7aee6c24aad33a7023d6a679853ff216c051fe322418490e5e9e4)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                check_type(argname="argument delivery_method", value=delivery_method, expected_type=type_hints["delivery_method"])
                check_type(argname="argument recipient", value=recipient, expected_type=type_hints["recipient"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "content": content,
                "content_type": content_type,
                "delivery_method": delivery_method,
                "recipient": recipient,
            }
            if subject is not None:
                self._values["subject"] = subject

        @builtins.property
        def content(self) -> builtins.str:
            '''Notification content.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-content
            '''
            result = self._values.get("content")
            assert result is not None, "Required property 'content' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def content_type(self) -> builtins.str:
            '''Content type format.

            *Allowed value* : ``PLAIN_TEXT``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-contenttype
            '''
            result = self._values.get("content_type")
            assert result is not None, "Required property 'content_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def delivery_method(self) -> builtins.str:
            '''Notification delivery method.

            *Allowed value* : ``EMAIL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-deliverymethod
            '''
            result = self._values.get("delivery_method")
            assert result is not None, "Required property 'delivery_method' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def recipient(
            self,
        ) -> typing.Union["CfnRule.NotificationRecipientTypeProperty", _IResolvable_da3f097b]:
            '''Notification recipient.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-recipient
            '''
            result = self._values.get("recipient")
            assert result is not None, "Required property 'recipient' is missing"
            return typing.cast(typing.Union["CfnRule.NotificationRecipientTypeProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def subject(self) -> typing.Optional[builtins.str]:
            '''The subject of the email if the delivery method is ``EMAIL`` .

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SendNotificationActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnRule.TaskActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "contact_flow_arn": "contactFlowArn",
            "name": "name",
            "description": "description",
            "references": "references",
        },
    )
    class TaskActionProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: builtins.str,
            name: builtins.str,
            description: typing.Optional[builtins.str] = None,
            references: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnRule.ReferenceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Information about the task action.

            This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param name: The name. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param description: The description. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param references: Information about the reference when the ``referenceType`` is ``URL`` . Otherwise, null. ``URL`` is the only accepted type. (Supports variable injection in the ``Value`` field.)

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                task_action_property = connect.CfnRule.TaskActionProperty(
                    contact_flow_arn="contactFlowArn",
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    references={
                        "references_key": connect.CfnRule.ReferenceProperty(
                            type="type",
                            value="value"
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36d4ac91ef6fb71bdda5474ed1cbe12228c8f5caa3aec2778c4c6642b1ab6b3b)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument references", value=references, expected_type=type_hints["references"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "contact_flow_arn": contact_flow_arn,
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if references is not None:
                self._values["references"] = references

        @builtins.property
        def contact_flow_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            assert result is not None, "Required property 'contact_flow_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def references(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnRule.ReferenceProperty", _IResolvable_da3f097b]]]]:
            '''Information about the reference when the ``referenceType`` is ``URL`` .

            Otherwise, null. ``URL`` is the only accepted type. (Supports variable injection in the ``Value`` field.)

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-references
            '''
            result = self._values.get("references")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnRule.ReferenceProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "function": "function",
        "instance_arn": "instanceArn",
        "name": "name",
        "publish_status": "publishStatus",
        "trigger_event_source": "triggerEventSource",
        "tags": "tags",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        actions: typing.Union[typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        function: builtins.str,
        instance_arn: builtins.str,
        name: builtins.str,
        publish_status: builtins.str,
        trigger_event_source: typing.Union[typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRule``.

        :param actions: A list of actions to be run when the rule is triggered.
        :param function: The conditions of the rule.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the rule.
        :param publish_status: The publish status of the rule. *Allowed values* : ``DRAFT`` | ``PUBLISHED``
        :param trigger_event_source: The event source to trigger the rule.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            # assign_contact_category_actions: Any
            
            cfn_rule_props = connect.CfnRuleProps(
                actions=connect.CfnRule.ActionsProperty(
                    assign_contact_category_actions=[assign_contact_category_actions],
                    event_bridge_actions=[connect.CfnRule.EventBridgeActionProperty(
                        name="name"
                    )],
                    send_notification_actions=[connect.CfnRule.SendNotificationActionProperty(
                        content="content",
                        content_type="contentType",
                        delivery_method="deliveryMethod",
                        recipient=connect.CfnRule.NotificationRecipientTypeProperty(
                            user_arns=["userArns"],
                            user_tags={
                                "user_tags_key": "userTags"
                            }
                        ),
            
                        # the properties below are optional
                        subject="subject"
                    )],
                    task_actions=[connect.CfnRule.TaskActionProperty(
                        contact_flow_arn="contactFlowArn",
                        name="name",
            
                        # the properties below are optional
                        description="description",
                        references={
                            "references_key": connect.CfnRule.ReferenceProperty(
                                type="type",
                                value="value"
                            )
                        }
                    )]
                ),
                function="function",
                instance_arn="instanceArn",
                name="name",
                publish_status="publishStatus",
                trigger_event_source=connect.CfnRule.RuleTriggerEventSourceProperty(
                    event_source_name="eventSourceName",
            
                    # the properties below are optional
                    integration_association_arn="integrationAssociationArn"
                ),
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86228e744389fdc43748e3523fb391089cfd59a98fc3cac55a6aff07ca243441)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publish_status", value=publish_status, expected_type=type_hints["publish_status"])
            check_type(argname="argument trigger_event_source", value=trigger_event_source, expected_type=type_hints["trigger_event_source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "function": function,
            "instance_arn": instance_arn,
            "name": name,
            "publish_status": publish_status,
            "trigger_event_source": trigger_event_source,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def actions(self) -> typing.Union[CfnRule.ActionsProperty, _IResolvable_da3f097b]:
        '''A list of actions to be run when the rule is triggered.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-actions
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.Union[CfnRule.ActionsProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def function(self) -> builtins.str:
        '''The conditions of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-function
        '''
        result = self._values.get("function")
        assert result is not None, "Required property 'function' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publish_status(self) -> builtins.str:
        '''The publish status of the rule.

        *Allowed values* : ``DRAFT`` | ``PUBLISHED``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-publishstatus
        '''
        result = self._values.get("publish_status")
        assert result is not None, "Required property 'publish_status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_event_source(
        self,
    ) -> typing.Union[CfnRule.RuleTriggerEventSourceProperty, _IResolvable_da3f097b]:
        '''The event source to trigger the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-triggereventsource
        '''
        result = self._values.get("trigger_event_source")
        assert result is not None, "Required property 'trigger_event_source' is missing"
        return typing.cast(typing.Union[CfnRule.RuleTriggerEventSourceProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnSecurityKey(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnSecurityKey",
):
    '''A CloudFormation ``AWS::Connect::SecurityKey``.

    The security key for the instance.
    .. epigraph::

       Only two security keys are allowed per Amazon Connect instance.

    :cloudformationResource: AWS::Connect::SecurityKey
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_security_key = connect.CfnSecurityKey(self, "MyCfnSecurityKey",
            instance_id="instanceId",
            key="key"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_id: builtins.str,
        key: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Connect::SecurityKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param key: A valid security key in PEM format. *Minimum* : ``1`` *Maximum* : ``1024``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eec1c8c6bb56659ae557c882f85d373b6d643a7be8fd81d7dcb8e28a45f3d99e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSecurityKeyProps(instance_id=instance_id, key=key)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23c2e847b86bfc09195d252c47aea6a4403071968a249a46d9beca03100b5358)
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
            type_hints = typing.get_type_hints(_typecheckingstub__324830fb8488f0e9a9d62f4765f4824a32ded877f4766d2c34ea20eef4c4a506)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationId")
    def attr_association_id(self) -> builtins.str:
        '''An ``AssociationId`` is automatically generated when a storage config is associated with an instance.

        :cloudformationAttribute: AssociationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html#cfn-connect-securitykey-instanceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94821c1bb0576049b170e315ebfd7632b76a9c0cbe46f78111e960033839544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value)

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        '''A valid security key in PEM format.

        *Minimum* : ``1``

        *Maximum* : ``1024``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html#cfn-connect-securitykey-key
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae1fd3a5ae97acd56284508ad71af29fda88e415500606aed041d91bc4fe256)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnSecurityKeyProps",
    jsii_struct_bases=[],
    name_mapping={"instance_id": "instanceId", "key": "key"},
)
class CfnSecurityKeyProps:
    def __init__(self, *, instance_id: builtins.str, key: builtins.str) -> None:
        '''Properties for defining a ``CfnSecurityKey``.

        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param key: A valid security key in PEM format. *Minimum* : ``1`` *Maximum* : ``1024``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_security_key_props = connect.CfnSecurityKeyProps(
                instance_id="instanceId",
                key="key"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328945501d2d11db9e341c31e7f88f7eaea8695d95d7c557b2d470e619744f5e)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_id": instance_id,
            "key": key,
        }

    @builtins.property
    def instance_id(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html#cfn-connect-securitykey-instanceid
        '''
        result = self._values.get("instance_id")
        assert result is not None, "Required property 'instance_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''A valid security key in PEM format.

        *Minimum* : ``1``

        *Maximum* : ``1024``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html#cfn-connect-securitykey-key
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnTaskTemplate(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplate",
):
    '''A CloudFormation ``AWS::Connect::TaskTemplate``.

    Specifies a task template for a Amazon Connect instance.

    :cloudformationResource: AWS::Connect::TaskTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        # constraints: Any
        
        cfn_task_template = connect.CfnTaskTemplate(self, "MyCfnTaskTemplate",
            instance_arn="instanceArn",
        
            # the properties below are optional
            client_token="clientToken",
            constraints=constraints,
            contact_flow_arn="contactFlowArn",
            defaults=[connect.CfnTaskTemplate.DefaultFieldValueProperty(
                default_value="defaultValue",
                id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                    name="name"
                )
            )],
            description="description",
            fields=[connect.CfnTaskTemplate.FieldProperty(
                id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                    name="name"
                ),
                type="type",
        
                # the properties below are optional
                description="description",
                single_select_options=["singleSelectOptions"]
            )],
            name="name",
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        constraints: typing.Any = None,
        contact_flow_arn: typing.Optional[builtins.str] = None,
        defaults: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        description: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.FieldProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::TaskTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param client_token: A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.
        :param constraints: Constraints that are applicable to the fields listed. The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.
        :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template. ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .
        :param defaults: The default values for fields when a task is created by referencing this template.
        :param description: The description of the task template.
        :param fields: Fields that are part of the template. A template requires at least one field that has type ``Name`` .
        :param name: The name of the task template.
        :param status: The status of the task template.
        :param tags: The tags used to organize, track, or control access for this resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e55cf6106eb4919ab3d57f42477e52e40f628476ec3364c5bf5b40089c4746bc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTaskTemplateProps(
            instance_arn=instance_arn,
            client_token=client_token,
            constraints=constraints,
            contact_flow_arn=contact_flow_arn,
            defaults=defaults,
            description=description,
            fields=fields,
            name=name,
            status=status,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46cdd562656d586fa446b953fbbb0484300c8ed5d89c5bdf38b9ee2a994cd465)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a527f307b10d7d5baa2def0fbd31d398ac1b585ebbd7f3a9ba7d38d25d6829e7)
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
        '''The Amazon Resource Name (ARN) of the task template.

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
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(self) -> typing.Any:
        '''Constraints that are applicable to the fields listed.

        The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-constraints
        '''
        return typing.cast(typing.Any, jsii.get(self, "constraints"))

    @constraints.setter
    def constraints(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a898069ebffaab98fcbaee0053da25444060ad49ffcbfe6f0368eff95f5b200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "constraints", value)

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9540278151bed9f69d9f399c73f9a40e63e164ba823222a94733e2f75af92d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        '''A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-clienttoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientToken"))

    @client_token.setter
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bbd2064bc52aa0f530521bac3bae9c5f12656b7d845175af66583e2c4478aff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientToken", value)

    @builtins.property
    @jsii.member(jsii_name="contactFlowArn")
    def contact_flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template.

        ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-contactflowarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactFlowArn"))

    @contact_flow_arn.setter
    def contact_flow_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b4de1aedec1ca589ae0fc007dad4a4b2bd2d8d34fc17ea98b736695f7ce943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactFlowArn", value)

    @builtins.property
    @jsii.member(jsii_name="defaults")
    def defaults(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", _IResolvable_da3f097b]]]]:
        '''The default values for fields when a task is created by referencing this template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-defaults
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", _IResolvable_da3f097b]]]], jsii.get(self, "defaults"))

    @defaults.setter
    def defaults(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.DefaultFieldValueProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8763e4dc1a72bd2993b2130ce895c2796dd673f1913cef1346294ad7cdfb3f84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaults", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8feafa724c930c70f39fc9a4f2b3943981c6c26d175bdeef9ccc7a3dddb78a19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="fields")
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.FieldProperty", _IResolvable_da3f097b]]]]:
        '''Fields that are part of the template.

        A template requires at least one field that has type ``Name`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-fields
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.FieldProperty", _IResolvable_da3f097b]]]], jsii.get(self, "fields"))

    @fields.setter
    def fields(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.FieldProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445eadfb11465e7ab28af66fe2e12f9b6e2c4693cde068247ac72a5db1d0f8bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fields", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__536360af8980f014d8658d43741c6a3560607c1550e93deaec8025ead2486e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd486363bb52c46e2e9463e955a4ed4c9ffc963b921dce5f0a41124a306b893e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplate.ConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "invisible_fields": "invisibleFields",
            "read_only_fields": "readOnlyFields",
            "required_fields": "requiredFields",
        },
    )
    class ConstraintsProperty:
        def __init__(
            self,
            *,
            invisible_fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.InvisibleFieldInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            read_only_fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.ReadOnlyFieldInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            required_fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnTaskTemplate.RequiredFieldInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''
            :param invisible_fields: ``CfnTaskTemplate.ConstraintsProperty.InvisibleFields``.
            :param read_only_fields: ``CfnTaskTemplate.ConstraintsProperty.ReadOnlyFields``.
            :param required_fields: ``CfnTaskTemplate.ConstraintsProperty.RequiredFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                constraints_property = connect.CfnTaskTemplate.ConstraintsProperty(
                    invisible_fields=[connect.CfnTaskTemplate.InvisibleFieldInfoProperty(
                        id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                            name="name"
                        )
                    )],
                    read_only_fields=[connect.CfnTaskTemplate.ReadOnlyFieldInfoProperty(
                        id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                            name="name"
                        )
                    )],
                    required_fields=[connect.CfnTaskTemplate.RequiredFieldInfoProperty(
                        id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                            name="name"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8ebbf1d682cf676accdf4695ae9748eb71839e0255117fb6c27fe1391e7e7cc)
                check_type(argname="argument invisible_fields", value=invisible_fields, expected_type=type_hints["invisible_fields"])
                check_type(argname="argument read_only_fields", value=read_only_fields, expected_type=type_hints["read_only_fields"])
                check_type(argname="argument required_fields", value=required_fields, expected_type=type_hints["required_fields"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invisible_fields is not None:
                self._values["invisible_fields"] = invisible_fields
            if read_only_fields is not None:
                self._values["read_only_fields"] = read_only_fields
            if required_fields is not None:
                self._values["required_fields"] = required_fields

        @builtins.property
        def invisible_fields(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.InvisibleFieldInfoProperty", _IResolvable_da3f097b]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.InvisibleFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-invisiblefields
            '''
            result = self._values.get("invisible_fields")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.InvisibleFieldInfoProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def read_only_fields(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.ReadOnlyFieldInfoProperty", _IResolvable_da3f097b]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.ReadOnlyFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-readonlyfields
            '''
            result = self._values.get("read_only_fields")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.ReadOnlyFieldInfoProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def required_fields(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.RequiredFieldInfoProperty", _IResolvable_da3f097b]]]]:
            '''``CfnTaskTemplate.ConstraintsProperty.RequiredFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-requiredfields
            '''
            result = self._values.get("required_fields")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnTaskTemplate.RequiredFieldInfoProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplate.DefaultFieldValueProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue", "id": "id"},
    )
    class DefaultFieldValueProperty:
        def __init__(
            self,
            *,
            default_value: builtins.str,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        ) -> None:
            '''Describes a default field and its corresponding value.

            :param default_value: Default value for the field.
            :param id: Identifier of a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                default_field_value_property = connect.CfnTaskTemplate.DefaultFieldValueProperty(
                    default_value="defaultValue",
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7e2fbafd545cd91d979ca1524a9207544758d59734dcb28e71382c3e329623f)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "default_value": default_value,
                "id": id,
            }

        @builtins.property
        def default_value(self) -> builtins.str:
            '''Default value for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html#cfn-connect-tasktemplate-defaultfieldvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            assert result is not None, "Required property 'default_value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b]:
            '''Identifier of a field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html#cfn-connect-tasktemplate-defaultfieldvalue-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultFieldValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplate.FieldIdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class FieldIdentifierProperty:
        def __init__(self, *, name: builtins.str) -> None:
            '''The identifier of the task template field.

            :param name: The name of the task template field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-fieldidentifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                field_identifier_property = connect.CfnTaskTemplate.FieldIdentifierProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56cfea0cc2f28aaee625e6baeef27a54e4f0441cc4cb1502475522d9e1c29e4e)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the task template field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-fieldidentifier.html#cfn-connect-tasktemplate-fieldidentifier-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldIdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplate.FieldProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "type": "type",
            "description": "description",
            "single_select_options": "singleSelectOptions",
        },
    )
    class FieldProperty:
        def __init__(
            self,
            *,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
            type: builtins.str,
            description: typing.Optional[builtins.str] = None,
            single_select_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes a single task template field.

            :param id: The unique identifier for the field.
            :param type: Indicates the type of field. Following are the valid field types: ``NAME`` ``DESCRIPTION`` | ``SCHEDULED_TIME`` | ``QUICK_CONNECT`` | ``URL`` | ``NUMBER`` | ``TEXT`` | ``TEXT_AREA`` | ``DATE_TIME`` | ``BOOLEAN`` | ``SINGLE_SELECT`` | ``EMAIL``
            :param description: The description of the field.
            :param single_select_options: A list of options for a single select field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                field_property = connect.CfnTaskTemplate.FieldProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    ),
                    type="type",
                
                    # the properties below are optional
                    description="description",
                    single_select_options=["singleSelectOptions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d065a4a87520f8d3b9711b85f794e75a7c06a4b21d323c419a06f25c134bcaf)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument single_select_options", value=single_select_options, expected_type=type_hints["single_select_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
                "type": type,
            }
            if description is not None:
                self._values["description"] = description
            if single_select_options is not None:
                self._values["single_select_options"] = single_select_options

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b]:
            '''The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''Indicates the type of field.

            Following are the valid field types: ``NAME`` ``DESCRIPTION`` | ``SCHEDULED_TIME`` | ``QUICK_CONNECT`` | ``URL`` | ``NUMBER`` | ``TEXT`` | ``TEXT_AREA`` | ``DATE_TIME`` | ``BOOLEAN`` | ``SINGLE_SELECT`` | ``EMAIL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def single_select_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of options for a single select field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-singleselectoptions
            '''
            result = self._values.get("single_select_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplate.InvisibleFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class InvisibleFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        ) -> None:
            '''A field that is invisible to an agent.

            :param id: Identifier of the invisible field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-invisiblefieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                invisible_field_info_property = connect.CfnTaskTemplate.InvisibleFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d784f103d652729901e9c8a241de453a38a7535564f57cdea8070b407515bff)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b]:
            '''Identifier of the invisible field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-invisiblefieldinfo.html#cfn-connect-tasktemplate-invisiblefieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InvisibleFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplate.ReadOnlyFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class ReadOnlyFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        ) -> None:
            '''Indicates a field that is read-only to an agent.

            :param id: Identifier of the read-only field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-readonlyfieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                read_only_field_info_property = connect.CfnTaskTemplate.ReadOnlyFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f99f25935a58d0e69a63e663c70e9233ab3f544824e97f26f01abba7a02906b9)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b]:
            '''Identifier of the read-only field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-readonlyfieldinfo.html#cfn-connect-tasktemplate-readonlyfieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadOnlyFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplate.RequiredFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class RequiredFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Union[typing.Union["CfnTaskTemplate.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        ) -> None:
            '''Information about a required field.

            :param id: The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-requiredfieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                required_field_info_property = connect.CfnTaskTemplate.RequiredFieldInfoProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04c2c12eb06cef0a8d595c1a918e7fea99c1d59c019fe5a92fb573ffc0dd280d)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }

        @builtins.property
        def id(
            self,
        ) -> typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b]:
            '''The unique identifier for the field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-requiredfieldinfo.html#cfn-connect-tasktemplate-requiredfieldinfo-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(typing.Union["CfnTaskTemplate.FieldIdentifierProperty", _IResolvable_da3f097b], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequiredFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnTaskTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "client_token": "clientToken",
        "constraints": "constraints",
        "contact_flow_arn": "contactFlowArn",
        "defaults": "defaults",
        "description": "description",
        "fields": "fields",
        "name": "name",
        "status": "status",
        "tags": "tags",
    },
)
class CfnTaskTemplateProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        client_token: typing.Optional[builtins.str] = None,
        constraints: typing.Any = None,
        contact_flow_arn: typing.Optional[builtins.str] = None,
        defaults: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        description: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTaskTemplate``.

        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param client_token: A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.
        :param constraints: Constraints that are applicable to the fields listed. The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.
        :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template. ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .
        :param defaults: The default values for fields when a task is created by referencing this template.
        :param description: The description of the task template.
        :param fields: Fields that are part of the template. A template requires at least one field that has type ``Name`` .
        :param name: The name of the task template.
        :param status: The status of the task template.
        :param tags: The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            # constraints: Any
            
            cfn_task_template_props = connect.CfnTaskTemplateProps(
                instance_arn="instanceArn",
            
                # the properties below are optional
                client_token="clientToken",
                constraints=constraints,
                contact_flow_arn="contactFlowArn",
                defaults=[connect.CfnTaskTemplate.DefaultFieldValueProperty(
                    default_value="defaultValue",
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    )
                )],
                description="description",
                fields=[connect.CfnTaskTemplate.FieldProperty(
                    id=connect.CfnTaskTemplate.FieldIdentifierProperty(
                        name="name"
                    ),
                    type="type",
            
                    # the properties below are optional
                    description="description",
                    single_select_options=["singleSelectOptions"]
                )],
                name="name",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa2d0f88c266e5f2522dfd1af262def0d3061b82ebb529283e7afc28ef8b7bb)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
            check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
        }
        if client_token is not None:
            self._values["client_token"] = client_token
        if constraints is not None:
            self._values["constraints"] = constraints
        if contact_flow_arn is not None:
            self._values["contact_flow_arn"] = contact_flow_arn
        if defaults is not None:
            self._values["defaults"] = defaults
        if description is not None:
            self._values["description"] = description
        if fields is not None:
            self._values["fields"] = fields
        if name is not None:
            self._values["name"] = name
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def constraints(self) -> typing.Any:
        '''Constraints that are applicable to the fields listed.

        The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-constraints
        '''
        result = self._values.get("constraints")
        return typing.cast(typing.Any, result)

    @builtins.property
    def contact_flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template.

        ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-contactflowarn
        '''
        result = self._values.get("contact_flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def defaults(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, _IResolvable_da3f097b]]]]:
        '''The default values for fields when a task is created by referencing this template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-defaults
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTaskTemplate.FieldProperty, _IResolvable_da3f097b]]]]:
        '''Fields that are part of the template.

        A template requires at least one field that has type ``Name`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-fields
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTaskTemplate.FieldProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the task template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''The tags used to organize, track, or control access for this resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTaskTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnUser(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnUser",
):
    '''A CloudFormation ``AWS::Connect::User``.

    Specifies a user account for an Amazon Connect instance.

    For information about how to create user accounts using the Amazon Connect console, see `Add Users <https://docs.aws.amazon.com/connect/latest/adminguide/user-management.html>`_ in the *Amazon Connect Administrator Guide* .

    :cloudformationResource: AWS::Connect::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_user = connect.CfnUser(self, "MyCfnUser",
            instance_arn="instanceArn",
            phone_config=connect.CfnUser.UserPhoneConfigProperty(
                phone_type="phoneType",
        
                # the properties below are optional
                after_contact_work_time_limit=123,
                auto_accept=False,
                desk_phone_number="deskPhoneNumber"
            ),
            routing_profile_arn="routingProfileArn",
            security_profile_arns=["securityProfileArns"],
            username="username",
        
            # the properties below are optional
            directory_user_id="directoryUserId",
            hierarchy_group_arn="hierarchyGroupArn",
            identity_info=connect.CfnUser.UserIdentityInfoProperty(
                email="email",
                first_name="firstName",
                last_name="lastName",
                mobile="mobile",
                secondary_email="secondaryEmail"
            ),
            password="password",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        phone_config: typing.Union[typing.Union["CfnUser.UserPhoneConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        routing_profile_arn: builtins.str,
        security_profile_arns: typing.Sequence[builtins.str],
        username: builtins.str,
        directory_user_id: typing.Optional[builtins.str] = None,
        hierarchy_group_arn: typing.Optional[builtins.str] = None,
        identity_info: typing.Optional[typing.Union[typing.Union["CfnUser.UserIdentityInfoProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        password: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param phone_config: Information about the phone configuration for the user.
        :param routing_profile_arn: The Amazon Resource Name (ARN) of the user's routing profile.
        :param security_profile_arns: The Amazon Resource Name (ARN) of the user's security profile.
        :param username: The user name assigned to the user account.
        :param directory_user_id: The identifier of the user account in the directory used for identity management.
        :param hierarchy_group_arn: The Amazon Resource Name (ARN) of the user's hierarchy group.
        :param identity_info: Information about the user identity.
        :param password: The user's password.
        :param tags: The tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05b3c171d418de057737855a6729454df2138450ce49f656f47804ab286addf6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            instance_arn=instance_arn,
            phone_config=phone_config,
            routing_profile_arn=routing_profile_arn,
            security_profile_arns=security_profile_arns,
            username=username,
            directory_user_id=directory_user_id,
            hierarchy_group_arn=hierarchy_group_arn,
            identity_info=identity_info,
            password=password,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__868e9d73ebd6da6bc01f1a454c28b6ce77bb38b7722cc539dee5d631af8ab7a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8a7ab4c4c68abf101e561bdcaa3fccf82a51680bd75b6060ffd85b7b39cee53)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrUserArn")
    def attr_user_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user.

        :cloudformationAttribute: UserArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUserArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''The tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39c63e5bec20724a75b863eaf92b750aa2b43e84007f59f8101f109aded4b62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="phoneConfig")
    def phone_config(
        self,
    ) -> typing.Union["CfnUser.UserPhoneConfigProperty", _IResolvable_da3f097b]:
        '''Information about the phone configuration for the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-phoneconfig
        '''
        return typing.cast(typing.Union["CfnUser.UserPhoneConfigProperty", _IResolvable_da3f097b], jsii.get(self, "phoneConfig"))

    @phone_config.setter
    def phone_config(
        self,
        value: typing.Union["CfnUser.UserPhoneConfigProperty", _IResolvable_da3f097b],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f182c7afc61ebf14606fef1a70e2527bc3c149561eed985aa3c521e419741e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneConfig", value)

    @builtins.property
    @jsii.member(jsii_name="routingProfileArn")
    def routing_profile_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user's routing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-routingprofilearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "routingProfileArn"))

    @routing_profile_arn.setter
    def routing_profile_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ec4c5274e442b13ba6263b0a0699bceadb2d594cb4553cf3256514da5ba718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routingProfileArn", value)

    @builtins.property
    @jsii.member(jsii_name="securityProfileArns")
    def security_profile_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's security profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-securityprofilearns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityProfileArns"))

    @security_profile_arns.setter
    def security_profile_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59f37aa37416b07a1920b9fb28c6db10aa7091b532298ff46eddb3200c94afd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityProfileArns", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        '''The user name assigned to the user account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d3c1f0374209b5f9480c6b6571b89c26495747acd0440d47b7b3d3a95f28f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="directoryUserId")
    def directory_user_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the user account in the directory used for identity management.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-directoryuserid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "directoryUserId"))

    @directory_user_id.setter
    def directory_user_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f09389f8f59128c5950972d770de7815f263ca9cf4c25735591417ea4b72939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "directoryUserId", value)

    @builtins.property
    @jsii.member(jsii_name="hierarchyGroupArn")
    def hierarchy_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-hierarchygrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hierarchyGroupArn"))

    @hierarchy_group_arn.setter
    def hierarchy_group_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f855d98db219c907988e531c32926bf279294c9a15359f1bf876ac28120857f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hierarchyGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="identityInfo")
    def identity_info(
        self,
    ) -> typing.Optional[typing.Union["CfnUser.UserIdentityInfoProperty", _IResolvable_da3f097b]]:
        '''Information about the user identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-identityinfo
        '''
        return typing.cast(typing.Optional[typing.Union["CfnUser.UserIdentityInfoProperty", _IResolvable_da3f097b]], jsii.get(self, "identityInfo"))

    @identity_info.setter
    def identity_info(
        self,
        value: typing.Optional[typing.Union["CfnUser.UserIdentityInfoProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c0b838f75f47cfedc3da42d9842c603514aa585b6a8bdfd39ab14e8a57d5ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityInfo", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        '''The user's password.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-password
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97a2c5140ffd2e76246aa4b882ace6caee9e3c89751b5c2dc0c27a7d20caf26d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnUser.UserIdentityInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email": "email",
            "first_name": "firstName",
            "last_name": "lastName",
            "mobile": "mobile",
            "secondary_email": "secondaryEmail",
        },
    )
    class UserIdentityInfoProperty:
        def __init__(
            self,
            *,
            email: typing.Optional[builtins.str] = None,
            first_name: typing.Optional[builtins.str] = None,
            last_name: typing.Optional[builtins.str] = None,
            mobile: typing.Optional[builtins.str] = None,
            secondary_email: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the identity of a user.

            :param email: The email address. If you are using SAML for identity management and include this parameter, an error is returned.
            :param first_name: The first name. This is required if you are using Amazon Connect or SAML for identity management.
            :param last_name: The last name. This is required if you are using Amazon Connect or SAML for identity management.
            :param mobile: The user's mobile number.
            :param secondary_email: The user's secondary email address. If you provide a secondary email, the user receives email notifications -- other than password reset notifications -- to this email address instead of to their primary email address. *Pattern* : ``(?=^.{0,265}$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,63}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                user_identity_info_property = connect.CfnUser.UserIdentityInfoProperty(
                    email="email",
                    first_name="firstName",
                    last_name="lastName",
                    mobile="mobile",
                    secondary_email="secondaryEmail"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__675484167c56516574409f5f87a82bc61f2bd18d297494deb996e1e0a0c63262)
                check_type(argname="argument email", value=email, expected_type=type_hints["email"])
                check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
                check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
                check_type(argname="argument mobile", value=mobile, expected_type=type_hints["mobile"])
                check_type(argname="argument secondary_email", value=secondary_email, expected_type=type_hints["secondary_email"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email is not None:
                self._values["email"] = email
            if first_name is not None:
                self._values["first_name"] = first_name
            if last_name is not None:
                self._values["last_name"] = last_name
            if mobile is not None:
                self._values["mobile"] = mobile
            if secondary_email is not None:
                self._values["secondary_email"] = secondary_email

        @builtins.property
        def email(self) -> typing.Optional[builtins.str]:
            '''The email address.

            If you are using SAML for identity management and include this parameter, an error is returned.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-email
            '''
            result = self._values.get("email")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def first_name(self) -> typing.Optional[builtins.str]:
            '''The first name.

            This is required if you are using Amazon Connect or SAML for identity management.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-firstname
            '''
            result = self._values.get("first_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_name(self) -> typing.Optional[builtins.str]:
            '''The last name.

            This is required if you are using Amazon Connect or SAML for identity management.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-lastname
            '''
            result = self._values.get("last_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mobile(self) -> typing.Optional[builtins.str]:
            '''The user's mobile number.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-mobile
            '''
            result = self._values.get("mobile")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secondary_email(self) -> typing.Optional[builtins.str]:
            '''The user's secondary email address.

            If you provide a secondary email, the user receives email notifications -- other than password reset notifications -- to this email address instead of to their primary email address.

            *Pattern* : ``(?=^.{0,265}$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,63}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-secondaryemail
            '''
            result = self._values.get("secondary_email")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserIdentityInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_connect.CfnUser.UserPhoneConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "phone_type": "phoneType",
            "after_contact_work_time_limit": "afterContactWorkTimeLimit",
            "auto_accept": "autoAccept",
            "desk_phone_number": "deskPhoneNumber",
        },
    )
    class UserPhoneConfigProperty:
        def __init__(
            self,
            *,
            phone_type: builtins.str,
            after_contact_work_time_limit: typing.Optional[jsii.Number] = None,
            auto_accept: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            desk_phone_number: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the phone configuration settings for a user.

            :param phone_type: The phone type.
            :param after_contact_work_time_limit: The After Call Work (ACW) timeout setting, in seconds. .. epigraph:: When returned by a ``SearchUsers`` call, ``AfterContactWorkTimeLimit`` is returned in milliseconds.
            :param auto_accept: The Auto accept setting.
            :param desk_phone_number: The phone number for the user's desk phone.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_connect as connect
                
                user_phone_config_property = connect.CfnUser.UserPhoneConfigProperty(
                    phone_type="phoneType",
                
                    # the properties below are optional
                    after_contact_work_time_limit=123,
                    auto_accept=False,
                    desk_phone_number="deskPhoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e774e2d87fa8144ee9994624937d62ce4393d565b8e6982f7d2e1c5bf0c9ca67)
                check_type(argname="argument phone_type", value=phone_type, expected_type=type_hints["phone_type"])
                check_type(argname="argument after_contact_work_time_limit", value=after_contact_work_time_limit, expected_type=type_hints["after_contact_work_time_limit"])
                check_type(argname="argument auto_accept", value=auto_accept, expected_type=type_hints["auto_accept"])
                check_type(argname="argument desk_phone_number", value=desk_phone_number, expected_type=type_hints["desk_phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "phone_type": phone_type,
            }
            if after_contact_work_time_limit is not None:
                self._values["after_contact_work_time_limit"] = after_contact_work_time_limit
            if auto_accept is not None:
                self._values["auto_accept"] = auto_accept
            if desk_phone_number is not None:
                self._values["desk_phone_number"] = desk_phone_number

        @builtins.property
        def phone_type(self) -> builtins.str:
            '''The phone type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-phonetype
            '''
            result = self._values.get("phone_type")
            assert result is not None, "Required property 'phone_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def after_contact_work_time_limit(self) -> typing.Optional[jsii.Number]:
            '''The After Call Work (ACW) timeout setting, in seconds.

            .. epigraph::

               When returned by a ``SearchUsers`` call, ``AfterContactWorkTimeLimit`` is returned in milliseconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-aftercontactworktimelimit
            '''
            result = self._values.get("after_contact_work_time_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def auto_accept(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''The Auto accept setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-autoaccept
            '''
            result = self._values.get("auto_accept")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def desk_phone_number(self) -> typing.Optional[builtins.str]:
            '''The phone number for the user's desk phone.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-deskphonenumber
            '''
            result = self._values.get("desk_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPhoneConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_c2943556)
class CfnUserHierarchyGroup(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_connect.CfnUserHierarchyGroup",
):
    '''A CloudFormation ``AWS::Connect::UserHierarchyGroup``.

    Specifies a new user hierarchy group.

    :cloudformationResource: AWS::Connect::UserHierarchyGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_connect as connect
        
        cfn_user_hierarchy_group = connect.CfnUserHierarchyGroup(self, "MyCfnUserHierarchyGroup",
            instance_arn="instanceArn",
            name="name",
        
            # the properties below are optional
            parent_group_arn="parentGroupArn"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        parent_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Connect::UserHierarchyGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_arn: The Amazon Resource Name (ARN) of the user hierarchy group.
        :param name: The name of the user hierarchy group.
        :param parent_group_arn: The Amazon Resource Name (ARN) of the parent group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee71292692b3a4ed0bb1ecb030ac42cd8de9fe7fd30c25bca5b2f1eaaa6bb48)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserHierarchyGroupProps(
            instance_arn=instance_arn, name=name, parent_group_arn=parent_group_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__752f8fce7f90c25285d3743bf24f50aec111d37047ee0c4af63a38e966735a03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac67c3ecd95bbbc55bc130d457e245f00decbc275854bb8b407db1329f860025)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrUserHierarchyGroupArn")
    def attr_user_hierarchy_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) for the user hierarchy group.

        :cloudformationAttribute: UserHierarchyGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUserHierarchyGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-instancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @instance_arn.setter
    def instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8fb77dfbead9199eb5f47ecaa078f50ea02c5ce873fd226cd349a59b527fb3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the user hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d0815b3361eabab5affbe2f0e2d26f64eecd0bba911c06147e98f374796565c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="parentGroupArn")
    def parent_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the parent group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-parentgrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentGroupArn"))

    @parent_group_arn.setter
    def parent_group_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2be8f8330a2a7250df106f290a4e8ddeda8715a95a83b481ae76d8ac2d2d8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentGroupArn", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnUserHierarchyGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "name": "name",
        "parent_group_arn": "parentGroupArn",
    },
)
class CfnUserHierarchyGroupProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        name: builtins.str,
        parent_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnUserHierarchyGroup``.

        :param instance_arn: The Amazon Resource Name (ARN) of the user hierarchy group.
        :param name: The name of the user hierarchy group.
        :param parent_group_arn: The Amazon Resource Name (ARN) of the parent group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_user_hierarchy_group_props = connect.CfnUserHierarchyGroupProps(
                instance_arn="instanceArn",
                name="name",
            
                # the properties below are optional
                parent_group_arn="parentGroupArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f9a797f445ffc1deaff140a69a030bdb25f3fa135ef233a56621cf7d99867c)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_group_arn", value=parent_group_arn, expected_type=type_hints["parent_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "name": name,
        }
        if parent_group_arn is not None:
            self._values["parent_group_arn"] = parent_group_arn

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the user hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parent_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the parent group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-parentgrouparn
        '''
        result = self._values.get("parent_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserHierarchyGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_connect.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "phone_config": "phoneConfig",
        "routing_profile_arn": "routingProfileArn",
        "security_profile_arns": "securityProfileArns",
        "username": "username",
        "directory_user_id": "directoryUserId",
        "hierarchy_group_arn": "hierarchyGroupArn",
        "identity_info": "identityInfo",
        "password": "password",
        "tags": "tags",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        instance_arn: builtins.str,
        phone_config: typing.Union[typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        routing_profile_arn: builtins.str,
        security_profile_arns: typing.Sequence[builtins.str],
        username: builtins.str,
        directory_user_id: typing.Optional[builtins.str] = None,
        hierarchy_group_arn: typing.Optional[builtins.str] = None,
        identity_info: typing.Optional[typing.Union[typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        password: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnUser``.

        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param phone_config: Information about the phone configuration for the user.
        :param routing_profile_arn: The Amazon Resource Name (ARN) of the user's routing profile.
        :param security_profile_arns: The Amazon Resource Name (ARN) of the user's security profile.
        :param username: The user name assigned to the user account.
        :param directory_user_id: The identifier of the user account in the directory used for identity management.
        :param hierarchy_group_arn: The Amazon Resource Name (ARN) of the user's hierarchy group.
        :param identity_info: Information about the user identity.
        :param password: The user's password.
        :param tags: The tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_connect as connect
            
            cfn_user_props = connect.CfnUserProps(
                instance_arn="instanceArn",
                phone_config=connect.CfnUser.UserPhoneConfigProperty(
                    phone_type="phoneType",
            
                    # the properties below are optional
                    after_contact_work_time_limit=123,
                    auto_accept=False,
                    desk_phone_number="deskPhoneNumber"
                ),
                routing_profile_arn="routingProfileArn",
                security_profile_arns=["securityProfileArns"],
                username="username",
            
                # the properties below are optional
                directory_user_id="directoryUserId",
                hierarchy_group_arn="hierarchyGroupArn",
                identity_info=connect.CfnUser.UserIdentityInfoProperty(
                    email="email",
                    first_name="firstName",
                    last_name="lastName",
                    mobile="mobile",
                    secondary_email="secondaryEmail"
                ),
                password="password",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494987ef0f9b905c50c1efbd53f96fb396b7f25b5354dfbb4027a32dbf61b9b1)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument phone_config", value=phone_config, expected_type=type_hints["phone_config"])
            check_type(argname="argument routing_profile_arn", value=routing_profile_arn, expected_type=type_hints["routing_profile_arn"])
            check_type(argname="argument security_profile_arns", value=security_profile_arns, expected_type=type_hints["security_profile_arns"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument directory_user_id", value=directory_user_id, expected_type=type_hints["directory_user_id"])
            check_type(argname="argument hierarchy_group_arn", value=hierarchy_group_arn, expected_type=type_hints["hierarchy_group_arn"])
            check_type(argname="argument identity_info", value=identity_info, expected_type=type_hints["identity_info"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_arn": instance_arn,
            "phone_config": phone_config,
            "routing_profile_arn": routing_profile_arn,
            "security_profile_arns": security_profile_arns,
            "username": username,
        }
        if directory_user_id is not None:
            self._values["directory_user_id"] = directory_user_id
        if hierarchy_group_arn is not None:
            self._values["hierarchy_group_arn"] = hierarchy_group_arn
        if identity_info is not None:
            self._values["identity_info"] = identity_info
        if password is not None:
            self._values["password"] = password
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-instancearn
        '''
        result = self._values.get("instance_arn")
        assert result is not None, "Required property 'instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def phone_config(
        self,
    ) -> typing.Union[CfnUser.UserPhoneConfigProperty, _IResolvable_da3f097b]:
        '''Information about the phone configuration for the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-phoneconfig
        '''
        result = self._values.get("phone_config")
        assert result is not None, "Required property 'phone_config' is missing"
        return typing.cast(typing.Union[CfnUser.UserPhoneConfigProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def routing_profile_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the user's routing profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-routingprofilearn
        '''
        result = self._values.get("routing_profile_arn")
        assert result is not None, "Required property 'routing_profile_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_profile_arns(self) -> typing.List[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's security profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-securityprofilearns
        '''
        result = self._values.get("security_profile_arns")
        assert result is not None, "Required property 'security_profile_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The user name assigned to the user account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-username
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def directory_user_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the user account in the directory used for identity management.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-directoryuserid
        '''
        result = self._values.get("directory_user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hierarchy_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's hierarchy group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-hierarchygrouparn
        '''
        result = self._values.get("hierarchy_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_info(
        self,
    ) -> typing.Optional[typing.Union[CfnUser.UserIdentityInfoProperty, _IResolvable_da3f097b]]:
        '''Information about the user identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-identityinfo
        '''
        result = self._values.get("identity_info")
        return typing.cast(typing.Optional[typing.Union[CfnUser.UserIdentityInfoProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The user's password.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''The tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApprovedOrigin",
    "CfnApprovedOriginProps",
    "CfnContactFlow",
    "CfnContactFlowModule",
    "CfnContactFlowModuleProps",
    "CfnContactFlowProps",
    "CfnHoursOfOperation",
    "CfnHoursOfOperationProps",
    "CfnInstance",
    "CfnInstanceProps",
    "CfnInstanceStorageConfig",
    "CfnInstanceStorageConfigProps",
    "CfnIntegrationAssociation",
    "CfnIntegrationAssociationProps",
    "CfnPhoneNumber",
    "CfnPhoneNumberProps",
    "CfnQuickConnect",
    "CfnQuickConnectProps",
    "CfnRule",
    "CfnRuleProps",
    "CfnSecurityKey",
    "CfnSecurityKeyProps",
    "CfnTaskTemplate",
    "CfnTaskTemplateProps",
    "CfnUser",
    "CfnUserHierarchyGroup",
    "CfnUserHierarchyGroupProps",
    "CfnUserProps",
]

publication.publish()

def _typecheckingstub__44955422cb4c00b338f45e52a0d4136fdcdb94c8e433595b636f468d589e514a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_id: builtins.str,
    origin: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b611bd9c5a92c253c2e2b0cba97b9f73bad0cfc8494953acb694fda143bba2(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc2ef7b8d5a06b007fe66bb9f5b0208e869ed47a6e5af0d6bf354f4df2d4d6c8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd219e5b157d40fbc4254297a9308245796269c824a72c0b9db3bad7013261c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49fb9b02cf4a1b22d6433eac9cb35377d1877512b477dbf9c030fec47fb54f75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437fb8bad3e7665288233ec7ee3b4db6669d85ab53efddb888b5d729979a4e2f(
    *,
    instance_id: builtins.str,
    origin: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bacec198fd7006a7e922c6b62694383eb7200d23c3f8da491f520191bdc8353f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca14ea5542ff9acc3dc06746c7580c88c1e0b75d66bf0ac0a8cd785404cc173(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b3abb60d405603981215ec7d659c3d8939dbf9b5de879c8d56dfd0631f9d5b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a517102f202efaced50f937df38d5374d2d8ae33c5659296852d677cbe73e2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f6a7aacca6b49f3791bf907484b7af427677a1079ea79db9a45489b963b9d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f576a62faffae972ec30039ac3019bddb9b613e8dd2dce2b52723ba8a64dbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213719edbc55495f331c0d1f51b7ab8a359f2c5cc563f3fa97077760121c6aa9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4573df3b75ab7b2ea3d0cba32ff3c515f11f6cbec43c0885d9ee30d25616a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b6f72cf71dca93b2b2baae1d002d73d66de8e16bec7709efdb45c4bb811336(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008a6ee0ce6447d7f5f7c62774a959e253bc4a69cef26848e6d3f74cf2381193(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82176173dbe238b7a4715d8a94792d3696ada52a4372f823ab10f4c590c6193f(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3e317a83e30b22f766c5d65c8451e4d9e5ffcd6510573aa22d0063860e7b99(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1701812aa93a58317265edab1cd66b5a843fc9845a1aed0b81f83c4f738b5b0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b9231af4bcfc40233b3b8fbbd6acd02fe21a59b2f962738d2ce93d6ffa7fa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e18e7239d9aefba3afcb9b93bf7f3ec9f6e4f173d51f91e93f5543efe25658a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c1841af03e44ad4a3c471a24f30aa57c457ec766515db087b0745fb9a6a68d9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25db523d57560a8813a16f507ae8c09c28625a53b6a24b5744ca978282ff51a3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f0f2ba3fd7010e7e0bb6aaa71b591e31e6d4c4ad736e9c4e08be6f11de0102(
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0555b19a226cc1a8bd054951921ffd23e0c635fe29a3d69a330d8262710a7d8(
    *,
    content: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9a7b2f06b8b2d053fcfa26018be9202b48193f9ffb7fc1d9518391cd9b5afe(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    config: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]],
    instance_arn: builtins.str,
    name: builtins.str,
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1892c64bc10c89577bb1c7c1cbafe5e7256d59298765e4d13fa8bc792aff27cb(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1be399a62772419844397558be775450dd4c2dc740a8864f61b03b483610073(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390986701d928ed3f41379b144a434426999d52505eaf487d066a0865f299c42(
    value: typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, _IResolvable_da3f097b]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff371c180e62831feb4bd92859ad779161086fed20f40c5fcaec70aedbd1d950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314c5f51a2268bd65be9864b4a46c3d2279936b4a2675b16522bc736ba5fb373(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__442605da8563582cbafb26c421377e100eaf1791f47f7f84657994d9d7347b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224611189f5992474af63688324a9a850ba31b7aad01b0eaae5a8fd63f4ea172(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ef26f457a53e548698c50361c4e334e5f633638af5ae2b9230dccc5fd5c1dd3(
    *,
    day: builtins.str,
    end_time: typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationTimeSliceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    start_time: typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationTimeSliceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5c5b128d189787db53fa22c88668d84b3efd31f5b54320dcda0838372db008(
    *,
    hours: jsii.Number,
    minutes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cef12b59765322de54d22fe6de568f262a635899fc46cbe6a5f5a97b848467(
    *,
    config: typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnHoursOfOperation.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]],
    instance_arn: builtins.str,
    name: builtins.str,
    time_zone: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f291b6bb708a40e1a35dc95de4a38d5f9d8117683bed082183bd387f4848fef9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    attributes: typing.Union[typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    identity_management_type: builtins.str,
    directory_id: typing.Optional[builtins.str] = None,
    instance_alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e4dee5bd55d2c2f964814ca3e2747955315fb5bc8f0a80efc7cbad1ed39cbdc(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__023c45bbafb1abf38373b2528d8531c6e7048604e4fabca7c6a4684feb4413d6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b81c5f62ba93ec0d3e48188cccf781d5861eac87dc5aa4a4038e6d2176145e(
    value: typing.Union[CfnInstance.AttributesProperty, _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1723398c06ebefeb9e3f4e11e08b8929e713cae56a36abf11fae424fa1c0cea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a002f21d50b37114edc464bd9143a0e1abc1702e5ff455644179b2ac7acbfbdd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225190f7b3c1545c436fe6b710e05a3a5b7d256f1ece21dcb8ad6ba49cf45c90(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40aedafdc4ea4fb2b717cc5c6ef0e2db4eb7490be99c35b78dc90f18526d068(
    *,
    inbound_calls: typing.Union[builtins.bool, _IResolvable_da3f097b],
    outbound_calls: typing.Union[builtins.bool, _IResolvable_da3f097b],
    auto_resolve_best_voices: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    contactflow_logs: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    contact_lens: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    early_media: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    use_custom_tts_voices: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67fdacfbc8ac4206df45637f43843e90e644b42387d3af9173f714ef095953b4(
    *,
    attributes: typing.Union[typing.Union[CfnInstance.AttributesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    identity_management_type: builtins.str,
    directory_id: typing.Optional[builtins.str] = None,
    instance_alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c8e9e3ad538fac1acafd66e46e4e7a4f3893f93a8c6bb42ba1525f14973522(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    resource_type: builtins.str,
    storage_type: builtins.str,
    kinesis_firehose_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    kinesis_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    kinesis_video_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    s3_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047b8a3f497a61ecbf349954496260297e95ce2a4561a42f301589ab2cee4b2a(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e208c0e80a04bb7be2d96f8d6f17f40b00cfff9d7822b7f4ecb07751859062(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb171c6a585c549bf0fad4d15990fc6ee838655cd803c3fd46739aba98a2a1d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae5f517bee9d34ee21bd11e2d5f0247d46092ae2f3deb37dcf2893b2f798f14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e576862f1e107b0e3735b4d183525ba16593162db67ddb46e8ca789a1af5850(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c82cfbbde3b0d4520ea2bf1db2e6d9a0262e0c56473bd9769a65fc32f975a8(
    value: typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a364c6eb62a091d24f417f496838aa90b1e63e040b4dad6e12dd8288568f014(
    value: typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43628a93b9adb2e5341b48d5f226f90e92dc0574e63f1fabc8616c9c49b35ef(
    value: typing.Optional[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e076b90fc0b5155e89233d8d5afcf24aea56049cea6a67a56da67867dd963c3(
    value: typing.Optional[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc46269845c7184ad0679658c798d342839ec1fbf50541709790ef0d801dd540(
    *,
    encryption_type: builtins.str,
    key_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a572a34b9441880677e439712bb7b9dbc0a79fc55daf5839857f2041774e7c99(
    *,
    firehose_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198e237e2c62ec06cc78609686ceeb43aaecd21ba79e09b267cdd8be2c3743a1(
    *,
    stream_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52c9485c197abc64e1dbe93a9ffbdf11fda8b3df13bc67381180643da843a5b8(
    *,
    prefix: builtins.str,
    retention_period_hours: jsii.Number,
    encryption_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7296a98085d62b3fe09acddef52fca10fedbaae666bc4512bfa543fd1ddcccab(
    *,
    bucket_name: builtins.str,
    bucket_prefix: builtins.str,
    encryption_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__220fe9c269db6e3bcb651e492fae1b71e17d6b254dfd6b60c71dc0cda259419b(
    *,
    instance_arn: builtins.str,
    resource_type: builtins.str,
    storage_type: builtins.str,
    kinesis_firehose_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    kinesis_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    kinesis_video_stream_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    s3_config: typing.Optional[typing.Union[typing.Union[CfnInstanceStorageConfig.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0623057688349069456f9eae4995faa9cd189f98024c1f76262706d5734b311e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_id: builtins.str,
    integration_arn: builtins.str,
    integration_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb2bfc240169367a312e392a1f57215cf8d8c8079407283c69a1ce7b13f7f09(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d2595ec7f89aa2a00d106ed9c54cd5cee3b8f448483b246b960847d1347cd0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7925af3a6409e56b03183e28600488914d5fe9b4e7accd90ff869ac4ba2618e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc0c68d9b0ec88ff8644cffd658aa26a913dcd92e1fc6ea4af9e71598d78538(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb9a11163321e5e540a87e2baf965475a45e960cf9aa4a424acc86dcad3feef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe194aedf3230ea702915cbc89ea1228fbcd7507b4352cd6ca6f2c8b3d412d21(
    *,
    instance_id: builtins.str,
    integration_arn: builtins.str,
    integration_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ec70d84fd2bda163d290722acbb6feca633b4ee134732d8b720c0b96701cb7b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    country_code: builtins.str,
    target_arn: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccee69f4a06306d444592cd5cf9588d2bb31a952c87c3487ff8ad82fc8c8cf94(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b523ee72d695f2e00f7a42b04d5ef172e9c4c9f850d546d7d54f31058efcbf64(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8049a6bcb60451cb780647e8cad2360b140018c95db8d6b0e339ed0524e56f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aee914dbb9c13734690f391827e9cd37ca89f521141f3de61e900bfbbd902752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0868299e1426aef01fcea4843c3c28737fa3b7614cce2aa77e978bfa8976f8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9949958c848f257cc25ceae67fe2e9cee4b1972f09d90ea4ed667dac758be40e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572d2dd079d87f4a7578acddb0bc7dbcca5ec4c2fecd370ff662ac4d429ea5b5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b6cbf832a5409fafc1645b1b1a1567ef5e6d173dfed6d56cae08b977fd4b95(
    *,
    country_code: builtins.str,
    target_arn: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44121049328c061f99076678805110a34e47bc31097d43b030f388eca53234e9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    quick_connect_config: typing.Union[typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac17b042f7cf408478c49ac00f219efb0ede78bbe556a5ec55b66c5025bf6198(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a25858c0bb7501da609f58db5989e1c4593c28fa68b47618b9ed5533379f506(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4d649c9007065ac09a0caa875fd618788a773aab62e76f33a48ae54d5284ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d7d088ec5e9e804f349ff7c9f716ab0de501abdb1561144e8cba5e16ae351d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf95cf02ae05236caa122a481ca15ec758f528b67ca083a27c0d64c2c3c7f4d2(
    value: typing.Union[CfnQuickConnect.QuickConnectConfigProperty, _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f4633c9c2a7464e4f507d168aa19eee91126aef113fdfcb12ab23fe37d443cc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c594b9d59e37b885f89d8bea8817c96760d7982a4ec30c3cec4c9d6620f0690(
    *,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7632a33b2bc55f259222d21532508c7c3f8f6ef77e1098e16a144fdb3514616(
    *,
    contact_flow_arn: builtins.str,
    queue_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5ffbc184bff7cbc8cc0dd5bf20c11b8676ca18d518a33d4b7ae2d76891f05d(
    *,
    quick_connect_type: builtins.str,
    phone_config: typing.Optional[typing.Union[typing.Union[CfnQuickConnect.PhoneNumberQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    queue_config: typing.Optional[typing.Union[typing.Union[CfnQuickConnect.QueueQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    user_config: typing.Optional[typing.Union[typing.Union[CfnQuickConnect.UserQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7730396d4c494428f6ddd636283d9d5c17ba3fbc6013f1c545a8788d686e0fc1(
    *,
    contact_flow_arn: builtins.str,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d4ffda8775de853a0509cc15bc43b59e37fc8f6d1d2c110c1202c4192841fbd(
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    quick_connect_config: typing.Union[typing.Union[CfnQuickConnect.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999d5f7971fc0ea0f693e0f9a61faf62317d493403a6d249ca1db6bc52d61e6f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    actions: typing.Union[typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    function: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    publish_status: builtins.str,
    trigger_event_source: typing.Union[typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa852f8205e0acaca3e6361c61c512ea090fe504a708495d2b5bdadc81b30809(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8f82a813645b192cb4d0a6df6a35e9ffe4fe072375390e4d29ebb42555752ad(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bdf3e9c3a73f02992b32c967f3457b7eeade7d3dfa554da9d661f54924ad9a2(
    value: typing.Union[CfnRule.ActionsProperty, _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85af4feedf296e30da787ccf9bc61e248b9a97c21a29fd8fbf38621d5d654fdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec5da44206c20fbb184f7443ea185123d28ab75d447650604f654e3fe336b233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6699a016b8fc3ffcc40b2227c32c82c77dcef5f7a74d28bea7e181707fb33bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464a87f0223cf9d2bd4ca32eeb79cbb74d44d9fead6bf2a81a1db65870834bf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a752b13b9a86d9caa3ed642e2b19a8ac6db9d24515c76f729c8ad704d664388(
    value: typing.Union[CfnRule.RuleTriggerEventSourceProperty, _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef20a75dbfc13161d3fff13ec1c4969adde44c34f62addd27e480514ce92395(
    *,
    assign_contact_category_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _IResolvable_da3f097b]] = None,
    event_bridge_actions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnRule.EventBridgeActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    send_notification_actions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnRule.SendNotificationActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    task_actions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnRule.TaskActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037f7c36eff1515bc6e2d8e67f9b2bac8beade9773e2103dd3b8b5ca5405e447(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d577395a2866fe40fdf75bbcc932da0701cd7985bbb4de4e2ef65243ba9d387(
    *,
    user_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_tags: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a9deeefd8de7f6bdabd5dee0827f879a4b6911d8516976e0492403b3a4724a(
    *,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16bc3686835833422d3f82ede42c0b9acf288c30c14f9b3b761db32339bbd1f5(
    *,
    event_source_name: builtins.str,
    integration_association_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199075d61da7aee6c24aad33a7023d6a679853ff216c051fe322418490e5e9e4(
    *,
    content: builtins.str,
    content_type: builtins.str,
    delivery_method: builtins.str,
    recipient: typing.Union[typing.Union[CfnRule.NotificationRecipientTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d4ac91ef6fb71bdda5474ed1cbe12228c8f5caa3aec2778c4c6642b1ab6b3b(
    *,
    contact_flow_arn: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    references: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnRule.ReferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86228e744389fdc43748e3523fb391089cfd59a98fc3cac55a6aff07ca243441(
    *,
    actions: typing.Union[typing.Union[CfnRule.ActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    function: builtins.str,
    instance_arn: builtins.str,
    name: builtins.str,
    publish_status: builtins.str,
    trigger_event_source: typing.Union[typing.Union[CfnRule.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec1c8c6bb56659ae557c882f85d373b6d643a7be8fd81d7dcb8e28a45f3d99e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_id: builtins.str,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c2e847b86bfc09195d252c47aea6a4403071968a249a46d9beca03100b5358(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324830fb8488f0e9a9d62f4765f4824a32ded877f4766d2c34ea20eef4c4a506(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94821c1bb0576049b170e315ebfd7632b76a9c0cbe46f78111e960033839544(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae1fd3a5ae97acd56284508ad71af29fda88e415500606aed041d91bc4fe256(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328945501d2d11db9e341c31e7f88f7eaea8695d95d7c557b2d470e619744f5e(
    *,
    instance_id: builtins.str,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e55cf6106eb4919ab3d57f42477e52e40f628476ec3364c5bf5b40089c4746bc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    constraints: typing.Any = None,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    defaults: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    description: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46cdd562656d586fa446b953fbbb0484300c8ed5d89c5bdf38b9ee2a994cd465(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a527f307b10d7d5baa2def0fbd31d398ac1b585ebbd7f3a9ba7d38d25d6829e7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a898069ebffaab98fcbaee0053da25444060ad49ffcbfe6f0368eff95f5b200(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9540278151bed9f69d9f399c73f9a40e63e164ba823222a94733e2f75af92d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bbd2064bc52aa0f530521bac3bae9c5f12656b7d845175af66583e2c4478aff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b4de1aedec1ca589ae0fc007dad4a4b2bd2d8d34fc17ea98b736695f7ce943(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8763e4dc1a72bd2993b2130ce895c2796dd673f1913cef1346294ad7cdfb3f84(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, _IResolvable_da3f097b]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8feafa724c930c70f39fc9a4f2b3943981c6c26d175bdeef9ccc7a3dddb78a19(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445eadfb11465e7ab28af66fe2e12f9b6e2c4693cde068247ac72a5db1d0f8bf(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnTaskTemplate.FieldProperty, _IResolvable_da3f097b]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__536360af8980f014d8658d43741c6a3560607c1550e93deaec8025ead2486e33(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd486363bb52c46e2e9463e955a4ed4c9ffc963b921dce5f0a41124a306b893e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ebbf1d682cf676accdf4695ae9748eb71839e0255117fb6c27fe1391e7e7cc(
    *,
    invisible_fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.InvisibleFieldInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    read_only_fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.ReadOnlyFieldInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    required_fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.RequiredFieldInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e2fbafd545cd91d979ca1524a9207544758d59734dcb28e71382c3e329623f(
    *,
    default_value: builtins.str,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56cfea0cc2f28aaee625e6baeef27a54e4f0441cc4cb1502475522d9e1c29e4e(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d065a4a87520f8d3b9711b85f794e75a7c06a4b21d323c419a06f25c134bcaf(
    *,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    single_select_options: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d784f103d652729901e9c8a241de453a38a7535564f57cdea8070b407515bff(
    *,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99f25935a58d0e69a63e663c70e9233ab3f544824e97f26f01abba7a02906b9(
    *,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c2c12eb06cef0a8d595c1a918e7fea99c1d59c019fe5a92fb573ffc0dd280d(
    *,
    id: typing.Union[typing.Union[CfnTaskTemplate.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa2d0f88c266e5f2522dfd1af262def0d3061b82ebb529283e7afc28ef8b7bb(
    *,
    instance_arn: builtins.str,
    client_token: typing.Optional[builtins.str] = None,
    constraints: typing.Any = None,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    defaults: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    description: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnTaskTemplate.FieldProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05b3c171d418de057737855a6729454df2138450ce49f656f47804ab286addf6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    phone_config: typing.Union[typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    routing_profile_arn: builtins.str,
    security_profile_arns: typing.Sequence[builtins.str],
    username: builtins.str,
    directory_user_id: typing.Optional[builtins.str] = None,
    hierarchy_group_arn: typing.Optional[builtins.str] = None,
    identity_info: typing.Optional[typing.Union[typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    password: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868e9d73ebd6da6bc01f1a454c28b6ce77bb38b7722cc539dee5d631af8ab7a1(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a7ab4c4c68abf101e561bdcaa3fccf82a51680bd75b6060ffd85b7b39cee53(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39c63e5bec20724a75b863eaf92b750aa2b43e84007f59f8101f109aded4b62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f182c7afc61ebf14606fef1a70e2527bc3c149561eed985aa3c521e419741e73(
    value: typing.Union[CfnUser.UserPhoneConfigProperty, _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ec4c5274e442b13ba6263b0a0699bceadb2d594cb4553cf3256514da5ba718(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59f37aa37416b07a1920b9fb28c6db10aa7091b532298ff46eddb3200c94afd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d3c1f0374209b5f9480c6b6571b89c26495747acd0440d47b7b3d3a95f28f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f09389f8f59128c5950972d770de7815f263ca9cf4c25735591417ea4b72939(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f855d98db219c907988e531c32926bf279294c9a15359f1bf876ac28120857f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c0b838f75f47cfedc3da42d9842c603514aa585b6a8bdfd39ab14e8a57d5ec(
    value: typing.Optional[typing.Union[CfnUser.UserIdentityInfoProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a2c5140ffd2e76246aa4b882ace6caee9e3c89751b5c2dc0c27a7d20caf26d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675484167c56516574409f5f87a82bc61f2bd18d297494deb996e1e0a0c63262(
    *,
    email: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mobile: typing.Optional[builtins.str] = None,
    secondary_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e774e2d87fa8144ee9994624937d62ce4393d565b8e6982f7d2e1c5bf0c9ca67(
    *,
    phone_type: builtins.str,
    after_contact_work_time_limit: typing.Optional[jsii.Number] = None,
    auto_accept: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    desk_phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee71292692b3a4ed0bb1ecb030ac42cd8de9fe7fd30c25bca5b2f1eaaa6bb48(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    parent_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__752f8fce7f90c25285d3743bf24f50aec111d37047ee0c4af63a38e966735a03(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac67c3ecd95bbbc55bc130d457e245f00decbc275854bb8b407db1329f860025(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8fb77dfbead9199eb5f47ecaa078f50ea02c5ce873fd226cd349a59b527fb3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d0815b3361eabab5affbe2f0e2d26f64eecd0bba911c06147e98f374796565c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2be8f8330a2a7250df106f290a4e8ddeda8715a95a83b481ae76d8ac2d2d8e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f9a797f445ffc1deaff140a69a030bdb25f3fa135ef233a56621cf7d99867c(
    *,
    instance_arn: builtins.str,
    name: builtins.str,
    parent_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494987ef0f9b905c50c1efbd53f96fb396b7f25b5354dfbb4027a32dbf61b9b1(
    *,
    instance_arn: builtins.str,
    phone_config: typing.Union[typing.Union[CfnUser.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    routing_profile_arn: builtins.str,
    security_profile_arns: typing.Sequence[builtins.str],
    username: builtins.str,
    directory_user_id: typing.Optional[builtins.str] = None,
    hierarchy_group_arn: typing.Optional[builtins.str] = None,
    identity_info: typing.Optional[typing.Union[typing.Union[CfnUser.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    password: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
