'''
# AWS Resource Access Manager Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_ram as ram
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for RAM construct libraries](https://constructs.dev/search?q=ram)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::RAM resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RAM.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::RAM](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_RAM.html).

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
class CfnResourceShare(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_ram.CfnResourceShare",
):
    '''A CloudFormation ``AWS::RAM::ResourceShare``.

    Specifies a resource share.

    :cloudformationResource: AWS::RAM::ResourceShare
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_ram as ram
        
        cfn_resource_share = ram.CfnResourceShare(self, "MyCfnResourceShare",
            name="name",
        
            # the properties below are optional
            allow_external_principals=False,
            permission_arns=["permissionArns"],
            principals=["principals"],
            resource_arns=["resourceArns"],
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
        name: builtins.str,
        allow_external_principals: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::RAM::ResourceShare``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Specifies the name of the resource share.
        :param allow_external_principals: Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share. A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .
        :param permission_arns: Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param principals: Specifies a list of one or more principals to associate with the resource share. You can include the following values: - An AWS account ID, for example: ``123456789012`` - An `Amazon Resoure Name (ARN) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of an organization in AWS Organizations , for example: ``arn:aws:organizations::123456789012:organization/o-exampleorgid`` - An ARN of an organizational unit (OU) in AWS Organizations , for example: ``arn:aws:organizations::123456789012:ou/o-exampleorgid/ou-examplerootid-exampleouid123`` - An ARN of an IAM role, for example: ``arn:aws:iam::123456789012:role/rolename`` - An ARN of an IAM user, for example: ``arn:aws:iam::123456789012user/username`` .. epigraph:: Not all resource types can be shared with IAM roles and users. For more information, see `Sharing with IAM roles and users <https://docs.aws.amazon.com//ram/latest/userguide/permissions.html#permissions-rbp-supported-resource-types>`_ in the *AWS Resource Access Manager User Guide* .
        :param resource_arns: Specifies a list of one or more ARNs of the resources to associate with the resource share.
        :param tags: Specifies one or more tags to attach to the resource share itself. It doesn't attach the tags to the resources associated with the resource share.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fea9cca1996f068f8dde2c34bf4c41d370ee8638f9da1d855f8b0022d75af5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceShareProps(
            name=name,
            allow_external_principals=allow_external_principals,
            permission_arns=permission_arns,
            principals=principals,
            resource_arns=resource_arns,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8defbc280b992fb09ff90651c627ce1c4211d498c66f7c4b62a4b3a5285f92d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e124e85df525ca5d702f0b9a2b5bb739a12519bf552f8ea08a9f673f4077d696)
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
        '''The Amazon Resource Name (ARN) of the resource share.

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
        '''Specifies one or more tags to attach to the resource share itself.

        It doesn't attach the tags to the resources associated with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''Specifies the name of the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb76bd909afa4dee66debdd78e087883e909ff481a0f08820b4aee17388a74e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="allowExternalPrincipals")
    def allow_external_principals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share.

        A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], jsii.get(self, "allowExternalPrincipals"))

    @allow_external_principals.setter
    def allow_external_principals(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a8ac8ee18a992b418a8b6fc421772eee1a5d5b0b675ccfe6c0ce0c7f18b40e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowExternalPrincipals", value)

    @builtins.property
    @jsii.member(jsii_name="permissionArns")
    def permission_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-permissionarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "permissionArns"))

    @permission_arns.setter
    def permission_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411d88d3990f34296ef5770eb3cb3792a55b6b7805c6e7381207750e8fa15042)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionArns", value)

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of one or more principals to associate with the resource share.

        You can include the following values:

        - An AWS account ID, for example: ``123456789012``
        - An `Amazon Resoure Name (ARN) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of an organization in AWS Organizations , for example: ``arn:aws:organizations::123456789012:organization/o-exampleorgid``
        - An ARN of an organizational unit (OU) in AWS Organizations , for example: ``arn:aws:organizations::123456789012:ou/o-exampleorgid/ou-examplerootid-exampleouid123``
        - An ARN of an IAM role, for example: ``arn:aws:iam::123456789012:role/rolename``
        - An ARN of an IAM user, for example: ``arn:aws:iam::123456789012user/username``

        .. epigraph::

           Not all resource types can be shared with IAM roles and users. For more information, see `Sharing with IAM roles and users <https://docs.aws.amazon.com//ram/latest/userguide/permissions.html#permissions-rbp-supported-resource-types>`_ in the *AWS Resource Access Manager User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "principals"))

    @principals.setter
    def principals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e4971e92d1679357249799c9998f6cde7d19d4a39eec3a7d952e11f95d0b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principals", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArns")
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of one or more ARNs of the resources to associate with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceArns"))

    @resource_arns.setter
    def resource_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebcfa059a044b9468256f95fd1dc2d90bce40e3d6d96d59d1755b38b7d15db67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArns", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_ram.CfnResourceShareProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allow_external_principals": "allowExternalPrincipals",
        "permission_arns": "permissionArns",
        "principals": "principals",
        "resource_arns": "resourceArns",
        "tags": "tags",
    },
)
class CfnResourceShareProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        allow_external_principals: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceShare``.

        :param name: Specifies the name of the resource share.
        :param allow_external_principals: Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share. A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .
        :param permission_arns: Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.
        :param principals: Specifies a list of one or more principals to associate with the resource share. You can include the following values: - An AWS account ID, for example: ``123456789012`` - An `Amazon Resoure Name (ARN) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of an organization in AWS Organizations , for example: ``arn:aws:organizations::123456789012:organization/o-exampleorgid`` - An ARN of an organizational unit (OU) in AWS Organizations , for example: ``arn:aws:organizations::123456789012:ou/o-exampleorgid/ou-examplerootid-exampleouid123`` - An ARN of an IAM role, for example: ``arn:aws:iam::123456789012:role/rolename`` - An ARN of an IAM user, for example: ``arn:aws:iam::123456789012user/username`` .. epigraph:: Not all resource types can be shared with IAM roles and users. For more information, see `Sharing with IAM roles and users <https://docs.aws.amazon.com//ram/latest/userguide/permissions.html#permissions-rbp-supported-resource-types>`_ in the *AWS Resource Access Manager User Guide* .
        :param resource_arns: Specifies a list of one or more ARNs of the resources to associate with the resource share.
        :param tags: Specifies one or more tags to attach to the resource share itself. It doesn't attach the tags to the resources associated with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_ram as ram
            
            cfn_resource_share_props = ram.CfnResourceShareProps(
                name="name",
            
                # the properties below are optional
                allow_external_principals=False,
                permission_arns=["permissionArns"],
                principals=["principals"],
                resource_arns=["resourceArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a74e87907f43c8b632de2f93b4560b166f51134fc5a47c6f4892e716a268961a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allow_external_principals", value=allow_external_principals, expected_type=type_hints["allow_external_principals"])
            check_type(argname="argument permission_arns", value=permission_arns, expected_type=type_hints["permission_arns"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allow_external_principals is not None:
            self._values["allow_external_principals"] = allow_external_principals
        if permission_arns is not None:
            self._values["permission_arns"] = permission_arns
        if principals is not None:
            self._values["principals"] = principals
        if resource_arns is not None:
            self._values["resource_arns"] = resource_arns
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allow_external_principals(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''Specifies whether principals outside your organization in AWS Organizations can be associated with a resource share.

        A value of ``true`` lets you share with individual AWS accounts that are *not* in your organization. A value of ``false`` only has meaning if your account is a member of an AWS Organization. The default value is ``true`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-allowexternalprincipals
        '''
        result = self._values.get("allow_external_principals")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

    @builtins.property
    def permission_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of the AWS RAM permission to associate with the resource share. If you do not specify an ARN for the permission, AWS RAM automatically attaches the default version of the permission for each resource type. You can associate only one permission with each resource type included in the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-permissionarns
        '''
        result = self._values.get("permission_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of one or more principals to associate with the resource share.

        You can include the following values:

        - An AWS account ID, for example: ``123456789012``
        - An `Amazon Resoure Name (ARN) <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ of an organization in AWS Organizations , for example: ``arn:aws:organizations::123456789012:organization/o-exampleorgid``
        - An ARN of an organizational unit (OU) in AWS Organizations , for example: ``arn:aws:organizations::123456789012:ou/o-exampleorgid/ou-examplerootid-exampleouid123``
        - An ARN of an IAM role, for example: ``arn:aws:iam::123456789012:role/rolename``
        - An ARN of an IAM user, for example: ``arn:aws:iam::123456789012user/username``

        .. epigraph::

           Not all resource types can be shared with IAM roles and users. For more information, see `Sharing with IAM roles and users <https://docs.aws.amazon.com//ram/latest/userguide/permissions.html#permissions-rbp-supported-resource-types>`_ in the *AWS Resource Access Manager User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-principals
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of one or more ARNs of the resources to associate with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-resourcearns
        '''
        result = self._values.get("resource_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''Specifies one or more tags to attach to the resource share itself.

        It doesn't attach the tags to the resources associated with the resource share.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ram-resourceshare.html#cfn-ram-resourceshare-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceShareProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnResourceShare",
    "CfnResourceShareProps",
]

publication.publish()

def _typecheckingstub__1fea9cca1996f068f8dde2c34bf4c41d370ee8638f9da1d855f8b0022d75af5d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    allow_external_principals: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8defbc280b992fb09ff90651c627ce1c4211d498c66f7c4b62a4b3a5285f92d(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e124e85df525ca5d702f0b9a2b5bb739a12519bf552f8ea08a9f673f4077d696(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb76bd909afa4dee66debdd78e087883e909ff481a0f08820b4aee17388a74e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8ac8ee18a992b418a8b6fc421772eee1a5d5b0b675ccfe6c0ce0c7f18b40e7(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411d88d3990f34296ef5770eb3cb3792a55b6b7805c6e7381207750e8fa15042(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e4971e92d1679357249799c9998f6cde7d19d4a39eec3a7d952e11f95d0b64(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebcfa059a044b9468256f95fd1dc2d90bce40e3d6d96d59d1755b38b7d15db67(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74e87907f43c8b632de2f93b4560b166f51134fc5a47c6f4892e716a268961a(
    *,
    name: builtins.str,
    allow_external_principals: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    permission_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
