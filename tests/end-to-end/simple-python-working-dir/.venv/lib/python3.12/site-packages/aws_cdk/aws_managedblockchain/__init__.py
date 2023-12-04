'''
# AWS::ManagedBlockchain Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_managedblockchain as managedblockchain
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ManagedBlockchain construct libraries](https://constructs.dev/search?q=managedblockchain)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ManagedBlockchain resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ManagedBlockchain.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ManagedBlockchain](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ManagedBlockchain.html).

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
    IResolvable as _IResolvable_da3f097b,
    TreeInspector as _TreeInspector_488e0dd5,
)


@jsii.implements(_IInspectable_c2943556)
class CfnMember(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember",
):
    '''A CloudFormation ``AWS::ManagedBlockchain::Member``.

    Creates a member within a Managed Blockchain network.

    Applies only to Hyperledger Fabric.

    :cloudformationResource: AWS::ManagedBlockchain::Member
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_managedblockchain as managedblockchain
        
        cfn_member = managedblockchain.CfnMember(self, "MyCfnMember",
            member_configuration=managedblockchain.CfnMember.MemberConfigurationProperty(
                name="name",
        
                # the properties below are optional
                description="description",
                member_framework_configuration=managedblockchain.CfnMember.MemberFrameworkConfigurationProperty(
                    member_fabric_configuration=managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                        admin_password="adminPassword",
                        admin_username="adminUsername"
                    )
                )
            ),
        
            # the properties below are optional
            invitation_id="invitationId",
            network_configuration=managedblockchain.CfnMember.NetworkConfigurationProperty(
                framework="framework",
                framework_version="frameworkVersion",
                name="name",
                voting_policy=managedblockchain.CfnMember.VotingPolicyProperty(
                    approval_threshold_policy=managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                        proposal_duration_in_hours=123,
                        threshold_comparator="thresholdComparator",
                        threshold_percentage=123
                    )
                ),
        
                # the properties below are optional
                description="description",
                network_framework_configuration=managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty(
                    network_fabric_configuration=managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                        edition="edition"
                    )
                )
            ),
            network_id="networkId"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        member_configuration: typing.Union[typing.Union["CfnMember.MemberConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        invitation_id: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ManagedBlockchain::Member``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param member_configuration: Configuration properties of the member.
        :param invitation_id: The unique identifier of the invitation to join the network sent to the account that creates the member.
        :param network_configuration: Configuration properties of the network to which the member belongs.
        :param network_id: The unique identifier of the network to which the member belongs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f440aedf38983e9bd6c40a21512108e2511416c6c14702ff310a996c2d3c8090)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMemberProps(
            member_configuration=member_configuration,
            invitation_id=invitation_id,
            network_configuration=network_configuration,
            network_id=network_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a9dd6743a85bd3e4a8e4cd1e70d4394c71e0592b92008a8d4ead6f921817bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__422ce170be4ab6b24dec58576ce57919dadd194701d6f0efe583539b675dc413)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrMemberId")
    def attr_member_id(self) -> builtins.str:
        '''The unique identifier of the member.

        :cloudformationAttribute: MemberId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMemberId"))

    @builtins.property
    @jsii.member(jsii_name="attrNetworkId")
    def attr_network_id(self) -> builtins.str:
        '''The unique identifier of the network to which the member belongs.

        :cloudformationAttribute: NetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="memberConfiguration")
    def member_configuration(
        self,
    ) -> typing.Union["CfnMember.MemberConfigurationProperty", _IResolvable_da3f097b]:
        '''Configuration properties of the member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-memberconfiguration
        '''
        return typing.cast(typing.Union["CfnMember.MemberConfigurationProperty", _IResolvable_da3f097b], jsii.get(self, "memberConfiguration"))

    @member_configuration.setter
    def member_configuration(
        self,
        value: typing.Union["CfnMember.MemberConfigurationProperty", _IResolvable_da3f097b],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24495100bf25afd24d813b99fff4af16320194e2dd30a50b0952045777315fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="invitationId")
    def invitation_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the invitation to join the network sent to the account that creates the member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-invitationid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invitationId"))

    @invitation_id.setter
    def invitation_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06c817eef5c6850a2fb97f59cc2644d04847835af445f0fd00e77528462baa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invitationId", value)

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnMember.NetworkConfigurationProperty", _IResolvable_da3f097b]]:
        '''Configuration properties of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnMember.NetworkConfigurationProperty", _IResolvable_da3f097b]], jsii.get(self, "networkConfiguration"))

    @network_configuration.setter
    def network_configuration(
        self,
        value: typing.Optional[typing.Union["CfnMember.NetworkConfigurationProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b38bc2452a008056f7d9695d2f2aa5c754336deb3398e3ac24b7db0b0e515bb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7db9bb09cf2b486e4ee7d51e16f18507645763161c21100ce0b0bccc37fe6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember.ApprovalThresholdPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "proposal_duration_in_hours": "proposalDurationInHours",
            "threshold_comparator": "thresholdComparator",
            "threshold_percentage": "thresholdPercentage",
        },
    )
    class ApprovalThresholdPolicyProperty:
        def __init__(
            self,
            *,
            proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
            threshold_comparator: typing.Optional[builtins.str] = None,
            threshold_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A policy type that defines the voting rules for the network.

            The rules decide if a proposal is approved. Approval may be based on criteria such as the percentage of ``YES`` votes and the duration of the proposal. The policy applies to all proposals and is specified when the network is created.

            Applies only to Hyperledger Fabric.

            :param proposal_duration_in_hours: The duration from the time that a proposal is created until it expires. If members cast neither the required number of ``YES`` votes to approve the proposal nor the number of ``NO`` votes required to reject it before the duration expires, the proposal is ``EXPIRED`` and ``ProposalActions`` aren't carried out.
            :param threshold_comparator: Determines whether the vote percentage must be greater than the ``ThresholdPercentage`` or must be greater than or equal to the ``ThreholdPercentage`` to be approved.
            :param threshold_percentage: The percentage of votes among all members that must be ``YES`` for a proposal to be approved. For example, a ``ThresholdPercentage`` value of ``50`` indicates 50%. The ``ThresholdComparator`` determines the precise comparison. If a ``ThresholdPercentage`` value of ``50`` is specified on a network with 10 members, along with a ``ThresholdComparator`` value of ``GREATER_THAN`` , this indicates that 6 ``YES`` votes are required for the proposal to be approved.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                approval_threshold_policy_property = managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                    proposal_duration_in_hours=123,
                    threshold_comparator="thresholdComparator",
                    threshold_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02cea2c83641ac318cbb1c6438d76d5b709ab88ac8944d419dc7c76a4d5afe98)
                check_type(argname="argument proposal_duration_in_hours", value=proposal_duration_in_hours, expected_type=type_hints["proposal_duration_in_hours"])
                check_type(argname="argument threshold_comparator", value=threshold_comparator, expected_type=type_hints["threshold_comparator"])
                check_type(argname="argument threshold_percentage", value=threshold_percentage, expected_type=type_hints["threshold_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if proposal_duration_in_hours is not None:
                self._values["proposal_duration_in_hours"] = proposal_duration_in_hours
            if threshold_comparator is not None:
                self._values["threshold_comparator"] = threshold_comparator
            if threshold_percentage is not None:
                self._values["threshold_percentage"] = threshold_percentage

        @builtins.property
        def proposal_duration_in_hours(self) -> typing.Optional[jsii.Number]:
            '''The duration from the time that a proposal is created until it expires.

            If members cast neither the required number of ``YES`` votes to approve the proposal nor the number of ``NO`` votes required to reject it before the duration expires, the proposal is ``EXPIRED`` and ``ProposalActions`` aren't carried out.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-proposaldurationinhours
            '''
            result = self._values.get("proposal_duration_in_hours")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def threshold_comparator(self) -> typing.Optional[builtins.str]:
            '''Determines whether the vote percentage must be greater than the ``ThresholdPercentage`` or must be greater than or equal to the ``ThreholdPercentage`` to be approved.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-thresholdcomparator
            '''
            result = self._values.get("threshold_comparator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of votes among all members that must be ``YES`` for a proposal to be approved.

            For example, a ``ThresholdPercentage`` value of ``50`` indicates 50%. The ``ThresholdComparator`` determines the precise comparison. If a ``ThresholdPercentage`` value of ``50`` is specified on a network with 10 members, along with a ``ThresholdComparator`` value of ``GREATER_THAN`` , this indicates that 6 ``YES`` votes are required for the proposal to be approved.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-thresholdpercentage
            '''
            result = self._values.get("threshold_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApprovalThresholdPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember.MemberConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "description": "description",
            "member_framework_configuration": "memberFrameworkConfiguration",
        },
    )
    class MemberConfigurationProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            description: typing.Optional[builtins.str] = None,
            member_framework_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.MemberFrameworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Configuration properties of the member.

            Applies only to Hyperledger Fabric.

            :param name: The name of the member.
            :param description: An optional description of the member.
            :param member_framework_configuration: Configuration properties of the blockchain framework relevant to the member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                member_configuration_property = managedblockchain.CfnMember.MemberConfigurationProperty(
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    member_framework_configuration=managedblockchain.CfnMember.MemberFrameworkConfigurationProperty(
                        member_fabric_configuration=managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                            admin_password="adminPassword",
                            admin_username="adminUsername"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51367f640e718063d1e630299be0afb17c875b3b308a048f746cac3c699a5f99)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument member_framework_configuration", value=member_framework_configuration, expected_type=type_hints["member_framework_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if member_framework_configuration is not None:
                self._values["member_framework_configuration"] = member_framework_configuration

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''An optional description of the member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def member_framework_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.MemberFrameworkConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration properties of the blockchain framework relevant to the member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-memberframeworkconfiguration
            '''
            result = self._values.get("member_framework_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnMember.MemberFrameworkConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember.MemberFabricConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "admin_password": "adminPassword",
            "admin_username": "adminUsername",
        },
    )
    class MemberFabricConfigurationProperty:
        def __init__(
            self,
            *,
            admin_password: builtins.str,
            admin_username: builtins.str,
        ) -> None:
            '''Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network that is using the Hyperledger Fabric framework.

            :param admin_password: The password for the member's initial administrative user. The ``AdminPassword`` must be at least 8 characters long and no more than 32 characters. It must contain at least one uppercase letter, one lowercase letter, and one digit. It cannot have a single quotation mark (‘), a double quotation marks (“), a forward slash(/), a backward slash(), @, or a space.
            :param admin_username: The user name for the member's initial administrative user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                member_fabric_configuration_property = managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                    admin_password="adminPassword",
                    admin_username="adminUsername"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37e983734011eb49a2c46ca3def8c6bfcb990bded4c5b014249a9eeecaab157d)
                check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
                check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "admin_password": admin_password,
                "admin_username": admin_username,
            }

        @builtins.property
        def admin_password(self) -> builtins.str:
            '''The password for the member's initial administrative user.

            The ``AdminPassword`` must be at least 8 characters long and no more than 32 characters. It must contain at least one uppercase letter, one lowercase letter, and one digit. It cannot have a single quotation mark (‘), a double quotation marks (“), a forward slash(/), a backward slash(), @, or a space.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html#cfn-managedblockchain-member-memberfabricconfiguration-adminpassword
            '''
            result = self._values.get("admin_password")
            assert result is not None, "Required property 'admin_password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def admin_username(self) -> builtins.str:
            '''The user name for the member's initial administrative user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html#cfn-managedblockchain-member-memberfabricconfiguration-adminusername
            '''
            result = self._values.get("admin_username")
            assert result is not None, "Required property 'admin_username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberFabricConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember.MemberFrameworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"member_fabric_configuration": "memberFabricConfiguration"},
    )
    class MemberFrameworkConfigurationProperty:
        def __init__(
            self,
            *,
            member_fabric_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.MemberFabricConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Configuration properties relevant to a member for the blockchain framework that the Managed Blockchain network uses.

            :param member_fabric_configuration: Configuration properties for Hyperledger Fabric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberframeworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                member_framework_configuration_property = managedblockchain.CfnMember.MemberFrameworkConfigurationProperty(
                    member_fabric_configuration=managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                        admin_password="adminPassword",
                        admin_username="adminUsername"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b491217906f30cb4191d01752451ada84d5ea4301b6220726758f96d896e06cf)
                check_type(argname="argument member_fabric_configuration", value=member_fabric_configuration, expected_type=type_hints["member_fabric_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if member_fabric_configuration is not None:
                self._values["member_fabric_configuration"] = member_fabric_configuration

        @builtins.property
        def member_fabric_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.MemberFabricConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration properties for Hyperledger Fabric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberframeworkconfiguration.html#cfn-managedblockchain-member-memberframeworkconfiguration-memberfabricconfiguration
            '''
            result = self._values.get("member_fabric_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnMember.MemberFabricConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberFrameworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "framework": "framework",
            "framework_version": "frameworkVersion",
            "name": "name",
            "voting_policy": "votingPolicy",
            "description": "description",
            "network_framework_configuration": "networkFrameworkConfiguration",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            framework: builtins.str,
            framework_version: builtins.str,
            name: builtins.str,
            voting_policy: typing.Union[typing.Union["CfnMember.VotingPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
            description: typing.Optional[builtins.str] = None,
            network_framework_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.NetworkFrameworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Configuration properties of the network to which the member belongs.

            :param framework: The blockchain framework that the network uses.
            :param framework_version: The version of the blockchain framework that the network uses.
            :param name: The name of the network.
            :param voting_policy: The voting rules that the network uses to decide if a proposal is accepted.
            :param description: Attributes of the blockchain framework for the network.
            :param network_framework_configuration: Configuration properties relevant to the network for the blockchain framework that the network uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                network_configuration_property = managedblockchain.CfnMember.NetworkConfigurationProperty(
                    framework="framework",
                    framework_version="frameworkVersion",
                    name="name",
                    voting_policy=managedblockchain.CfnMember.VotingPolicyProperty(
                        approval_threshold_policy=managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                            proposal_duration_in_hours=123,
                            threshold_comparator="thresholdComparator",
                            threshold_percentage=123
                        )
                    ),
                
                    # the properties below are optional
                    description="description",
                    network_framework_configuration=managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty(
                        network_fabric_configuration=managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                            edition="edition"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04f1d8c07c23e365bc54ad25776dbc36fa43df91de362da315b8515f9df8d802)
                check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
                check_type(argname="argument framework_version", value=framework_version, expected_type=type_hints["framework_version"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument voting_policy", value=voting_policy, expected_type=type_hints["voting_policy"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument network_framework_configuration", value=network_framework_configuration, expected_type=type_hints["network_framework_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "framework": framework,
                "framework_version": framework_version,
                "name": name,
                "voting_policy": voting_policy,
            }
            if description is not None:
                self._values["description"] = description
            if network_framework_configuration is not None:
                self._values["network_framework_configuration"] = network_framework_configuration

        @builtins.property
        def framework(self) -> builtins.str:
            '''The blockchain framework that the network uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-framework
            '''
            result = self._values.get("framework")
            assert result is not None, "Required property 'framework' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def framework_version(self) -> builtins.str:
            '''The version of the blockchain framework that the network uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-frameworkversion
            '''
            result = self._values.get("framework_version")
            assert result is not None, "Required property 'framework_version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def voting_policy(
            self,
        ) -> typing.Union["CfnMember.VotingPolicyProperty", _IResolvable_da3f097b]:
            '''The voting rules that the network uses to decide if a proposal is accepted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-votingpolicy
            '''
            result = self._values.get("voting_policy")
            assert result is not None, "Required property 'voting_policy' is missing"
            return typing.cast(typing.Union["CfnMember.VotingPolicyProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''Attributes of the blockchain framework for the network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_framework_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.NetworkFrameworkConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration properties relevant to the network for the blockchain framework that the network uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-networkframeworkconfiguration
            '''
            result = self._values.get("network_framework_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnMember.NetworkFrameworkConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember.NetworkFabricConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"edition": "edition"},
    )
    class NetworkFabricConfigurationProperty:
        def __init__(self, *, edition: builtins.str) -> None:
            '''Hyperledger Fabric configuration properties for the network.

            :param edition: The edition of Amazon Managed Blockchain that the network uses. Valid values are ``standard`` and ``starter`` . For more information, see `Amazon Managed Blockchain Pricing <https://docs.aws.amazon.com/managed-blockchain/pricing/>`_

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkfabricconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                network_fabric_configuration_property = managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                    edition="edition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd3f379780118ac508a3d57d16dcdde085bac183f3ac71d031313c234626e7c7)
                check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "edition": edition,
            }

        @builtins.property
        def edition(self) -> builtins.str:
            '''The edition of Amazon Managed Blockchain that the network uses.

            Valid values are ``standard`` and ``starter`` . For more information, see `Amazon Managed Blockchain Pricing <https://docs.aws.amazon.com/managed-blockchain/pricing/>`_

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkfabricconfiguration.html#cfn-managedblockchain-member-networkfabricconfiguration-edition
            '''
            result = self._values.get("edition")
            assert result is not None, "Required property 'edition' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkFabricConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"network_fabric_configuration": "networkFabricConfiguration"},
    )
    class NetworkFrameworkConfigurationProperty:
        def __init__(
            self,
            *,
            network_fabric_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.NetworkFabricConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Configuration properties relevant to the network for the blockchain framework that the network uses.

            :param network_fabric_configuration: Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network that is using the Hyperledger Fabric framework.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkframeworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                network_framework_configuration_property = managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty(
                    network_fabric_configuration=managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                        edition="edition"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8773f0a05758e613681da54a9e276d174cf38cbd9be1372a0cb1ed08ec6a6e2b)
                check_type(argname="argument network_fabric_configuration", value=network_fabric_configuration, expected_type=type_hints["network_fabric_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_fabric_configuration is not None:
                self._values["network_fabric_configuration"] = network_fabric_configuration

        @builtins.property
        def network_fabric_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.NetworkFabricConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network that is using the Hyperledger Fabric framework.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkframeworkconfiguration.html#cfn-managedblockchain-member-networkframeworkconfiguration-networkfabricconfiguration
            '''
            result = self._values.get("network_fabric_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnMember.NetworkFabricConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkFrameworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMember.VotingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"approval_threshold_policy": "approvalThresholdPolicy"},
    )
    class VotingPolicyProperty:
        def __init__(
            self,
            *,
            approval_threshold_policy: typing.Optional[typing.Union[typing.Union["CfnMember.ApprovalThresholdPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''The voting rules for the network to decide if a proposal is accepted.

            Applies only to Hyperledger Fabric.

            :param approval_threshold_policy: Defines the rules for the network for voting on proposals, such as the percentage of ``YES`` votes required for the proposal to be approved and the duration of the proposal. The policy applies to all proposals and is specified when the network is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-votingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                voting_policy_property = managedblockchain.CfnMember.VotingPolicyProperty(
                    approval_threshold_policy=managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                        proposal_duration_in_hours=123,
                        threshold_comparator="thresholdComparator",
                        threshold_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c68c8e4a9368be2e89a33105aa99ab4212e33852ff178527742919731a930d87)
                check_type(argname="argument approval_threshold_policy", value=approval_threshold_policy, expected_type=type_hints["approval_threshold_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approval_threshold_policy is not None:
                self._values["approval_threshold_policy"] = approval_threshold_policy

        @builtins.property
        def approval_threshold_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.ApprovalThresholdPolicyProperty", _IResolvable_da3f097b]]:
            '''Defines the rules for the network for voting on proposals, such as the percentage of ``YES`` votes required for the proposal to be approved and the duration of the proposal.

            The policy applies to all proposals and is specified when the network is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-votingpolicy.html#cfn-managedblockchain-member-votingpolicy-approvalthresholdpolicy
            '''
            result = self._values.get("approval_threshold_policy")
            return typing.cast(typing.Optional[typing.Union["CfnMember.ApprovalThresholdPolicyProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VotingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_managedblockchain.CfnMemberProps",
    jsii_struct_bases=[],
    name_mapping={
        "member_configuration": "memberConfiguration",
        "invitation_id": "invitationId",
        "network_configuration": "networkConfiguration",
        "network_id": "networkId",
    },
)
class CfnMemberProps:
    def __init__(
        self,
        *,
        member_configuration: typing.Union[typing.Union[CfnMember.MemberConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        invitation_id: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMember``.

        :param member_configuration: Configuration properties of the member.
        :param invitation_id: The unique identifier of the invitation to join the network sent to the account that creates the member.
        :param network_configuration: Configuration properties of the network to which the member belongs.
        :param network_id: The unique identifier of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_managedblockchain as managedblockchain
            
            cfn_member_props = managedblockchain.CfnMemberProps(
                member_configuration=managedblockchain.CfnMember.MemberConfigurationProperty(
                    name="name",
            
                    # the properties below are optional
                    description="description",
                    member_framework_configuration=managedblockchain.CfnMember.MemberFrameworkConfigurationProperty(
                        member_fabric_configuration=managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                            admin_password="adminPassword",
                            admin_username="adminUsername"
                        )
                    )
                ),
            
                # the properties below are optional
                invitation_id="invitationId",
                network_configuration=managedblockchain.CfnMember.NetworkConfigurationProperty(
                    framework="framework",
                    framework_version="frameworkVersion",
                    name="name",
                    voting_policy=managedblockchain.CfnMember.VotingPolicyProperty(
                        approval_threshold_policy=managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                            proposal_duration_in_hours=123,
                            threshold_comparator="thresholdComparator",
                            threshold_percentage=123
                        )
                    ),
            
                    # the properties below are optional
                    description="description",
                    network_framework_configuration=managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty(
                        network_fabric_configuration=managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                            edition="edition"
                        )
                    )
                ),
                network_id="networkId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e66a18793d1c75e230157cc8b1b1b82fe1269a8b280b51df9b9f4c5c751dea9c)
            check_type(argname="argument member_configuration", value=member_configuration, expected_type=type_hints["member_configuration"])
            check_type(argname="argument invitation_id", value=invitation_id, expected_type=type_hints["invitation_id"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "member_configuration": member_configuration,
        }
        if invitation_id is not None:
            self._values["invitation_id"] = invitation_id
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if network_id is not None:
            self._values["network_id"] = network_id

    @builtins.property
    def member_configuration(
        self,
    ) -> typing.Union[CfnMember.MemberConfigurationProperty, _IResolvable_da3f097b]:
        '''Configuration properties of the member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-memberconfiguration
        '''
        result = self._values.get("member_configuration")
        assert result is not None, "Required property 'member_configuration' is missing"
        return typing.cast(typing.Union[CfnMember.MemberConfigurationProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def invitation_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the invitation to join the network sent to the account that creates the member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-invitationid
        '''
        result = self._values.get("invitation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnMember.NetworkConfigurationProperty, _IResolvable_da3f097b]]:
        '''Configuration properties of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnMember.NetworkConfigurationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkid
        '''
        result = self._values.get("network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMemberProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnNode(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_managedblockchain.CfnNode",
):
    '''A CloudFormation ``AWS::ManagedBlockchain::Node``.

    Creates a node on the specified blockchain network.

    Applies to Hyperledger Fabric and Ethereum.

    :cloudformationResource: AWS::ManagedBlockchain::Node
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_managedblockchain as managedblockchain
        
        cfn_node = managedblockchain.CfnNode(self, "MyCfnNode",
            network_id="networkId",
            node_configuration=managedblockchain.CfnNode.NodeConfigurationProperty(
                availability_zone="availabilityZone",
                instance_type="instanceType"
            ),
        
            # the properties below are optional
            member_id="memberId"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        network_id: builtins.str,
        node_configuration: typing.Union[typing.Union["CfnNode.NodeConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        member_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ManagedBlockchain::Node``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param network_id: The unique identifier of the network for the node. Ethereum public networks have the following ``NetworkId`` s: - ``n-ethereum-mainnet`` - ``n-ethereum-goerli`` - ``n-ethereum-rinkeby``
        :param node_configuration: Configuration properties of a peer node.
        :param member_id: The unique identifier of the member to which the node belongs. Applies only to Hyperledger Fabric.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48dbd6ef5c42666453e84796d418e81144be49dedf064e93bf40d44fb4dc0cab)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNodeProps(
            network_id=network_id,
            node_configuration=node_configuration,
            member_id=member_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c388501c993f487cedc15db18e2da552e99448b2fbbb73df0c86ca6b0ff1f9c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddb1eca2d00ac1be0c81a50a971bbb0d2c013f62f102ab0af5b3b2de742953ba)
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
        '''The Amazon Resource Name (ARN) of the node.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrMemberId")
    def attr_member_id(self) -> builtins.str:
        '''The unique identifier of the member in which the node is created.

        Applies only to Hyperledger Fabric.

        :cloudformationAttribute: MemberId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMemberId"))

    @builtins.property
    @jsii.member(jsii_name="attrNetworkId")
    def attr_network_id(self) -> builtins.str:
        '''The unique identifier of the network that the node is in.

        :cloudformationAttribute: NetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="attrNodeId")
    def attr_node_id(self) -> builtins.str:
        '''The unique identifier of the node.

        :cloudformationAttribute: NodeId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNodeId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        '''The unique identifier of the network for the node.

        Ethereum public networks have the following ``NetworkId`` s:

        - ``n-ethereum-mainnet``
        - ``n-ethereum-goerli``
        - ``n-ethereum-rinkeby``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-networkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e973c708787ea875c475d8d5e3d65d9fabaadd752c9985d2ef28c9fb514ec25a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value)

    @builtins.property
    @jsii.member(jsii_name="nodeConfiguration")
    def node_configuration(
        self,
    ) -> typing.Union["CfnNode.NodeConfigurationProperty", _IResolvable_da3f097b]:
        '''Configuration properties of a peer node.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-nodeconfiguration
        '''
        return typing.cast(typing.Union["CfnNode.NodeConfigurationProperty", _IResolvable_da3f097b], jsii.get(self, "nodeConfiguration"))

    @node_configuration.setter
    def node_configuration(
        self,
        value: typing.Union["CfnNode.NodeConfigurationProperty", _IResolvable_da3f097b],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01c3ae152356712a3452a2f9b3ad805619970b05a968191d4ccda7f6fe9c951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the member to which the node belongs.

        Applies only to Hyperledger Fabric.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-memberid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberId"))

    @member_id.setter
    def member_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d89f5294a350105d930c39902dc2d9e7d7bb6e37ace303d0b49609bd81e60b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberId", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_managedblockchain.CfnNode.NodeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "instance_type": "instanceType",
        },
    )
    class NodeConfigurationProperty:
        def __init__(
            self,
            *,
            availability_zone: builtins.str,
            instance_type: builtins.str,
        ) -> None:
            '''Configuration properties of a peer node within a membership.

            :param availability_zone: The Availability Zone in which the node exists. Required for Ethereum nodes.
            :param instance_type: The Amazon Managed Blockchain instance type for the node.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_managedblockchain as managedblockchain
                
                node_configuration_property = managedblockchain.CfnNode.NodeConfigurationProperty(
                    availability_zone="availabilityZone",
                    instance_type="instanceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17aa04ca4abfb63493c324177d7e99bb4c80136ba0c4e225db7ff9fd5f085bc6)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "availability_zone": availability_zone,
                "instance_type": instance_type,
            }

        @builtins.property
        def availability_zone(self) -> builtins.str:
            '''The Availability Zone in which the node exists.

            Required for Ethereum nodes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html#cfn-managedblockchain-node-nodeconfiguration-availabilityzone
            '''
            result = self._values.get("availability_zone")
            assert result is not None, "Required property 'availability_zone' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def instance_type(self) -> builtins.str:
            '''The Amazon Managed Blockchain instance type for the node.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html#cfn-managedblockchain-node-nodeconfiguration-instancetype
            '''
            result = self._values.get("instance_type")
            assert result is not None, "Required property 'instance_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_managedblockchain.CfnNodeProps",
    jsii_struct_bases=[],
    name_mapping={
        "network_id": "networkId",
        "node_configuration": "nodeConfiguration",
        "member_id": "memberId",
    },
)
class CfnNodeProps:
    def __init__(
        self,
        *,
        network_id: builtins.str,
        node_configuration: typing.Union[typing.Union[CfnNode.NodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        member_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnNode``.

        :param network_id: The unique identifier of the network for the node. Ethereum public networks have the following ``NetworkId`` s: - ``n-ethereum-mainnet`` - ``n-ethereum-goerli`` - ``n-ethereum-rinkeby``
        :param node_configuration: Configuration properties of a peer node.
        :param member_id: The unique identifier of the member to which the node belongs. Applies only to Hyperledger Fabric.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_managedblockchain as managedblockchain
            
            cfn_node_props = managedblockchain.CfnNodeProps(
                network_id="networkId",
                node_configuration=managedblockchain.CfnNode.NodeConfigurationProperty(
                    availability_zone="availabilityZone",
                    instance_type="instanceType"
                ),
            
                # the properties below are optional
                member_id="memberId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06cdf753357136b8f6ace00b35f059256fbc98e2c163d6c1eee33fcfacb0e64b)
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument node_configuration", value=node_configuration, expected_type=type_hints["node_configuration"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_id": network_id,
            "node_configuration": node_configuration,
        }
        if member_id is not None:
            self._values["member_id"] = member_id

    @builtins.property
    def network_id(self) -> builtins.str:
        '''The unique identifier of the network for the node.

        Ethereum public networks have the following ``NetworkId`` s:

        - ``n-ethereum-mainnet``
        - ``n-ethereum-goerli``
        - ``n-ethereum-rinkeby``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-networkid
        '''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_configuration(
        self,
    ) -> typing.Union[CfnNode.NodeConfigurationProperty, _IResolvable_da3f097b]:
        '''Configuration properties of a peer node.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-nodeconfiguration
        '''
        result = self._values.get("node_configuration")
        assert result is not None, "Required property 'node_configuration' is missing"
        return typing.cast(typing.Union[CfnNode.NodeConfigurationProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def member_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the member to which the node belongs.

        Applies only to Hyperledger Fabric.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-memberid
        '''
        result = self._values.get("member_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMember",
    "CfnMemberProps",
    "CfnNode",
    "CfnNodeProps",
]

publication.publish()

def _typecheckingstub__f440aedf38983e9bd6c40a21512108e2511416c6c14702ff310a996c2d3c8090(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    member_configuration: typing.Union[typing.Union[CfnMember.MemberConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    invitation_id: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a9dd6743a85bd3e4a8e4cd1e70d4394c71e0592b92008a8d4ead6f921817bd(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422ce170be4ab6b24dec58576ce57919dadd194701d6f0efe583539b675dc413(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24495100bf25afd24d813b99fff4af16320194e2dd30a50b0952045777315fb(
    value: typing.Union[CfnMember.MemberConfigurationProperty, _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06c817eef5c6850a2fb97f59cc2644d04847835af445f0fd00e77528462baa2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38bc2452a008056f7d9695d2f2aa5c754336deb3398e3ac24b7db0b0e515bb8(
    value: typing.Optional[typing.Union[CfnMember.NetworkConfigurationProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7db9bb09cf2b486e4ee7d51e16f18507645763161c21100ce0b0bccc37fe6e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02cea2c83641ac318cbb1c6438d76d5b709ab88ac8944d419dc7c76a4d5afe98(
    *,
    proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
    threshold_comparator: typing.Optional[builtins.str] = None,
    threshold_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51367f640e718063d1e630299be0afb17c875b3b308a048f746cac3c699a5f99(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    member_framework_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.MemberFrameworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e983734011eb49a2c46ca3def8c6bfcb990bded4c5b014249a9eeecaab157d(
    *,
    admin_password: builtins.str,
    admin_username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b491217906f30cb4191d01752451ada84d5ea4301b6220726758f96d896e06cf(
    *,
    member_fabric_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.MemberFabricConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f1d8c07c23e365bc54ad25776dbc36fa43df91de362da315b8515f9df8d802(
    *,
    framework: builtins.str,
    framework_version: builtins.str,
    name: builtins.str,
    voting_policy: typing.Union[typing.Union[CfnMember.VotingPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    description: typing.Optional[builtins.str] = None,
    network_framework_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkFrameworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3f379780118ac508a3d57d16dcdde085bac183f3ac71d031313c234626e7c7(
    *,
    edition: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8773f0a05758e613681da54a9e276d174cf38cbd9be1372a0cb1ed08ec6a6e2b(
    *,
    network_fabric_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkFabricConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68c8e4a9368be2e89a33105aa99ab4212e33852ff178527742919731a930d87(
    *,
    approval_threshold_policy: typing.Optional[typing.Union[typing.Union[CfnMember.ApprovalThresholdPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e66a18793d1c75e230157cc8b1b1b82fe1269a8b280b51df9b9f4c5c751dea9c(
    *,
    member_configuration: typing.Union[typing.Union[CfnMember.MemberConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    invitation_id: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48dbd6ef5c42666453e84796d418e81144be49dedf064e93bf40d44fb4dc0cab(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    network_id: builtins.str,
    node_configuration: typing.Union[typing.Union[CfnNode.NodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    member_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c388501c993f487cedc15db18e2da552e99448b2fbbb73df0c86ca6b0ff1f9c9(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb1eca2d00ac1be0c81a50a971bbb0d2c013f62f102ab0af5b3b2de742953ba(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e973c708787ea875c475d8d5e3d65d9fabaadd752c9985d2ef28c9fb514ec25a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01c3ae152356712a3452a2f9b3ad805619970b05a968191d4ccda7f6fe9c951(
    value: typing.Union[CfnNode.NodeConfigurationProperty, _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89f5294a350105d930c39902dc2d9e7d7bb6e37ace303d0b49609bd81e60b25(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17aa04ca4abfb63493c324177d7e99bb4c80136ba0c4e225db7ff9fd5f085bc6(
    *,
    availability_zone: builtins.str,
    instance_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cdf753357136b8f6ace00b35f059256fbc98e2c163d6c1eee33fcfacb0e64b(
    *,
    network_id: builtins.str,
    node_configuration: typing.Union[typing.Union[CfnNode.NodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    member_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
