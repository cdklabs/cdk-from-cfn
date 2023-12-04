'''
# AWS::IoTTwinMaker Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_iottwinmaker as iottwinmaker
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for IoTTwinMaker construct libraries](https://constructs.dev/search?q=iottwinmaker)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::IoTTwinMaker resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTTwinMaker.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::IoTTwinMaker](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_IoTTwinMaker.html).

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
    TagManager as _TagManager_0a598cb3,
    TreeInspector as _TreeInspector_488e0dd5,
)


@jsii.implements(_IInspectable_c2943556)
class CfnComponentType(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::ComponentType``.

    Use the ``AWS::IoTTwinMaker::ComponentType`` resource to declare a component type.

    :cloudformationResource: AWS::IoTTwinMaker::ComponentType
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_iottwinmaker as iottwinmaker
        
        # data_type_property_: iottwinmaker.CfnComponentType.DataTypeProperty
        # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
        # relationship_value: Any
        
        cfn_component_type = iottwinmaker.CfnComponentType(self, "MyCfnComponentType",
            component_type_id="componentTypeId",
            workspace_id="workspaceId",
        
            # the properties below are optional
            description="description",
            extends_from=["extendsFrom"],
            functions={
                "functions_key": iottwinmaker.CfnComponentType.FunctionProperty(
                    implemented_by=iottwinmaker.CfnComponentType.DataConnectorProperty(
                        is_native=False,
                        lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                            arn="arn"
                        )
                    ),
                    required_properties=["requiredProperties"],
                    scope="scope"
                )
            },
            is_singleton=False,
            property_definitions={
                "property_definitions_key": iottwinmaker.CfnComponentType.PropertyDefinitionProperty(
                    configurations={
                        "configurations_key": "configurations"
                    },
                    data_type=iottwinmaker.CfnComponentType.DataTypeProperty(
                        type="type",
        
                        # the properties below are optional
                        allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        unit_of_measure="unitOfMeasure"
                    ),
                    default_value=iottwinmaker.CfnComponentType.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    ),
                    is_external_id=False,
                    is_required_in_entity=False,
                    is_stored_externally=False,
                    is_time_series=False
                )
            },
            property_groups={
                "property_groups_key": iottwinmaker.CfnComponentType.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            },
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
        component_type_id: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        functions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentType.FunctionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        is_singleton: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        property_definitions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentType.PropertyDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        property_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentType.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::ComponentType``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param component_type_id: The ID of the component type.
        :param workspace_id: The ID of the workspace.
        :param description: The description of the component type.
        :param extends_from: The name of the parent component type that this component type extends.
        :param functions: An object that maps strings to the functions in the component type. Each string in the mapping must be unique to this object. For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.
        :param is_singleton: A boolean value that specifies whether an entity can have more than one component of this type.
        :param property_definitions: An object that maps strings to the property definitions in the component type. Each string in the mapping must be unique to this object. For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.
        :param property_groups: An object that maps strings to the property groups in the component type. Each string in the mapping must be unique to this object.
        :param tags: The ComponentType tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8644c92bbff89aa9e628d0fdc0ded7a2f9a39289146f897d6c9e6d84975a7a2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnComponentTypeProps(
            component_type_id=component_type_id,
            workspace_id=workspace_id,
            description=description,
            extends_from=extends_from,
            functions=functions,
            is_singleton=is_singleton,
            property_definitions=property_definitions,
            property_groups=property_groups,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9021df5b01719a9f8ef0ced4ac31ece64c48f2d9a6f8a2a8e1b3dc52181751a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__980d08eeb6e6054720e3cbf007fada113e5791e2cc6fddb21f88ce57af3f67a7)
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
        '''The ARN of the component type.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time when the component type was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrIsAbstract")
    def attr_is_abstract(self) -> _IResolvable_da3f097b:
        '''A boolean value that specifies whether the component type is abstract.

        :cloudformationAttribute: IsAbstract
        '''
        return typing.cast(_IResolvable_da3f097b, jsii.get(self, "attrIsAbstract"))

    @builtins.property
    @jsii.member(jsii_name="attrIsSchemaInitialized")
    def attr_is_schema_initialized(self) -> _IResolvable_da3f097b:
        '''A boolean value that specifies whether the component type has a schema initializer and that the schema initializer has run.

        :cloudformationAttribute: IsSchemaInitialized
        '''
        return typing.cast(_IResolvable_da3f097b, jsii.get(self, "attrIsSchemaInitialized"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusErrorCode")
    def attr_status_error_code(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.Error.Code
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusErrorCode"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusErrorMessage")
    def attr_status_error_message(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.Error.Message
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusErrorMessage"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusState")
    def attr_status_state(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The component type the update time.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="componentTypeId")
    def component_type_id(self) -> builtins.str:
        '''The ID of the component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-componenttypeid
        '''
        return typing.cast(builtins.str, jsii.get(self, "componentTypeId"))

    @component_type_id.setter
    def component_type_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3995a78286949349e004f99ea0c8d16e95bcee5d158e0e48f00b2b4f8527b034)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentTypeId", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2de3147a6b2674e530d30f8b5182e3c9439f2a356e4c875b3698b24221b97584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47d9f5f634e196d4115e50936c2bee2a81dabb9327edc3a41578e1176dbda51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="extendsFrom")
    def extends_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the parent component type that this component type extends.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-extendsfrom
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "extendsFrom"))

    @extends_from.setter
    def extends_from(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f86b83703d7a5bd869a7593399801c17824b55ace45f888bf02c81af5378c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extendsFrom", value)

    @builtins.property
    @jsii.member(jsii_name="functions")
    def functions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.FunctionProperty", _IResolvable_da3f097b]]]]:
        '''An object that maps strings to the functions in the component type.

        Each string in the mapping must be unique to this object.

        For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-functions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.FunctionProperty", _IResolvable_da3f097b]]]], jsii.get(self, "functions"))

    @functions.setter
    def functions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.FunctionProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c18d78b62d26be5852013391c05c78956f0decd19a229ac7f58b866ae466c14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functions", value)

    @builtins.property
    @jsii.member(jsii_name="isSingleton")
    def is_singleton(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''A boolean value that specifies whether an entity can have more than one component of this type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-issingleton
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], jsii.get(self, "isSingleton"))

    @is_singleton.setter
    def is_singleton(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f5b5fcf3c80cef383cad8a20c79fb45b21b0d73ef476054a81873ff26b199c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isSingleton", value)

    @builtins.property
    @jsii.member(jsii_name="propertyDefinitions")
    def property_definitions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyDefinitionProperty", _IResolvable_da3f097b]]]]:
        '''An object that maps strings to the property definitions in the component type.

        Each string in the mapping must be unique to this object.

        For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertydefinitions
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyDefinitionProperty", _IResolvable_da3f097b]]]], jsii.get(self, "propertyDefinitions"))

    @property_definitions.setter
    def property_definitions(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyDefinitionProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1be07e93843a09c1fedf2924bac62d38324ad54f2879a9be1a8e23ad7beb09f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propertyDefinitions", value)

    @builtins.property
    @jsii.member(jsii_name="propertyGroups")
    def property_groups(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyGroupProperty", _IResolvable_da3f097b]]]]:
        '''An object that maps strings to the property groups in the component type.

        Each string in the mapping must be unique to this object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertygroups
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyGroupProperty", _IResolvable_da3f097b]]]], jsii.get(self, "propertyGroups"))

    @property_groups.setter
    def property_groups(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.PropertyGroupProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36507cd81b3c73a3a55b64d8b8b5eda472ce5b6929f6f7ba9baa53055e83dcb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propertyGroups", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.DataConnectorProperty",
        jsii_struct_bases=[],
        name_mapping={"is_native": "isNative", "lambda_": "lambda"},
    )
    class DataConnectorProperty:
        def __init__(
            self,
            *,
            is_native: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            lambda_: typing.Optional[typing.Union[typing.Union["CfnComponentType.LambdaFunctionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''The data connector.

            :param is_native: A boolean value that specifies whether the data connector is native to IoT TwinMaker.
            :param lambda_: The Lambda function associated with the data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                data_connector_property = iottwinmaker.CfnComponentType.DataConnectorProperty(
                    is_native=False,
                    lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                        arn="arn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e095ca9ff9009a5ff6712910bff836e9c2473e499b8c06a1b4806c6ca1441915)
                check_type(argname="argument is_native", value=is_native, expected_type=type_hints["is_native"])
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_native is not None:
                self._values["is_native"] = is_native
            if lambda_ is not None:
                self._values["lambda_"] = lambda_

        @builtins.property
        def is_native(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''A boolean value that specifies whether the data connector is native to IoT TwinMaker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html#cfn-iottwinmaker-componenttype-dataconnector-isnative
            '''
            result = self._values.get("is_native")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.LambdaFunctionProperty", _IResolvable_da3f097b]]:
            '''The Lambda function associated with the data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-dataconnector.html#cfn-iottwinmaker-componenttype-dataconnector-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.LambdaFunctionProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataConnectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.DataTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "allowed_values": "allowedValues",
            "nested_type": "nestedType",
            "relationship": "relationship",
            "unit_of_measure": "unitOfMeasure",
        },
    )
    class DataTypeProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            allowed_values: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            nested_type: typing.Optional[typing.Union[typing.Union["CfnComponentType.DataTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            relationship: typing.Optional[typing.Union[typing.Union["CfnComponentType.RelationshipProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            unit_of_measure: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies the data type of a property.

            :param type: The underlying type of the data type. Valid Values: ``RELATIONSHIP | STRING | LONG | BOOLEAN | INTEGER | DOUBLE | LIST | MAP``
            :param allowed_values: The allowed values for this data type.
            :param nested_type: The nested type in the data type.
            :param relationship: A relationship that associates a component with another component.
            :param unit_of_measure: The unit of measure used in this data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # data_type_property_: iottwinmaker.CfnComponentType.DataTypeProperty
                # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
                # relationship_value: Any
                
                data_type_property = iottwinmaker.CfnComponentType.DataTypeProperty(
                    type="type",
                
                    # the properties below are optional
                    allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    nested_type=iottwinmaker.CfnComponentType.DataTypeProperty(
                        type="type",
                
                        # the properties below are optional
                        allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        unit_of_measure="unitOfMeasure"
                    ),
                    relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                        relationship_type="relationshipType",
                        target_component_type_id="targetComponentTypeId"
                    ),
                    unit_of_measure="unitOfMeasure"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__273be5e09d6f9d95c15698e5ec925c4c3ec65b0759e24097c34ef449c37a2c81)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument nested_type", value=nested_type, expected_type=type_hints["nested_type"])
                check_type(argname="argument relationship", value=relationship, expected_type=type_hints["relationship"])
                check_type(argname="argument unit_of_measure", value=unit_of_measure, expected_type=type_hints["unit_of_measure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if nested_type is not None:
                self._values["nested_type"] = nested_type
            if relationship is not None:
                self._values["relationship"] = relationship
            if unit_of_measure is not None:
                self._values["unit_of_measure"] = unit_of_measure

        @builtins.property
        def type(self) -> builtins.str:
            '''The underlying type of the data type.

            Valid Values: ``RELATIONSHIP | STRING | LONG | BOOLEAN | INTEGER | DOUBLE | LIST | MAP``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allowed_values(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_da3f097b]]]]:
            '''The allowed values for this data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def nested_type(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.DataTypeProperty", _IResolvable_da3f097b]]:
            '''The nested type in the data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-nestedtype
            '''
            result = self._values.get("nested_type")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.DataTypeProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def relationship(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.RelationshipProperty", _IResolvable_da3f097b]]:
            '''A relationship that associates a component with another component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-relationship
            '''
            result = self._values.get("relationship")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.RelationshipProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def unit_of_measure(self) -> typing.Optional[builtins.str]:
            '''The unit of measure used in this data type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datatype.html#cfn-iottwinmaker-componenttype-datatype-unitofmeasure
            '''
            result = self._values.get("unit_of_measure")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.DataValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "expression": "expression",
            "integer_value": "integerValue",
            "list_value": "listValue",
            "long_value": "longValue",
            "map_value": "mapValue",
            "relationship_value": "relationshipValue",
            "string_value": "stringValue",
        },
    )
    class DataValueProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[jsii.Number] = None,
            list_value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            long_value: typing.Optional[jsii.Number] = None,
            map_value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            relationship_value: typing.Any = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a value for a property.

            :param boolean_value: A boolean value.
            :param double_value: A double value.
            :param expression: An expression that produces the value.
            :param integer_value: An integer value.
            :param list_value: A list of multiple values.
            :param long_value: A long value.
            :param map_value: An object that maps strings to multiple ``DataValue`` objects.
            :param relationship_value: A value that relates a component to another component.
            :param string_value: A string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
                # relationship_value: Any
                
                data_value_property = iottwinmaker.CfnComponentType.DataValueProperty(
                    boolean_value=False,
                    double_value=123,
                    expression="expression",
                    integer_value=123,
                    list_value=[iottwinmaker.CfnComponentType.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    long_value=123,
                    map_value={
                        "map_value_key": iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )
                    },
                    relationship_value=relationship_value,
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a40a165220ec5d269b66d44c8fedc1d32d50ec3b5ffb0460c6bce31dbe65807b)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument list_value", value=list_value, expected_type=type_hints["list_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument map_value", value=map_value, expected_type=type_hints["map_value"])
                check_type(argname="argument relationship_value", value=relationship_value, expected_type=type_hints["relationship_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if expression is not None:
                self._values["expression"] = expression
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if list_value is not None:
                self._values["list_value"] = list_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if map_value is not None:
                self._values["map_value"] = map_value
            if relationship_value is not None:
                self._values["relationship_value"] = relationship_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''A boolean value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''A double value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''An expression that produces the value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[jsii.Number]:
            '''An integer value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def list_value(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_da3f097b]]]]:
            '''A list of multiple values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-listvalue
            '''
            result = self._values.get("list_value")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def map_value(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.DataValueProperty", _IResolvable_da3f097b]]]]:
            '''An object that maps strings to multiple ``DataValue`` objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-mapvalue
            '''
            result = self._values.get("map_value")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnComponentType.DataValueProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def relationship_value(self) -> typing.Any:
            '''A value that relates a component to another component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-relationshipvalue
            '''
            result = self._values.get("relationship_value")
            return typing.cast(typing.Any, result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-datavalue.html#cfn-iottwinmaker-componenttype-datavalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.ErrorProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param code: ``CfnComponentType.ErrorProperty.Code``.
            :param message: ``CfnComponentType.ErrorProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                error_property = iottwinmaker.CfnComponentType.ErrorProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34ba6dda94f512be388b31fafb7bdd74f4da3e6f6bfac56519dc5dd55c44080f)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.ErrorProperty.Code``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html#cfn-iottwinmaker-componenttype-error-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.ErrorProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-error.html#cfn-iottwinmaker-componenttype-error-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.FunctionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "implemented_by": "implementedBy",
            "required_properties": "requiredProperties",
            "scope": "scope",
        },
    )
    class FunctionProperty:
        def __init__(
            self,
            *,
            implemented_by: typing.Optional[typing.Union[typing.Union["CfnComponentType.DataConnectorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            required_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
            scope: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The function body.

            :param implemented_by: The data connector.
            :param required_properties: The required properties of the function.
            :param scope: The scope of the function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                function_property = iottwinmaker.CfnComponentType.FunctionProperty(
                    implemented_by=iottwinmaker.CfnComponentType.DataConnectorProperty(
                        is_native=False,
                        lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                            arn="arn"
                        )
                    ),
                    required_properties=["requiredProperties"],
                    scope="scope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a4e223e00848234f4d432d4b5f935b1dc442846c59536e19e08a436eff737f2)
                check_type(argname="argument implemented_by", value=implemented_by, expected_type=type_hints["implemented_by"])
                check_type(argname="argument required_properties", value=required_properties, expected_type=type_hints["required_properties"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if implemented_by is not None:
                self._values["implemented_by"] = implemented_by
            if required_properties is not None:
                self._values["required_properties"] = required_properties
            if scope is not None:
                self._values["scope"] = scope

        @builtins.property
        def implemented_by(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.DataConnectorProperty", _IResolvable_da3f097b]]:
            '''The data connector.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-implementedby
            '''
            result = self._values.get("implemented_by")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.DataConnectorProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def required_properties(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The required properties of the function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-requiredproperties
            '''
            result = self._values.get("required_properties")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The scope of the function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-function.html#cfn-iottwinmaker-componenttype-function-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.LambdaFunctionProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class LambdaFunctionProperty:
        def __init__(self, *, arn: builtins.str) -> None:
            '''The Lambda function.

            :param arn: The Lambda function ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-lambdafunction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                lambda_function_property = iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__011f4caacaac8a9678c7e6f682b14051c4e3f54b1af2a1a5fbc3725d3ec93be2)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "arn": arn,
            }

        @builtins.property
        def arn(self) -> builtins.str:
            '''The Lambda function ARN.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-lambdafunction.html#cfn-iottwinmaker-componenttype-lambdafunction-arn
            '''
            result = self._values.get("arn")
            assert result is not None, "Required property 'arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaFunctionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.PropertyDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configurations": "configurations",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "is_external_id": "isExternalId",
            "is_required_in_entity": "isRequiredInEntity",
            "is_stored_externally": "isStoredExternally",
            "is_time_series": "isTimeSeries",
        },
    )
    class PropertyDefinitionProperty:
        def __init__(
            self,
            *,
            configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
            data_type: typing.Optional[typing.Union[typing.Union["CfnComponentType.DataTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            default_value: typing.Optional[typing.Union[typing.Union["CfnComponentType.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            is_external_id: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_stored_externally: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_time_series: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''PropertyDefinition is an object that maps strings to the property definitions in the component type.

            :param configurations: A mapping that specifies configuration information about the property.
            :param data_type: ``CfnComponentType.PropertyDefinitionProperty.DataType``.
            :param default_value: A boolean value that specifies whether the property ID comes from an external data store.
            :param is_external_id: A boolean value that specifies whether the property ID comes from an external data store.
            :param is_required_in_entity: A boolean value that specifies whether the property is required in an entity.
            :param is_stored_externally: A boolean value that specifies whether the property is stored externally.
            :param is_time_series: A boolean value that specifies whether the property consists of time series data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # data_type_property_: iottwinmaker.CfnComponentType.DataTypeProperty
                # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
                # relationship_value: Any
                
                property_definition_property = iottwinmaker.CfnComponentType.PropertyDefinitionProperty(
                    configurations={
                        "configurations_key": "configurations"
                    },
                    data_type=iottwinmaker.CfnComponentType.DataTypeProperty(
                        type="type",
                
                        # the properties below are optional
                        allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        unit_of_measure="unitOfMeasure"
                    ),
                    default_value=iottwinmaker.CfnComponentType.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    ),
                    is_external_id=False,
                    is_required_in_entity=False,
                    is_stored_externally=False,
                    is_time_series=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f6468ee4b88bb9dcef8da418cc59d1b3fceed119d2e1ade2c3b9f57b529a31a)
                check_type(argname="argument configurations", value=configurations, expected_type=type_hints["configurations"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument is_external_id", value=is_external_id, expected_type=type_hints["is_external_id"])
                check_type(argname="argument is_required_in_entity", value=is_required_in_entity, expected_type=type_hints["is_required_in_entity"])
                check_type(argname="argument is_stored_externally", value=is_stored_externally, expected_type=type_hints["is_stored_externally"])
                check_type(argname="argument is_time_series", value=is_time_series, expected_type=type_hints["is_time_series"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configurations is not None:
                self._values["configurations"] = configurations
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if is_external_id is not None:
                self._values["is_external_id"] = is_external_id
            if is_required_in_entity is not None:
                self._values["is_required_in_entity"] = is_required_in_entity
            if is_stored_externally is not None:
                self._values["is_stored_externally"] = is_stored_externally
            if is_time_series is not None:
                self._values["is_time_series"] = is_time_series

        @builtins.property
        def configurations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
            '''A mapping that specifies configuration information about the property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-configurations
            '''
            result = self._values.get("configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def data_type(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.DataTypeProperty", _IResolvable_da3f097b]]:
            '''``CfnComponentType.PropertyDefinitionProperty.DataType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.DataTypeProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def default_value(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_da3f097b]]:
            '''A boolean value that specifies whether the property ID comes from an external data store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.DataValueProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def is_external_id(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''A boolean value that specifies whether the property ID comes from an external data store.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isexternalid
            '''
            result = self._values.get("is_external_id")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_required_in_entity(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''A boolean value that specifies whether the property is required in an entity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isrequiredinentity
            '''
            result = self._values.get("is_required_in_entity")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_stored_externally(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''A boolean value that specifies whether the property is stored externally.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-isstoredexternally
            '''
            result = self._values.get("is_stored_externally")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_time_series(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''A boolean value that specifies whether the property consists of time series data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertydefinition.html#cfn-iottwinmaker-componenttype-propertydefinition-istimeseries
            '''
            result = self._values.get("is_time_series")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.PropertyGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"group_type": "groupType", "property_names": "propertyNames"},
    )
    class PropertyGroupProperty:
        def __init__(
            self,
            *,
            group_type: typing.Optional[builtins.str] = None,
            property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The property group.

            :param group_type: The group type.
            :param property_names: The property names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                property_group_property = iottwinmaker.CfnComponentType.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d41c24934073ef871df6ba445dcdf9cc53474d18bc8a6abdf5a2e9cff4e25f22)
                check_type(argname="argument group_type", value=group_type, expected_type=type_hints["group_type"])
                check_type(argname="argument property_names", value=property_names, expected_type=type_hints["property_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_type is not None:
                self._values["group_type"] = group_type
            if property_names is not None:
                self._values["property_names"] = property_names

        @builtins.property
        def group_type(self) -> typing.Optional[builtins.str]:
            '''The group type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html#cfn-iottwinmaker-componenttype-propertygroup-grouptype
            '''
            result = self._values.get("group_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The property names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-propertygroup.html#cfn-iottwinmaker-componenttype-propertygroup-propertynames
            '''
            result = self._values.get("property_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.RelationshipProperty",
        jsii_struct_bases=[],
        name_mapping={
            "relationship_type": "relationshipType",
            "target_component_type_id": "targetComponentTypeId",
        },
    )
    class RelationshipProperty:
        def __init__(
            self,
            *,
            relationship_type: typing.Optional[builtins.str] = None,
            target_component_type_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a relationship with another component type.

            :param relationship_type: The type of the relationship.
            :param target_component_type_id: The ID of the target component type associated with this relationship.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                relationship_property = iottwinmaker.CfnComponentType.RelationshipProperty(
                    relationship_type="relationshipType",
                    target_component_type_id="targetComponentTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b47b99571be3f27c50e535a75cdfdf14ca06d5215f64fdf40109961b2293b546)
                check_type(argname="argument relationship_type", value=relationship_type, expected_type=type_hints["relationship_type"])
                check_type(argname="argument target_component_type_id", value=target_component_type_id, expected_type=type_hints["target_component_type_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if relationship_type is not None:
                self._values["relationship_type"] = relationship_type
            if target_component_type_id is not None:
                self._values["target_component_type_id"] = target_component_type_id

        @builtins.property
        def relationship_type(self) -> typing.Optional[builtins.str]:
            '''The type of the relationship.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html#cfn-iottwinmaker-componenttype-relationship-relationshiptype
            '''
            result = self._values.get("relationship_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_component_type_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the target component type associated with this relationship.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationship.html#cfn-iottwinmaker-componenttype-relationship-targetcomponenttypeid
            '''
            result = self._values.get("target_component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.RelationshipValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_component_name": "targetComponentName",
            "target_entity_id": "targetEntityId",
        },
    )
    class RelationshipValueProperty:
        def __init__(
            self,
            *,
            target_component_name: typing.Optional[builtins.str] = None,
            target_entity_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param target_component_name: ``CfnComponentType.RelationshipValueProperty.TargetComponentName``.
            :param target_entity_id: ``CfnComponentType.RelationshipValueProperty.TargetEntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationshipvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                relationship_value_property = iottwinmaker.CfnComponentType.RelationshipValueProperty(
                    target_component_name="targetComponentName",
                    target_entity_id="targetEntityId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dbc10d1d938365a15f08cf5a673508117d98b2ab0ecd5a788ee85722bda49a71)
                check_type(argname="argument target_component_name", value=target_component_name, expected_type=type_hints["target_component_name"])
                check_type(argname="argument target_entity_id", value=target_entity_id, expected_type=type_hints["target_entity_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_component_name is not None:
                self._values["target_component_name"] = target_component_name
            if target_entity_id is not None:
                self._values["target_entity_id"] = target_entity_id

        @builtins.property
        def target_component_name(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.RelationshipValueProperty.TargetComponentName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationshipvalue.html#cfn-iottwinmaker-componenttype-relationshipvalue-targetcomponentname
            '''
            result = self._values.get("target_component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_entity_id(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.RelationshipValueProperty.TargetEntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-relationshipvalue.html#cfn-iottwinmaker-componenttype-relationshipvalue-targetentityid
            '''
            result = self._values.get("target_entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentType.StatusProperty",
        jsii_struct_bases=[],
        name_mapping={"error": "error", "state": "state"},
    )
    class StatusProperty:
        def __init__(
            self,
            *,
            error: typing.Optional[typing.Union[typing.Union["CfnComponentType.ErrorProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param error: ``CfnComponentType.StatusProperty.Error``.
            :param state: ``CfnComponentType.StatusProperty.State``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                status_property = iottwinmaker.CfnComponentType.StatusProperty(
                    error=iottwinmaker.CfnComponentType.ErrorProperty(
                        code="code",
                        message="message"
                    ),
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac6fe13a7b05f6856183480bafda65ea9e1351e2adfec7908b91529e2228a26c)
                check_type(argname="argument error", value=error, expected_type=type_hints["error"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error is not None:
                self._values["error"] = error
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def error(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentType.ErrorProperty", _IResolvable_da3f097b]]:
            '''``CfnComponentType.StatusProperty.Error``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html#cfn-iottwinmaker-componenttype-status-error
            '''
            result = self._values.get("error")
            return typing.cast(typing.Optional[typing.Union["CfnComponentType.ErrorProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''``CfnComponentType.StatusProperty.State``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-componenttype-status.html#cfn-iottwinmaker-componenttype-status-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnComponentTypeProps",
    jsii_struct_bases=[],
    name_mapping={
        "component_type_id": "componentTypeId",
        "workspace_id": "workspaceId",
        "description": "description",
        "extends_from": "extendsFrom",
        "functions": "functions",
        "is_singleton": "isSingleton",
        "property_definitions": "propertyDefinitions",
        "property_groups": "propertyGroups",
        "tags": "tags",
    },
)
class CfnComponentTypeProps:
    def __init__(
        self,
        *,
        component_type_id: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
        functions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        is_singleton: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        property_definitions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        property_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnComponentType``.

        :param component_type_id: The ID of the component type.
        :param workspace_id: The ID of the workspace.
        :param description: The description of the component type.
        :param extends_from: The name of the parent component type that this component type extends.
        :param functions: An object that maps strings to the functions in the component type. Each string in the mapping must be unique to this object. For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.
        :param is_singleton: A boolean value that specifies whether an entity can have more than one component of this type.
        :param property_definitions: An object that maps strings to the property definitions in the component type. Each string in the mapping must be unique to this object. For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.
        :param property_groups: An object that maps strings to the property groups in the component type. Each string in the mapping must be unique to this object.
        :param tags: The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_iottwinmaker as iottwinmaker
            
            # data_type_property_: iottwinmaker.CfnComponentType.DataTypeProperty
            # data_value_property_: iottwinmaker.CfnComponentType.DataValueProperty
            # relationship_value: Any
            
            cfn_component_type_props = iottwinmaker.CfnComponentTypeProps(
                component_type_id="componentTypeId",
                workspace_id="workspaceId",
            
                # the properties below are optional
                description="description",
                extends_from=["extendsFrom"],
                functions={
                    "functions_key": iottwinmaker.CfnComponentType.FunctionProperty(
                        implemented_by=iottwinmaker.CfnComponentType.DataConnectorProperty(
                            is_native=False,
                            lambda_=iottwinmaker.CfnComponentType.LambdaFunctionProperty(
                                arn="arn"
                            )
                        ),
                        required_properties=["requiredProperties"],
                        scope="scope"
                    )
                },
                is_singleton=False,
                property_definitions={
                    "property_definitions_key": iottwinmaker.CfnComponentType.PropertyDefinitionProperty(
                        configurations={
                            "configurations_key": "configurations"
                        },
                        data_type=iottwinmaker.CfnComponentType.DataTypeProperty(
                            type="type",
            
                            # the properties below are optional
                            allowed_values=[iottwinmaker.CfnComponentType.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )],
                            nested_type=data_type_property_,
                            relationship=iottwinmaker.CfnComponentType.RelationshipProperty(
                                relationship_type="relationshipType",
                                target_component_type_id="targetComponentTypeId"
                            ),
                            unit_of_measure="unitOfMeasure"
                        ),
                        default_value=iottwinmaker.CfnComponentType.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        ),
                        is_external_id=False,
                        is_required_in_entity=False,
                        is_stored_externally=False,
                        is_time_series=False
                    )
                },
                property_groups={
                    "property_groups_key": iottwinmaker.CfnComponentType.PropertyGroupProperty(
                        group_type="groupType",
                        property_names=["propertyNames"]
                    )
                },
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__324a0cc887ec1065b9d5ba872572072fa8c481530426ba50811e338f2dde6f9b)
            check_type(argname="argument component_type_id", value=component_type_id, expected_type=type_hints["component_type_id"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument extends_from", value=extends_from, expected_type=type_hints["extends_from"])
            check_type(argname="argument functions", value=functions, expected_type=type_hints["functions"])
            check_type(argname="argument is_singleton", value=is_singleton, expected_type=type_hints["is_singleton"])
            check_type(argname="argument property_definitions", value=property_definitions, expected_type=type_hints["property_definitions"])
            check_type(argname="argument property_groups", value=property_groups, expected_type=type_hints["property_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_type_id": component_type_id,
            "workspace_id": workspace_id,
        }
        if description is not None:
            self._values["description"] = description
        if extends_from is not None:
            self._values["extends_from"] = extends_from
        if functions is not None:
            self._values["functions"] = functions
        if is_singleton is not None:
            self._values["is_singleton"] = is_singleton
        if property_definitions is not None:
            self._values["property_definitions"] = property_definitions
        if property_groups is not None:
            self._values["property_groups"] = property_groups
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def component_type_id(self) -> builtins.str:
        '''The ID of the component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-componenttypeid
        '''
        result = self._values.get("component_type_id")
        assert result is not None, "Required property 'component_type_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extends_from(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the parent component type that this component type extends.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-extendsfrom
        '''
        result = self._values.get("extends_from")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def functions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.FunctionProperty, _IResolvable_da3f097b]]]]:
        '''An object that maps strings to the functions in the component type.

        Each string in the mapping must be unique to this object.

        For information on the FunctionResponse object see the `FunctionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_FunctionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-functions
        '''
        result = self._values.get("functions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.FunctionProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def is_singleton(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
        '''A boolean value that specifies whether an entity can have more than one component of this type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-issingleton
        '''
        result = self._values.get("is_singleton")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

    @builtins.property
    def property_definitions(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyDefinitionProperty, _IResolvable_da3f097b]]]]:
        '''An object that maps strings to the property definitions in the component type.

        Each string in the mapping must be unique to this object.

        For information about the PropertyDefinitionResponse object, see the `PropertyDefinitionResponse <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_PropertyDefinitionResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertydefinitions
        '''
        result = self._values.get("property_definitions")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyDefinitionProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def property_groups(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyGroupProperty, _IResolvable_da3f097b]]]]:
        '''An object that maps strings to the property groups in the component type.

        Each string in the mapping must be unique to this object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-propertygroups
        '''
        result = self._values.get("property_groups")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyGroupProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-componenttype.html#cfn-iottwinmaker-componenttype-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComponentTypeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnEntity(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Entity``.

    Use the ``AWS::IoTTwinMaker::Entity`` resource to declare an entity.

    :cloudformationResource: AWS::IoTTwinMaker::Entity
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_iottwinmaker as iottwinmaker
        
        # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
        # definition: Any
        # error: Any
        # relationship_value: Any
        
        cfn_entity = iottwinmaker.CfnEntity(self, "MyCfnEntity",
            entity_name="entityName",
            workspace_id="workspaceId",
        
            # the properties below are optional
            components={
                "components_key": iottwinmaker.CfnEntity.ComponentProperty(
                    component_name="componentName",
                    component_type_id="componentTypeId",
                    defined_in="definedIn",
                    description="description",
                    properties={
                        "properties_key": iottwinmaker.CfnEntity.PropertyProperty(
                            definition=definition,
                            value=iottwinmaker.CfnEntity.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )
                        )
                    },
                    property_groups={
                        "property_groups_key": iottwinmaker.CfnEntity.PropertyGroupProperty(
                            group_type="groupType",
                            property_names=["propertyNames"]
                        )
                    },
                    status=iottwinmaker.CfnEntity.StatusProperty(
                        error=error,
                        state="state"
                    )
                )
            },
            description="description",
            entity_id="entityId",
            parent_entity_id="parentEntityId",
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
        entity_name: builtins.str,
        workspace_id: builtins.str,
        components: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnEntity.ComponentProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        description: typing.Optional[builtins.str] = None,
        entity_id: typing.Optional[builtins.str] = None,
        parent_entity_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::Entity``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param entity_name: The entity name.
        :param workspace_id: The ID of the workspace.
        :param components: An object that maps strings to the components in the entity. Each string in the mapping must be unique to this object. For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.
        :param description: The description of the entity.
        :param entity_id: The entity ID.
        :param parent_entity_id: The ID of the parent entity.
        :param tags: Metadata that you can use to manage the entity.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e1a29b5ee0db8b0f9fe80447cc93db85e2ed400b28a3c61bfca379d292ea661)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEntityProps(
            entity_name=entity_name,
            workspace_id=workspace_id,
            components=components,
            description=description,
            entity_id=entity_id,
            parent_entity_id=parent_entity_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e51d270d4440681d46f1e667f106ed384931f38df7092845daad0ed9f82b4739)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4e6df7cdcbaa7bb71c0f98e6b81417fbefaaee9fa2525cc6d3e448f5fb8a0ac)
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
        '''The entity ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time the entity was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrHasChildEntities")
    def attr_has_child_entities(self) -> _IResolvable_da3f097b:
        '''A boolean value that specifies whether the entity has child entities or not.

        :cloudformationAttribute: HasChildEntities
        '''
        return typing.cast(_IResolvable_da3f097b, jsii.get(self, "attrHasChildEntities"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusErrorCode")
    def attr_status_error_code(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.Error.Code
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusErrorCode"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusErrorMessage")
    def attr_status_error_message(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.Error.Message
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusErrorMessage"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusState")
    def attr_status_state(self) -> builtins.str:
        '''
        :cloudformationAttribute: Status.State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The date and time when the component type was last updated.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''Metadata that you can use to manage the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="entityName")
    def entity_name(self) -> builtins.str:
        '''The entity name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityname
        '''
        return typing.cast(builtins.str, jsii.get(self, "entityName"))

    @entity_name.setter
    def entity_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b22be6154cc92786e71f5ade2798dfd6ec3b1454e285e563bb83c7b6cd4f165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityName", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc57b76e292f6e6cc6693d0d00219ab00040aa359ab079b08cd8f04ada9f78e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.ComponentProperty", _IResolvable_da3f097b]]]]:
        '''An object that maps strings to the components in the entity.

        Each string in the mapping must be unique to this object.

        For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-components
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.ComponentProperty", _IResolvable_da3f097b]]]], jsii.get(self, "components"))

    @components.setter
    def components(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.ComponentProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d33ce5aae02e9b9d53db2dc6a1f173aca65b2d0541e1f42ac4dcedca4032bbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c066a8d095e32951abe069a62394d16267b44a974544cb8a532331626aca268f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="entityId")
    def entity_id(self) -> typing.Optional[builtins.str]:
        '''The entity ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entityId"))

    @entity_id.setter
    def entity_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c2c2a1d07260ab64ca67bbdcc394460319d917fbad0788d8c84e729a4f0010)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entityId", value)

    @builtins.property
    @jsii.member(jsii_name="parentEntityId")
    def parent_entity_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the parent entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-parententityid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentEntityId"))

    @parent_entity_id.setter
    def parent_entity_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838f65778509f9139a5dfa429adefddf900b5f2f386b0122e5f5c57ccbe5ef86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentEntityId", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.ComponentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_name": "componentName",
            "component_type_id": "componentTypeId",
            "defined_in": "definedIn",
            "description": "description",
            "properties": "properties",
            "property_groups": "propertyGroups",
            "status": "status",
        },
    )
    class ComponentProperty:
        def __init__(
            self,
            *,
            component_name: typing.Optional[builtins.str] = None,
            component_type_id: typing.Optional[builtins.str] = None,
            defined_in: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            properties: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnEntity.PropertyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            property_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnEntity.PropertyGroupProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            status: typing.Optional[typing.Union[typing.Union["CfnEntity.StatusProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''The entity component.

            :param component_name: The name of the component.
            :param component_type_id: The ID of the ComponentType.
            :param defined_in: The name of the property definition set in the request.
            :param description: The description of the component.
            :param properties: An object that maps strings to the properties to set in the component type. Each string in the mapping must be unique to this object.
            :param property_groups: An object that maps strings to the property groups in the component type. Each string in the mapping must be unique to this object.
            :param status: The status of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # definition: Any
                # error: Any
                # relationship_value: Any
                
                component_property = iottwinmaker.CfnEntity.ComponentProperty(
                    component_name="componentName",
                    component_type_id="componentTypeId",
                    defined_in="definedIn",
                    description="description",
                    properties={
                        "properties_key": iottwinmaker.CfnEntity.PropertyProperty(
                            definition=definition,
                            value=iottwinmaker.CfnEntity.DataValueProperty(
                                boolean_value=False,
                                double_value=123,
                                expression="expression",
                                integer_value=123,
                                list_value=[data_value_property_],
                                long_value=123,
                                map_value={
                                    "map_value_key": data_value_property_
                                },
                                relationship_value=relationship_value,
                                string_value="stringValue"
                            )
                        )
                    },
                    property_groups={
                        "property_groups_key": iottwinmaker.CfnEntity.PropertyGroupProperty(
                            group_type="groupType",
                            property_names=["propertyNames"]
                        )
                    },
                    status=iottwinmaker.CfnEntity.StatusProperty(
                        error=error,
                        state="state"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5940403f2280c2499fc9c10c883fa2fcac0dd0a9bf77111ee145480c06c9f15)
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument component_type_id", value=component_type_id, expected_type=type_hints["component_type_id"])
                check_type(argname="argument defined_in", value=defined_in, expected_type=type_hints["defined_in"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
                check_type(argname="argument property_groups", value=property_groups, expected_type=type_hints["property_groups"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_name is not None:
                self._values["component_name"] = component_name
            if component_type_id is not None:
                self._values["component_type_id"] = component_type_id
            if defined_in is not None:
                self._values["defined_in"] = defined_in
            if description is not None:
                self._values["description"] = description
            if properties is not None:
                self._values["properties"] = properties
            if property_groups is not None:
                self._values["property_groups"] = property_groups
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_type_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the ComponentType.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-componenttypeid
            '''
            result = self._values.get("component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def defined_in(self) -> typing.Optional[builtins.str]:
            '''The name of the property definition set in the request.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-definedin
            '''
            result = self._values.get("defined_in")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def properties(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.PropertyProperty", _IResolvable_da3f097b]]]]:
            '''An object that maps strings to the properties to set in the component type.

            Each string in the mapping must be unique to this object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-properties
            '''
            result = self._values.get("properties")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.PropertyProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def property_groups(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.PropertyGroupProperty", _IResolvable_da3f097b]]]]:
            '''An object that maps strings to the property groups in the component type.

            Each string in the mapping must be unique to this object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-propertygroups
            '''
            result = self._values.get("property_groups")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.PropertyGroupProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def status(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.StatusProperty", _IResolvable_da3f097b]]:
            '''The status of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-component.html#cfn-iottwinmaker-entity-component-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.StatusProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.DataTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_values": "allowedValues",
            "nested_type": "nestedType",
            "relationship": "relationship",
            "type": "type",
            "unit_of_measure": "unitOfMeasure",
        },
    )
    class DataTypeProperty:
        def __init__(
            self,
            *,
            allowed_values: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            nested_type: typing.Optional[typing.Union[typing.Union["CfnEntity.DataTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            relationship: typing.Optional[typing.Union[typing.Union["CfnEntity.RelationshipProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            type: typing.Optional[builtins.str] = None,
            unit_of_measure: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param allowed_values: ``CfnEntity.DataTypeProperty.AllowedValues``.
            :param nested_type: ``CfnEntity.DataTypeProperty.NestedType``.
            :param relationship: ``CfnEntity.DataTypeProperty.Relationship``.
            :param type: ``CfnEntity.DataTypeProperty.Type``.
            :param unit_of_measure: ``CfnEntity.DataTypeProperty.UnitOfMeasure``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # data_type_property_: iottwinmaker.CfnEntity.DataTypeProperty
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # relationship_value: Any
                
                data_type_property = iottwinmaker.CfnEntity.DataTypeProperty(
                    allowed_values=[iottwinmaker.CfnEntity.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    nested_type=iottwinmaker.CfnEntity.DataTypeProperty(
                        allowed_values=[iottwinmaker.CfnEntity.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnEntity.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        type="type",
                        unit_of_measure="unitOfMeasure"
                    ),
                    relationship=iottwinmaker.CfnEntity.RelationshipProperty(
                        relationship_type="relationshipType",
                        target_component_type_id="targetComponentTypeId"
                    ),
                    type="type",
                    unit_of_measure="unitOfMeasure"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9c5ea634d5e6bd56e791cf605b04f67fafafb43348fa60e51ac9a7c41739999)
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument nested_type", value=nested_type, expected_type=type_hints["nested_type"])
                check_type(argname="argument relationship", value=relationship, expected_type=type_hints["relationship"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument unit_of_measure", value=unit_of_measure, expected_type=type_hints["unit_of_measure"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if nested_type is not None:
                self._values["nested_type"] = nested_type
            if relationship is not None:
                self._values["relationship"] = relationship
            if type is not None:
                self._values["type"] = type
            if unit_of_measure is not None:
                self._values["unit_of_measure"] = unit_of_measure

        @builtins.property
        def allowed_values(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]]]]:
            '''``CfnEntity.DataTypeProperty.AllowedValues``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def nested_type(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.DataTypeProperty", _IResolvable_da3f097b]]:
            '''``CfnEntity.DataTypeProperty.NestedType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-nestedtype
            '''
            result = self._values.get("nested_type")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.DataTypeProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def relationship(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.RelationshipProperty", _IResolvable_da3f097b]]:
            '''``CfnEntity.DataTypeProperty.Relationship``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-relationship
            '''
            result = self._values.get("relationship")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.RelationshipProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.DataTypeProperty.Type``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit_of_measure(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.DataTypeProperty.UnitOfMeasure``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datatype.html#cfn-iottwinmaker-entity-datatype-unitofmeasure
            '''
            result = self._values.get("unit_of_measure")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.DataValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "expression": "expression",
            "integer_value": "integerValue",
            "list_value": "listValue",
            "long_value": "longValue",
            "map_value": "mapValue",
            "relationship_value": "relationshipValue",
            "string_value": "stringValue",
        },
    )
    class DataValueProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            expression: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[jsii.Number] = None,
            list_value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            long_value: typing.Optional[jsii.Number] = None,
            map_value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            relationship_value: typing.Any = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that specifies a value for a property.

            :param boolean_value: A boolean value.
            :param double_value: A double value.
            :param expression: An expression that produces the value.
            :param integer_value: An integer value.
            :param list_value: A list of multiple values.
            :param long_value: A long value.
            :param map_value: An object that maps strings to multiple DataValue objects.
            :param relationship_value: A value that relates a component to another component.
            :param string_value: A string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # relationship_value: Any
                
                data_value_property = iottwinmaker.CfnEntity.DataValueProperty(
                    boolean_value=False,
                    double_value=123,
                    expression="expression",
                    integer_value=123,
                    list_value=[iottwinmaker.CfnEntity.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )],
                    long_value=123,
                    map_value={
                        "map_value_key": iottwinmaker.CfnEntity.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )
                    },
                    relationship_value=relationship_value,
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bee2e6498d955df8493500bf9e927820daa7a2e32fb446fcd06dfea586442db8)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument list_value", value=list_value, expected_type=type_hints["list_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument map_value", value=map_value, expected_type=type_hints["map_value"])
                check_type(argname="argument relationship_value", value=relationship_value, expected_type=type_hints["relationship_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if expression is not None:
                self._values["expression"] = expression
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if list_value is not None:
                self._values["list_value"] = list_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if map_value is not None:
                self._values["map_value"] = map_value
            if relationship_value is not None:
                self._values["relationship_value"] = relationship_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''A boolean value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''A double value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''An expression that produces the value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[jsii.Number]:
            '''An integer value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def list_value(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]]]]:
            '''A list of multiple values.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-listvalue
            '''
            result = self._values.get("list_value")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def map_value(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]]]]:
            '''An object that maps strings to multiple DataValue objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-mapvalue
            '''
            result = self._values.get("map_value")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def relationship_value(self) -> typing.Any:
            '''A value that relates a component to another component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-relationshipvalue
            '''
            result = self._values.get("relationship_value")
            return typing.cast(typing.Any, result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-datavalue.html#cfn-iottwinmaker-entity-datavalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.DefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "configuration": "configuration",
            "data_type": "dataType",
            "default_value": "defaultValue",
            "is_external_id": "isExternalId",
            "is_final": "isFinal",
            "is_imported": "isImported",
            "is_inherited": "isInherited",
            "is_required_in_entity": "isRequiredInEntity",
            "is_stored_externally": "isStoredExternally",
            "is_time_series": "isTimeSeries",
        },
    )
    class DefinitionProperty:
        def __init__(
            self,
            *,
            configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
            data_type: typing.Optional[typing.Union[typing.Union["CfnEntity.DataTypeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            default_value: typing.Optional[typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            is_external_id: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_final: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_imported: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_inherited: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_stored_externally: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            is_time_series: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''
            :param configuration: ``CfnEntity.DefinitionProperty.Configuration``.
            :param data_type: ``CfnEntity.DefinitionProperty.DataType``.
            :param default_value: ``CfnEntity.DefinitionProperty.DefaultValue``.
            :param is_external_id: ``CfnEntity.DefinitionProperty.IsExternalId``.
            :param is_final: ``CfnEntity.DefinitionProperty.IsFinal``.
            :param is_imported: ``CfnEntity.DefinitionProperty.IsImported``.
            :param is_inherited: ``CfnEntity.DefinitionProperty.IsInherited``.
            :param is_required_in_entity: ``CfnEntity.DefinitionProperty.IsRequiredInEntity``.
            :param is_stored_externally: ``CfnEntity.DefinitionProperty.IsStoredExternally``.
            :param is_time_series: ``CfnEntity.DefinitionProperty.IsTimeSeries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # data_type_property_: iottwinmaker.CfnEntity.DataTypeProperty
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # relationship_value: Any
                
                definition_property = iottwinmaker.CfnEntity.DefinitionProperty(
                    configuration={
                        "configuration_key": "configuration"
                    },
                    data_type=iottwinmaker.CfnEntity.DataTypeProperty(
                        allowed_values=[iottwinmaker.CfnEntity.DataValueProperty(
                            boolean_value=False,
                            double_value=123,
                            expression="expression",
                            integer_value=123,
                            list_value=[data_value_property_],
                            long_value=123,
                            map_value={
                                "map_value_key": data_value_property_
                            },
                            relationship_value=relationship_value,
                            string_value="stringValue"
                        )],
                        nested_type=data_type_property_,
                        relationship=iottwinmaker.CfnEntity.RelationshipProperty(
                            relationship_type="relationshipType",
                            target_component_type_id="targetComponentTypeId"
                        ),
                        type="type",
                        unit_of_measure="unitOfMeasure"
                    ),
                    default_value=iottwinmaker.CfnEntity.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    ),
                    is_external_id=False,
                    is_final=False,
                    is_imported=False,
                    is_inherited=False,
                    is_required_in_entity=False,
                    is_stored_externally=False,
                    is_time_series=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__347d62ba072131593e5021b7610bb93a0bbad5f67a110b1404655f0235ef81eb)
                check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument is_external_id", value=is_external_id, expected_type=type_hints["is_external_id"])
                check_type(argname="argument is_final", value=is_final, expected_type=type_hints["is_final"])
                check_type(argname="argument is_imported", value=is_imported, expected_type=type_hints["is_imported"])
                check_type(argname="argument is_inherited", value=is_inherited, expected_type=type_hints["is_inherited"])
                check_type(argname="argument is_required_in_entity", value=is_required_in_entity, expected_type=type_hints["is_required_in_entity"])
                check_type(argname="argument is_stored_externally", value=is_stored_externally, expected_type=type_hints["is_stored_externally"])
                check_type(argname="argument is_time_series", value=is_time_series, expected_type=type_hints["is_time_series"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration is not None:
                self._values["configuration"] = configuration
            if data_type is not None:
                self._values["data_type"] = data_type
            if default_value is not None:
                self._values["default_value"] = default_value
            if is_external_id is not None:
                self._values["is_external_id"] = is_external_id
            if is_final is not None:
                self._values["is_final"] = is_final
            if is_imported is not None:
                self._values["is_imported"] = is_imported
            if is_inherited is not None:
                self._values["is_inherited"] = is_inherited
            if is_required_in_entity is not None:
                self._values["is_required_in_entity"] = is_required_in_entity
            if is_stored_externally is not None:
                self._values["is_stored_externally"] = is_stored_externally
            if is_time_series is not None:
                self._values["is_time_series"] = is_time_series

        @builtins.property
        def configuration(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]]:
            '''``CfnEntity.DefinitionProperty.Configuration``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-configuration
            '''
            result = self._values.get("configuration")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def data_type(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.DataTypeProperty", _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.DataType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.DataTypeProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def default_value(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.DefaultValue``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def is_external_id(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.IsExternalId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isexternalid
            '''
            result = self._values.get("is_external_id")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_final(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.IsFinal``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isfinal
            '''
            result = self._values.get("is_final")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_imported(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.IsImported``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isimported
            '''
            result = self._values.get("is_imported")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_inherited(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.IsInherited``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isinherited
            '''
            result = self._values.get("is_inherited")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_required_in_entity(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.IsRequiredInEntity``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isrequiredinentity
            '''
            result = self._values.get("is_required_in_entity")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_stored_externally(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.IsStoredExternally``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-isstoredexternally
            '''
            result = self._values.get("is_stored_externally")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def is_time_series(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``CfnEntity.DefinitionProperty.IsTimeSeries``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-definition.html#cfn-iottwinmaker-entity-definition-istimeseries
            '''
            result = self._values.get("is_time_series")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.ErrorProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param code: ``CfnEntity.ErrorProperty.Code``.
            :param message: ``CfnEntity.ErrorProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                error_property = iottwinmaker.CfnEntity.ErrorProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c778853c1f1dbe9882df8a699b0e19cdd214f25fb32899ce13b88ddc29191712)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.ErrorProperty.Code``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html#cfn-iottwinmaker-entity-error-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.ErrorProperty.Message``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-error.html#cfn-iottwinmaker-entity-error-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.PropertyGroupProperty",
        jsii_struct_bases=[],
        name_mapping={"group_type": "groupType", "property_names": "propertyNames"},
    )
    class PropertyGroupProperty:
        def __init__(
            self,
            *,
            group_type: typing.Optional[builtins.str] = None,
            property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The property group.

            :param group_type: The group type.
            :param property_names: The property names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                property_group_property = iottwinmaker.CfnEntity.PropertyGroupProperty(
                    group_type="groupType",
                    property_names=["propertyNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42db694573f925f93c6b240c30df8cabf5a4960ff073e14a5a7cfdcf955374f1)
                check_type(argname="argument group_type", value=group_type, expected_type=type_hints["group_type"])
                check_type(argname="argument property_names", value=property_names, expected_type=type_hints["property_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_type is not None:
                self._values["group_type"] = group_type
            if property_names is not None:
                self._values["property_names"] = property_names

        @builtins.property
        def group_type(self) -> typing.Optional[builtins.str]:
            '''The group type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html#cfn-iottwinmaker-entity-propertygroup-grouptype
            '''
            result = self._values.get("group_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The property names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-propertygroup.html#cfn-iottwinmaker-entity-propertygroup-propertynames
            '''
            result = self._values.get("property_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.PropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition", "value": "value"},
    )
    class PropertyProperty:
        def __init__(
            self,
            *,
            definition: typing.Any = None,
            value: typing.Optional[typing.Union[typing.Union["CfnEntity.DataValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''An object that sets information about a property.

            :param definition: An object that specifies information about a property.
            :param value: An object that contains information about a value for a time series property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
                # definition: Any
                # relationship_value: Any
                
                property_property = iottwinmaker.CfnEntity.PropertyProperty(
                    definition=definition,
                    value=iottwinmaker.CfnEntity.DataValueProperty(
                        boolean_value=False,
                        double_value=123,
                        expression="expression",
                        integer_value=123,
                        list_value=[data_value_property_],
                        long_value=123,
                        map_value={
                            "map_value_key": data_value_property_
                        },
                        relationship_value=relationship_value,
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24a9328bc8f6cfe5025ae4d451c1d5700ea92588c53715a2a735d8c9e887e52f)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def definition(self) -> typing.Any:
            '''An object that specifies information about a property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html#cfn-iottwinmaker-entity-property-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Any, result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]]:
            '''An object that contains information about a value for a time series property.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-property.html#cfn-iottwinmaker-entity-property-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union["CfnEntity.DataValueProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.RelationshipProperty",
        jsii_struct_bases=[],
        name_mapping={
            "relationship_type": "relationshipType",
            "target_component_type_id": "targetComponentTypeId",
        },
    )
    class RelationshipProperty:
        def __init__(
            self,
            *,
            relationship_type: typing.Optional[builtins.str] = None,
            target_component_type_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param relationship_type: ``CfnEntity.RelationshipProperty.RelationshipType``.
            :param target_component_type_id: ``CfnEntity.RelationshipProperty.TargetComponentTypeId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationship.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                relationship_property = iottwinmaker.CfnEntity.RelationshipProperty(
                    relationship_type="relationshipType",
                    target_component_type_id="targetComponentTypeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a2669a78539a59c9601ed42020c3074fd1666a65003972ddee491b7be87a32e)
                check_type(argname="argument relationship_type", value=relationship_type, expected_type=type_hints["relationship_type"])
                check_type(argname="argument target_component_type_id", value=target_component_type_id, expected_type=type_hints["target_component_type_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if relationship_type is not None:
                self._values["relationship_type"] = relationship_type
            if target_component_type_id is not None:
                self._values["target_component_type_id"] = target_component_type_id

        @builtins.property
        def relationship_type(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.RelationshipProperty.RelationshipType``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationship.html#cfn-iottwinmaker-entity-relationship-relationshiptype
            '''
            result = self._values.get("relationship_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_component_type_id(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.RelationshipProperty.TargetComponentTypeId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationship.html#cfn-iottwinmaker-entity-relationship-targetcomponenttypeid
            '''
            result = self._values.get("target_component_type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.RelationshipValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_component_name": "targetComponentName",
            "target_entity_id": "targetEntityId",
        },
    )
    class RelationshipValueProperty:
        def __init__(
            self,
            *,
            target_component_name: typing.Optional[builtins.str] = None,
            target_entity_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param target_component_name: ``CfnEntity.RelationshipValueProperty.TargetComponentName``.
            :param target_entity_id: ``CfnEntity.RelationshipValueProperty.TargetEntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationshipvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                relationship_value_property = iottwinmaker.CfnEntity.RelationshipValueProperty(
                    target_component_name="targetComponentName",
                    target_entity_id="targetEntityId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__50e51369cd4e121c1c1511111247d4d515d7e3f546b629cf0107d91fc3da672d)
                check_type(argname="argument target_component_name", value=target_component_name, expected_type=type_hints["target_component_name"])
                check_type(argname="argument target_entity_id", value=target_entity_id, expected_type=type_hints["target_entity_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_component_name is not None:
                self._values["target_component_name"] = target_component_name
            if target_entity_id is not None:
                self._values["target_entity_id"] = target_entity_id

        @builtins.property
        def target_component_name(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.RelationshipValueProperty.TargetComponentName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationshipvalue.html#cfn-iottwinmaker-entity-relationshipvalue-targetcomponentname
            '''
            result = self._values.get("target_component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_entity_id(self) -> typing.Optional[builtins.str]:
            '''``CfnEntity.RelationshipValueProperty.TargetEntityId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-relationshipvalue.html#cfn-iottwinmaker-entity-relationshipvalue-targetentityid
            '''
            result = self._values.get("target_entity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationshipValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntity.StatusProperty",
        jsii_struct_bases=[],
        name_mapping={"error": "error", "state": "state"},
    )
    class StatusProperty:
        def __init__(
            self,
            *,
            error: typing.Any = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The current status of the entity.

            :param error: The error message.
            :param state: The current state of the entity, component, component type, or workspace. Valid Values: ``CREATING | UPDATING | DELETING | ACTIVE | ERROR``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_iottwinmaker as iottwinmaker
                
                # error: Any
                
                status_property = iottwinmaker.CfnEntity.StatusProperty(
                    error=error,
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28ab81751c1d2e7e539a71d287760369286bfc3d825eeb956567885e8536f4b1)
                check_type(argname="argument error", value=error, expected_type=type_hints["error"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if error is not None:
                self._values["error"] = error
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def error(self) -> typing.Any:
            '''The error message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html#cfn-iottwinmaker-entity-status-error
            '''
            result = self._values.get("error")
            return typing.cast(typing.Any, result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The current state of the entity, component, component type, or workspace.

            Valid Values: ``CREATING | UPDATING | DELETING | ACTIVE | ERROR``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iottwinmaker-entity-status.html#cfn-iottwinmaker-entity-status-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnEntityProps",
    jsii_struct_bases=[],
    name_mapping={
        "entity_name": "entityName",
        "workspace_id": "workspaceId",
        "components": "components",
        "description": "description",
        "entity_id": "entityId",
        "parent_entity_id": "parentEntityId",
        "tags": "tags",
    },
)
class CfnEntityProps:
    def __init__(
        self,
        *,
        entity_name: builtins.str,
        workspace_id: builtins.str,
        components: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        description: typing.Optional[builtins.str] = None,
        entity_id: typing.Optional[builtins.str] = None,
        parent_entity_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEntity``.

        :param entity_name: The entity name.
        :param workspace_id: The ID of the workspace.
        :param components: An object that maps strings to the components in the entity. Each string in the mapping must be unique to this object. For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.
        :param description: The description of the entity.
        :param entity_id: The entity ID.
        :param parent_entity_id: The ID of the parent entity.
        :param tags: Metadata that you can use to manage the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_iottwinmaker as iottwinmaker
            
            # data_value_property_: iottwinmaker.CfnEntity.DataValueProperty
            # definition: Any
            # error: Any
            # relationship_value: Any
            
            cfn_entity_props = iottwinmaker.CfnEntityProps(
                entity_name="entityName",
                workspace_id="workspaceId",
            
                # the properties below are optional
                components={
                    "components_key": iottwinmaker.CfnEntity.ComponentProperty(
                        component_name="componentName",
                        component_type_id="componentTypeId",
                        defined_in="definedIn",
                        description="description",
                        properties={
                            "properties_key": iottwinmaker.CfnEntity.PropertyProperty(
                                definition=definition,
                                value=iottwinmaker.CfnEntity.DataValueProperty(
                                    boolean_value=False,
                                    double_value=123,
                                    expression="expression",
                                    integer_value=123,
                                    list_value=[data_value_property_],
                                    long_value=123,
                                    map_value={
                                        "map_value_key": data_value_property_
                                    },
                                    relationship_value=relationship_value,
                                    string_value="stringValue"
                                )
                            )
                        },
                        property_groups={
                            "property_groups_key": iottwinmaker.CfnEntity.PropertyGroupProperty(
                                group_type="groupType",
                                property_names=["propertyNames"]
                            )
                        },
                        status=iottwinmaker.CfnEntity.StatusProperty(
                            error=error,
                            state="state"
                        )
                    )
                },
                description="description",
                entity_id="entityId",
                parent_entity_id="parentEntityId",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b197f79cd935d9bcd530ddc23032a643cc5a8cb23ce9b819abd0e828c83616)
            check_type(argname="argument entity_name", value=entity_name, expected_type=type_hints["entity_name"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument entity_id", value=entity_id, expected_type=type_hints["entity_id"])
            check_type(argname="argument parent_entity_id", value=parent_entity_id, expected_type=type_hints["parent_entity_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entity_name": entity_name,
            "workspace_id": workspace_id,
        }
        if components is not None:
            self._values["components"] = components
        if description is not None:
            self._values["description"] = description
        if entity_id is not None:
            self._values["entity_id"] = entity_id
        if parent_entity_id is not None:
            self._values["parent_entity_id"] = parent_entity_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def entity_name(self) -> builtins.str:
        '''The entity name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityname
        '''
        result = self._values.get("entity_name")
        assert result is not None, "Required property 'entity_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def components(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnEntity.ComponentProperty, _IResolvable_da3f097b]]]]:
        '''An object that maps strings to the components in the entity.

        Each string in the mapping must be unique to this object.

        For information on the component object see the `component <https://docs.aws.amazon.com//iot-twinmaker/latest/apireference/API_ComponentResponse.html>`_ API reference.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-components
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnEntity.ComponentProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entity_id(self) -> typing.Optional[builtins.str]:
        '''The entity ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-entityid
        '''
        result = self._values.get("entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_entity_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the parent entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-parententityid
        '''
        result = self._values.get("parent_entity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can use to manage the entity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-entity.html#cfn-iottwinmaker-entity-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEntityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnScene(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnScene",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Scene``.

    Use the ``AWS::IoTTwinMaker::Scene`` resource to declare a scene.

    :cloudformationResource: AWS::IoTTwinMaker::Scene
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_iottwinmaker as iottwinmaker
        
        cfn_scene = iottwinmaker.CfnScene(self, "MyCfnScene",
            content_location="contentLocation",
            scene_id="sceneId",
            workspace_id="workspaceId",
        
            # the properties below are optional
            capabilities=["capabilities"],
            description="description",
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
        content_location: builtins.str,
        scene_id: builtins.str,
        workspace_id: builtins.str,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::Scene``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param content_location: The relative path that specifies the location of the content definition file.
        :param scene_id: The scene ID.
        :param workspace_id: The ID of the workspace.
        :param capabilities: A list of capabilities that the scene uses to render.
        :param description: The description of this scene.
        :param tags: The ComponentType tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e723b8d84cf2c976c8c38d181a6082d3d8068ee103592ec3b3ba4c19985c5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSceneProps(
            content_location=content_location,
            scene_id=scene_id,
            workspace_id=workspace_id,
            capabilities=capabilities,
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7ac259a68f733194753cd8d59f080da530527147659943b6caacf6661e6917a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c94ac43e307952d46defa1ffc12826cd8185b40404235dd7fe11f91611d596ac)
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
        '''The scene ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time when the scene was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The scene the update time.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="contentLocation")
    def content_location(self) -> builtins.str:
        '''The relative path that specifies the location of the content definition file.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-contentlocation
        '''
        return typing.cast(builtins.str, jsii.get(self, "contentLocation"))

    @content_location.setter
    def content_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6452663aff10e046b5644861ade7613a91512b74fa92c22d30e60fe324d4a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentLocation", value)

    @builtins.property
    @jsii.member(jsii_name="sceneId")
    def scene_id(self) -> builtins.str:
        '''The scene ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-sceneid
        '''
        return typing.cast(builtins.str, jsii.get(self, "sceneId"))

    @scene_id.setter
    def scene_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d06577e2b86148d6655000dfc0c2ef2dd2efa77434190567c46002186829ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sceneId", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413b8a3a665814630ea85bfe0c5bb154caa5edaef52f591fb4a3db98292bdeb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="capabilities")
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of capabilities that the scene uses to render.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-capabilities
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capabilities"))

    @capabilities.setter
    def capabilities(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a21d8f1378d81993cfa0c5a2e5c7febb4ba8cf09e311b532da48c09220d293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capabilities", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this scene.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ba1e36c6c22d532bb08da27fcb8c31ccfa0d64c1ea755831c3a22bebc63c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnSceneProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_location": "contentLocation",
        "scene_id": "sceneId",
        "workspace_id": "workspaceId",
        "capabilities": "capabilities",
        "description": "description",
        "tags": "tags",
    },
)
class CfnSceneProps:
    def __init__(
        self,
        *,
        content_location: builtins.str,
        scene_id: builtins.str,
        workspace_id: builtins.str,
        capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnScene``.

        :param content_location: The relative path that specifies the location of the content definition file.
        :param scene_id: The scene ID.
        :param workspace_id: The ID of the workspace.
        :param capabilities: A list of capabilities that the scene uses to render.
        :param description: The description of this scene.
        :param tags: The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_iottwinmaker as iottwinmaker
            
            cfn_scene_props = iottwinmaker.CfnSceneProps(
                content_location="contentLocation",
                scene_id="sceneId",
                workspace_id="workspaceId",
            
                # the properties below are optional
                capabilities=["capabilities"],
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82a36415e841f5ed3140cd3e0387f54673b74205e417aba4df516fe5cce73da5)
            check_type(argname="argument content_location", value=content_location, expected_type=type_hints["content_location"])
            check_type(argname="argument scene_id", value=scene_id, expected_type=type_hints["scene_id"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "content_location": content_location,
            "scene_id": scene_id,
            "workspace_id": workspace_id,
        }
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content_location(self) -> builtins.str:
        '''The relative path that specifies the location of the content definition file.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-contentlocation
        '''
        result = self._values.get("content_location")
        assert result is not None, "Required property 'content_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scene_id(self) -> builtins.str:
        '''The scene ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-sceneid
        '''
        result = self._values.get("scene_id")
        assert result is not None, "Required property 'scene_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of capabilities that the scene uses to render.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-capabilities
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of this scene.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The ComponentType tags.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-scene.html#cfn-iottwinmaker-scene-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSceneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnSyncJob(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnSyncJob",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::SyncJob``.

    The SyncJob.

    :cloudformationResource: AWS::IoTTwinMaker::SyncJob
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_iottwinmaker as iottwinmaker
        
        cfn_sync_job = iottwinmaker.CfnSyncJob(self, "MyCfnSyncJob",
            sync_role="syncRole",
            sync_source="syncSource",
            workspace_id="workspaceId",
        
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
        sync_role: builtins.str,
        sync_source: builtins.str,
        workspace_id: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::SyncJob``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param sync_role: The SyncJob IAM role. This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.
        :param sync_source: The sync source. .. epigraph:: Currently the only supported syncSoucre is ``SITEWISE`` .
        :param workspace_id: The ID of the workspace that contains the sync job.
        :param tags: Metadata you can use to manage the SyncJob.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861d883ddd39366312e5f4587a1c3e710d67db29706ef3b27eceb4a2acf126c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSyncJobProps(
            sync_role=sync_role,
            sync_source=sync_source,
            workspace_id=workspace_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd45586e2655ed2ae789ad688eed3cf775233bf2a1f2fb441e8c5f468c8de29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__986b8dad16fa1cb9825760af6a47717fbaa65d345479abfc069328243b86637d)
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
        '''The SyncJob ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The creation date and time of the SyncJob.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The SyncJob's state.

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The update date and time.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''Metadata you can use to manage the SyncJob.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="syncRole")
    def sync_role(self) -> builtins.str:
        '''The SyncJob IAM role.

        This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncrole
        '''
        return typing.cast(builtins.str, jsii.get(self, "syncRole"))

    @sync_role.setter
    def sync_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f7b2224cfa5161e4c7d5914c0979fbd8b3de236019477c6cf9f922952c111f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncRole", value)

    @builtins.property
    @jsii.member(jsii_name="syncSource")
    def sync_source(self) -> builtins.str:
        '''The sync source.

        .. epigraph::

           Currently the only supported syncSoucre is ``SITEWISE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncsource
        '''
        return typing.cast(builtins.str, jsii.get(self, "syncSource"))

    @sync_source.setter
    def sync_source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1142dc0e07cd229569f30e0b556941a5ac1c48bf434e65ca93c995e012916410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "syncSource", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace that contains the sync job.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31853dbd41600582497d38f889f9ce661a966f6774f88f121e2936b12b4b275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnSyncJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "sync_role": "syncRole",
        "sync_source": "syncSource",
        "workspace_id": "workspaceId",
        "tags": "tags",
    },
)
class CfnSyncJobProps:
    def __init__(
        self,
        *,
        sync_role: builtins.str,
        sync_source: builtins.str,
        workspace_id: builtins.str,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSyncJob``.

        :param sync_role: The SyncJob IAM role. This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.
        :param sync_source: The sync source. .. epigraph:: Currently the only supported syncSoucre is ``SITEWISE`` .
        :param workspace_id: The ID of the workspace that contains the sync job.
        :param tags: Metadata you can use to manage the SyncJob.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_iottwinmaker as iottwinmaker
            
            cfn_sync_job_props = iottwinmaker.CfnSyncJobProps(
                sync_role="syncRole",
                sync_source="syncSource",
                workspace_id="workspaceId",
            
                # the properties below are optional
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a2dfd00663f2a7f6d86ff78981dd0901f87d56236db0c3e11164cf2a3f6f40b)
            check_type(argname="argument sync_role", value=sync_role, expected_type=type_hints["sync_role"])
            check_type(argname="argument sync_source", value=sync_source, expected_type=type_hints["sync_source"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sync_role": sync_role,
            "sync_source": sync_source,
            "workspace_id": workspace_id,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def sync_role(self) -> builtins.str:
        '''The SyncJob IAM role.

        This IAM role is used by the sync job to read from the syncSource, and create, update or delete the corresponding resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncrole
        '''
        result = self._values.get("sync_role")
        assert result is not None, "Required property 'sync_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sync_source(self) -> builtins.str:
        '''The sync source.

        .. epigraph::

           Currently the only supported syncSoucre is ``SITEWISE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-syncsource
        '''
        result = self._values.get("sync_source")
        assert result is not None, "Required property 'sync_source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace that contains the sync job.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata you can use to manage the SyncJob.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-syncjob.html#cfn-iottwinmaker-syncjob-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSyncJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnWorkspace(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnWorkspace",
):
    '''A CloudFormation ``AWS::IoTTwinMaker::Workspace``.

    Use the ``AWS::IoTTwinMaker::Workspace`` resource to declare a workspace.

    :cloudformationResource: AWS::IoTTwinMaker::Workspace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_iottwinmaker as iottwinmaker
        
        cfn_workspace = iottwinmaker.CfnWorkspace(self, "MyCfnWorkspace",
            role="role",
            s3_location="s3Location",
            workspace_id="workspaceId",
        
            # the properties below are optional
            description="description",
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
        role: builtins.str,
        s3_location: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IoTTwinMaker::Workspace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param role: The ARN of the execution role associated with the workspace.
        :param s3_location: The ARN of the S3 bucket where resources associated with the workspace are stored.
        :param workspace_id: The ID of the workspace.
        :param description: The description of the workspace.
        :param tags: Metadata that you can use to manage the workspace.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a54630b543997f0ca51ac34c4ac61386dc1bfeff7f09a65da3a4a9973c6b351)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnWorkspaceProps(
            role=role,
            s3_location=s3_location,
            workspace_id=workspace_id,
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
            type_hints = typing.get_type_hints(_typecheckingstub__901476f62ea6db67ff7dc838ee97d3889ba799c44b6d2968616c87169f064cc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31c3a0a7f4ad680ec19eea32c8810cc377bd80457829d215fd5236c9d17a58b7)
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
        '''The workspace ARN.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationDateTime")
    def attr_creation_date_time(self) -> builtins.str:
        '''The date and time the workspace was created.

        :cloudformationAttribute: CreationDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationDateTime"))

    @builtins.property
    @jsii.member(jsii_name="attrUpdateDateTime")
    def attr_update_date_time(self) -> builtins.str:
        '''The date and time the workspace was updated.

        :cloudformationAttribute: UpdateDateTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrUpdateDateTime"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''Metadata that you can use to manage the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        '''The ARN of the execution role associated with the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-role
        '''
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5709651e582e7e5662c1f0f814e85742225a9c155bfb79937aace64d4d1464a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value)

    @builtins.property
    @jsii.member(jsii_name="s3Location")
    def s3_location(self) -> builtins.str:
        '''The ARN of the S3 bucket where resources associated with the workspace are stored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-s3location
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Location"))

    @s3_location.setter
    def s3_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108457ed5ea0976ff280e57e58fc1d2af84710f3b66b21000414fb40ef2e8656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Location", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-workspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8c44533657a1d66b91c9b534c4bd3b87def8f248efa1a56e3ac8bef4c0724b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773f4c4f782018ddeab6d3a548948fa83f854afc74f3ee7b2a8dc3e09653eef4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_iottwinmaker.CfnWorkspaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "role": "role",
        "s3_location": "s3Location",
        "workspace_id": "workspaceId",
        "description": "description",
        "tags": "tags",
    },
)
class CfnWorkspaceProps:
    def __init__(
        self,
        *,
        role: builtins.str,
        s3_location: builtins.str,
        workspace_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnWorkspace``.

        :param role: The ARN of the execution role associated with the workspace.
        :param s3_location: The ARN of the S3 bucket where resources associated with the workspace are stored.
        :param workspace_id: The ID of the workspace.
        :param description: The description of the workspace.
        :param tags: Metadata that you can use to manage the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_iottwinmaker as iottwinmaker
            
            cfn_workspace_props = iottwinmaker.CfnWorkspaceProps(
                role="role",
                s3_location="s3Location",
                workspace_id="workspaceId",
            
                # the properties below are optional
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28aa375d16a697afdd54efb7fe26200b47cdb12808e073e144acd26ed6356448)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "role": role,
            "s3_location": s3_location,
            "workspace_id": workspace_id,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def role(self) -> builtins.str:
        '''The ARN of the execution role associated with the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-role
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_location(self) -> builtins.str:
        '''The ARN of the S3 bucket where resources associated with the workspace are stored.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-s3location
        '''
        result = self._values.get("s3_location")
        assert result is not None, "Required property 's3_location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''The ID of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-workspaceid
        '''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that you can use to manage the workspace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iottwinmaker-workspace.html#cfn-iottwinmaker-workspace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkspaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnComponentType",
    "CfnComponentTypeProps",
    "CfnEntity",
    "CfnEntityProps",
    "CfnScene",
    "CfnSceneProps",
    "CfnSyncJob",
    "CfnSyncJobProps",
    "CfnWorkspace",
    "CfnWorkspaceProps",
]

publication.publish()

def _typecheckingstub__b8644c92bbff89aa9e628d0fdc0ded7a2f9a39289146f897d6c9e6d84975a7a2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    component_type_id: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    functions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    is_singleton: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    property_definitions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    property_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9021df5b01719a9f8ef0ced4ac31ece64c48f2d9a6f8a2a8e1b3dc52181751a(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__980d08eeb6e6054720e3cbf007fada113e5791e2cc6fddb21f88ce57af3f67a7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3995a78286949349e004f99ea0c8d16e95bcee5d158e0e48f00b2b4f8527b034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2de3147a6b2674e530d30f8b5182e3c9439f2a356e4c875b3698b24221b97584(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47d9f5f634e196d4115e50936c2bee2a81dabb9327edc3a41578e1176dbda51(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f86b83703d7a5bd869a7593399801c17824b55ace45f888bf02c81af5378c6(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c18d78b62d26be5852013391c05c78956f0decd19a229ac7f58b866ae466c14(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.FunctionProperty, _IResolvable_da3f097b]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f5b5fcf3c80cef383cad8a20c79fb45b21b0d73ef476054a81873ff26b199c(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1be07e93843a09c1fedf2924bac62d38324ad54f2879a9be1a8e23ad7beb09f8(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyDefinitionProperty, _IResolvable_da3f097b]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36507cd81b3c73a3a55b64d8b8b5eda472ce5b6929f6f7ba9baa53055e83dcb5(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnComponentType.PropertyGroupProperty, _IResolvable_da3f097b]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e095ca9ff9009a5ff6712910bff836e9c2473e499b8c06a1b4806c6ca1441915(
    *,
    is_native: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    lambda_: typing.Optional[typing.Union[typing.Union[CfnComponentType.LambdaFunctionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273be5e09d6f9d95c15698e5ec925c4c3ec65b0759e24097c34ef449c37a2c81(
    *,
    type: builtins.str,
    allowed_values: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    nested_type: typing.Optional[typing.Union[typing.Union[CfnComponentType.DataTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    relationship: typing.Optional[typing.Union[typing.Union[CfnComponentType.RelationshipProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    unit_of_measure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a40a165220ec5d269b66d44c8fedc1d32d50ec3b5ffb0460c6bce31dbe65807b(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    list_value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    long_value: typing.Optional[jsii.Number] = None,
    map_value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    relationship_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ba6dda94f512be388b31fafb7bdd74f4da3e6f6bfac56519dc5dd55c44080f(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4e223e00848234f4d432d4b5f935b1dc442846c59536e19e08a436eff737f2(
    *,
    implemented_by: typing.Optional[typing.Union[typing.Union[CfnComponentType.DataConnectorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    required_properties: typing.Optional[typing.Sequence[builtins.str]] = None,
    scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011f4caacaac8a9678c7e6f682b14051c4e3f54b1af2a1a5fbc3725d3ec93be2(
    *,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6468ee4b88bb9dcef8da418cc59d1b3fceed119d2e1ade2c3b9f57b529a31a(
    *,
    configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
    data_type: typing.Optional[typing.Union[typing.Union[CfnComponentType.DataTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    default_value: typing.Optional[typing.Union[typing.Union[CfnComponentType.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    is_external_id: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_stored_externally: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_time_series: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41c24934073ef871df6ba445dcdf9cc53474d18bc8a6abdf5a2e9cff4e25f22(
    *,
    group_type: typing.Optional[builtins.str] = None,
    property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47b99571be3f27c50e535a75cdfdf14ca06d5215f64fdf40109961b2293b546(
    *,
    relationship_type: typing.Optional[builtins.str] = None,
    target_component_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbc10d1d938365a15f08cf5a673508117d98b2ab0ecd5a788ee85722bda49a71(
    *,
    target_component_name: typing.Optional[builtins.str] = None,
    target_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6fe13a7b05f6856183480bafda65ea9e1351e2adfec7908b91529e2228a26c(
    *,
    error: typing.Optional[typing.Union[typing.Union[CfnComponentType.ErrorProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__324a0cc887ec1065b9d5ba872572072fa8c481530426ba50811e338f2dde6f9b(
    *,
    component_type_id: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    extends_from: typing.Optional[typing.Sequence[builtins.str]] = None,
    functions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.FunctionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    is_singleton: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    property_definitions: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    property_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentType.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e1a29b5ee0db8b0f9fe80447cc93db85e2ed400b28a3c61bfca379d292ea661(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    entity_name: builtins.str,
    workspace_id: builtins.str,
    components: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    parent_entity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e51d270d4440681d46f1e667f106ed384931f38df7092845daad0ed9f82b4739(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4e6df7cdcbaa7bb71c0f98e6b81417fbefaaee9fa2525cc6d3e448f5fb8a0ac(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b22be6154cc92786e71f5ade2798dfd6ec3b1454e285e563bb83c7b6cd4f165(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc57b76e292f6e6cc6693d0d00219ab00040aa359ab079b08cd8f04ada9f78e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d33ce5aae02e9b9d53db2dc6a1f173aca65b2d0541e1f42ac4dcedca4032bbc(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[CfnEntity.ComponentProperty, _IResolvable_da3f097b]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c066a8d095e32951abe069a62394d16267b44a974544cb8a532331626aca268f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c2c2a1d07260ab64ca67bbdcc394460319d917fbad0788d8c84e729a4f0010(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838f65778509f9139a5dfa429adefddf900b5f2f386b0122e5f5c57ccbe5ef86(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5940403f2280c2499fc9c10c883fa2fcac0dd0a9bf77111ee145480c06c9f15(
    *,
    component_name: typing.Optional[builtins.str] = None,
    component_type_id: typing.Optional[builtins.str] = None,
    defined_in: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.PropertyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    property_groups: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.PropertyGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    status: typing.Optional[typing.Union[typing.Union[CfnEntity.StatusProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c5ea634d5e6bd56e791cf605b04f67fafafb43348fa60e51ac9a7c41739999(
    *,
    allowed_values: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    nested_type: typing.Optional[typing.Union[typing.Union[CfnEntity.DataTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    relationship: typing.Optional[typing.Union[typing.Union[CfnEntity.RelationshipProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    type: typing.Optional[builtins.str] = None,
    unit_of_measure: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee2e6498d955df8493500bf9e927820daa7a2e32fb446fcd06dfea586442db8(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    expression: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[jsii.Number] = None,
    list_value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    long_value: typing.Optional[jsii.Number] = None,
    map_value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    relationship_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347d62ba072131593e5021b7610bb93a0bbad5f67a110b1404655f0235ef81eb(
    *,
    configuration: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, builtins.str]]] = None,
    data_type: typing.Optional[typing.Union[typing.Union[CfnEntity.DataTypeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    default_value: typing.Optional[typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    is_external_id: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_final: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_imported: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_inherited: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_required_in_entity: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_stored_externally: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    is_time_series: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c778853c1f1dbe9882df8a699b0e19cdd214f25fb32899ce13b88ddc29191712(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42db694573f925f93c6b240c30df8cabf5a4960ff073e14a5a7cfdcf955374f1(
    *,
    group_type: typing.Optional[builtins.str] = None,
    property_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a9328bc8f6cfe5025ae4d451c1d5700ea92588c53715a2a735d8c9e887e52f(
    *,
    definition: typing.Any = None,
    value: typing.Optional[typing.Union[typing.Union[CfnEntity.DataValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2669a78539a59c9601ed42020c3074fd1666a65003972ddee491b7be87a32e(
    *,
    relationship_type: typing.Optional[builtins.str] = None,
    target_component_type_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e51369cd4e121c1c1511111247d4d515d7e3f546b629cf0107d91fc3da672d(
    *,
    target_component_name: typing.Optional[builtins.str] = None,
    target_entity_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ab81751c1d2e7e539a71d287760369286bfc3d825eeb956567885e8536f4b1(
    *,
    error: typing.Any = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b197f79cd935d9bcd530ddc23032a643cc5a8cb23ce9b819abd0e828c83616(
    *,
    entity_name: builtins.str,
    workspace_id: builtins.str,
    components: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnEntity.ComponentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    description: typing.Optional[builtins.str] = None,
    entity_id: typing.Optional[builtins.str] = None,
    parent_entity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e723b8d84cf2c976c8c38d181a6082d3d8068ee103592ec3b3ba4c19985c5b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    content_location: builtins.str,
    scene_id: builtins.str,
    workspace_id: builtins.str,
    capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ac259a68f733194753cd8d59f080da530527147659943b6caacf6661e6917a(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94ac43e307952d46defa1ffc12826cd8185b40404235dd7fe11f91611d596ac(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6452663aff10e046b5644861ade7613a91512b74fa92c22d30e60fe324d4a1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d06577e2b86148d6655000dfc0c2ef2dd2efa77434190567c46002186829ce8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413b8a3a665814630ea85bfe0c5bb154caa5edaef52f591fb4a3db98292bdeb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a21d8f1378d81993cfa0c5a2e5c7febb4ba8cf09e311b532da48c09220d293(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ba1e36c6c22d532bb08da27fcb8c31ccfa0d64c1ea755831c3a22bebc63c3d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a36415e841f5ed3140cd3e0387f54673b74205e417aba4df516fe5cce73da5(
    *,
    content_location: builtins.str,
    scene_id: builtins.str,
    workspace_id: builtins.str,
    capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861d883ddd39366312e5f4587a1c3e710d67db29706ef3b27eceb4a2acf126c5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    sync_role: builtins.str,
    sync_source: builtins.str,
    workspace_id: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd45586e2655ed2ae789ad688eed3cf775233bf2a1f2fb441e8c5f468c8de29(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__986b8dad16fa1cb9825760af6a47717fbaa65d345479abfc069328243b86637d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f7b2224cfa5161e4c7d5914c0979fbd8b3de236019477c6cf9f922952c111f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1142dc0e07cd229569f30e0b556941a5ac1c48bf434e65ca93c995e012916410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31853dbd41600582497d38f889f9ce661a966f6774f88f121e2936b12b4b275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a2dfd00663f2a7f6d86ff78981dd0901f87d56236db0c3e11164cf2a3f6f40b(
    *,
    sync_role: builtins.str,
    sync_source: builtins.str,
    workspace_id: builtins.str,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a54630b543997f0ca51ac34c4ac61386dc1bfeff7f09a65da3a4a9973c6b351(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    role: builtins.str,
    s3_location: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901476f62ea6db67ff7dc838ee97d3889ba799c44b6d2968616c87169f064cc1(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c3a0a7f4ad680ec19eea32c8810cc377bd80457829d215fd5236c9d17a58b7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5709651e582e7e5662c1f0f814e85742225a9c155bfb79937aace64d4d1464a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108457ed5ea0976ff280e57e58fc1d2af84710f3b66b21000414fb40ef2e8656(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8c44533657a1d66b91c9b534c4bd3b87def8f248efa1a56e3ac8bef4c0724b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773f4c4f782018ddeab6d3a548948fa83f854afc74f3ee7b2a8dc3e09653eef4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28aa375d16a697afdd54efb7fe26200b47cdb12808e073e144acd26ed6356448(
    *,
    role: builtins.str,
    s3_location: builtins.str,
    workspace_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
