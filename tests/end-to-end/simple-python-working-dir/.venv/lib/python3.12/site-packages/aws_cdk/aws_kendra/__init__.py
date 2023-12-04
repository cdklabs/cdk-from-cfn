'''
# AWS::Kendra Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_kendra as kendra
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Kendra construct libraries](https://constructs.dev/search?q=kendra)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Kendra resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Kendra.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Kendra](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Kendra.html).

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
class CfnDataSource(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource",
):
    '''A CloudFormation ``AWS::Kendra::DataSource``.

    Creates a data source connector that you want to use with an Amazon Kendra index.

    You specify a name, data source connector type and description for your data source. You also specify configuration information for the data source connector.

    :cloudformationResource: AWS::Kendra::DataSource
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_kendra as kendra
        
        cfn_data_source = kendra.CfnDataSource(self, "MyCfnDataSource",
            index_id="indexId",
            name="name",
            type="type",
        
            # the properties below are optional
            custom_document_enrichment_configuration=kendra.CfnDataSource.CustomDocumentEnrichmentConfigurationProperty(
                inline_configurations=[kendra.CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty(
                    condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        operator="operator",
        
                        # the properties below are optional
                        condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    document_content_deletion=False,
                    target=kendra.CfnDataSource.DocumentAttributeTargetProperty(
                        target_document_attribute_key="targetDocumentAttributeKey",
        
                        # the properties below are optional
                        target_document_attribute_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        target_document_attribute_value_deletion=False
                    )
                )],
                post_extraction_hook_configuration=kendra.CfnDataSource.HookConfigurationProperty(
                    lambda_arn="lambdaArn",
                    s3_bucket="s3Bucket",
        
                    # the properties below are optional
                    invocation_condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        operator="operator",
        
                        # the properties below are optional
                        condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    )
                ),
                pre_extraction_hook_configuration=kendra.CfnDataSource.HookConfigurationProperty(
                    lambda_arn="lambdaArn",
                    s3_bucket="s3Bucket",
        
                    # the properties below are optional
                    invocation_condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        operator="operator",
        
                        # the properties below are optional
                        condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    )
                ),
                role_arn="roleArn"
            ),
            data_source_configuration=kendra.CfnDataSource.DataSourceConfigurationProperty(
                confluence_configuration=kendra.CfnDataSource.ConfluenceConfigurationProperty(
                    secret_arn="secretArn",
                    server_url="serverUrl",
                    version="version",
        
                    # the properties below are optional
                    attachment_configuration=kendra.CfnDataSource.ConfluenceAttachmentConfigurationProperty(
                        attachment_field_mappings=[kendra.CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        crawl_attachments=False
                    ),
                    blog_configuration=kendra.CfnDataSource.ConfluenceBlogConfigurationProperty(
                        blog_field_mappings=[kendra.CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    exclusion_patterns=["exclusionPatterns"],
                    inclusion_patterns=["inclusionPatterns"],
                    page_configuration=kendra.CfnDataSource.ConfluencePageConfigurationProperty(
                        page_field_mappings=[kendra.CfnDataSource.ConfluencePageToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    space_configuration=kendra.CfnDataSource.ConfluenceSpaceConfigurationProperty(
                        crawl_archived_spaces=False,
                        crawl_personal_spaces=False,
                        exclude_spaces=["excludeSpaces"],
                        include_spaces=["includeSpaces"],
                        space_field_mappings=[kendra.CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                ),
                database_configuration=kendra.CfnDataSource.DatabaseConfigurationProperty(
                    column_configuration=kendra.CfnDataSource.ColumnConfigurationProperty(
                        change_detecting_columns=["changeDetectingColumns"],
                        document_data_column_name="documentDataColumnName",
                        document_id_column_name="documentIdColumnName",
        
                        # the properties below are optional
                        document_title_column_name="documentTitleColumnName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    connection_configuration=kendra.CfnDataSource.ConnectionConfigurationProperty(
                        database_host="databaseHost",
                        database_name="databaseName",
                        database_port=123,
                        secret_arn="secretArn",
                        table_name="tableName"
                    ),
                    database_engine_type="databaseEngineType",
        
                    # the properties below are optional
                    acl_configuration=kendra.CfnDataSource.AclConfigurationProperty(
                        allowed_groups_column_name="allowedGroupsColumnName"
                    ),
                    sql_configuration=kendra.CfnDataSource.SqlConfigurationProperty(
                        query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                    ),
                    vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                ),
                google_drive_configuration=kendra.CfnDataSource.GoogleDriveConfigurationProperty(
                    secret_arn="secretArn",
        
                    # the properties below are optional
                    exclude_mime_types=["excludeMimeTypes"],
                    exclude_shared_drives=["excludeSharedDrives"],
                    exclude_user_accounts=["excludeUserAccounts"],
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
        
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    inclusion_patterns=["inclusionPatterns"]
                ),
                one_drive_configuration=kendra.CfnDataSource.OneDriveConfigurationProperty(
                    one_drive_users=kendra.CfnDataSource.OneDriveUsersProperty(
                        one_drive_user_list=["oneDriveUserList"],
                        one_drive_user_s3_path=kendra.CfnDataSource.S3PathProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    secret_arn="secretArn",
                    tenant_domain="tenantDomain",
        
                    # the properties below are optional
                    disable_local_groups=False,
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
        
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    inclusion_patterns=["inclusionPatterns"]
                ),
                s3_configuration=kendra.CfnDataSource.S3DataSourceConfigurationProperty(
                    bucket_name="bucketName",
        
                    # the properties below are optional
                    access_control_list_configuration=kendra.CfnDataSource.AccessControlListConfigurationProperty(
                        key_path="keyPath"
                    ),
                    documents_metadata_configuration=kendra.CfnDataSource.DocumentsMetadataConfigurationProperty(
                        s3_prefix="s3Prefix"
                    ),
                    exclusion_patterns=["exclusionPatterns"],
                    inclusion_patterns=["inclusionPatterns"],
                    inclusion_prefixes=["inclusionPrefixes"]
                ),
                salesforce_configuration=kendra.CfnDataSource.SalesforceConfigurationProperty(
                    secret_arn="secretArn",
                    server_url="serverUrl",
        
                    # the properties below are optional
                    chatter_feed_configuration=kendra.CfnDataSource.SalesforceChatterFeedConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
        
                        # the properties below are optional
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        include_filter_types=["includeFilterTypes"]
                    ),
                    crawl_attachments=False,
                    exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                    include_attachment_file_patterns=["includeAttachmentFilePatterns"],
                    knowledge_article_configuration=kendra.CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty(
                        included_states=["includedStates"],
        
                        # the properties below are optional
                        custom_knowledge_article_type_configurations=[kendra.CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            name="name",
        
                            # the properties below are optional
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
        
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        )],
                        standard_knowledge_article_type_configuration=kendra.CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
        
                            # the properties below are optional
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
        
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        )
                    ),
                    standard_object_attachment_configuration=kendra.CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty(
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    standard_object_configurations=[kendra.CfnDataSource.SalesforceStandardObjectConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        name="name",
        
                        # the properties below are optional
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    )]
                ),
                service_now_configuration=kendra.CfnDataSource.ServiceNowConfigurationProperty(
                    host_url="hostUrl",
                    secret_arn="secretArn",
                    service_now_build_version="serviceNowBuildVersion",
        
                    # the properties below are optional
                    authentication_type="authenticationType",
                    knowledge_article_configuration=kendra.CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
        
                        # the properties below are optional
                        crawl_attachments=False,
                        document_title_field_name="documentTitleFieldName",
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        filter_query="filterQuery",
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                    ),
                    service_catalog_configuration=kendra.CfnDataSource.ServiceNowServiceCatalogConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
        
                        # the properties below are optional
                        crawl_attachments=False,
                        document_title_field_name="documentTitleFieldName",
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
        
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                    )
                ),
                share_point_configuration=kendra.CfnDataSource.SharePointConfigurationProperty(
                    secret_arn="secretArn",
                    share_point_version="sharePointVersion",
                    urls=["urls"],
        
                    # the properties below are optional
                    crawl_attachments=False,
                    disable_local_groups=False,
                    document_title_field_name="documentTitleFieldName",
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
        
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    ssl_certificate_s3_path=kendra.CfnDataSource.S3PathProperty(
                        bucket="bucket",
                        key="key"
                    ),
                    use_change_log=False,
                    vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                ),
                web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
                    urls=kendra.CfnDataSource.WebCrawlerUrlsProperty(
                        seed_url_configuration=kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                            seed_urls=["seedUrls"],
        
                            # the properties below are optional
                            web_crawler_mode="webCrawlerMode"
                        ),
                        site_maps_configuration=kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                            site_maps=["siteMaps"]
                        )
                    ),
        
                    # the properties below are optional
                    authentication_configuration=kendra.CfnDataSource.WebCrawlerAuthenticationConfigurationProperty(
                        basic_authentication=[kendra.CfnDataSource.WebCrawlerBasicAuthenticationProperty(
                            credentials="credentials",
                            host="host",
                            port=123
                        )]
                    ),
                    crawl_depth=123,
                    max_content_size_per_page_in_mega_bytes=123,
                    max_links_per_page=123,
                    max_urls_per_minute_crawl_rate=123,
                    proxy_configuration=kendra.CfnDataSource.ProxyConfigurationProperty(
                        host="host",
                        port=123,
        
                        # the properties below are optional
                        credentials="credentials"
                    ),
                    url_exclusion_patterns=["urlExclusionPatterns"],
                    url_inclusion_patterns=["urlInclusionPatterns"]
                ),
                work_docs_configuration=kendra.CfnDataSource.WorkDocsConfigurationProperty(
                    organization_id="organizationId",
        
                    # the properties below are optional
                    crawl_comments=False,
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
        
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    use_change_log=False
                )
            ),
            description="description",
            role_arn="roleArn",
            schedule="schedule",
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
        index_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        custom_document_enrichment_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.CustomDocumentEnrichmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        data_source_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        description: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Kendra::DataSource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param index_id: The identifier of the index you want to use with the data source connector.
        :param name: The name of the data source.
        :param type: The type of the data source.
        :param custom_document_enrichment_configuration: Configuration information for altering document metadata and content during the document ingestion process.
        :param data_source_configuration: Configuration information for an Amazon Kendra data source. The contents of the configuration depend on the type of data source. You can only specify one type of data source in the configuration. You can't specify the ``Configuration`` parameter when the ``Type`` parameter is set to ``CUSTOM`` . The ``Configuration`` parameter is required for all other data sources.
        :param description: A description for the data source connector.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the data source. You can't specify the ``RoleArn`` parameter when the ``Type`` parameter is set to ``CUSTOM`` . The ``RoleArn`` parameter is required for all other data sources.
        :param schedule: Sets the frequency that Amazon Kendra checks the documents in your data source and updates the index. If you don't set a schedule, Amazon Kendra doesn't periodically update the index.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7b870c602f215572ec4f7667cd46c2ae4e2c6035e16924c08cf6d68dc1e858)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDataSourceProps(
            index_id=index_id,
            name=name,
            type=type,
            custom_document_enrichment_configuration=custom_document_enrichment_configuration,
            data_source_configuration=data_source_configuration,
            description=description,
            role_arn=role_arn,
            schedule=schedule,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__857c3d47368883ad30477d4c7721d4f448bafe37d7457ab7e8fa7ab0c70e6c2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4df69e7835817b60bff4c27a777904898be17518f1553fa5fd56e28c646990)
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
        '''The Amazon Resource Name (ARN) of the data source. For example:.

        ``arn:aws:kendra:us-west-2:111122223333:index/335c3741-41df-46a6-b5d3-61f85b787884/data-source/b8cae438-6787-4091-8897-684a652bbb0a``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier for the data source. For example:.

        ``b8cae438-6787-4091-8897-684a652bbb0a`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="indexId")
    def index_id(self) -> builtins.str:
        '''The identifier of the index you want to use with the data source connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-indexid
        '''
        return typing.cast(builtins.str, jsii.get(self, "indexId"))

    @index_id.setter
    def index_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da518cc177b71ad2703234f2e02607e32d9ae04f8b106e8ef880eda822ebfbc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727aa22774141fa3563f0859859874f94f89dcfafca54202ef16cd4039fae247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of the data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75ff38538f8b7b5ad592fb8de907503bd940ef472178a94ea71872c5e0e52e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="customDocumentEnrichmentConfiguration")
    def custom_document_enrichment_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnDataSource.CustomDocumentEnrichmentConfigurationProperty", _IResolvable_da3f097b]]:
        '''Configuration information for altering document metadata and content during the document ingestion process.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataSource.CustomDocumentEnrichmentConfigurationProperty", _IResolvable_da3f097b]], jsii.get(self, "customDocumentEnrichmentConfiguration"))

    @custom_document_enrichment_configuration.setter
    def custom_document_enrichment_configuration(
        self,
        value: typing.Optional[typing.Union["CfnDataSource.CustomDocumentEnrichmentConfigurationProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13b151417bd0a802a711d66b55ba6494eed4691c8ad5b5af2f894a431892d5fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDocumentEnrichmentConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="dataSourceConfiguration")
    def data_source_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnDataSource.DataSourceConfigurationProperty", _IResolvable_da3f097b]]:
        '''Configuration information for an Amazon Kendra data source.

        The contents of the configuration depend on the type of data source. You can only specify one type of data source in the configuration.

        You can't specify the ``Configuration`` parameter when the ``Type`` parameter is set to ``CUSTOM`` .

        The ``Configuration`` parameter is required for all other data sources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-datasourceconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDataSource.DataSourceConfigurationProperty", _IResolvable_da3f097b]], jsii.get(self, "dataSourceConfiguration"))

    @data_source_configuration.setter
    def data_source_configuration(
        self,
        value: typing.Optional[typing.Union["CfnDataSource.DataSourceConfigurationProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea79eed634a5ae09c1e689638d3ede50cbd8c33dae75c020cff75930d087664e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataSourceConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the data source connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3fe842db3dcb4fce0cdde73f8c5e1e2a0746c534ecd6c08bed0359e2beefe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a role with permission to access the data source.

        You can't specify the ``RoleArn`` parameter when the ``Type`` parameter is set to ``CUSTOM`` .

        The ``RoleArn`` parameter is required for all other data sources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-rolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf11b1fe015a07a79a94cab233a319e551a36b06278e679c1bf6a049d269c0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Sets the frequency that Amazon Kendra checks the documents in your data source and updates the index.

        If you don't set a schedule, Amazon Kendra doesn't periodically update the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-schedule
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646a3352fddea09391f6d6bab4d6fa7a13f4b27c607bb5778a4fb3b77c8850b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.AccessControlListConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"key_path": "keyPath"},
    )
    class AccessControlListConfigurationProperty:
        def __init__(self, *, key_path: typing.Optional[builtins.str] = None) -> None:
            '''Specifies access control list files for the documents in a data source.

            :param key_path: Path to the AWS S3 bucket that contains the access control list files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-accesscontrollistconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                access_control_list_configuration_property = kendra.CfnDataSource.AccessControlListConfigurationProperty(
                    key_path="keyPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c75a85e279b4b8eeb32b079b870a3a505c72193be98cbf8a512ba78fb2c7edaf)
                check_type(argname="argument key_path", value=key_path, expected_type=type_hints["key_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_path is not None:
                self._values["key_path"] = key_path

        @builtins.property
        def key_path(self) -> typing.Optional[builtins.str]:
            '''Path to the AWS S3 bucket that contains the access control list files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-accesscontrollistconfiguration.html#cfn-kendra-datasource-accesscontrollistconfiguration-keypath
            '''
            result = self._values.get("key_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessControlListConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.AclConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"allowed_groups_column_name": "allowedGroupsColumnName"},
    )
    class AclConfigurationProperty:
        def __init__(self, *, allowed_groups_column_name: builtins.str) -> None:
            '''Provides information about the column that should be used for filtering the query response by groups.

            :param allowed_groups_column_name: A list of groups, separated by semi-colons, that filters a query response based on user context. The document is only returned to users that are in one of the groups specified in the ``UserContext`` field of the `Query <https://docs.aws.amazon.com/kendra/latest/dg/API_Query.html>`_ operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-aclconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                acl_configuration_property = kendra.CfnDataSource.AclConfigurationProperty(
                    allowed_groups_column_name="allowedGroupsColumnName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49de6c4a08f15d0f081e52ec45a2bc4ccf3f2d2b5dd047fdd170d597181f21b2)
                check_type(argname="argument allowed_groups_column_name", value=allowed_groups_column_name, expected_type=type_hints["allowed_groups_column_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "allowed_groups_column_name": allowed_groups_column_name,
            }

        @builtins.property
        def allowed_groups_column_name(self) -> builtins.str:
            '''A list of groups, separated by semi-colons, that filters a query response based on user context.

            The document is only returned to users that are in one of the groups specified in the ``UserContext`` field of the `Query <https://docs.aws.amazon.com/kendra/latest/dg/API_Query.html>`_ operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-aclconfiguration.html#cfn-kendra-datasource-aclconfiguration-allowedgroupscolumnname
            '''
            result = self._values.get("allowed_groups_column_name")
            assert result is not None, "Required property 'allowed_groups_column_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AclConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ColumnConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "change_detecting_columns": "changeDetectingColumns",
            "document_data_column_name": "documentDataColumnName",
            "document_id_column_name": "documentIdColumnName",
            "document_title_column_name": "documentTitleColumnName",
            "field_mappings": "fieldMappings",
        },
    )
    class ColumnConfigurationProperty:
        def __init__(
            self,
            *,
            change_detecting_columns: typing.Sequence[builtins.str],
            document_data_column_name: builtins.str,
            document_id_column_name: builtins.str,
            document_title_column_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Provides information about how Amazon Kendra should use the columns of a database in an index.

            :param change_detecting_columns: One to five columns that indicate when a document in the database has changed.
            :param document_data_column_name: The column that contains the contents of the document.
            :param document_id_column_name: The column that provides the document's identifier.
            :param document_title_column_name: The column that contains the title of the document.
            :param field_mappings: An array of objects that map database column names to the corresponding fields in an index. You must first create the fields in the index using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                column_configuration_property = kendra.CfnDataSource.ColumnConfigurationProperty(
                    change_detecting_columns=["changeDetectingColumns"],
                    document_data_column_name="documentDataColumnName",
                    document_id_column_name="documentIdColumnName",
                
                    # the properties below are optional
                    document_title_column_name="documentTitleColumnName",
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1cfb41c0445e5b29959324b1ac11eef70234922023e3fca11ee3192079da9e5c)
                check_type(argname="argument change_detecting_columns", value=change_detecting_columns, expected_type=type_hints["change_detecting_columns"])
                check_type(argname="argument document_data_column_name", value=document_data_column_name, expected_type=type_hints["document_data_column_name"])
                check_type(argname="argument document_id_column_name", value=document_id_column_name, expected_type=type_hints["document_id_column_name"])
                check_type(argname="argument document_title_column_name", value=document_title_column_name, expected_type=type_hints["document_title_column_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "change_detecting_columns": change_detecting_columns,
                "document_data_column_name": document_data_column_name,
                "document_id_column_name": document_id_column_name,
            }
            if document_title_column_name is not None:
                self._values["document_title_column_name"] = document_title_column_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings

        @builtins.property
        def change_detecting_columns(self) -> typing.List[builtins.str]:
            '''One to five columns that indicate when a document in the database has changed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-changedetectingcolumns
            '''
            result = self._values.get("change_detecting_columns")
            assert result is not None, "Required property 'change_detecting_columns' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def document_data_column_name(self) -> builtins.str:
            '''The column that contains the contents of the document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-documentdatacolumnname
            '''
            result = self._values.get("document_data_column_name")
            assert result is not None, "Required property 'document_data_column_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def document_id_column_name(self) -> builtins.str:
            '''The column that provides the document's identifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-documentidcolumnname
            '''
            result = self._values.get("document_id_column_name")
            assert result is not None, "Required property 'document_id_column_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def document_title_column_name(self) -> typing.Optional[builtins.str]:
            '''The column that contains the title of the document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-documenttitlecolumnname
            '''
            result = self._values.get("document_title_column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''An array of objects that map database column names to the corresponding fields in an index.

            You must first create the fields in the index using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-columnconfiguration.html#cfn-kendra-datasource-columnconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluenceAttachmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_field_mappings": "attachmentFieldMappings",
            "crawl_attachments": "crawlAttachments",
        },
    )
    class ConfluenceAttachmentConfigurationProperty:
        def __init__(
            self,
            *,
            attachment_field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Configuration of attachment settings for the Confluence data source.

            Attachment settings are optional, if you don't specify settings attachments, Amazon Kendra won't index them.

            :param attachment_field_mappings: Maps attributes or field names of Confluence attachments to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata. If you specify the ``AttachentFieldMappings`` parameter, you must specify at least one field mapping.
            :param crawl_attachments: ``TRUE`` to index attachments of pages and blogs in Confluence.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_attachment_configuration_property = kendra.CfnDataSource.ConfluenceAttachmentConfigurationProperty(
                    attachment_field_mappings=[kendra.CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    crawl_attachments=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee6cfb9bb5093bde33f429779799db80d83d5393cdfc89e20b3430270efbe1e5)
                check_type(argname="argument attachment_field_mappings", value=attachment_field_mappings, expected_type=type_hints["attachment_field_mappings"])
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_field_mappings is not None:
                self._values["attachment_field_mappings"] = attachment_field_mappings
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments

        @builtins.property
        def attachment_field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of Confluence attachments to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            If you specify the ``AttachentFieldMappings`` parameter, you must specify at least one field mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmentconfiguration.html#cfn-kendra-datasource-confluenceattachmentconfiguration-attachmentfieldmappings
            '''
            result = self._values.get("attachment_field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to index attachments of pages and blogs in Confluence.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmentconfiguration.html#cfn-kendra-datasource-confluenceattachmentconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceAttachmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "index_field_name": "indexFieldName",
            "date_field_format": "dateFieldFormat",
        },
    )
    class ConfluenceAttachmentToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: builtins.str,
            index_field_name: builtins.str,
            date_field_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps attributes or field names of Confluence attachments to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confuence data source field names must exist in your Confluence custom metadata.

            :param data_source_field_name: The name of the field in the data source. You must first create the index field using the ``UpdateIndex`` API.
            :param index_field_name: The name of the index field to map to the Confluence data source field. The index field type must match the Confluence field type.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmenttoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_attachment_to_index_field_mapping_property = kendra.CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    index_field_name="indexFieldName",
                
                    # the properties below are optional
                    date_field_format="dateFieldFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__529bdb052ea312464a1abde7c9704238bd18f7b0dd291c002a95313af6956988)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_source_field_name": data_source_field_name,
                "index_field_name": index_field_name,
            }
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format

        @builtins.property
        def data_source_field_name(self) -> builtins.str:
            '''The name of the field in the data source.

            You must first create the index field using the ``UpdateIndex`` API.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmenttoindexfieldmapping.html#cfn-kendra-datasource-confluenceattachmenttoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            assert result is not None, "Required property 'data_source_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def index_field_name(self) -> builtins.str:
            '''The name of the index field to map to the Confluence data source field.

            The index field type must match the Confluence field type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmenttoindexfieldmapping.html#cfn-kendra-datasource-confluenceattachmenttoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            assert result is not None, "Required property 'index_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceattachmenttoindexfieldmapping.html#cfn-kendra-datasource-confluenceattachmenttoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceAttachmentToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluenceBlogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"blog_field_mappings": "blogFieldMappings"},
    )
    class ConfluenceBlogConfigurationProperty:
        def __init__(
            self,
            *,
            blog_field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Configuration of blog settings for the Confluence data source.

            Blogs are always indexed unless filtered from the index by the ``ExclusionPatterns`` or ``InclusionPatterns`` fields in the ``ConfluenceConfiguration`` object.

            :param blog_field_mappings: Maps attributes or field names of Confluence blogs to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata. If you specify the ``BlogFieldMappings`` parameter, you must specify at least one field mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_blog_configuration_property = kendra.CfnDataSource.ConfluenceBlogConfigurationProperty(
                    blog_field_mappings=[kendra.CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6a264b7f2ddc83b3c490f89e320f16d205c5edb37049b498464df2b9eb674f1)
                check_type(argname="argument blog_field_mappings", value=blog_field_mappings, expected_type=type_hints["blog_field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if blog_field_mappings is not None:
                self._values["blog_field_mappings"] = blog_field_mappings

        @builtins.property
        def blog_field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of Confluence blogs to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            If you specify the ``BlogFieldMappings`` parameter, you must specify at least one field mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogconfiguration.html#cfn-kendra-datasource-confluenceblogconfiguration-blogfieldmappings
            '''
            result = self._values.get("blog_field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceBlogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "index_field_name": "indexFieldName",
            "date_field_format": "dateFieldFormat",
        },
    )
    class ConfluenceBlogToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: builtins.str,
            index_field_name: builtins.str,
            date_field_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps attributes or field names of Confluence blog to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            :param data_source_field_name: The name of the field in the data source.
            :param index_field_name: The name of the index field to map to the Confluence data source field. The index field type must match the Confluence field type.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogtoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_blog_to_index_field_mapping_property = kendra.CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    index_field_name="indexFieldName",
                
                    # the properties below are optional
                    date_field_format="dateFieldFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__48a1e22fe3cbe861fbcbb273e85a7b63fd46b8626479abb9f9eb183a662b101f)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_source_field_name": data_source_field_name,
                "index_field_name": index_field_name,
            }
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format

        @builtins.property
        def data_source_field_name(self) -> builtins.str:
            '''The name of the field in the data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogtoindexfieldmapping.html#cfn-kendra-datasource-confluenceblogtoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            assert result is not None, "Required property 'data_source_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def index_field_name(self) -> builtins.str:
            '''The name of the index field to map to the Confluence data source field.

            The index field type must match the Confluence field type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogtoindexfieldmapping.html#cfn-kendra-datasource-confluenceblogtoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            assert result is not None, "Required property 'index_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceblogtoindexfieldmapping.html#cfn-kendra-datasource-confluenceblogtoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceBlogToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluenceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secret_arn": "secretArn",
            "server_url": "serverUrl",
            "version": "version",
            "attachment_configuration": "attachmentConfiguration",
            "blog_configuration": "blogConfiguration",
            "exclusion_patterns": "exclusionPatterns",
            "inclusion_patterns": "inclusionPatterns",
            "page_configuration": "pageConfiguration",
            "space_configuration": "spaceConfiguration",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class ConfluenceConfigurationProperty:
        def __init__(
            self,
            *,
            secret_arn: builtins.str,
            server_url: builtins.str,
            version: builtins.str,
            attachment_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ConfluenceAttachmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            blog_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ConfluenceBlogConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            page_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ConfluencePageConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            space_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ConfluenceSpaceConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            vpc_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information to connect to Confluence as your data source.

            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password required to connect to the Confluence instance. If you use Confluence Cloud, you use a generated API token as the password. You can also provide authentication credentials in the form of a personal access token. For more information, see `Using a Confluence data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-confluence.html>`_ .
            :param server_url: The URL of your Confluence instance. Use the full URL of the server. For example, *https://server.example.com:port/* . You can also use an IP address, for example, *https://192.168.1.113/* .
            :param version: The version or the type of Confluence installation to connect to.
            :param attachment_configuration: Configuration information for indexing attachments to Confluence blogs and pages.
            :param blog_configuration: Configuration information for indexing Confluence blogs.
            :param exclusion_patterns: A list of regular expression patterns to exclude certain blog posts, pages, spaces, or attachments in your Confluence. Content that matches the patterns are excluded from the index. Content that doesn't match the patterns is included in the index. If content matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the content isn't included in the index.
            :param inclusion_patterns: A list of regular expression patterns to include certain blog posts, pages, spaces, or attachments in your Confluence. Content that matches the patterns are included in the index. Content that doesn't match the patterns is excluded from the index. If content matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the content isn't included in the index.
            :param page_configuration: Configuration information for indexing Confluence pages.
            :param space_configuration: Configuration information for indexing Confluence spaces.
            :param vpc_configuration: Configuration information for an Amazon Virtual Private Cloud to connect to your Confluence. For more information, see `Configuring a VPC <https://docs.aws.amazon.com/kendra/latest/dg/vpc-configuration.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_configuration_property = kendra.CfnDataSource.ConfluenceConfigurationProperty(
                    secret_arn="secretArn",
                    server_url="serverUrl",
                    version="version",
                
                    # the properties below are optional
                    attachment_configuration=kendra.CfnDataSource.ConfluenceAttachmentConfigurationProperty(
                        attachment_field_mappings=[kendra.CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        crawl_attachments=False
                    ),
                    blog_configuration=kendra.CfnDataSource.ConfluenceBlogConfigurationProperty(
                        blog_field_mappings=[kendra.CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    exclusion_patterns=["exclusionPatterns"],
                    inclusion_patterns=["inclusionPatterns"],
                    page_configuration=kendra.CfnDataSource.ConfluencePageConfigurationProperty(
                        page_field_mappings=[kendra.CfnDataSource.ConfluencePageToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    space_configuration=kendra.CfnDataSource.ConfluenceSpaceConfigurationProperty(
                        crawl_archived_spaces=False,
                        crawl_personal_spaces=False,
                        exclude_spaces=["excludeSpaces"],
                        include_spaces=["includeSpaces"],
                        space_field_mappings=[kendra.CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0fc73a495264eef013dab776a4e7c3b95e5d3a9ae1ca4f62716fbbf86103e685)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument server_url", value=server_url, expected_type=type_hints["server_url"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
                check_type(argname="argument attachment_configuration", value=attachment_configuration, expected_type=type_hints["attachment_configuration"])
                check_type(argname="argument blog_configuration", value=blog_configuration, expected_type=type_hints["blog_configuration"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument page_configuration", value=page_configuration, expected_type=type_hints["page_configuration"])
                check_type(argname="argument space_configuration", value=space_configuration, expected_type=type_hints["space_configuration"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secret_arn": secret_arn,
                "server_url": server_url,
                "version": version,
            }
            if attachment_configuration is not None:
                self._values["attachment_configuration"] = attachment_configuration
            if blog_configuration is not None:
                self._values["blog_configuration"] = blog_configuration
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if page_configuration is not None:
                self._values["page_configuration"] = page_configuration
            if space_configuration is not None:
                self._values["space_configuration"] = space_configuration
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password required to connect to the Confluence instance.

            If you use Confluence Cloud, you use a generated API token as the password.

            You can also provide authentication credentials in the form of a personal access token. For more information, see `Using a Confluence data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-confluence.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def server_url(self) -> builtins.str:
            '''The URL of your Confluence instance.

            Use the full URL of the server. For example, *https://server.example.com:port/* . You can also use an IP address, for example, *https://192.168.1.113/* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-serverurl
            '''
            result = self._values.get("server_url")
            assert result is not None, "Required property 'server_url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def version(self) -> builtins.str:
            '''The version or the type of Confluence installation to connect to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-version
            '''
            result = self._values.get("version")
            assert result is not None, "Required property 'version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def attachment_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ConfluenceAttachmentConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for indexing attachments to Confluence blogs and pages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-attachmentconfiguration
            '''
            result = self._values.get("attachment_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ConfluenceAttachmentConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def blog_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ConfluenceBlogConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for indexing Confluence blogs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-blogconfiguration
            '''
            result = self._values.get("blog_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ConfluenceBlogConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain blog posts, pages, spaces, or attachments in your Confluence.

            Content that matches the patterns are excluded from the index. Content that doesn't match the patterns is included in the index. If content matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the content isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain blog posts, pages, spaces, or attachments in your Confluence.

            Content that matches the patterns are included in the index. Content that doesn't match the patterns is excluded from the index. If content matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the content isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def page_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ConfluencePageConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for indexing Confluence pages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-pageconfiguration
            '''
            result = self._values.get("page_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ConfluencePageConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def space_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ConfluenceSpaceConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for indexing Confluence spaces.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-spaceconfiguration
            '''
            result = self._values.get("space_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ConfluenceSpaceConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for an Amazon Virtual Private Cloud to connect to your Confluence.

            For more information, see `Configuring a VPC <https://docs.aws.amazon.com/kendra/latest/dg/vpc-configuration.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluenceconfiguration.html#cfn-kendra-datasource-confluenceconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluencePageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"page_field_mappings": "pageFieldMappings"},
    )
    class ConfluencePageConfigurationProperty:
        def __init__(
            self,
            *,
            page_field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.ConfluencePageToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Configuration of the page settings for the Confluence data source.

            :param page_field_mappings: Maps attributes or field names of Confluence pages to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata. If you specify the ``PageFieldMappings`` parameter, you must specify at least one field mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_page_configuration_property = kendra.CfnDataSource.ConfluencePageConfigurationProperty(
                    page_field_mappings=[kendra.CfnDataSource.ConfluencePageToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__067682c93bcdb09a9f476748f97c89f1397c33c7f36fd58bb32a166d78fb3ce4)
                check_type(argname="argument page_field_mappings", value=page_field_mappings, expected_type=type_hints["page_field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if page_field_mappings is not None:
                self._values["page_field_mappings"] = page_field_mappings

        @builtins.property
        def page_field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.ConfluencePageToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of Confluence pages to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            If you specify the ``PageFieldMappings`` parameter, you must specify at least one field mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepageconfiguration.html#cfn-kendra-datasource-confluencepageconfiguration-pagefieldmappings
            '''
            result = self._values.get("page_field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.ConfluencePageToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluencePageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluencePageToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "index_field_name": "indexFieldName",
            "date_field_format": "dateFieldFormat",
        },
    )
    class ConfluencePageToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: builtins.str,
            index_field_name: builtins.str,
            date_field_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps attributes or field names of Confluence pages to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            :param data_source_field_name: The name of the field in the data source.
            :param index_field_name: The name of the index field to map to the Confluence data source field. The index field type must match the Confluence field type.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepagetoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_page_to_index_field_mapping_property = kendra.CfnDataSource.ConfluencePageToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    index_field_name="indexFieldName",
                
                    # the properties below are optional
                    date_field_format="dateFieldFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02db3b1eb2295ad6b3ca31a8a741242f9a81c7568d7e1cdd398ad8df1941bf58)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_source_field_name": data_source_field_name,
                "index_field_name": index_field_name,
            }
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format

        @builtins.property
        def data_source_field_name(self) -> builtins.str:
            '''The name of the field in the data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepagetoindexfieldmapping.html#cfn-kendra-datasource-confluencepagetoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            assert result is not None, "Required property 'data_source_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def index_field_name(self) -> builtins.str:
            '''The name of the index field to map to the Confluence data source field.

            The index field type must match the Confluence field type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepagetoindexfieldmapping.html#cfn-kendra-datasource-confluencepagetoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            assert result is not None, "Required property 'index_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencepagetoindexfieldmapping.html#cfn-kendra-datasource-confluencepagetoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluencePageToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluenceSpaceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crawl_archived_spaces": "crawlArchivedSpaces",
            "crawl_personal_spaces": "crawlPersonalSpaces",
            "exclude_spaces": "excludeSpaces",
            "include_spaces": "includeSpaces",
            "space_field_mappings": "spaceFieldMappings",
        },
    )
    class ConfluenceSpaceConfigurationProperty:
        def __init__(
            self,
            *,
            crawl_archived_spaces: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            crawl_personal_spaces: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            exclude_spaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_spaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            space_field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Configuration information for indexing Confluence spaces.

            :param crawl_archived_spaces: ``TRUE`` to index archived spaces.
            :param crawl_personal_spaces: ``TRUE`` to index personal spaces. You can add restrictions to items in personal spaces. If personal spaces are indexed, queries without user context information may return restricted items from a personal space in their results. For more information, see `Filtering on user context <https://docs.aws.amazon.com/kendra/latest/dg/user-context-filter.html>`_ .
            :param exclude_spaces: A list of space keys of Confluence spaces. If you include a key, the blogs, documents, and attachments in the space are not indexed. If a space is in both the ``ExcludeSpaces`` and the ``IncludeSpaces`` list, the space is excluded.
            :param include_spaces: A list of space keys for Confluence spaces. If you include a key, the blogs, documents, and attachments in the space are indexed. Spaces that aren't in the list aren't indexed. A space in the list must exist. Otherwise, Amazon Kendra logs an error when the data source is synchronized. If a space is in both the ``IncludeSpaces`` and the ``ExcludeSpaces`` list, the space is excluded.
            :param space_field_mappings: Maps attributes or field names of Confluence spaces to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata. If you specify the ``SpaceFieldMappings`` parameter, you must specify at least one field mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_space_configuration_property = kendra.CfnDataSource.ConfluenceSpaceConfigurationProperty(
                    crawl_archived_spaces=False,
                    crawl_personal_spaces=False,
                    exclude_spaces=["excludeSpaces"],
                    include_spaces=["includeSpaces"],
                    space_field_mappings=[kendra.CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f40a78d184b37483bcef61e3c4870f87360262d1fd7a7621e6a3a1ef3a7888c2)
                check_type(argname="argument crawl_archived_spaces", value=crawl_archived_spaces, expected_type=type_hints["crawl_archived_spaces"])
                check_type(argname="argument crawl_personal_spaces", value=crawl_personal_spaces, expected_type=type_hints["crawl_personal_spaces"])
                check_type(argname="argument exclude_spaces", value=exclude_spaces, expected_type=type_hints["exclude_spaces"])
                check_type(argname="argument include_spaces", value=include_spaces, expected_type=type_hints["include_spaces"])
                check_type(argname="argument space_field_mappings", value=space_field_mappings, expected_type=type_hints["space_field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crawl_archived_spaces is not None:
                self._values["crawl_archived_spaces"] = crawl_archived_spaces
            if crawl_personal_spaces is not None:
                self._values["crawl_personal_spaces"] = crawl_personal_spaces
            if exclude_spaces is not None:
                self._values["exclude_spaces"] = exclude_spaces
            if include_spaces is not None:
                self._values["include_spaces"] = include_spaces
            if space_field_mappings is not None:
                self._values["space_field_mappings"] = space_field_mappings

        @builtins.property
        def crawl_archived_spaces(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to index archived spaces.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-crawlarchivedspaces
            '''
            result = self._values.get("crawl_archived_spaces")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def crawl_personal_spaces(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to index personal spaces.

            You can add restrictions to items in personal spaces. If personal spaces are indexed, queries without user context information may return restricted items from a personal space in their results. For more information, see `Filtering on user context <https://docs.aws.amazon.com/kendra/latest/dg/user-context-filter.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-crawlpersonalspaces
            '''
            result = self._values.get("crawl_personal_spaces")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def exclude_spaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of space keys of Confluence spaces.

            If you include a key, the blogs, documents, and attachments in the space are not indexed. If a space is in both the ``ExcludeSpaces`` and the ``IncludeSpaces`` list, the space is excluded.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-excludespaces
            '''
            result = self._values.get("exclude_spaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_spaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of space keys for Confluence spaces.

            If you include a key, the blogs, documents, and attachments in the space are indexed. Spaces that aren't in the list aren't indexed. A space in the list must exist. Otherwise, Amazon Kendra logs an error when the data source is synchronized. If a space is in both the ``IncludeSpaces`` and the ``ExcludeSpaces`` list, the space is excluded.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-includespaces
            '''
            result = self._values.get("include_spaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def space_field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of Confluence spaces to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            If you specify the ``SpaceFieldMappings`` parameter, you must specify at least one field mapping.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespaceconfiguration.html#cfn-kendra-datasource-confluencespaceconfiguration-spacefieldmappings
            '''
            result = self._values.get("space_field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceSpaceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "index_field_name": "indexFieldName",
            "date_field_format": "dateFieldFormat",
        },
    )
    class ConfluenceSpaceToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: builtins.str,
            index_field_name: builtins.str,
            date_field_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps attributes or field names of Confluence spaces to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Confluence fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Confluence data source field names must exist in your Confluence custom metadata.

            :param data_source_field_name: The name of the field in the data source.
            :param index_field_name: The name of the index field to map to the Confluence data source field. The index field type must match the Confluence field type.
            :param date_field_format: The format for date fields in the data source. If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespacetoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                confluence_space_to_index_field_mapping_property = kendra.CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    index_field_name="indexFieldName",
                
                    # the properties below are optional
                    date_field_format="dateFieldFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0000b03ae40dd75637e6d7b6c78c5df60c30c415f5ceda4611012d456c139d0)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_source_field_name": data_source_field_name,
                "index_field_name": index_field_name,
            }
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format

        @builtins.property
        def data_source_field_name(self) -> builtins.str:
            '''The name of the field in the data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespacetoindexfieldmapping.html#cfn-kendra-datasource-confluencespacetoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            assert result is not None, "Required property 'data_source_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def index_field_name(self) -> builtins.str:
            '''The name of the index field to map to the Confluence data source field.

            The index field type must match the Confluence field type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespacetoindexfieldmapping.html#cfn-kendra-datasource-confluencespacetoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            assert result is not None, "Required property 'index_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The format for date fields in the data source.

            If the field specified in ``DataSourceFieldName`` is a date field you must specify the date format. If the field is not a date field, an exception is thrown.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-confluencespacetoindexfieldmapping.html#cfn-kendra-datasource-confluencespacetoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfluenceSpaceToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ConnectionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_host": "databaseHost",
            "database_name": "databaseName",
            "database_port": "databasePort",
            "secret_arn": "secretArn",
            "table_name": "tableName",
        },
    )
    class ConnectionConfigurationProperty:
        def __init__(
            self,
            *,
            database_host: builtins.str,
            database_name: builtins.str,
            database_port: jsii.Number,
            secret_arn: builtins.str,
            table_name: builtins.str,
        ) -> None:
            '''Provides the configuration information that's required to connect to a database.

            :param database_host: The name of the host for the database. Can be either a string (host.subdomain.domain.tld) or an IPv4 or IPv6 address.
            :param database_name: The name of the database containing the document data.
            :param database_port: The port that the database uses for connections.
            :param secret_arn: The Amazon Resource Name (ARN) of credentials stored in AWS Secrets Manager . The credentials should be a user/password pair. For more information, see `Using a Database Data Source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-database.html>`_ . For more information about AWS Secrets Manager , see `What Is AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ in the *AWS Secrets Manager* user guide.
            :param table_name: The name of the table that contains the document data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                connection_configuration_property = kendra.CfnDataSource.ConnectionConfigurationProperty(
                    database_host="databaseHost",
                    database_name="databaseName",
                    database_port=123,
                    secret_arn="secretArn",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__010dd9b2b9a8c77bfe2d4ed8e974fc62d5bb8091dd9fbf486410bd89c29b52f8)
                check_type(argname="argument database_host", value=database_host, expected_type=type_hints["database_host"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument database_port", value=database_port, expected_type=type_hints["database_port"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "database_host": database_host,
                "database_name": database_name,
                "database_port": database_port,
                "secret_arn": secret_arn,
                "table_name": table_name,
            }

        @builtins.property
        def database_host(self) -> builtins.str:
            '''The name of the host for the database.

            Can be either a string (host.subdomain.domain.tld) or an IPv4 or IPv6 address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-databasehost
            '''
            result = self._values.get("database_host")
            assert result is not None, "Required property 'database_host' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def database_name(self) -> builtins.str:
            '''The name of the database containing the document data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-databasename
            '''
            result = self._values.get("database_name")
            assert result is not None, "Required property 'database_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def database_port(self) -> jsii.Number:
            '''The port that the database uses for connections.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-databaseport
            '''
            result = self._values.get("database_port")
            assert result is not None, "Required property 'database_port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of credentials stored in AWS Secrets Manager .

            The credentials should be a user/password pair. For more information, see `Using a Database Data Source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-database.html>`_ . For more information about AWS Secrets Manager , see `What Is AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ in the *AWS Secrets Manager* user guide.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def table_name(self) -> builtins.str:
            '''The name of the table that contains the document data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-connectionconfiguration.html#cfn-kendra-datasource-connectionconfiguration-tablename
            '''
            result = self._values.get("table_name")
            assert result is not None, "Required property 'table_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.CustomDocumentEnrichmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "inline_configurations": "inlineConfigurations",
            "post_extraction_hook_configuration": "postExtractionHookConfiguration",
            "pre_extraction_hook_configuration": "preExtractionHookConfiguration",
            "role_arn": "roleArn",
        },
    )
    class CustomDocumentEnrichmentConfigurationProperty:
        def __init__(
            self,
            *,
            inline_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            post_extraction_hook_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.HookConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            pre_extraction_hook_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.HookConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for altering document metadata and content during the document ingestion process.

            For more information, see `Customizing document metadata during the ingestion process <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html>`_ .

            :param inline_configurations: Configuration information to alter document attributes or metadata fields and content when ingesting documents into Amazon Kendra.
            :param post_extraction_hook_configuration: Configuration information for invoking a Lambda function in AWS Lambda on the structured documents with their metadata and text extracted. You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Advanced data manipulation <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#advanced-data-manipulation>`_ .
            :param pre_extraction_hook_configuration: Configuration information for invoking a Lambda function in AWS Lambda on the original or raw documents before extracting their metadata and text. You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Advanced data manipulation <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#advanced-data-manipulation>`_ .
            :param role_arn: The Amazon Resource Name (ARN) of a role with permission to run ``PreExtractionHookConfiguration`` and ``PostExtractionHookConfiguration`` for altering document metadata and content during the document ingestion process. For more information, see `IAM roles for Amazon Kendra <https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                custom_document_enrichment_configuration_property = kendra.CfnDataSource.CustomDocumentEnrichmentConfigurationProperty(
                    inline_configurations=[kendra.CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty(
                        condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            operator="operator",
                
                            # the properties below are optional
                            condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        document_content_deletion=False,
                        target=kendra.CfnDataSource.DocumentAttributeTargetProperty(
                            target_document_attribute_key="targetDocumentAttributeKey",
                
                            # the properties below are optional
                            target_document_attribute_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            target_document_attribute_value_deletion=False
                        )
                    )],
                    post_extraction_hook_configuration=kendra.CfnDataSource.HookConfigurationProperty(
                        lambda_arn="lambdaArn",
                        s3_bucket="s3Bucket",
                
                        # the properties below are optional
                        invocation_condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            operator="operator",
                
                            # the properties below are optional
                            condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        )
                    ),
                    pre_extraction_hook_configuration=kendra.CfnDataSource.HookConfigurationProperty(
                        lambda_arn="lambdaArn",
                        s3_bucket="s3Bucket",
                
                        # the properties below are optional
                        invocation_condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            operator="operator",
                
                            # the properties below are optional
                            condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        )
                    ),
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4048e2fee9d6603c2251b77fb03f4d3bb19fa55563651003cac3f2513230697f)
                check_type(argname="argument inline_configurations", value=inline_configurations, expected_type=type_hints["inline_configurations"])
                check_type(argname="argument post_extraction_hook_configuration", value=post_extraction_hook_configuration, expected_type=type_hints["post_extraction_hook_configuration"])
                check_type(argname="argument pre_extraction_hook_configuration", value=pre_extraction_hook_configuration, expected_type=type_hints["pre_extraction_hook_configuration"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if inline_configurations is not None:
                self._values["inline_configurations"] = inline_configurations
            if post_extraction_hook_configuration is not None:
                self._values["post_extraction_hook_configuration"] = post_extraction_hook_configuration
            if pre_extraction_hook_configuration is not None:
                self._values["pre_extraction_hook_configuration"] = pre_extraction_hook_configuration
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def inline_configurations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty", _IResolvable_da3f097b]]]]:
            '''Configuration information to alter document attributes or metadata fields and content when ingesting documents into Amazon Kendra.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration-inlineconfigurations
            '''
            result = self._values.get("inline_configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def post_extraction_hook_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.HookConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for invoking a Lambda function in AWS Lambda on the structured documents with their metadata and text extracted.

            You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Advanced data manipulation <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#advanced-data-manipulation>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration-postextractionhookconfiguration
            '''
            result = self._values.get("post_extraction_hook_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.HookConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def pre_extraction_hook_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.HookConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for invoking a Lambda function in AWS Lambda on the original or raw documents before extracting their metadata and text.

            You can use a Lambda function to apply advanced logic for creating, modifying, or deleting document metadata and content. For more information, see `Advanced data manipulation <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#advanced-data-manipulation>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration-preextractionhookconfiguration
            '''
            result = self._values.get("pre_extraction_hook_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.HookConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of a role with permission to run ``PreExtractionHookConfiguration`` and ``PostExtractionHookConfiguration`` for altering document metadata and content during the document ingestion process.

            For more information, see `IAM roles for Amazon Kendra <https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-customdocumentenrichmentconfiguration.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomDocumentEnrichmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "confluence_configuration": "confluenceConfiguration",
            "database_configuration": "databaseConfiguration",
            "google_drive_configuration": "googleDriveConfiguration",
            "one_drive_configuration": "oneDriveConfiguration",
            "s3_configuration": "s3Configuration",
            "salesforce_configuration": "salesforceConfiguration",
            "service_now_configuration": "serviceNowConfiguration",
            "share_point_configuration": "sharePointConfiguration",
            "web_crawler_configuration": "webCrawlerConfiguration",
            "work_docs_configuration": "workDocsConfiguration",
        },
    )
    class DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            confluence_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ConfluenceConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            database_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.DatabaseConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            google_drive_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.GoogleDriveConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            one_drive_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.OneDriveConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            s3_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.S3DataSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            salesforce_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.SalesforceConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            service_now_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ServiceNowConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            share_point_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.SharePointConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            web_crawler_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.WebCrawlerConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            work_docs_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.WorkDocsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information for an Amazon Kendra data source.

            :param confluence_configuration: Provides the configuration information to connect to Confluence as your data source.
            :param database_configuration: Provides the configuration information to connect to a database as your data source.
            :param google_drive_configuration: Provides the configuration information to connect to Google Drive as your data source.
            :param one_drive_configuration: Provides the configuration information to connect to Microsoft OneDrive as your data source.
            :param s3_configuration: Provides the configuration information to connect to an Amazon S3 bucket as your data source.
            :param salesforce_configuration: Provides the configuration information to connect to Salesforce as your data source.
            :param service_now_configuration: Provides the configuration information to connect to ServiceNow as your data source.
            :param share_point_configuration: Provides the configuration information to connect to Microsoft SharePoint as your data source.
            :param web_crawler_configuration: Provides the configuration information required for Amazon Kendra Web Crawler.
            :param work_docs_configuration: Provides the configuration information to connect to Amazon WorkDocs as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                data_source_configuration_property = kendra.CfnDataSource.DataSourceConfigurationProperty(
                    confluence_configuration=kendra.CfnDataSource.ConfluenceConfigurationProperty(
                        secret_arn="secretArn",
                        server_url="serverUrl",
                        version="version",
                
                        # the properties below are optional
                        attachment_configuration=kendra.CfnDataSource.ConfluenceAttachmentConfigurationProperty(
                            attachment_field_mappings=[kendra.CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )],
                            crawl_attachments=False
                        ),
                        blog_configuration=kendra.CfnDataSource.ConfluenceBlogConfigurationProperty(
                            blog_field_mappings=[kendra.CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        exclusion_patterns=["exclusionPatterns"],
                        inclusion_patterns=["inclusionPatterns"],
                        page_configuration=kendra.CfnDataSource.ConfluencePageConfigurationProperty(
                            page_field_mappings=[kendra.CfnDataSource.ConfluencePageToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        space_configuration=kendra.CfnDataSource.ConfluenceSpaceConfigurationProperty(
                            crawl_archived_spaces=False,
                            crawl_personal_spaces=False,
                            exclude_spaces=["excludeSpaces"],
                            include_spaces=["includeSpaces"],
                            space_field_mappings=[kendra.CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    database_configuration=kendra.CfnDataSource.DatabaseConfigurationProperty(
                        column_configuration=kendra.CfnDataSource.ColumnConfigurationProperty(
                            change_detecting_columns=["changeDetectingColumns"],
                            document_data_column_name="documentDataColumnName",
                            document_id_column_name="documentIdColumnName",
                
                            # the properties below are optional
                            document_title_column_name="documentTitleColumnName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        connection_configuration=kendra.CfnDataSource.ConnectionConfigurationProperty(
                            database_host="databaseHost",
                            database_name="databaseName",
                            database_port=123,
                            secret_arn="secretArn",
                            table_name="tableName"
                        ),
                        database_engine_type="databaseEngineType",
                
                        # the properties below are optional
                        acl_configuration=kendra.CfnDataSource.AclConfigurationProperty(
                            allowed_groups_column_name="allowedGroupsColumnName"
                        ),
                        sql_configuration=kendra.CfnDataSource.SqlConfigurationProperty(
                            query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                        ),
                        vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    google_drive_configuration=kendra.CfnDataSource.GoogleDriveConfigurationProperty(
                        secret_arn="secretArn",
                
                        # the properties below are optional
                        exclude_mime_types=["excludeMimeTypes"],
                        exclude_shared_drives=["excludeSharedDrives"],
                        exclude_user_accounts=["excludeUserAccounts"],
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        inclusion_patterns=["inclusionPatterns"]
                    ),
                    one_drive_configuration=kendra.CfnDataSource.OneDriveConfigurationProperty(
                        one_drive_users=kendra.CfnDataSource.OneDriveUsersProperty(
                            one_drive_user_list=["oneDriveUserList"],
                            one_drive_user_s3_path=kendra.CfnDataSource.S3PathProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        secret_arn="secretArn",
                        tenant_domain="tenantDomain",
                
                        # the properties below are optional
                        disable_local_groups=False,
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        inclusion_patterns=["inclusionPatterns"]
                    ),
                    s3_configuration=kendra.CfnDataSource.S3DataSourceConfigurationProperty(
                        bucket_name="bucketName",
                
                        # the properties below are optional
                        access_control_list_configuration=kendra.CfnDataSource.AccessControlListConfigurationProperty(
                            key_path="keyPath"
                        ),
                        documents_metadata_configuration=kendra.CfnDataSource.DocumentsMetadataConfigurationProperty(
                            s3_prefix="s3Prefix"
                        ),
                        exclusion_patterns=["exclusionPatterns"],
                        inclusion_patterns=["inclusionPatterns"],
                        inclusion_prefixes=["inclusionPrefixes"]
                    ),
                    salesforce_configuration=kendra.CfnDataSource.SalesforceConfigurationProperty(
                        secret_arn="secretArn",
                        server_url="serverUrl",
                
                        # the properties below are optional
                        chatter_feed_configuration=kendra.CfnDataSource.SalesforceChatterFeedConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                
                            # the properties below are optional
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )],
                            include_filter_types=["includeFilterTypes"]
                        ),
                        crawl_attachments=False,
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"],
                        knowledge_article_configuration=kendra.CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty(
                            included_states=["includedStates"],
                
                            # the properties below are optional
                            custom_knowledge_article_type_configurations=[kendra.CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                                document_data_field_name="documentDataFieldName",
                                name="name",
                
                                # the properties below are optional
                                document_title_field_name="documentTitleFieldName",
                                field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                    data_source_field_name="dataSourceFieldName",
                                    index_field_name="indexFieldName",
                
                                    # the properties below are optional
                                    date_field_format="dateFieldFormat"
                                )]
                            )],
                            standard_knowledge_article_type_configuration=kendra.CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                                document_data_field_name="documentDataFieldName",
                
                                # the properties below are optional
                                document_title_field_name="documentTitleFieldName",
                                field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                    data_source_field_name="dataSourceFieldName",
                                    index_field_name="indexFieldName",
                
                                    # the properties below are optional
                                    date_field_format="dateFieldFormat"
                                )]
                            )
                        ),
                        standard_object_attachment_configuration=kendra.CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty(
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        standard_object_configurations=[kendra.CfnDataSource.SalesforceStandardObjectConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            name="name",
                
                            # the properties below are optional
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        )]
                    ),
                    service_now_configuration=kendra.CfnDataSource.ServiceNowConfigurationProperty(
                        host_url="hostUrl",
                        secret_arn="secretArn",
                        service_now_build_version="serviceNowBuildVersion",
                
                        # the properties below are optional
                        authentication_type="authenticationType",
                        knowledge_article_configuration=kendra.CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                
                            # the properties below are optional
                            crawl_attachments=False,
                            document_title_field_name="documentTitleFieldName",
                            exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )],
                            filter_query="filterQuery",
                            include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                        ),
                        service_catalog_configuration=kendra.CfnDataSource.ServiceNowServiceCatalogConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                
                            # the properties below are optional
                            crawl_attachments=False,
                            document_title_field_name="documentTitleFieldName",
                            exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )],
                            include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                        )
                    ),
                    share_point_configuration=kendra.CfnDataSource.SharePointConfigurationProperty(
                        secret_arn="secretArn",
                        share_point_version="sharePointVersion",
                        urls=["urls"],
                
                        # the properties below are optional
                        crawl_attachments=False,
                        disable_local_groups=False,
                        document_title_field_name="documentTitleFieldName",
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        ssl_certificate_s3_path=kendra.CfnDataSource.S3PathProperty(
                            bucket="bucket",
                            key="key"
                        ),
                        use_change_log=False,
                        vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
                        urls=kendra.CfnDataSource.WebCrawlerUrlsProperty(
                            seed_url_configuration=kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                                seed_urls=["seedUrls"],
                
                                # the properties below are optional
                                web_crawler_mode="webCrawlerMode"
                            ),
                            site_maps_configuration=kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                                site_maps=["siteMaps"]
                            )
                        ),
                
                        # the properties below are optional
                        authentication_configuration=kendra.CfnDataSource.WebCrawlerAuthenticationConfigurationProperty(
                            basic_authentication=[kendra.CfnDataSource.WebCrawlerBasicAuthenticationProperty(
                                credentials="credentials",
                                host="host",
                                port=123
                            )]
                        ),
                        crawl_depth=123,
                        max_content_size_per_page_in_mega_bytes=123,
                        max_links_per_page=123,
                        max_urls_per_minute_crawl_rate=123,
                        proxy_configuration=kendra.CfnDataSource.ProxyConfigurationProperty(
                            host="host",
                            port=123,
                
                            # the properties below are optional
                            credentials="credentials"
                        ),
                        url_exclusion_patterns=["urlExclusionPatterns"],
                        url_inclusion_patterns=["urlInclusionPatterns"]
                    ),
                    work_docs_configuration=kendra.CfnDataSource.WorkDocsConfigurationProperty(
                        organization_id="organizationId",
                
                        # the properties below are optional
                        crawl_comments=False,
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        use_change_log=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0f9c312cf9cd7088a9eba0183b5f0bf4960a0c56630a30d0a7208794a6863f3)
                check_type(argname="argument confluence_configuration", value=confluence_configuration, expected_type=type_hints["confluence_configuration"])
                check_type(argname="argument database_configuration", value=database_configuration, expected_type=type_hints["database_configuration"])
                check_type(argname="argument google_drive_configuration", value=google_drive_configuration, expected_type=type_hints["google_drive_configuration"])
                check_type(argname="argument one_drive_configuration", value=one_drive_configuration, expected_type=type_hints["one_drive_configuration"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
                check_type(argname="argument salesforce_configuration", value=salesforce_configuration, expected_type=type_hints["salesforce_configuration"])
                check_type(argname="argument service_now_configuration", value=service_now_configuration, expected_type=type_hints["service_now_configuration"])
                check_type(argname="argument share_point_configuration", value=share_point_configuration, expected_type=type_hints["share_point_configuration"])
                check_type(argname="argument web_crawler_configuration", value=web_crawler_configuration, expected_type=type_hints["web_crawler_configuration"])
                check_type(argname="argument work_docs_configuration", value=work_docs_configuration, expected_type=type_hints["work_docs_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if confluence_configuration is not None:
                self._values["confluence_configuration"] = confluence_configuration
            if database_configuration is not None:
                self._values["database_configuration"] = database_configuration
            if google_drive_configuration is not None:
                self._values["google_drive_configuration"] = google_drive_configuration
            if one_drive_configuration is not None:
                self._values["one_drive_configuration"] = one_drive_configuration
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration
            if salesforce_configuration is not None:
                self._values["salesforce_configuration"] = salesforce_configuration
            if service_now_configuration is not None:
                self._values["service_now_configuration"] = service_now_configuration
            if share_point_configuration is not None:
                self._values["share_point_configuration"] = share_point_configuration
            if web_crawler_configuration is not None:
                self._values["web_crawler_configuration"] = web_crawler_configuration
            if work_docs_configuration is not None:
                self._values["work_docs_configuration"] = work_docs_configuration

        @builtins.property
        def confluence_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ConfluenceConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to Confluence as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-confluenceconfiguration
            '''
            result = self._values.get("confluence_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ConfluenceConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def database_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DatabaseConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to a database as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-databaseconfiguration
            '''
            result = self._values.get("database_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DatabaseConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def google_drive_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.GoogleDriveConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to Google Drive as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-googledriveconfiguration
            '''
            result = self._values.get("google_drive_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.GoogleDriveConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def one_drive_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.OneDriveConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to Microsoft OneDrive as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-onedriveconfiguration
            '''
            result = self._values.get("one_drive_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.OneDriveConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def s3_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.S3DataSourceConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to an Amazon S3 bucket as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.S3DataSourceConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def salesforce_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.SalesforceConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to Salesforce as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-salesforceconfiguration
            '''
            result = self._values.get("salesforce_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.SalesforceConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def service_now_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ServiceNowConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to ServiceNow as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-servicenowconfiguration
            '''
            result = self._values.get("service_now_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ServiceNowConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def share_point_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.SharePointConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to Microsoft SharePoint as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-sharepointconfiguration
            '''
            result = self._values.get("share_point_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.SharePointConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def web_crawler_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.WebCrawlerConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information required for Amazon Kendra Web Crawler.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-webcrawlerconfiguration
            '''
            result = self._values.get("web_crawler_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.WebCrawlerConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def work_docs_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.WorkDocsConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the configuration information to connect to Amazon WorkDocs as your data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourceconfiguration.html#cfn-kendra-datasource-datasourceconfiguration-workdocsconfiguration
            '''
            result = self._values.get("work_docs_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.WorkDocsConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_source_field_name": "dataSourceFieldName",
            "index_field_name": "indexFieldName",
            "date_field_format": "dateFieldFormat",
        },
    )
    class DataSourceToIndexFieldMappingProperty:
        def __init__(
            self,
            *,
            data_source_field_name: builtins.str,
            index_field_name: builtins.str,
            date_field_format: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Maps a column or attribute in the data source to an index field.

            You must first create the fields in the index using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation.

            :param data_source_field_name: The name of the column or attribute in the data source.
            :param index_field_name: The name of the field in the index.
            :param date_field_format: The type of data stored in the column or attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcetoindexfieldmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                data_source_to_index_field_mapping_property = kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                    data_source_field_name="dataSourceFieldName",
                    index_field_name="indexFieldName",
                
                    # the properties below are optional
                    date_field_format="dateFieldFormat"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8208bd51030836955a10bbcba314957eac24c0ca6dae40b87bfb3b46ccc25db5)
                check_type(argname="argument data_source_field_name", value=data_source_field_name, expected_type=type_hints["data_source_field_name"])
                check_type(argname="argument index_field_name", value=index_field_name, expected_type=type_hints["index_field_name"])
                check_type(argname="argument date_field_format", value=date_field_format, expected_type=type_hints["date_field_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "data_source_field_name": data_source_field_name,
                "index_field_name": index_field_name,
            }
            if date_field_format is not None:
                self._values["date_field_format"] = date_field_format

        @builtins.property
        def data_source_field_name(self) -> builtins.str:
            '''The name of the column or attribute in the data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcetoindexfieldmapping.html#cfn-kendra-datasource-datasourcetoindexfieldmapping-datasourcefieldname
            '''
            result = self._values.get("data_source_field_name")
            assert result is not None, "Required property 'data_source_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def index_field_name(self) -> builtins.str:
            '''The name of the field in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcetoindexfieldmapping.html#cfn-kendra-datasource-datasourcetoindexfieldmapping-indexfieldname
            '''
            result = self._values.get("index_field_name")
            assert result is not None, "Required property 'index_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def date_field_format(self) -> typing.Optional[builtins.str]:
            '''The type of data stored in the column or attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcetoindexfieldmapping.html#cfn-kendra-datasource-datasourcetoindexfieldmapping-datefieldformat
            '''
            result = self._values.get("date_field_format")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceToIndexFieldMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.DataSourceVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class DataSourceVpcConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Sequence[builtins.str],
            subnet_ids: typing.Sequence[builtins.str],
        ) -> None:
            '''Provides the configuration information to connect to an Amazon VPC.

            :param security_group_ids: A list of identifiers of security groups within your Amazon VPC. The security groups should enable Amazon Kendra to connect to the data source.
            :param subnet_ids: A list of identifiers for subnets within your Amazon VPC. The subnets should be able to connect to each other in the VPC, and they should have outgoing access to the Internet through a NAT device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcevpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                data_source_vpc_configuration_property = kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83a29196b7634080fa4eab0118a19b31a589c1e30145e12231546ff92e046bd0)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }

        @builtins.property
        def security_group_ids(self) -> typing.List[builtins.str]:
            '''A list of identifiers of security groups within your Amazon VPC.

            The security groups should enable Amazon Kendra to connect to the data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcevpcconfiguration.html#cfn-kendra-datasource-datasourcevpcconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            assert result is not None, "Required property 'security_group_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def subnet_ids(self) -> typing.List[builtins.str]:
            '''A list of identifiers for subnets within your Amazon VPC.

            The subnets should be able to connect to each other in the VPC, and they should have outgoing access to the Internet through a NAT device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-datasourcevpcconfiguration.html#cfn-kendra-datasource-datasourcevpcconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            assert result is not None, "Required property 'subnet_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.DatabaseConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "column_configuration": "columnConfiguration",
            "connection_configuration": "connectionConfiguration",
            "database_engine_type": "databaseEngineType",
            "acl_configuration": "aclConfiguration",
            "sql_configuration": "sqlConfiguration",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class DatabaseConfigurationProperty:
        def __init__(
            self,
            *,
            column_configuration: typing.Union[typing.Union["CfnDataSource.ColumnConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
            connection_configuration: typing.Union[typing.Union["CfnDataSource.ConnectionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
            database_engine_type: builtins.str,
            acl_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.AclConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            sql_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.SqlConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            vpc_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information to connect to a index.

            :param column_configuration: Information about where the index should get the document information from the database.
            :param connection_configuration: Configuration information that's required to connect to a database.
            :param database_engine_type: The type of database engine that runs the database.
            :param acl_configuration: Information about the database column that provides information for user context filtering.
            :param sql_configuration: Provides information about how Amazon Kendra uses quote marks around SQL identifiers when querying a database data source.
            :param vpc_configuration: Provides information for connecting to an Amazon VPC.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                database_configuration_property = kendra.CfnDataSource.DatabaseConfigurationProperty(
                    column_configuration=kendra.CfnDataSource.ColumnConfigurationProperty(
                        change_detecting_columns=["changeDetectingColumns"],
                        document_data_column_name="documentDataColumnName",
                        document_id_column_name="documentIdColumnName",
                
                        # the properties below are optional
                        document_title_column_name="documentTitleColumnName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    connection_configuration=kendra.CfnDataSource.ConnectionConfigurationProperty(
                        database_host="databaseHost",
                        database_name="databaseName",
                        database_port=123,
                        secret_arn="secretArn",
                        table_name="tableName"
                    ),
                    database_engine_type="databaseEngineType",
                
                    # the properties below are optional
                    acl_configuration=kendra.CfnDataSource.AclConfigurationProperty(
                        allowed_groups_column_name="allowedGroupsColumnName"
                    ),
                    sql_configuration=kendra.CfnDataSource.SqlConfigurationProperty(
                        query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                    ),
                    vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5428173a27262b90e5499e20bdad87f915015d24730fdc55d29ea42f98f783f9)
                check_type(argname="argument column_configuration", value=column_configuration, expected_type=type_hints["column_configuration"])
                check_type(argname="argument connection_configuration", value=connection_configuration, expected_type=type_hints["connection_configuration"])
                check_type(argname="argument database_engine_type", value=database_engine_type, expected_type=type_hints["database_engine_type"])
                check_type(argname="argument acl_configuration", value=acl_configuration, expected_type=type_hints["acl_configuration"])
                check_type(argname="argument sql_configuration", value=sql_configuration, expected_type=type_hints["sql_configuration"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "column_configuration": column_configuration,
                "connection_configuration": connection_configuration,
                "database_engine_type": database_engine_type,
            }
            if acl_configuration is not None:
                self._values["acl_configuration"] = acl_configuration
            if sql_configuration is not None:
                self._values["sql_configuration"] = sql_configuration
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def column_configuration(
            self,
        ) -> typing.Union["CfnDataSource.ColumnConfigurationProperty", _IResolvable_da3f097b]:
            '''Information about where the index should get the document information from the database.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-columnconfiguration
            '''
            result = self._values.get("column_configuration")
            assert result is not None, "Required property 'column_configuration' is missing"
            return typing.cast(typing.Union["CfnDataSource.ColumnConfigurationProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def connection_configuration(
            self,
        ) -> typing.Union["CfnDataSource.ConnectionConfigurationProperty", _IResolvable_da3f097b]:
            '''Configuration information that's required to connect to a database.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-connectionconfiguration
            '''
            result = self._values.get("connection_configuration")
            assert result is not None, "Required property 'connection_configuration' is missing"
            return typing.cast(typing.Union["CfnDataSource.ConnectionConfigurationProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def database_engine_type(self) -> builtins.str:
            '''The type of database engine that runs the database.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-databaseenginetype
            '''
            result = self._values.get("database_engine_type")
            assert result is not None, "Required property 'database_engine_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def acl_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.AclConfigurationProperty", _IResolvable_da3f097b]]:
            '''Information about the database column that provides information for user context filtering.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-aclconfiguration
            '''
            result = self._values.get("acl_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.AclConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def sql_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.SqlConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides information about how Amazon Kendra uses quote marks around SQL identifiers when querying a database data source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-sqlconfiguration
            '''
            result = self._values.get("sql_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.SqlConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides information for connecting to an Amazon VPC.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-databaseconfiguration.html#cfn-kendra-datasource-databaseconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.DocumentAttributeConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition_document_attribute_key": "conditionDocumentAttributeKey",
            "operator": "operator",
            "condition_on_value": "conditionOnValue",
        },
    )
    class DocumentAttributeConditionProperty:
        def __init__(
            self,
            *,
            condition_document_attribute_key: builtins.str,
            operator: builtins.str,
            condition_on_value: typing.Optional[typing.Union[typing.Union["CfnDataSource.DocumentAttributeValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''The condition used for the target document attribute or metadata field when ingesting documents into Amazon Kendra.

            You use this with `DocumentAttributeTarget to apply the condition <https://docs.aws.amazon.com/kendra/latest/dg/API_DocumentAttributeTarget.html>`_ .

            For example, you can create the 'Department' target field and have it prefill department names associated with the documents based on information in the 'Source_URI' field. Set the condition that if the 'Source_URI' field contains 'financial' in its URI value, then prefill the target field 'Department' with the target value 'Finance' for the document.

            Amazon Kendra cannot create a target field if it has not already been created as an index field. After you create your index field, you can create a document metadata field using ``DocumentAttributeTarget`` . Amazon Kendra then will map your newly created metadata field to your index field.

            :param condition_document_attribute_key: The identifier of the document attribute used for the condition. For example, 'Source_URI' could be an identifier for the attribute or metadata field that contains source URIs associated with the documents. Amazon Kendra currently does not support ``_document_body`` as an attribute key used for the condition.
            :param operator: The condition operator. For example, you can use 'Contains' to partially match a string.
            :param condition_on_value: The value used by the operator. For example, you can specify the value 'financial' for strings in the 'Source_URI' field that partially match or contain this value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributecondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                document_attribute_condition_property = kendra.CfnDataSource.DocumentAttributeConditionProperty(
                    condition_document_attribute_key="conditionDocumentAttributeKey",
                    operator="operator",
                
                    # the properties below are optional
                    condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                        date_value="dateValue",
                        long_value=123,
                        string_list_value=["stringListValue"],
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3be9f331fb30fc1120b64fb67b31c482fab661057041712cb9b0aa689b0c477)
                check_type(argname="argument condition_document_attribute_key", value=condition_document_attribute_key, expected_type=type_hints["condition_document_attribute_key"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
                check_type(argname="argument condition_on_value", value=condition_on_value, expected_type=type_hints["condition_on_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "condition_document_attribute_key": condition_document_attribute_key,
                "operator": operator,
            }
            if condition_on_value is not None:
                self._values["condition_on_value"] = condition_on_value

        @builtins.property
        def condition_document_attribute_key(self) -> builtins.str:
            '''The identifier of the document attribute used for the condition.

            For example, 'Source_URI' could be an identifier for the attribute or metadata field that contains source URIs associated with the documents.

            Amazon Kendra currently does not support ``_document_body`` as an attribute key used for the condition.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributecondition.html#cfn-kendra-datasource-documentattributecondition-conditiondocumentattributekey
            '''
            result = self._values.get("condition_document_attribute_key")
            assert result is not None, "Required property 'condition_document_attribute_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def operator(self) -> builtins.str:
            '''The condition operator.

            For example, you can use 'Contains' to partially match a string.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributecondition.html#cfn-kendra-datasource-documentattributecondition-operator
            '''
            result = self._values.get("operator")
            assert result is not None, "Required property 'operator' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def condition_on_value(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DocumentAttributeValueProperty", _IResolvable_da3f097b]]:
            '''The value used by the operator.

            For example, you can specify the value 'financial' for strings in the 'Source_URI' field that partially match or contain this value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributecondition.html#cfn-kendra-datasource-documentattributecondition-conditiononvalue
            '''
            result = self._values.get("condition_on_value")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DocumentAttributeValueProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.DocumentAttributeTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_document_attribute_key": "targetDocumentAttributeKey",
            "target_document_attribute_value": "targetDocumentAttributeValue",
            "target_document_attribute_value_deletion": "targetDocumentAttributeValueDeletion",
        },
    )
    class DocumentAttributeTargetProperty:
        def __init__(
            self,
            *,
            target_document_attribute_key: builtins.str,
            target_document_attribute_value: typing.Optional[typing.Union[typing.Union["CfnDataSource.DocumentAttributeValueProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''The target document attribute or metadata field you want to alter when ingesting documents into Amazon Kendra.

            For example, you can delete customer identification numbers associated with the documents, stored in the document metadata field called 'Customer_ID'. You set the target key as 'Customer_ID' and the deletion flag to ``TRUE`` . This removes all customer ID values in the field 'Customer_ID'. This would scrub personally identifiable information from each document's metadata.

            Amazon Kendra cannot create a target field if it has not already been created as an index field. After you create your index field, you can create a document metadata field using ``DocumentAttributeTarget`` . Amazon Kendra then will map your newly created metadata field to your index field.

            You can also use this with `DocumentAttributeCondition <https://docs.aws.amazon.com/kendra/latest/dg/API_DocumentAttributeCondition.html>`_ .

            :param target_document_attribute_key: The identifier of the target document attribute or metadata field. For example, 'Department' could be an identifier for the target attribute or metadata field that includes the department names associated with the documents.
            :param target_document_attribute_value: The target value you want to create for the target attribute. For example, 'Finance' could be the target value for the target attribute key 'Department'.
            :param target_document_attribute_value_deletion: ``TRUE`` to delete the existing target value for your specified target attribute key. You cannot create a target value and set this to ``TRUE`` . To create a target value ( ``TargetDocumentAttributeValue`` ), set this to ``FALSE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributetarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                document_attribute_target_property = kendra.CfnDataSource.DocumentAttributeTargetProperty(
                    target_document_attribute_key="targetDocumentAttributeKey",
                
                    # the properties below are optional
                    target_document_attribute_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                        date_value="dateValue",
                        long_value=123,
                        string_list_value=["stringListValue"],
                        string_value="stringValue"
                    ),
                    target_document_attribute_value_deletion=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3693fd552c97d013bc352a51fe708bffae6e362b87808be7aee9daf036f228f5)
                check_type(argname="argument target_document_attribute_key", value=target_document_attribute_key, expected_type=type_hints["target_document_attribute_key"])
                check_type(argname="argument target_document_attribute_value", value=target_document_attribute_value, expected_type=type_hints["target_document_attribute_value"])
                check_type(argname="argument target_document_attribute_value_deletion", value=target_document_attribute_value_deletion, expected_type=type_hints["target_document_attribute_value_deletion"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_document_attribute_key": target_document_attribute_key,
            }
            if target_document_attribute_value is not None:
                self._values["target_document_attribute_value"] = target_document_attribute_value
            if target_document_attribute_value_deletion is not None:
                self._values["target_document_attribute_value_deletion"] = target_document_attribute_value_deletion

        @builtins.property
        def target_document_attribute_key(self) -> builtins.str:
            '''The identifier of the target document attribute or metadata field.

            For example, 'Department' could be an identifier for the target attribute or metadata field that includes the department names associated with the documents.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributetarget.html#cfn-kendra-datasource-documentattributetarget-targetdocumentattributekey
            '''
            result = self._values.get("target_document_attribute_key")
            assert result is not None, "Required property 'target_document_attribute_key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target_document_attribute_value(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DocumentAttributeValueProperty", _IResolvable_da3f097b]]:
            '''The target value you want to create for the target attribute.

            For example, 'Finance' could be the target value for the target attribute key 'Department'.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributetarget.html#cfn-kendra-datasource-documentattributetarget-targetdocumentattributevalue
            '''
            result = self._values.get("target_document_attribute_value")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DocumentAttributeValueProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def target_document_attribute_value_deletion(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to delete the existing target value for your specified target attribute key.

            You cannot create a target value and set this to ``TRUE`` . To create a target value ( ``TargetDocumentAttributeValue`` ), set this to ``FALSE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributetarget.html#cfn-kendra-datasource-documentattributetarget-targetdocumentattributevaluedeletion
            '''
            result = self._values.get("target_document_attribute_value_deletion")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.DocumentAttributeValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "date_value": "dateValue",
            "long_value": "longValue",
            "string_list_value": "stringListValue",
            "string_value": "stringValue",
        },
    )
    class DocumentAttributeValueProperty:
        def __init__(
            self,
            *,
            date_value: typing.Optional[builtins.str] = None,
            long_value: typing.Optional[jsii.Number] = None,
            string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The value of a document attribute.

            You can only provide one value for a document attribute.

            :param date_value: A date expressed as an ISO 8601 string. It is important for the time zone to be included in the ISO 8601 date-time format. For example, 2012-03-25T12:30:10+01:00 is the ISO 8601 date-time format for March 25th 2012 at 12:30PM (plus 10 seconds) in Central European Time.
            :param long_value: A long integer value.
            :param string_list_value: A list of strings. The default maximum length or number of strings is 10.
            :param string_value: A string, such as "department".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                document_attribute_value_property = kendra.CfnDataSource.DocumentAttributeValueProperty(
                    date_value="dateValue",
                    long_value=123,
                    string_list_value=["stringListValue"],
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6664394a01ef732c5ed7f23d9d64a2dd01e3979fcbd6c750a603aa225b728522)
                check_type(argname="argument date_value", value=date_value, expected_type=type_hints["date_value"])
                check_type(argname="argument long_value", value=long_value, expected_type=type_hints["long_value"])
                check_type(argname="argument string_list_value", value=string_list_value, expected_type=type_hints["string_list_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if date_value is not None:
                self._values["date_value"] = date_value
            if long_value is not None:
                self._values["long_value"] = long_value
            if string_list_value is not None:
                self._values["string_list_value"] = string_list_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def date_value(self) -> typing.Optional[builtins.str]:
            '''A date expressed as an ISO 8601 string.

            It is important for the time zone to be included in the ISO 8601 date-time format. For example, 2012-03-25T12:30:10+01:00 is the ISO 8601 date-time format for March 25th 2012 at 12:30PM (plus 10 seconds) in Central European Time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html#cfn-kendra-datasource-documentattributevalue-datevalue
            '''
            result = self._values.get("date_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def long_value(self) -> typing.Optional[jsii.Number]:
            '''A long integer value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html#cfn-kendra-datasource-documentattributevalue-longvalue
            '''
            result = self._values.get("long_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def string_list_value(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of strings.

            The default maximum length or number of strings is 10.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html#cfn-kendra-datasource-documentattributevalue-stringlistvalue
            '''
            result = self._values.get("string_list_value")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''A string, such as "department".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentattributevalue.html#cfn-kendra-datasource-documentattributevalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentAttributeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.DocumentsMetadataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_prefix": "s3Prefix"},
    )
    class DocumentsMetadataConfigurationProperty:
        def __init__(self, *, s3_prefix: typing.Optional[builtins.str] = None) -> None:
            '''Document metadata files that contain information such as the document access control information, source URI, document author, and custom attributes.

            Each metadata file contains metadata about a single document.

            :param s3_prefix: A prefix used to filter metadata configuration files in the AWS S3 bucket. The S3 bucket might contain multiple metadata files. Use ``S3Prefix`` to include only the desired metadata files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentsmetadataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                documents_metadata_configuration_property = kendra.CfnDataSource.DocumentsMetadataConfigurationProperty(
                    s3_prefix="s3Prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63838fe65353180f3dde04339d577dd6cef52eeb9c6cb95bdd18eabb89519089)
                check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_prefix is not None:
                self._values["s3_prefix"] = s3_prefix

        @builtins.property
        def s3_prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix used to filter metadata configuration files in the AWS S3 bucket.

            The S3 bucket might contain multiple metadata files. Use ``S3Prefix`` to include only the desired metadata files.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-documentsmetadataconfiguration.html#cfn-kendra-datasource-documentsmetadataconfiguration-s3prefix
            '''
            result = self._values.get("s3_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentsMetadataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.GoogleDriveConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secret_arn": "secretArn",
            "exclude_mime_types": "excludeMimeTypes",
            "exclude_shared_drives": "excludeSharedDrives",
            "exclude_user_accounts": "excludeUserAccounts",
            "exclusion_patterns": "exclusionPatterns",
            "field_mappings": "fieldMappings",
            "inclusion_patterns": "inclusionPatterns",
        },
    )
    class GoogleDriveConfigurationProperty:
        def __init__(
            self,
            *,
            secret_arn: builtins.str,
            exclude_mime_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            exclude_shared_drives: typing.Optional[typing.Sequence[builtins.str]] = None,
            exclude_user_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information to connect to Google Drive as your data source.

            :param secret_arn: The Amazon Resource Name (ARN) of a AWS Secrets Manager secret that contains the credentials required to connect to Google Drive. For more information, see `Using a Google Workspace Drive data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-google-drive.html>`_ .
            :param exclude_mime_types: A list of MIME types to exclude from the index. All documents matching the specified MIME type are excluded. For a list of MIME types, see `Using a Google Workspace Drive data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-google-drive.html>`_ .
            :param exclude_shared_drives: A list of identifiers or shared drives to exclude from the index. All files and folders stored on the shared drive are excluded.
            :param exclude_user_accounts: A list of email addresses of the users. Documents owned by these users are excluded from the index. Documents shared with excluded users are indexed unless they are excluded in another way.
            :param exclusion_patterns: A list of regular expression patterns to exclude certain items in your Google Drive, including shared drives and users' My Drives. Items that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.
            :param field_mappings: Maps Google Drive data source attributes or field names to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Google Drive fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Google Drive data source field names must exist in your Google Drive custom metadata.
            :param inclusion_patterns: A list of regular expression patterns to include certain items in your Google Drive, including shared drives and users' My Drives. Items that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                google_drive_configuration_property = kendra.CfnDataSource.GoogleDriveConfigurationProperty(
                    secret_arn="secretArn",
                
                    # the properties below are optional
                    exclude_mime_types=["excludeMimeTypes"],
                    exclude_shared_drives=["excludeSharedDrives"],
                    exclude_user_accounts=["excludeUserAccounts"],
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    inclusion_patterns=["inclusionPatterns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c923274fb398190dddefca2aff2f3ac3a6a978b70c7d65bb404d600266d9b1fc)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument exclude_mime_types", value=exclude_mime_types, expected_type=type_hints["exclude_mime_types"])
                check_type(argname="argument exclude_shared_drives", value=exclude_shared_drives, expected_type=type_hints["exclude_shared_drives"])
                check_type(argname="argument exclude_user_accounts", value=exclude_user_accounts, expected_type=type_hints["exclude_user_accounts"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secret_arn": secret_arn,
            }
            if exclude_mime_types is not None:
                self._values["exclude_mime_types"] = exclude_mime_types
            if exclude_shared_drives is not None:
                self._values["exclude_shared_drives"] = exclude_shared_drives
            if exclude_user_accounts is not None:
                self._values["exclude_user_accounts"] = exclude_user_accounts
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of a AWS Secrets Manager secret that contains the credentials required to connect to Google Drive.

            For more information, see `Using a Google Workspace Drive data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-google-drive.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def exclude_mime_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of MIME types to exclude from the index. All documents matching the specified MIME type are excluded.

            For a list of MIME types, see `Using a Google Workspace Drive data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-google-drive.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-excludemimetypes
            '''
            result = self._values.get("exclude_mime_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exclude_shared_drives(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of identifiers or shared drives to exclude from the index.

            All files and folders stored on the shared drive are excluded.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-excludeshareddrives
            '''
            result = self._values.get("exclude_shared_drives")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exclude_user_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of email addresses of the users.

            Documents owned by these users are excluded from the index. Documents shared with excluded users are indexed unless they are excluded in another way.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-excludeuseraccounts
            '''
            result = self._values.get("exclude_user_accounts")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain items in your Google Drive, including shared drives and users' My Drives.

            Items that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps Google Drive data source attributes or field names to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Google Drive fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Google Drive data source field names must exist in your Google Drive custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain items in your Google Drive, including shared drives and users' My Drives.

            Items that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-googledriveconfiguration.html#cfn-kendra-datasource-googledriveconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoogleDriveConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.HookConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lambda_arn": "lambdaArn",
            "s3_bucket": "s3Bucket",
            "invocation_condition": "invocationCondition",
        },
    )
    class HookConfigurationProperty:
        def __init__(
            self,
            *,
            lambda_arn: builtins.str,
            s3_bucket: builtins.str,
            invocation_condition: typing.Optional[typing.Union[typing.Union["CfnDataSource.DocumentAttributeConditionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information for invoking a Lambda function in AWS Lambda to alter document metadata and content when ingesting documents into Amazon Kendra.

            You can configure your Lambda function using `PreExtractionHookConfiguration <https://docs.aws.amazon.com/kendra/latest/dg/API_CustomDocumentEnrichmentConfiguration.html>`_ if you want to apply advanced alterations on the original or raw documents. If you want to apply advanced alterations on the Amazon Kendra structured documents, you must configure your Lambda function using `PostExtractionHookConfiguration <https://docs.aws.amazon.com/kendra/latest/dg/API_CustomDocumentEnrichmentConfiguration.html>`_ . You can only invoke one Lambda function. However, this function can invoke other functions it requires.

            For more information, see `Customizing document metadata during the ingestion process <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html>`_ .

            :param lambda_arn: The Amazon Resource Name (ARN) of a role with permission to run a Lambda function during ingestion. For more information, see `IAM roles for Amazon Kendra <https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html>`_ .
            :param s3_bucket: Stores the original, raw documents or the structured, parsed documents before and after altering them. For more information, see `Data contracts for Lambda functions <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#cde-data-contracts-lambda>`_ .
            :param invocation_condition: The condition used for when a Lambda function should be invoked. For example, you can specify a condition that if there are empty date-time values, then Amazon Kendra should invoke a function that inserts the current date-time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-hookconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                hook_configuration_property = kendra.CfnDataSource.HookConfigurationProperty(
                    lambda_arn="lambdaArn",
                    s3_bucket="s3Bucket",
                
                    # the properties below are optional
                    invocation_condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        operator="operator",
                
                        # the properties below are optional
                        condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__30b34e4d4b505681b8da4219b35bde24bf8a24d5dbe80f37f1c166073c9cbfd1)
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument invocation_condition", value=invocation_condition, expected_type=type_hints["invocation_condition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "lambda_arn": lambda_arn,
                "s3_bucket": s3_bucket,
            }
            if invocation_condition is not None:
                self._values["invocation_condition"] = invocation_condition

        @builtins.property
        def lambda_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of a role with permission to run a Lambda function during ingestion.

            For more information, see `IAM roles for Amazon Kendra <https://docs.aws.amazon.com/kendra/latest/dg/iam-roles.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-hookconfiguration.html#cfn-kendra-datasource-hookconfiguration-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            assert result is not None, "Required property 'lambda_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''Stores the original, raw documents or the structured, parsed documents before and after altering them.

            For more information, see `Data contracts for Lambda functions <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html#cde-data-contracts-lambda>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-hookconfiguration.html#cfn-kendra-datasource-hookconfiguration-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def invocation_condition(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DocumentAttributeConditionProperty", _IResolvable_da3f097b]]:
            '''The condition used for when a Lambda function should be invoked.

            For example, you can specify a condition that if there are empty date-time values, then Amazon Kendra should invoke a function that inserts the current date-time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-hookconfiguration.html#cfn-kendra-datasource-hookconfiguration-invocationcondition
            '''
            result = self._values.get("invocation_condition")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DocumentAttributeConditionProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HookConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition": "condition",
            "document_content_deletion": "documentContentDeletion",
            "target": "target",
        },
    )
    class InlineCustomDocumentEnrichmentConfigurationProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[typing.Union[typing.Union["CfnDataSource.DocumentAttributeConditionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            document_content_deletion: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            target: typing.Optional[typing.Union[typing.Union["CfnDataSource.DocumentAttributeTargetProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information for applying basic logic to alter document metadata and content when ingesting documents into Amazon Kendra.

            To apply advanced logic, to go beyond what you can do with basic logic, see `HookConfiguration <https://docs.aws.amazon.com/kendra/latest/dg/API_HookConfiguration.html>`_ .

            For more information, see `Customizing document metadata during the ingestion process <https://docs.aws.amazon.com/kendra/latest/dg/custom-document-enrichment.html>`_ .

            :param condition: Configuration of the condition used for the target document attribute or metadata field when ingesting documents into Amazon Kendra.
            :param document_content_deletion: ``TRUE`` to delete content if the condition used for the target attribute is met.
            :param target: Configuration of the target document attribute or metadata field when ingesting documents into Amazon Kendra. You can also include a value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-inlinecustomdocumentenrichmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                inline_custom_document_enrichment_configuration_property = kendra.CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty(
                    condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                        condition_document_attribute_key="conditionDocumentAttributeKey",
                        operator="operator",
                
                        # the properties below are optional
                        condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        )
                    ),
                    document_content_deletion=False,
                    target=kendra.CfnDataSource.DocumentAttributeTargetProperty(
                        target_document_attribute_key="targetDocumentAttributeKey",
                
                        # the properties below are optional
                        target_document_attribute_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                            date_value="dateValue",
                            long_value=123,
                            string_list_value=["stringListValue"],
                            string_value="stringValue"
                        ),
                        target_document_attribute_value_deletion=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39b4fdb9078ccf6b1abef814c1fa86146c3c7faee58757787d7e3ccd0de3b5eb)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument document_content_deletion", value=document_content_deletion, expected_type=type_hints["document_content_deletion"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if document_content_deletion is not None:
                self._values["document_content_deletion"] = document_content_deletion
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def condition(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DocumentAttributeConditionProperty", _IResolvable_da3f097b]]:
            '''Configuration of the condition used for the target document attribute or metadata field when ingesting documents into Amazon Kendra.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-inlinecustomdocumentenrichmentconfiguration.html#cfn-kendra-datasource-inlinecustomdocumentenrichmentconfiguration-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DocumentAttributeConditionProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def document_content_deletion(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to delete content if the condition used for the target attribute is met.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-inlinecustomdocumentenrichmentconfiguration.html#cfn-kendra-datasource-inlinecustomdocumentenrichmentconfiguration-documentcontentdeletion
            '''
            result = self._values.get("document_content_deletion")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def target(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DocumentAttributeTargetProperty", _IResolvable_da3f097b]]:
            '''Configuration of the target document attribute or metadata field when ingesting documents into Amazon Kendra.

            You can also include a value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-inlinecustomdocumentenrichmentconfiguration.html#cfn-kendra-datasource-inlinecustomdocumentenrichmentconfiguration-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DocumentAttributeTargetProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InlineCustomDocumentEnrichmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.OneDriveConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "one_drive_users": "oneDriveUsers",
            "secret_arn": "secretArn",
            "tenant_domain": "tenantDomain",
            "disable_local_groups": "disableLocalGroups",
            "exclusion_patterns": "exclusionPatterns",
            "field_mappings": "fieldMappings",
            "inclusion_patterns": "inclusionPatterns",
        },
    )
    class OneDriveConfigurationProperty:
        def __init__(
            self,
            *,
            one_drive_users: typing.Union[typing.Union["CfnDataSource.OneDriveUsersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
            secret_arn: builtins.str,
            tenant_domain: builtins.str,
            disable_local_groups: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information to connect to OneDrive as your data source.

            :param one_drive_users: A list of user accounts whose documents should be indexed.
            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password to connect to OneDrive. The user name should be the application ID for the OneDrive application, and the password is the application key for the OneDrive application.
            :param tenant_domain: The Azure Active Directory domain of the organization.
            :param disable_local_groups: ``TRUE`` to disable local groups information.
            :param exclusion_patterns: A list of regular expression patterns to exclude certain documents in your OneDrive. Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The pattern is applied to the file name.
            :param field_mappings: A list of ``DataSourceToIndexFieldMapping`` objects that map OneDrive data source attributes or field names to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to OneDrive fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The OneDrive data source field names must exist in your OneDrive custom metadata.
            :param inclusion_patterns: A list of regular expression patterns to include certain documents in your OneDrive. Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The pattern is applied to the file name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                one_drive_configuration_property = kendra.CfnDataSource.OneDriveConfigurationProperty(
                    one_drive_users=kendra.CfnDataSource.OneDriveUsersProperty(
                        one_drive_user_list=["oneDriveUserList"],
                        one_drive_user_s3_path=kendra.CfnDataSource.S3PathProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    secret_arn="secretArn",
                    tenant_domain="tenantDomain",
                
                    # the properties below are optional
                    disable_local_groups=False,
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    inclusion_patterns=["inclusionPatterns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__695d703d8c0b001be62c56ad50f3f4af915709c1284c26e428bfb6be0244d2ee)
                check_type(argname="argument one_drive_users", value=one_drive_users, expected_type=type_hints["one_drive_users"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument tenant_domain", value=tenant_domain, expected_type=type_hints["tenant_domain"])
                check_type(argname="argument disable_local_groups", value=disable_local_groups, expected_type=type_hints["disable_local_groups"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "one_drive_users": one_drive_users,
                "secret_arn": secret_arn,
                "tenant_domain": tenant_domain,
            }
            if disable_local_groups is not None:
                self._values["disable_local_groups"] = disable_local_groups
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns

        @builtins.property
        def one_drive_users(
            self,
        ) -> typing.Union["CfnDataSource.OneDriveUsersProperty", _IResolvable_da3f097b]:
            '''A list of user accounts whose documents should be indexed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-onedriveusers
            '''
            result = self._values.get("one_drive_users")
            assert result is not None, "Required property 'one_drive_users' is missing"
            return typing.cast(typing.Union["CfnDataSource.OneDriveUsersProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password to connect to OneDrive.

            The user name should be the application ID for the OneDrive application, and the password is the application key for the OneDrive application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def tenant_domain(self) -> builtins.str:
            '''The Azure Active Directory domain of the organization.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-tenantdomain
            '''
            result = self._values.get("tenant_domain")
            assert result is not None, "Required property 'tenant_domain' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def disable_local_groups(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to disable local groups information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-disablelocalgroups
            '''
            result = self._values.get("disable_local_groups")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain documents in your OneDrive.

            Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The pattern is applied to the file name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''A list of ``DataSourceToIndexFieldMapping`` objects that map OneDrive data source attributes or field names to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to OneDrive fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The OneDrive data source field names must exist in your OneDrive custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain documents in your OneDrive.

            Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The pattern is applied to the file name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveconfiguration.html#cfn-kendra-datasource-onedriveconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OneDriveConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.OneDriveUsersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "one_drive_user_list": "oneDriveUserList",
            "one_drive_user_s3_path": "oneDriveUserS3Path",
        },
    )
    class OneDriveUsersProperty:
        def __init__(
            self,
            *,
            one_drive_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            one_drive_user_s3_path: typing.Optional[typing.Union[typing.Union["CfnDataSource.S3PathProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''User accounts whose documents should be indexed.

            :param one_drive_user_list: A list of users whose documents should be indexed. Specify the user names in email format, for example, ``username@tenantdomain`` . If you need to index the documents of more than 100 users, use the ``OneDriveUserS3Path`` field to specify the location of a file containing a list of users.
            :param one_drive_user_s3_path: The S3 bucket location of a file containing a list of users whose documents should be indexed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveusers.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                one_drive_users_property = kendra.CfnDataSource.OneDriveUsersProperty(
                    one_drive_user_list=["oneDriveUserList"],
                    one_drive_user_s3_path=kendra.CfnDataSource.S3PathProperty(
                        bucket="bucket",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46b04aeb33b4fb722bc28444a3f3940da82f4017481948bf35f98659f0beb957)
                check_type(argname="argument one_drive_user_list", value=one_drive_user_list, expected_type=type_hints["one_drive_user_list"])
                check_type(argname="argument one_drive_user_s3_path", value=one_drive_user_s3_path, expected_type=type_hints["one_drive_user_s3_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if one_drive_user_list is not None:
                self._values["one_drive_user_list"] = one_drive_user_list
            if one_drive_user_s3_path is not None:
                self._values["one_drive_user_s3_path"] = one_drive_user_s3_path

        @builtins.property
        def one_drive_user_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of users whose documents should be indexed.

            Specify the user names in email format, for example, ``username@tenantdomain`` . If you need to index the documents of more than 100 users, use the ``OneDriveUserS3Path`` field to specify the location of a file containing a list of users.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveusers.html#cfn-kendra-datasource-onedriveusers-onedriveuserlist
            '''
            result = self._values.get("one_drive_user_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def one_drive_user_s3_path(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.S3PathProperty", _IResolvable_da3f097b]]:
            '''The S3 bucket location of a file containing a list of users whose documents should be indexed.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-onedriveusers.html#cfn-kendra-datasource-onedriveusers-onedriveusers3path
            '''
            result = self._values.get("one_drive_user_s3_path")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.S3PathProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OneDriveUsersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ProxyConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"host": "host", "port": "port", "credentials": "credentials"},
    )
    class ProxyConfigurationProperty:
        def __init__(
            self,
            *,
            host: builtins.str,
            port: jsii.Number,
            credentials: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for a web proxy to connect to website hosts.

            :param host: The name of the website host you want to connect to via a web proxy server. For example, the host name of https://a.example.com/page1.html is "a.example.com".
            :param port: The port number of the website host you want to connect to via a web proxy server. For example, the port for https://a.example.com/page1.html is 443, the standard port for HTTPS.
            :param credentials: Your secret ARN, which you can create in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_. The credentials are optional. You use a secret if web proxy credentials are required to connect to a website host. Amazon Kendra currently support basic authentication to connect to a web proxy server. The secret stores your credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-proxyconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                proxy_configuration_property = kendra.CfnDataSource.ProxyConfigurationProperty(
                    host="host",
                    port=123,
                
                    # the properties below are optional
                    credentials="credentials"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__52f669b52413aa28c0992bb60e68a3c50446a0d55409ec1ac95e949617563ad8)
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "host": host,
                "port": port,
            }
            if credentials is not None:
                self._values["credentials"] = credentials

        @builtins.property
        def host(self) -> builtins.str:
            '''The name of the website host you want to connect to via a web proxy server.

            For example, the host name of https://a.example.com/page1.html is "a.example.com".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-proxyconfiguration.html#cfn-kendra-datasource-proxyconfiguration-host
            '''
            result = self._values.get("host")
            assert result is not None, "Required property 'host' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def port(self) -> jsii.Number:
            '''The port number of the website host you want to connect to via a web proxy server.

            For example, the port for https://a.example.com/page1.html is 443, the standard port for HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-proxyconfiguration.html#cfn-kendra-datasource-proxyconfiguration-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def credentials(self) -> typing.Optional[builtins.str]:
            '''Your secret ARN, which you can create in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_.

            The credentials are optional. You use a secret if web proxy credentials are required to connect to a website host. Amazon Kendra currently support basic authentication to connect to a web proxy server. The secret stores your credentials.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-proxyconfiguration.html#cfn-kendra-datasource-proxyconfiguration-credentials
            '''
            result = self._values.get("credentials")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProxyConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.S3DataSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "access_control_list_configuration": "accessControlListConfiguration",
            "documents_metadata_configuration": "documentsMetadataConfiguration",
            "exclusion_patterns": "exclusionPatterns",
            "inclusion_patterns": "inclusionPatterns",
            "inclusion_prefixes": "inclusionPrefixes",
        },
    )
    class S3DataSourceConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            access_control_list_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.AccessControlListConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            documents_metadata_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.DocumentsMetadataConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information to connect to an Amazon S3 bucket.

            :param bucket_name: The name of the bucket that contains the documents.
            :param access_control_list_configuration: Provides the path to the S3 bucket that contains the user context filtering files for the data source. For the format of the file, see `Access control for S3 data sources <https://docs.aws.amazon.com/kendra/latest/dg/s3-acl.html>`_ .
            :param documents_metadata_configuration: Specifies document metadata files that contain information such as the document access control information, source URI, document author, and custom attributes. Each metadata file contains metadata about a single document.
            :param exclusion_patterns: A list of glob patterns for documents that should not be indexed. If a document that matches an inclusion prefix or inclusion pattern also matches an exclusion pattern, the document is not indexed. Some `examples <https://docs.aws.amazon.com/cli/latest/reference/s3/#use-of-exclude-and-include-filters>`_ are: - **.png , *.jpg* will exclude all PNG and JPEG image files in a directory (files with the extensions .png and .jpg). - **internal** will exclude all files in a directory that contain 'internal' in the file name, such as 'internal', 'internal_only', 'company_internal'. - *** /*internal** will exclude all internal-related files in a directory and its subdirectories.
            :param inclusion_patterns: A list of glob patterns for documents that should be indexed. If a document that matches an inclusion pattern also matches an exclusion pattern, the document is not indexed. Some `examples <https://docs.aws.amazon.com/cli/latest/reference/s3/#use-of-exclude-and-include-filters>`_ are: - **.txt* will include all text files in a directory (files with the extension .txt). - *** /*.txt* will include all text files in a directory and its subdirectories. - **tax** will include all files in a directory that contain 'tax' in the file name, such as 'tax', 'taxes', 'income_tax'.
            :param inclusion_prefixes: A list of S3 prefixes for the documents that should be included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                s3_data_source_configuration_property = kendra.CfnDataSource.S3DataSourceConfigurationProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    access_control_list_configuration=kendra.CfnDataSource.AccessControlListConfigurationProperty(
                        key_path="keyPath"
                    ),
                    documents_metadata_configuration=kendra.CfnDataSource.DocumentsMetadataConfigurationProperty(
                        s3_prefix="s3Prefix"
                    ),
                    exclusion_patterns=["exclusionPatterns"],
                    inclusion_patterns=["inclusionPatterns"],
                    inclusion_prefixes=["inclusionPrefixes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f41f6acb59e7453a4f264b5ea7dbe69a5cb3e25cbafd939a140f294a596121a)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument access_control_list_configuration", value=access_control_list_configuration, expected_type=type_hints["access_control_list_configuration"])
                check_type(argname="argument documents_metadata_configuration", value=documents_metadata_configuration, expected_type=type_hints["documents_metadata_configuration"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument inclusion_prefixes", value=inclusion_prefixes, expected_type=type_hints["inclusion_prefixes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if access_control_list_configuration is not None:
                self._values["access_control_list_configuration"] = access_control_list_configuration
            if documents_metadata_configuration is not None:
                self._values["documents_metadata_configuration"] = documents_metadata_configuration
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if inclusion_prefixes is not None:
                self._values["inclusion_prefixes"] = inclusion_prefixes

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The name of the bucket that contains the documents.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def access_control_list_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.AccessControlListConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides the path to the S3 bucket that contains the user context filtering files for the data source.

            For the format of the file, see `Access control for S3 data sources <https://docs.aws.amazon.com/kendra/latest/dg/s3-acl.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-accesscontrollistconfiguration
            '''
            result = self._values.get("access_control_list_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.AccessControlListConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def documents_metadata_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DocumentsMetadataConfigurationProperty", _IResolvable_da3f097b]]:
            '''Specifies document metadata files that contain information such as the document access control information, source URI, document author, and custom attributes.

            Each metadata file contains metadata about a single document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-documentsmetadataconfiguration
            '''
            result = self._values.get("documents_metadata_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DocumentsMetadataConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of glob patterns for documents that should not be indexed.

            If a document that matches an inclusion prefix or inclusion pattern also matches an exclusion pattern, the document is not indexed.

            Some `examples <https://docs.aws.amazon.com/cli/latest/reference/s3/#use-of-exclude-and-include-filters>`_ are:

            - **.png , *.jpg* will exclude all PNG and JPEG image files in a directory (files with the extensions .png and .jpg).
            - **internal** will exclude all files in a directory that contain 'internal' in the file name, such as 'internal', 'internal_only', 'company_internal'.
            - *** /*internal** will exclude all internal-related files in a directory and its subdirectories.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of glob patterns for documents that should be indexed.

            If a document that matches an inclusion pattern also matches an exclusion pattern, the document is not indexed.

            Some `examples <https://docs.aws.amazon.com/cli/latest/reference/s3/#use-of-exclude-and-include-filters>`_ are:

            - **.txt* will include all text files in a directory (files with the extension .txt).
            - *** /*.txt* will include all text files in a directory and its subdirectories.
            - **tax** will include all files in a directory that contain 'tax' in the file name, such as 'tax', 'taxes', 'income_tax'.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def inclusion_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of S3 prefixes for the documents that should be included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3datasourceconfiguration.html#cfn-kendra-datasource-s3datasourceconfiguration-inclusionprefixes
            '''
            result = self._values.get("inclusion_prefixes")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DataSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.S3PathProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3PathProperty:
        def __init__(self, *, bucket: builtins.str, key: builtins.str) -> None:
            '''Information required to find a specific file in an Amazon S3 bucket.

            :param bucket: The name of the S3 bucket that contains the file.
            :param key: The name of the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3path.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                s3_path_property = kendra.CfnDataSource.S3PathProperty(
                    bucket="bucket",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b4797593ba73adebab81646e1462689b8c7372f077d548f405b2bb475d02f9f)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }

        @builtins.property
        def bucket(self) -> builtins.str:
            '''The name of the S3 bucket that contains the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3path.html#cfn-kendra-datasource-s3path-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''The name of the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-s3path.html#cfn-kendra-datasource-s3path-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3PathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SalesforceChatterFeedConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
            "include_filter_types": "includeFilterTypes",
        },
    )
    class SalesforceChatterFeedConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: builtins.str,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            include_filter_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration information for syncing a Salesforce chatter feed.

            The contents of the object comes from the Salesforce FeedItem table.

            :param document_data_field_name: The name of the column in the Salesforce FeedItem table that contains the content to index. Typically this is the ``Body`` column.
            :param document_title_field_name: The name of the column in the Salesforce FeedItem table that contains the title of the document. This is typically the ``Title`` column.
            :param field_mappings: Maps fields from a Salesforce chatter feed into Amazon Kendra index fields.
            :param include_filter_types: Filters the documents in the feed based on status of the user. When you specify ``ACTIVE_USERS`` only documents from users who have an active account are indexed. When you specify ``STANDARD_USER`` only documents for Salesforce standard users are documented. You can specify both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                salesforce_chatter_feed_configuration_property = kendra.CfnDataSource.SalesforceChatterFeedConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                
                    # the properties below are optional
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    include_filter_types=["includeFilterTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a6483dd014a4f5b7c359695864d6e8e429fff879adca08f318e87dc0a92a743)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument include_filter_types", value=include_filter_types, expected_type=type_hints["include_filter_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "document_data_field_name": document_data_field_name,
            }
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if include_filter_types is not None:
                self._values["include_filter_types"] = include_filter_types

        @builtins.property
        def document_data_field_name(self) -> builtins.str:
            '''The name of the column in the Salesforce FeedItem table that contains the content to index.

            Typically this is the ``Body`` column.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html#cfn-kendra-datasource-salesforcechatterfeedconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            assert result is not None, "Required property 'document_data_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the column in the Salesforce FeedItem table that contains the title of the document.

            This is typically the ``Title`` column.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html#cfn-kendra-datasource-salesforcechatterfeedconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps fields from a Salesforce chatter feed into Amazon Kendra index fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html#cfn-kendra-datasource-salesforcechatterfeedconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def include_filter_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Filters the documents in the feed based on status of the user.

            When you specify ``ACTIVE_USERS`` only documents from users who have an active account are indexed. When you specify ``STANDARD_USER`` only documents for Salesforce standard users are documented. You can specify both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcechatterfeedconfiguration.html#cfn-kendra-datasource-salesforcechatterfeedconfiguration-includefiltertypes
            '''
            result = self._values.get("include_filter_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceChatterFeedConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SalesforceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secret_arn": "secretArn",
            "server_url": "serverUrl",
            "chatter_feed_configuration": "chatterFeedConfiguration",
            "crawl_attachments": "crawlAttachments",
            "exclude_attachment_file_patterns": "excludeAttachmentFilePatterns",
            "include_attachment_file_patterns": "includeAttachmentFilePatterns",
            "knowledge_article_configuration": "knowledgeArticleConfiguration",
            "standard_object_attachment_configuration": "standardObjectAttachmentConfiguration",
            "standard_object_configurations": "standardObjectConfigurations",
        },
    )
    class SalesforceConfigurationProperty:
        def __init__(
            self,
            *,
            secret_arn: builtins.str,
            server_url: builtins.str,
            chatter_feed_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.SalesforceChatterFeedConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            knowledge_article_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            standard_object_attachment_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            standard_object_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.SalesforceStandardObjectConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Provides the configuration information to connect to Salesforce as your data source.

            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the key/value pairs required to connect to your Salesforce instance. The secret must contain a JSON structure with the following keys: - authenticationUrl - The OAUTH endpoint that Amazon Kendra connects to get an OAUTH token. - consumerKey - The application public key generated when you created your Salesforce application. - consumerSecret - The application private key generated when you created your Salesforce application. - password - The password associated with the user logging in to the Salesforce instance. - securityToken - The token associated with the user logging in to the Salesforce instance. - username - The user name of the user logging in to the Salesforce instance.
            :param server_url: The instance URL for the Salesforce site that you want to index.
            :param chatter_feed_configuration: Configuration information for Salesforce chatter feeds.
            :param crawl_attachments: Indicates whether Amazon Kendra should index attachments to Salesforce objects.
            :param exclude_attachment_file_patterns: A list of regular expression patterns to exclude certain documents in your Salesforce. Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The pattern is applied to the name of the attached file.
            :param include_attachment_file_patterns: A list of regular expression patterns to include certain documents in your Salesforce. Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The pattern is applied to the name of the attached file.
            :param knowledge_article_configuration: Configuration information for the knowledge article types that Amazon Kendra indexes. Amazon Kendra indexes standard knowledge articles and the standard fields of knowledge articles, or the custom fields of custom knowledge articles, but not both.
            :param standard_object_attachment_configuration: Configuration information for processing attachments to Salesforce standard objects.
            :param standard_object_configurations: Configuration of the Salesforce standard objects that Amazon Kendra indexes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                salesforce_configuration_property = kendra.CfnDataSource.SalesforceConfigurationProperty(
                    secret_arn="secretArn",
                    server_url="serverUrl",
                
                    # the properties below are optional
                    chatter_feed_configuration=kendra.CfnDataSource.SalesforceChatterFeedConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                
                        # the properties below are optional
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        include_filter_types=["includeFilterTypes"]
                    ),
                    crawl_attachments=False,
                    exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                    include_attachment_file_patterns=["includeAttachmentFilePatterns"],
                    knowledge_article_configuration=kendra.CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty(
                        included_states=["includedStates"],
                
                        # the properties below are optional
                        custom_knowledge_article_type_configurations=[kendra.CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            name="name",
                
                            # the properties below are optional
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        )],
                        standard_knowledge_article_type_configuration=kendra.CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                
                            # the properties below are optional
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
                
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        )
                    ),
                    standard_object_attachment_configuration=kendra.CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty(
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    ),
                    standard_object_configurations=[kendra.CfnDataSource.SalesforceStandardObjectConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        name="name",
                
                        # the properties below are optional
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e3f13b2ba7bea487e478e44d5d01f374af605ea8a37637189ddbfa2bada9ef3)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument server_url", value=server_url, expected_type=type_hints["server_url"])
                check_type(argname="argument chatter_feed_configuration", value=chatter_feed_configuration, expected_type=type_hints["chatter_feed_configuration"])
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
                check_type(argname="argument exclude_attachment_file_patterns", value=exclude_attachment_file_patterns, expected_type=type_hints["exclude_attachment_file_patterns"])
                check_type(argname="argument include_attachment_file_patterns", value=include_attachment_file_patterns, expected_type=type_hints["include_attachment_file_patterns"])
                check_type(argname="argument knowledge_article_configuration", value=knowledge_article_configuration, expected_type=type_hints["knowledge_article_configuration"])
                check_type(argname="argument standard_object_attachment_configuration", value=standard_object_attachment_configuration, expected_type=type_hints["standard_object_attachment_configuration"])
                check_type(argname="argument standard_object_configurations", value=standard_object_configurations, expected_type=type_hints["standard_object_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secret_arn": secret_arn,
                "server_url": server_url,
            }
            if chatter_feed_configuration is not None:
                self._values["chatter_feed_configuration"] = chatter_feed_configuration
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments
            if exclude_attachment_file_patterns is not None:
                self._values["exclude_attachment_file_patterns"] = exclude_attachment_file_patterns
            if include_attachment_file_patterns is not None:
                self._values["include_attachment_file_patterns"] = include_attachment_file_patterns
            if knowledge_article_configuration is not None:
                self._values["knowledge_article_configuration"] = knowledge_article_configuration
            if standard_object_attachment_configuration is not None:
                self._values["standard_object_attachment_configuration"] = standard_object_attachment_configuration
            if standard_object_configurations is not None:
                self._values["standard_object_configurations"] = standard_object_configurations

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the key/value pairs required to connect to your Salesforce instance.

            The secret must contain a JSON structure with the following keys:

            - authenticationUrl - The OAUTH endpoint that Amazon Kendra connects to get an OAUTH token.
            - consumerKey - The application public key generated when you created your Salesforce application.
            - consumerSecret - The application private key generated when you created your Salesforce application.
            - password - The password associated with the user logging in to the Salesforce instance.
            - securityToken - The token associated with the user logging in to the Salesforce instance.
            - username - The user name of the user logging in to the Salesforce instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def server_url(self) -> builtins.str:
            '''The instance URL for the Salesforce site that you want to index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-serverurl
            '''
            result = self._values.get("server_url")
            assert result is not None, "Required property 'server_url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def chatter_feed_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.SalesforceChatterFeedConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for Salesforce chatter feeds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-chatterfeedconfiguration
            '''
            result = self._values.get("chatter_feed_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.SalesforceChatterFeedConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''Indicates whether Amazon Kendra should index attachments to Salesforce objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def exclude_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain documents in your Salesforce.

            Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The pattern is applied to the name of the attached file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-excludeattachmentfilepatterns
            '''
            result = self._values.get("exclude_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain documents in your Salesforce.

            Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The pattern is applied to the name of the attached file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-includeattachmentfilepatterns
            '''
            result = self._values.get("include_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def knowledge_article_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for the knowledge article types that Amazon Kendra indexes.

            Amazon Kendra indexes standard knowledge articles and the standard fields of knowledge articles, or the custom fields of custom knowledge articles, but not both.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-knowledgearticleconfiguration
            '''
            result = self._values.get("knowledge_article_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def standard_object_attachment_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for processing attachments to Salesforce standard objects.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-standardobjectattachmentconfiguration
            '''
            result = self._values.get("standard_object_attachment_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def standard_object_configurations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.SalesforceStandardObjectConfigurationProperty", _IResolvable_da3f097b]]]]:
            '''Configuration of the Salesforce standard objects that Amazon Kendra indexes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceconfiguration.html#cfn-kendra-datasource-salesforceconfiguration-standardobjectconfigurations
            '''
            result = self._values.get("standard_object_configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.SalesforceStandardObjectConfigurationProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "name": "name",
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
        },
    )
    class SalesforceCustomKnowledgeArticleTypeConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: builtins.str,
            name: builtins.str,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Provides the configuration information for indexing Salesforce custom articles.

            :param document_data_field_name: The name of the field in the custom knowledge article that contains the document data to index.
            :param name: The name of the configuration.
            :param document_title_field_name: The name of the field in the custom knowledge article that contains the document title.
            :param field_mappings: Maps attributes or field names of the custom knowledge article to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                salesforce_custom_knowledge_article_type_configuration_property = kendra.CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                    name="name",
                
                    # the properties below are optional
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e689bb017a19a170b0a1a7f34277387cff6153267437b9bd2f64824f0a8fd6a)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "document_data_field_name": document_data_field_name,
                "name": name,
            }
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings

        @builtins.property
        def document_data_field_name(self) -> builtins.str:
            '''The name of the field in the custom knowledge article that contains the document data to index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            assert result is not None, "Required property 'document_data_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the custom knowledge article that contains the document title.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of the custom knowledge article to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcecustomknowledgearticletypeconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceCustomKnowledgeArticleTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "included_states": "includedStates",
            "custom_knowledge_article_type_configurations": "customKnowledgeArticleTypeConfigurations",
            "standard_knowledge_article_type_configuration": "standardKnowledgeArticleTypeConfiguration",
        },
    )
    class SalesforceKnowledgeArticleConfigurationProperty:
        def __init__(
            self,
            *,
            included_states: typing.Sequence[builtins.str],
            custom_knowledge_article_type_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            standard_knowledge_article_type_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information for the knowledge article types that Amazon Kendra indexes.

            Amazon Kendra indexes standard knowledge articles and the standard fields of knowledge articles, or the custom fields of custom knowledge articles, but not both

            :param included_states: Specifies the document states that should be included when Amazon Kendra indexes knowledge articles. You must specify at least one state.
            :param custom_knowledge_article_type_configurations: Configuration information for custom Salesforce knowledge articles.
            :param standard_knowledge_article_type_configuration: Configuration information for standard Salesforce knowledge articles.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceknowledgearticleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                salesforce_knowledge_article_configuration_property = kendra.CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty(
                    included_states=["includedStates"],
                
                    # the properties below are optional
                    custom_knowledge_article_type_configurations=[kendra.CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                        name="name",
                
                        # the properties below are optional
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    )],
                    standard_knowledge_article_type_configuration=kendra.CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                
                        # the properties below are optional
                        document_title_field_name="documentTitleFieldName",
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54d2256d2f21288201eab3a954f64ece169e7a95f3fb70d3ee8ca96627a377f6)
                check_type(argname="argument included_states", value=included_states, expected_type=type_hints["included_states"])
                check_type(argname="argument custom_knowledge_article_type_configurations", value=custom_knowledge_article_type_configurations, expected_type=type_hints["custom_knowledge_article_type_configurations"])
                check_type(argname="argument standard_knowledge_article_type_configuration", value=standard_knowledge_article_type_configuration, expected_type=type_hints["standard_knowledge_article_type_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "included_states": included_states,
            }
            if custom_knowledge_article_type_configurations is not None:
                self._values["custom_knowledge_article_type_configurations"] = custom_knowledge_article_type_configurations
            if standard_knowledge_article_type_configuration is not None:
                self._values["standard_knowledge_article_type_configuration"] = standard_knowledge_article_type_configuration

        @builtins.property
        def included_states(self) -> typing.List[builtins.str]:
            '''Specifies the document states that should be included when Amazon Kendra indexes knowledge articles.

            You must specify at least one state.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceknowledgearticleconfiguration.html#cfn-kendra-datasource-salesforceknowledgearticleconfiguration-includedstates
            '''
            result = self._values.get("included_states")
            assert result is not None, "Required property 'included_states' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def custom_knowledge_article_type_configurations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty", _IResolvable_da3f097b]]]]:
            '''Configuration information for custom Salesforce knowledge articles.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceknowledgearticleconfiguration.html#cfn-kendra-datasource-salesforceknowledgearticleconfiguration-customknowledgearticletypeconfigurations
            '''
            result = self._values.get("custom_knowledge_article_type_configurations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def standard_knowledge_article_type_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for standard Salesforce knowledge articles.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforceknowledgearticleconfiguration.html#cfn-kendra-datasource-salesforceknowledgearticleconfiguration-standardknowledgearticletypeconfiguration
            '''
            result = self._values.get("standard_knowledge_article_type_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceKnowledgeArticleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
        },
    )
    class SalesforceStandardKnowledgeArticleTypeConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: builtins.str,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Provides the configuration information for standard Salesforce knowledge articles.

            :param document_data_field_name: The name of the field that contains the document data to index.
            :param document_title_field_name: The name of the field that contains the document title.
            :param field_mappings: Maps attributes or field names of the knowledge article to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                salesforce_standard_knowledge_article_type_configuration_property = kendra.CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                
                    # the properties below are optional
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__673113eebb1356ad8c49cba55bd0e063fede0e7da2dcadf3ade5650b7f4b2d0d)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "document_data_field_name": document_data_field_name,
            }
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings

        @builtins.property
        def document_data_field_name(self) -> builtins.str:
            '''The name of the field that contains the document data to index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            assert result is not None, "Required property 'document_data_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field that contains the document title.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of the knowledge article to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration.html#cfn-kendra-datasource-salesforcestandardknowledgearticletypeconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceStandardKnowledgeArticleTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
        },
    )
    class SalesforceStandardObjectAttachmentConfigurationProperty:
        def __init__(
            self,
            *,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Provides the configuration information for processing attachments to Salesforce standard objects.

            :param document_title_field_name: The name of the field used for the document title.
            :param field_mappings: One or more objects that map fields in attachments to Amazon Kendra index fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectattachmentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                salesforce_standard_object_attachment_configuration_property = kendra.CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty(
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7848e521c99f09cfcc736d593496d3342430c7a37a152f50ab8cb5d4a73b100)
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field used for the document title.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectattachmentconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectattachmentconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''One or more objects that map fields in attachments to Amazon Kendra index fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectattachmentconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectattachmentconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceStandardObjectAttachmentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SalesforceStandardObjectConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "name": "name",
            "document_title_field_name": "documentTitleFieldName",
            "field_mappings": "fieldMappings",
        },
    )
    class SalesforceStandardObjectConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: builtins.str,
            name: builtins.str,
            document_title_field_name: typing.Optional[builtins.str] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Specifies configuration information for indexing a single standard object.

            :param document_data_field_name: The name of the field in the standard object table that contains the document contents.
            :param name: The name of the standard object.
            :param document_title_field_name: The name of the field in the standard object table that contains the document title.
            :param field_mappings: Maps attributes or field names of the standard object to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                salesforce_standard_object_configuration_property = kendra.CfnDataSource.SalesforceStandardObjectConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                    name="name",
                
                    # the properties below are optional
                    document_title_field_name="documentTitleFieldName",
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__258f4f94facbd694e75c4e33c31082f6986db4b3015b0e86ec9210f0a2da544a)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "document_data_field_name": document_data_field_name,
                "name": name,
            }
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings

        @builtins.property
        def document_data_field_name(self) -> builtins.str:
            '''The name of the field in the standard object table that contains the document contents.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            assert result is not None, "Required property 'document_data_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the standard object.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the field in the standard object table that contains the document title.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of the standard object to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Salesforce fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Salesforce data source field names must exist in your Salesforce custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-salesforcestandardobjectconfiguration.html#cfn-kendra-datasource-salesforcestandardobjectconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SalesforceStandardObjectConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ServiceNowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "host_url": "hostUrl",
            "secret_arn": "secretArn",
            "service_now_build_version": "serviceNowBuildVersion",
            "authentication_type": "authenticationType",
            "knowledge_article_configuration": "knowledgeArticleConfiguration",
            "service_catalog_configuration": "serviceCatalogConfiguration",
        },
    )
    class ServiceNowConfigurationProperty:
        def __init__(
            self,
            *,
            host_url: builtins.str,
            secret_arn: builtins.str,
            service_now_build_version: builtins.str,
            authentication_type: typing.Optional[builtins.str] = None,
            knowledge_article_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            service_catalog_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ServiceNowServiceCatalogConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information to connect to ServiceNow as your data source.

            :param host_url: The ServiceNow instance that the data source connects to. The host endpoint should look like the following: *{instance}.service-now.com.*
            :param secret_arn: The Amazon Resource Name (ARN) of the AWS Secrets Manager secret that contains the user name and password required to connect to the ServiceNow instance. You can also provide OAuth authentication credentials of user name, password, client ID, and client secret. For more information, see `Using a ServiceNow data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-servicenow.html>`_ .
            :param service_now_build_version: The identifier of the release that the ServiceNow host is running. If the host is not running the ``LONDON`` release, use ``OTHERS`` .
            :param authentication_type: The type of authentication used to connect to the ServiceNow instance. If you choose ``HTTP_BASIC`` , Amazon Kendra is authenticated using the user name and password provided in the AWS Secrets Manager secret in the ``SecretArn`` field. If you choose ``OAUTH2`` , Amazon Kendra is authenticated using the credentials of client ID, client secret, user name and password. When you use ``OAUTH2`` authentication, you must generate a token and a client secret using the ServiceNow console. For more information, see `Using a ServiceNow data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-servicenow.html>`_ .
            :param knowledge_article_configuration: Configuration information for crawling knowledge articles in the ServiceNow site.
            :param service_catalog_configuration: Configuration information for crawling service catalogs in the ServiceNow site.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                service_now_configuration_property = kendra.CfnDataSource.ServiceNowConfigurationProperty(
                    host_url="hostUrl",
                    secret_arn="secretArn",
                    service_now_build_version="serviceNowBuildVersion",
                
                    # the properties below are optional
                    authentication_type="authenticationType",
                    knowledge_article_configuration=kendra.CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                
                        # the properties below are optional
                        crawl_attachments=False,
                        document_title_field_name="documentTitleFieldName",
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        filter_query="filterQuery",
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                    ),
                    service_catalog_configuration=kendra.CfnDataSource.ServiceNowServiceCatalogConfigurationProperty(
                        document_data_field_name="documentDataFieldName",
                
                        # the properties below are optional
                        crawl_attachments=False,
                        document_title_field_name="documentTitleFieldName",
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
                
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf6b2188dd486f22e5e5c83bbe485e54c8f2890629800d6adf78242466273d50)
                check_type(argname="argument host_url", value=host_url, expected_type=type_hints["host_url"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument service_now_build_version", value=service_now_build_version, expected_type=type_hints["service_now_build_version"])
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
                check_type(argname="argument knowledge_article_configuration", value=knowledge_article_configuration, expected_type=type_hints["knowledge_article_configuration"])
                check_type(argname="argument service_catalog_configuration", value=service_catalog_configuration, expected_type=type_hints["service_catalog_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "host_url": host_url,
                "secret_arn": secret_arn,
                "service_now_build_version": service_now_build_version,
            }
            if authentication_type is not None:
                self._values["authentication_type"] = authentication_type
            if knowledge_article_configuration is not None:
                self._values["knowledge_article_configuration"] = knowledge_article_configuration
            if service_catalog_configuration is not None:
                self._values["service_catalog_configuration"] = service_catalog_configuration

        @builtins.property
        def host_url(self) -> builtins.str:
            '''The ServiceNow instance that the data source connects to.

            The host endpoint should look like the following: *{instance}.service-now.com.*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-hosturl
            '''
            result = self._values.get("host_url")
            assert result is not None, "Required property 'host_url' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the AWS Secrets Manager secret that contains the user name and password required to connect to the ServiceNow instance.

            You can also provide OAuth authentication credentials of user name, password, client ID, and client secret. For more information, see `Using a ServiceNow data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-servicenow.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def service_now_build_version(self) -> builtins.str:
            '''The identifier of the release that the ServiceNow host is running.

            If the host is not running the ``LONDON`` release, use ``OTHERS`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-servicenowbuildversion
            '''
            result = self._values.get("service_now_build_version")
            assert result is not None, "Required property 'service_now_build_version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authentication_type(self) -> typing.Optional[builtins.str]:
            '''The type of authentication used to connect to the ServiceNow instance.

            If you choose ``HTTP_BASIC`` , Amazon Kendra is authenticated using the user name and password provided in the AWS Secrets Manager secret in the ``SecretArn`` field. If you choose ``OAUTH2`` , Amazon Kendra is authenticated using the credentials of client ID, client secret, user name and password.

            When you use ``OAUTH2`` authentication, you must generate a token and a client secret using the ServiceNow console. For more information, see `Using a ServiceNow data source <https://docs.aws.amazon.com/kendra/latest/dg/data-source-servicenow.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-authenticationtype
            '''
            result = self._values.get("authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def knowledge_article_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for crawling knowledge articles in the ServiceNow site.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-knowledgearticleconfiguration
            '''
            result = self._values.get("knowledge_article_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def service_catalog_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ServiceNowServiceCatalogConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information for crawling service catalogs in the ServiceNow site.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowconfiguration.html#cfn-kendra-datasource-servicenowconfiguration-servicecatalogconfiguration
            '''
            result = self._values.get("service_catalog_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ServiceNowServiceCatalogConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "crawl_attachments": "crawlAttachments",
            "document_title_field_name": "documentTitleFieldName",
            "exclude_attachment_file_patterns": "excludeAttachmentFilePatterns",
            "field_mappings": "fieldMappings",
            "filter_query": "filterQuery",
            "include_attachment_file_patterns": "includeAttachmentFilePatterns",
        },
    )
    class ServiceNowKnowledgeArticleConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: builtins.str,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            filter_query: typing.Optional[builtins.str] = None,
            include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information for crawling knowledge articles in the ServiceNow site.

            :param document_data_field_name: The name of the ServiceNow field that is mapped to the index document contents field in the Amazon Kendra index.
            :param crawl_attachments: ``TRUE`` to index attachments to knowledge articles.
            :param document_title_field_name: The name of the ServiceNow field that is mapped to the index document title field.
            :param exclude_attachment_file_patterns: A list of regular expression patterns to exclude certain attachments of knowledge articles in your ServiceNow. Item that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index. The regex is applied to the field specified in the ``PatternTargetField`` .
            :param field_mappings: Maps attributes or field names of knoweldge articles to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to ServiceNow fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The ServiceNow data source field names must exist in your ServiceNow custom metadata.
            :param filter_query: A query that selects the knowledge articles to index. The query can return articles from multiple knowledge bases, and the knowledge bases can be public or private. The query string must be one generated by the ServiceNow console. For more information, see `Specifying documents to index with a query <https://docs.aws.amazon.com/kendra/latest/dg/servicenow-query.html>`_ .
            :param include_attachment_file_patterns: A list of regular expression patterns to include certain attachments of knowledge articles in your ServiceNow. Item that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index. The regex is applied to the field specified in the ``PatternTargetField`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                service_now_knowledge_article_configuration_property = kendra.CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                
                    # the properties below are optional
                    crawl_attachments=False,
                    document_title_field_name="documentTitleFieldName",
                    exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    filter_query="filterQuery",
                    include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ced55b5dbc1895241f7179622dbcc184de664555043b2f78674509174c9bda1d)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument exclude_attachment_file_patterns", value=exclude_attachment_file_patterns, expected_type=type_hints["exclude_attachment_file_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument filter_query", value=filter_query, expected_type=type_hints["filter_query"])
                check_type(argname="argument include_attachment_file_patterns", value=include_attachment_file_patterns, expected_type=type_hints["include_attachment_file_patterns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "document_data_field_name": document_data_field_name,
            }
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if exclude_attachment_file_patterns is not None:
                self._values["exclude_attachment_file_patterns"] = exclude_attachment_file_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if filter_query is not None:
                self._values["filter_query"] = filter_query
            if include_attachment_file_patterns is not None:
                self._values["include_attachment_file_patterns"] = include_attachment_file_patterns

        @builtins.property
        def document_data_field_name(self) -> builtins.str:
            '''The name of the ServiceNow field that is mapped to the index document contents field in the Amazon Kendra index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            assert result is not None, "Required property 'document_data_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to index attachments to knowledge articles.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the ServiceNow field that is mapped to the index document title field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain attachments of knowledge articles in your ServiceNow.

            Item that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            The regex is applied to the field specified in the ``PatternTargetField`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-excludeattachmentfilepatterns
            '''
            result = self._values.get("exclude_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of knoweldge articles to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to ServiceNow fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The ServiceNow data source field names must exist in your ServiceNow custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def filter_query(self) -> typing.Optional[builtins.str]:
            '''A query that selects the knowledge articles to index.

            The query can return articles from multiple knowledge bases, and the knowledge bases can be public or private.

            The query string must be one generated by the ServiceNow console. For more information, see `Specifying documents to index with a query <https://docs.aws.amazon.com/kendra/latest/dg/servicenow-query.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-filterquery
            '''
            result = self._values.get("filter_query")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def include_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain attachments of knowledge articles in your ServiceNow.

            Item that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            The regex is applied to the field specified in the ``PatternTargetField`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowknowledgearticleconfiguration.html#cfn-kendra-datasource-servicenowknowledgearticleconfiguration-includeattachmentfilepatterns
            '''
            result = self._values.get("include_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowKnowledgeArticleConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.ServiceNowServiceCatalogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "document_data_field_name": "documentDataFieldName",
            "crawl_attachments": "crawlAttachments",
            "document_title_field_name": "documentTitleFieldName",
            "exclude_attachment_file_patterns": "excludeAttachmentFilePatterns",
            "field_mappings": "fieldMappings",
            "include_attachment_file_patterns": "includeAttachmentFilePatterns",
        },
    )
    class ServiceNowServiceCatalogConfigurationProperty:
        def __init__(
            self,
            *,
            document_data_field_name: builtins.str,
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information for crawling service catalog items in the ServiceNow site.

            :param document_data_field_name: The name of the ServiceNow field that is mapped to the index document contents field in the Amazon Kendra index.
            :param crawl_attachments: ``TRUE`` to index attachments to service catalog items.
            :param document_title_field_name: The name of the ServiceNow field that is mapped to the index document title field.
            :param exclude_attachment_file_patterns: A list of regular expression patterns to exclude certain attachments of catalogs in your ServiceNow. Item that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index. The regex is applied to the file name of the attachment.
            :param field_mappings: Maps attributes or field names of catalogs to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to ServiceNow fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The ServiceNow data source field names must exist in your ServiceNow custom metadata.
            :param include_attachment_file_patterns: A list of regular expression patterns to include certain attachments of catalogs in your ServiceNow. Item that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index. The regex is applied to the file name of the attachment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                service_now_service_catalog_configuration_property = kendra.CfnDataSource.ServiceNowServiceCatalogConfigurationProperty(
                    document_data_field_name="documentDataFieldName",
                
                    # the properties below are optional
                    crawl_attachments=False,
                    document_title_field_name="documentTitleFieldName",
                    exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73feebbd1e46487ffa1b46b0644d23b18756aaeeb319992b0f2f62ba081b975d)
                check_type(argname="argument document_data_field_name", value=document_data_field_name, expected_type=type_hints["document_data_field_name"])
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument exclude_attachment_file_patterns", value=exclude_attachment_file_patterns, expected_type=type_hints["exclude_attachment_file_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument include_attachment_file_patterns", value=include_attachment_file_patterns, expected_type=type_hints["include_attachment_file_patterns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "document_data_field_name": document_data_field_name,
            }
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if exclude_attachment_file_patterns is not None:
                self._values["exclude_attachment_file_patterns"] = exclude_attachment_file_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if include_attachment_file_patterns is not None:
                self._values["include_attachment_file_patterns"] = include_attachment_file_patterns

        @builtins.property
        def document_data_field_name(self) -> builtins.str:
            '''The name of the ServiceNow field that is mapped to the index document contents field in the Amazon Kendra index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-documentdatafieldname
            '''
            result = self._values.get("document_data_field_name")
            assert result is not None, "Required property 'document_data_field_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to index attachments to service catalog items.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The name of the ServiceNow field that is mapped to the index document title field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclude_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain attachments of catalogs in your ServiceNow.

            Item that match the patterns are excluded from the index. Items that don't match the patterns are included in the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            The regex is applied to the file name of the attachment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-excludeattachmentfilepatterns
            '''
            result = self._values.get("exclude_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''Maps attributes or field names of catalogs to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to ServiceNow fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The ServiceNow data source field names must exist in your ServiceNow custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def include_attachment_file_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain attachments of catalogs in your ServiceNow.

            Item that match the patterns are included in the index. Items that don't match the patterns are excluded from the index. If an item matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the item isn't included in the index.

            The regex is applied to the file name of the attachment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-servicenowservicecatalogconfiguration.html#cfn-kendra-datasource-servicenowservicecatalogconfiguration-includeattachmentfilepatterns
            '''
            result = self._values.get("include_attachment_file_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServiceNowServiceCatalogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SharePointConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secret_arn": "secretArn",
            "share_point_version": "sharePointVersion",
            "urls": "urls",
            "crawl_attachments": "crawlAttachments",
            "disable_local_groups": "disableLocalGroups",
            "document_title_field_name": "documentTitleFieldName",
            "exclusion_patterns": "exclusionPatterns",
            "field_mappings": "fieldMappings",
            "inclusion_patterns": "inclusionPatterns",
            "ssl_certificate_s3_path": "sslCertificateS3Path",
            "use_change_log": "useChangeLog",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class SharePointConfigurationProperty:
        def __init__(
            self,
            *,
            secret_arn: builtins.str,
            share_point_version: builtins.str,
            urls: typing.Sequence[builtins.str],
            crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            disable_local_groups: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            document_title_field_name: typing.Optional[builtins.str] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            ssl_certificate_s3_path: typing.Optional[typing.Union[typing.Union["CfnDataSource.S3PathProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            use_change_log: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            vpc_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information to connect to Microsoft SharePoint as your data source.

            :param secret_arn: The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password required to connect to the SharePoint instance. For more information, see `Microsoft SharePoint <https://docs.aws.amazon.com/kendra/latest/dg/data-source-sharepoint.html>`_ .
            :param share_point_version: The version of Microsoft SharePoint that you use.
            :param urls: The Microsoft SharePoint site URLs for the documents you want to index.
            :param crawl_attachments: ``TRUE`` to index document attachments.
            :param disable_local_groups: ``TRUE`` to disable local groups information.
            :param document_title_field_name: The Microsoft SharePoint attribute field that contains the title of the document.
            :param exclusion_patterns: A list of regular expression patterns. Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an exclusion pattern and an inclusion pattern, the document is not included in the index. The regex is applied to the display URL of the SharePoint document.
            :param field_mappings: A list of ``DataSourceToIndexFieldMapping`` objects that map Microsoft SharePoint attributes or fields to Amazon Kendra index fields. You must first create the index fields using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation before you map SharePoint attributes. For more information, see `Mapping Data Source Fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ .
            :param inclusion_patterns: A list of regular expression patterns to include certain documents in your SharePoint. Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index. The regex applies to the display URL of the SharePoint document.
            :param ssl_certificate_s3_path: Information required to find a specific file in an Amazon S3 bucket.
            :param use_change_log: ``TRUE`` to use the SharePoint change log to determine which documents require updating in the index. Depending on the change log's size, it may take longer for Amazon Kendra to use the change log than to scan all of your documents in SharePoint.
            :param vpc_configuration: Provides information for connecting to an Amazon VPC.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                share_point_configuration_property = kendra.CfnDataSource.SharePointConfigurationProperty(
                    secret_arn="secretArn",
                    share_point_version="sharePointVersion",
                    urls=["urls"],
                
                    # the properties below are optional
                    crawl_attachments=False,
                    disable_local_groups=False,
                    document_title_field_name="documentTitleFieldName",
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    ssl_certificate_s3_path=kendra.CfnDataSource.S3PathProperty(
                        bucket="bucket",
                        key="key"
                    ),
                    use_change_log=False,
                    vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f90fb1a0d84aaf9de16cb7f8f2186dfcef612e5416777877db5790d0e7925997)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument share_point_version", value=share_point_version, expected_type=type_hints["share_point_version"])
                check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
                check_type(argname="argument crawl_attachments", value=crawl_attachments, expected_type=type_hints["crawl_attachments"])
                check_type(argname="argument disable_local_groups", value=disable_local_groups, expected_type=type_hints["disable_local_groups"])
                check_type(argname="argument document_title_field_name", value=document_title_field_name, expected_type=type_hints["document_title_field_name"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument ssl_certificate_s3_path", value=ssl_certificate_s3_path, expected_type=type_hints["ssl_certificate_s3_path"])
                check_type(argname="argument use_change_log", value=use_change_log, expected_type=type_hints["use_change_log"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secret_arn": secret_arn,
                "share_point_version": share_point_version,
                "urls": urls,
            }
            if crawl_attachments is not None:
                self._values["crawl_attachments"] = crawl_attachments
            if disable_local_groups is not None:
                self._values["disable_local_groups"] = disable_local_groups
            if document_title_field_name is not None:
                self._values["document_title_field_name"] = document_title_field_name
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if ssl_certificate_s3_path is not None:
                self._values["ssl_certificate_s3_path"] = ssl_certificate_s3_path
            if use_change_log is not None:
                self._values["use_change_log"] = use_change_log
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of an AWS Secrets Manager secret that contains the user name and password required to connect to the SharePoint instance.

            For more information, see `Microsoft SharePoint <https://docs.aws.amazon.com/kendra/latest/dg/data-source-sharepoint.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-secretarn
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def share_point_version(self) -> builtins.str:
            '''The version of Microsoft SharePoint that you use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-sharepointversion
            '''
            result = self._values.get("share_point_version")
            assert result is not None, "Required property 'share_point_version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def urls(self) -> typing.List[builtins.str]:
            '''The Microsoft SharePoint site URLs for the documents you want to index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-urls
            '''
            result = self._values.get("urls")
            assert result is not None, "Required property 'urls' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def crawl_attachments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to index document attachments.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-crawlattachments
            '''
            result = self._values.get("crawl_attachments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def disable_local_groups(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to disable local groups information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-disablelocalgroups
            '''
            result = self._values.get("disable_local_groups")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def document_title_field_name(self) -> typing.Optional[builtins.str]:
            '''The Microsoft SharePoint attribute field that contains the title of the document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-documenttitlefieldname
            '''
            result = self._values.get("document_title_field_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns.

            Documents that match the patterns are excluded from the index. Documents that don't match the patterns are included in the index. If a document matches both an exclusion pattern and an inclusion pattern, the document is not included in the index.

            The regex is applied to the display URL of the SharePoint document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''A list of ``DataSourceToIndexFieldMapping`` objects that map Microsoft SharePoint attributes or fields to Amazon Kendra index fields.

            You must first create the index fields using the `UpdateIndex <https://docs.aws.amazon.com/kendra/latest/dg/API_UpdateIndex.html>`_ operation before you map SharePoint attributes. For more information, see `Mapping Data Source Fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain documents in your SharePoint.

            Documents that match the patterns are included in the index. Documents that don't match the patterns are excluded from the index. If a document matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the document isn't included in the index.

            The regex applies to the display URL of the SharePoint document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def ssl_certificate_s3_path(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.S3PathProperty", _IResolvable_da3f097b]]:
            '''Information required to find a specific file in an Amazon S3 bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-sslcertificates3path
            '''
            result = self._values.get("ssl_certificate_s3_path")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.S3PathProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def use_change_log(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to use the SharePoint change log to determine which documents require updating in the index.

            Depending on the change log's size, it may take longer for Amazon Kendra to use the change log than to scan all of your documents in SharePoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-usechangelog
            '''
            result = self._values.get("use_change_log")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", _IResolvable_da3f097b]]:
            '''Provides information for connecting to an Amazon VPC.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sharepointconfiguration.html#cfn-kendra-datasource-sharepointconfiguration-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.DataSourceVpcConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SharePointConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.SqlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_identifiers_enclosing_option": "queryIdentifiersEnclosingOption",
        },
    )
    class SqlConfigurationProperty:
        def __init__(
            self,
            *,
            query_identifiers_enclosing_option: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information that configures Amazon Kendra to use a SQL database.

            :param query_identifiers_enclosing_option: Determines whether Amazon Kendra encloses SQL identifiers for tables and column names in double quotes (") when making a database query. You can set the value to ``DOUBLE_QUOTES`` or ``NONE`` . By default, Amazon Kendra passes SQL identifiers the way that they are entered into the data source configuration. It does not change the case of identifiers or enclose them in quotes. PostgreSQL internally converts uppercase characters to lower case characters in identifiers unless they are quoted. Choosing this option encloses identifiers in quotes so that PostgreSQL does not convert the character's case. For MySQL databases, you must enable the ansi_quotes option when you set this field to ``DOUBLE_QUOTES`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sqlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                sql_configuration_property = kendra.CfnDataSource.SqlConfigurationProperty(
                    query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9058d8c99c505df3ace590b735e22ffca36be7920e96abbe2049836b6e0a93f1)
                check_type(argname="argument query_identifiers_enclosing_option", value=query_identifiers_enclosing_option, expected_type=type_hints["query_identifiers_enclosing_option"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if query_identifiers_enclosing_option is not None:
                self._values["query_identifiers_enclosing_option"] = query_identifiers_enclosing_option

        @builtins.property
        def query_identifiers_enclosing_option(self) -> typing.Optional[builtins.str]:
            '''Determines whether Amazon Kendra encloses SQL identifiers for tables and column names in double quotes (") when making a database query.

            You can set the value to ``DOUBLE_QUOTES`` or ``NONE`` .

            By default, Amazon Kendra passes SQL identifiers the way that they are entered into the data source configuration. It does not change the case of identifiers or enclose them in quotes.

            PostgreSQL internally converts uppercase characters to lower case characters in identifiers unless they are quoted. Choosing this option encloses identifiers in quotes so that PostgreSQL does not convert the character's case.

            For MySQL databases, you must enable the ansi_quotes option when you set this field to ``DOUBLE_QUOTES`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-sqlconfiguration.html#cfn-kendra-datasource-sqlconfiguration-queryidentifiersenclosingoption
            '''
            result = self._values.get("query_identifiers_enclosing_option")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.WebCrawlerAuthenticationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"basic_authentication": "basicAuthentication"},
    )
    class WebCrawlerAuthenticationConfigurationProperty:
        def __init__(
            self,
            *,
            basic_authentication: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.WebCrawlerBasicAuthenticationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Provides the configuration information to connect to websites that require user authentication.

            :param basic_authentication: The list of configuration information that's required to connect to and crawl a website host using basic authentication credentials. The list includes the name and port number of the website host.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerauthenticationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                web_crawler_authentication_configuration_property = kendra.CfnDataSource.WebCrawlerAuthenticationConfigurationProperty(
                    basic_authentication=[kendra.CfnDataSource.WebCrawlerBasicAuthenticationProperty(
                        credentials="credentials",
                        host="host",
                        port=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78dcdcac178c8a64cb2a657a51649bac6d70ac8b2c0e4bc1b93bd0d4daabf383)
                check_type(argname="argument basic_authentication", value=basic_authentication, expected_type=type_hints["basic_authentication"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if basic_authentication is not None:
                self._values["basic_authentication"] = basic_authentication

        @builtins.property
        def basic_authentication(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.WebCrawlerBasicAuthenticationProperty", _IResolvable_da3f097b]]]]:
            '''The list of configuration information that's required to connect to and crawl a website host using basic authentication credentials.

            The list includes the name and port number of the website host.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerauthenticationconfiguration.html#cfn-kendra-datasource-webcrawlerauthenticationconfiguration-basicauthentication
            '''
            result = self._values.get("basic_authentication")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.WebCrawlerBasicAuthenticationProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerAuthenticationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.WebCrawlerBasicAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={"credentials": "credentials", "host": "host", "port": "port"},
    )
    class WebCrawlerBasicAuthenticationProperty:
        def __init__(
            self,
            *,
            credentials: builtins.str,
            host: builtins.str,
            port: jsii.Number,
        ) -> None:
            '''Provides the configuration information to connect to websites that require basic user authentication.

            :param credentials: Your secret ARN, which you can create in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_. You use a secret if basic authentication credentials are required to connect to a website. The secret stores your credentials of user name and password.
            :param host: The name of the website host you want to connect to using authentication credentials. For example, the host name of https://a.example.com/page1.html is "a.example.com".
            :param port: The port number of the website host you want to connect to using authentication credentials. For example, the port for https://a.example.com/page1.html is 443, the standard port for HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerbasicauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                web_crawler_basic_authentication_property = kendra.CfnDataSource.WebCrawlerBasicAuthenticationProperty(
                    credentials="credentials",
                    host="host",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ff4b862a7ea02f0fb1b4bcbb9f7770d415fb18ebebd2dfa6134f78f04cad9a8)
                check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "credentials": credentials,
                "host": host,
                "port": port,
            }

        @builtins.property
        def credentials(self) -> builtins.str:
            '''Your secret ARN, which you can create in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_.

            You use a secret if basic authentication credentials are required to connect to a website. The secret stores your credentials of user name and password.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerbasicauthentication.html#cfn-kendra-datasource-webcrawlerbasicauthentication-credentials
            '''
            result = self._values.get("credentials")
            assert result is not None, "Required property 'credentials' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def host(self) -> builtins.str:
            '''The name of the website host you want to connect to using authentication credentials.

            For example, the host name of https://a.example.com/page1.html is "a.example.com".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerbasicauthentication.html#cfn-kendra-datasource-webcrawlerbasicauthentication-host
            '''
            result = self._values.get("host")
            assert result is not None, "Required property 'host' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def port(self) -> jsii.Number:
            '''The port number of the website host you want to connect to using authentication credentials.

            For example, the port for https://a.example.com/page1.html is 443, the standard port for HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerbasicauthentication.html#cfn-kendra-datasource-webcrawlerbasicauthentication-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerBasicAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.WebCrawlerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "urls": "urls",
            "authentication_configuration": "authenticationConfiguration",
            "crawl_depth": "crawlDepth",
            "max_content_size_per_page_in_mega_bytes": "maxContentSizePerPageInMegaBytes",
            "max_links_per_page": "maxLinksPerPage",
            "max_urls_per_minute_crawl_rate": "maxUrlsPerMinuteCrawlRate",
            "proxy_configuration": "proxyConfiguration",
            "url_exclusion_patterns": "urlExclusionPatterns",
            "url_inclusion_patterns": "urlInclusionPatterns",
        },
    )
    class WebCrawlerConfigurationProperty:
        def __init__(
            self,
            *,
            urls: typing.Union[typing.Union["CfnDataSource.WebCrawlerUrlsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
            authentication_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.WebCrawlerAuthenticationConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            crawl_depth: typing.Optional[jsii.Number] = None,
            max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
            max_links_per_page: typing.Optional[jsii.Number] = None,
            max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
            proxy_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.ProxyConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Provides the configuration information required for Amazon Kendra Web Crawler.

            :param urls: Specifies the seed or starting point URLs of the websites or the sitemap URLs of the websites you want to crawl. You can include website subdomains. You can list up to 100 seed URLs and up to three sitemap URLs. You can only crawl websites that use the secure communication protocol, Hypertext Transfer Protocol Secure (HTTPS). If you receive an error when crawling a website, it could be that the website is blocked from crawling. *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use Amazon Kendra Web Crawler to index your own webpages, or webpages that you have authorization to index.*
            :param authentication_configuration: Configuration information required to connect to websites using authentication. You can connect to websites using basic authentication of user name and password. You use a secret in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ to store your authentication credentials. You must provide the website host name and port number. For example, the host name of https://a.example.com/page1.html is "a.example.com" and the port is 443, the standard port for HTTPS.
            :param crawl_depth: Specifies the number of levels in a website that you want to crawl. The first level begins from the website seed or starting point URL. For example, if a website has 3 levels – index level (i.e. seed in this example), sections level, and subsections level – and you are only interested in crawling information up to the sections level (i.e. levels 0-1), you can set your depth to 1. The default crawl depth is set to 2.
            :param max_content_size_per_page_in_mega_bytes: The maximum size (in MB) of a webpage or attachment to crawl. Files larger than this size (in MB) are skipped/not crawled. The default maximum size of a webpage or attachment is set to 50 MB.
            :param max_links_per_page: The maximum number of URLs on a webpage to include when crawling a website. This number is per webpage. As a website’s webpages are crawled, any URLs the webpages link to are also crawled. URLs on a webpage are crawled in order of appearance. The default maximum links per page is 100.
            :param max_urls_per_minute_crawl_rate: The maximum number of URLs crawled per website host per minute. A minimum of one URL is required. The default maximum number of URLs crawled per website host per minute is 300.
            :param proxy_configuration: Configuration information required to connect to your internal websites via a web proxy. You must provide the website host name and port number. For example, the host name of https://a.example.com/page1.html is "a.example.com" and the port is 443, the standard port for HTTPS. Web proxy credentials are optional and you can use them to connect to a web proxy server that requires basic authentication. To store web proxy credentials, you use a secret in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ .
            :param url_exclusion_patterns: A list of regular expression patterns to exclude certain URLs to crawl. URLs that match the patterns are excluded from the index. URLs that don't match the patterns are included in the index. If a URL matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the URL file isn't included in the index.
            :param url_inclusion_patterns: A list of regular expression patterns to include certain URLs to crawl. URLs that match the patterns are included in the index. URLs that don't match the patterns are excluded from the index. If a URL matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the URL file isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                web_crawler_configuration_property = kendra.CfnDataSource.WebCrawlerConfigurationProperty(
                    urls=kendra.CfnDataSource.WebCrawlerUrlsProperty(
                        seed_url_configuration=kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                            seed_urls=["seedUrls"],
                
                            # the properties below are optional
                            web_crawler_mode="webCrawlerMode"
                        ),
                        site_maps_configuration=kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                            site_maps=["siteMaps"]
                        )
                    ),
                
                    # the properties below are optional
                    authentication_configuration=kendra.CfnDataSource.WebCrawlerAuthenticationConfigurationProperty(
                        basic_authentication=[kendra.CfnDataSource.WebCrawlerBasicAuthenticationProperty(
                            credentials="credentials",
                            host="host",
                            port=123
                        )]
                    ),
                    crawl_depth=123,
                    max_content_size_per_page_in_mega_bytes=123,
                    max_links_per_page=123,
                    max_urls_per_minute_crawl_rate=123,
                    proxy_configuration=kendra.CfnDataSource.ProxyConfigurationProperty(
                        host="host",
                        port=123,
                
                        # the properties below are optional
                        credentials="credentials"
                    ),
                    url_exclusion_patterns=["urlExclusionPatterns"],
                    url_inclusion_patterns=["urlInclusionPatterns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9c76bcf4dccdbef664e3afaa154bc20afb0b322dd0a2e57fd1d5a36d14747ac)
                check_type(argname="argument urls", value=urls, expected_type=type_hints["urls"])
                check_type(argname="argument authentication_configuration", value=authentication_configuration, expected_type=type_hints["authentication_configuration"])
                check_type(argname="argument crawl_depth", value=crawl_depth, expected_type=type_hints["crawl_depth"])
                check_type(argname="argument max_content_size_per_page_in_mega_bytes", value=max_content_size_per_page_in_mega_bytes, expected_type=type_hints["max_content_size_per_page_in_mega_bytes"])
                check_type(argname="argument max_links_per_page", value=max_links_per_page, expected_type=type_hints["max_links_per_page"])
                check_type(argname="argument max_urls_per_minute_crawl_rate", value=max_urls_per_minute_crawl_rate, expected_type=type_hints["max_urls_per_minute_crawl_rate"])
                check_type(argname="argument proxy_configuration", value=proxy_configuration, expected_type=type_hints["proxy_configuration"])
                check_type(argname="argument url_exclusion_patterns", value=url_exclusion_patterns, expected_type=type_hints["url_exclusion_patterns"])
                check_type(argname="argument url_inclusion_patterns", value=url_inclusion_patterns, expected_type=type_hints["url_inclusion_patterns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "urls": urls,
            }
            if authentication_configuration is not None:
                self._values["authentication_configuration"] = authentication_configuration
            if crawl_depth is not None:
                self._values["crawl_depth"] = crawl_depth
            if max_content_size_per_page_in_mega_bytes is not None:
                self._values["max_content_size_per_page_in_mega_bytes"] = max_content_size_per_page_in_mega_bytes
            if max_links_per_page is not None:
                self._values["max_links_per_page"] = max_links_per_page
            if max_urls_per_minute_crawl_rate is not None:
                self._values["max_urls_per_minute_crawl_rate"] = max_urls_per_minute_crawl_rate
            if proxy_configuration is not None:
                self._values["proxy_configuration"] = proxy_configuration
            if url_exclusion_patterns is not None:
                self._values["url_exclusion_patterns"] = url_exclusion_patterns
            if url_inclusion_patterns is not None:
                self._values["url_inclusion_patterns"] = url_inclusion_patterns

        @builtins.property
        def urls(
            self,
        ) -> typing.Union["CfnDataSource.WebCrawlerUrlsProperty", _IResolvable_da3f097b]:
            '''Specifies the seed or starting point URLs of the websites or the sitemap URLs of the websites you want to crawl.

            You can include website subdomains. You can list up to 100 seed URLs and up to three sitemap URLs.

            You can only crawl websites that use the secure communication protocol, Hypertext Transfer Protocol Secure (HTTPS). If you receive an error when crawling a website, it could be that the website is blocked from crawling.

            *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use Amazon Kendra Web Crawler to index your own webpages, or webpages that you have authorization to index.*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-urls
            '''
            result = self._values.get("urls")
            assert result is not None, "Required property 'urls' is missing"
            return typing.cast(typing.Union["CfnDataSource.WebCrawlerUrlsProperty", _IResolvable_da3f097b], result)

        @builtins.property
        def authentication_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.WebCrawlerAuthenticationConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information required to connect to websites using authentication.

            You can connect to websites using basic authentication of user name and password. You use a secret in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ to store your authentication credentials.

            You must provide the website host name and port number. For example, the host name of https://a.example.com/page1.html is "a.example.com" and the port is 443, the standard port for HTTPS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-authenticationconfiguration
            '''
            result = self._values.get("authentication_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.WebCrawlerAuthenticationConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def crawl_depth(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of levels in a website that you want to crawl.

            The first level begins from the website seed or starting point URL. For example, if a website has 3 levels – index level (i.e. seed in this example), sections level, and subsections level – and you are only interested in crawling information up to the sections level (i.e. levels 0-1), you can set your depth to 1.

            The default crawl depth is set to 2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-crawldepth
            '''
            result = self._values.get("crawl_depth")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_content_size_per_page_in_mega_bytes(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''The maximum size (in MB) of a webpage or attachment to crawl.

            Files larger than this size (in MB) are skipped/not crawled.

            The default maximum size of a webpage or attachment is set to 50 MB.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-maxcontentsizeperpageinmegabytes
            '''
            result = self._values.get("max_content_size_per_page_in_mega_bytes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_links_per_page(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of URLs on a webpage to include when crawling a website. This number is per webpage.

            As a website’s webpages are crawled, any URLs the webpages link to are also crawled. URLs on a webpage are crawled in order of appearance.

            The default maximum links per page is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-maxlinksperpage
            '''
            result = self._values.get("max_links_per_page")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_urls_per_minute_crawl_rate(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of URLs crawled per website host per minute.

            A minimum of one URL is required.

            The default maximum number of URLs crawled per website host per minute is 300.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-maxurlsperminutecrawlrate
            '''
            result = self._values.get("max_urls_per_minute_crawl_rate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def proxy_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.ProxyConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration information required to connect to your internal websites via a web proxy.

            You must provide the website host name and port number. For example, the host name of https://a.example.com/page1.html is "a.example.com" and the port is 443, the standard port for HTTPS.

            Web proxy credentials are optional and you can use them to connect to a web proxy server that requires basic authentication. To store web proxy credentials, you use a secret in `AWS Secrets Manager <https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-proxyconfiguration
            '''
            result = self._values.get("proxy_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.ProxyConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def url_exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain URLs to crawl.

            URLs that match the patterns are excluded from the index. URLs that don't match the patterns are included in the index. If a URL matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the URL file isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-urlexclusionpatterns
            '''
            result = self._values.get("url_exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def url_inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain URLs to crawl.

            URLs that match the patterns are included in the index. URLs that don't match the patterns are excluded from the index. If a URL matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the URL file isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerconfiguration.html#cfn-kendra-datasource-webcrawlerconfiguration-urlinclusionpatterns
            '''
            result = self._values.get("url_inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"seed_urls": "seedUrls", "web_crawler_mode": "webCrawlerMode"},
    )
    class WebCrawlerSeedUrlConfigurationProperty:
        def __init__(
            self,
            *,
            seed_urls: typing.Sequence[builtins.str],
            web_crawler_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information of the seed or starting point URLs to crawl.

            *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use the Amazon Kendra web crawler to index your own webpages, or webpages that you have authorization to index.*

            :param seed_urls: The list of seed or starting point URLs of the websites you want to crawl. The list can include a maximum of 100 seed URLs.
            :param web_crawler_mode: You can choose one of the following modes:. - ``HOST_ONLY`` – crawl only the website host names. For example, if the seed URL is "abc.example.com", then only URLs with host name "abc.example.com" are crawled. - ``SUBDOMAINS`` – crawl the website host names with subdomains. For example, if the seed URL is "abc.example.com", then "a.abc.example.com" and "b.abc.example.com" are also crawled. - ``EVERYTHING`` – crawl the website host names with subdomains and other domains that the webpages link to. The default mode is set to ``HOST_ONLY`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerseedurlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                web_crawler_seed_url_configuration_property = kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                    seed_urls=["seedUrls"],
                
                    # the properties below are optional
                    web_crawler_mode="webCrawlerMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ba5c0e84e98f69ec08d299dd403c87e60f8a2ec725d88ba034022f6dddd20c0)
                check_type(argname="argument seed_urls", value=seed_urls, expected_type=type_hints["seed_urls"])
                check_type(argname="argument web_crawler_mode", value=web_crawler_mode, expected_type=type_hints["web_crawler_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "seed_urls": seed_urls,
            }
            if web_crawler_mode is not None:
                self._values["web_crawler_mode"] = web_crawler_mode

        @builtins.property
        def seed_urls(self) -> typing.List[builtins.str]:
            '''The list of seed or starting point URLs of the websites you want to crawl.

            The list can include a maximum of 100 seed URLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerseedurlconfiguration.html#cfn-kendra-datasource-webcrawlerseedurlconfiguration-seedurls
            '''
            result = self._values.get("seed_urls")
            assert result is not None, "Required property 'seed_urls' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def web_crawler_mode(self) -> typing.Optional[builtins.str]:
            '''You can choose one of the following modes:.

            - ``HOST_ONLY`` – crawl only the website host names. For example, if the seed URL is "abc.example.com", then only URLs with host name "abc.example.com" are crawled.
            - ``SUBDOMAINS`` – crawl the website host names with subdomains. For example, if the seed URL is "abc.example.com", then "a.abc.example.com" and "b.abc.example.com" are also crawled.
            - ``EVERYTHING`` – crawl the website host names with subdomains and other domains that the webpages link to.

            The default mode is set to ``HOST_ONLY`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerseedurlconfiguration.html#cfn-kendra-datasource-webcrawlerseedurlconfiguration-webcrawlermode
            '''
            result = self._values.get("web_crawler_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerSeedUrlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"site_maps": "siteMaps"},
    )
    class WebCrawlerSiteMapsConfigurationProperty:
        def __init__(self, *, site_maps: typing.Sequence[builtins.str]) -> None:
            '''Provides the configuration information of the sitemap URLs to crawl.

            *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use the Amazon Kendra web crawler to index your own webpages, or webpages that you have authorization to index.*

            :param site_maps: The list of sitemap URLs of the websites you want to crawl. The list can include a maximum of three sitemap URLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlersitemapsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                web_crawler_site_maps_configuration_property = kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                    site_maps=["siteMaps"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f9026e7358b434f219fc3e9bf3da50ec0a37eb8f00e193fa38cf66badfbde60)
                check_type(argname="argument site_maps", value=site_maps, expected_type=type_hints["site_maps"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "site_maps": site_maps,
            }

        @builtins.property
        def site_maps(self) -> typing.List[builtins.str]:
            '''The list of sitemap URLs of the websites you want to crawl.

            The list can include a maximum of three sitemap URLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlersitemapsconfiguration.html#cfn-kendra-datasource-webcrawlersitemapsconfiguration-sitemaps
            '''
            result = self._values.get("site_maps")
            assert result is not None, "Required property 'site_maps' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerSiteMapsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.WebCrawlerUrlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "seed_url_configuration": "seedUrlConfiguration",
            "site_maps_configuration": "siteMapsConfiguration",
        },
    )
    class WebCrawlerUrlsProperty:
        def __init__(
            self,
            *,
            seed_url_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.WebCrawlerSeedUrlConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            site_maps_configuration: typing.Optional[typing.Union[typing.Union["CfnDataSource.WebCrawlerSiteMapsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Specifies the seed or starting point URLs of the websites or the sitemap URLs of the websites you want to crawl.

            You can include website subdomains. You can list up to 100 seed URLs and up to three sitemap URLs.

            You can only crawl websites that use the secure communication protocol, Hypertext Transfer Protocol Secure (HTTPS). If you receive an error when crawling a website, it could be that the website is blocked from crawling.

            *When selecting websites to index, you must adhere to the `Amazon Acceptable Use Policy <https://docs.aws.amazon.com/aup/>`_ and all other Amazon terms. Remember that you must only use the Amazon Kendra web crawler to index your own webpages, or webpages that you have authorization to index.*

            :param seed_url_configuration: Configuration of the seed or starting point URLs of the websites you want to crawl. You can choose to crawl only the website host names, or the website host names with subdomains, or the website host names with subdomains and other domains that the webpages link to. You can list up to 100 seed URLs.
            :param site_maps_configuration: Configuration of the sitemap URLs of the websites you want to crawl. Only URLs belonging to the same website host names are crawled. You can list up to three sitemap URLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerurls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                web_crawler_urls_property = kendra.CfnDataSource.WebCrawlerUrlsProperty(
                    seed_url_configuration=kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                        seed_urls=["seedUrls"],
                
                        # the properties below are optional
                        web_crawler_mode="webCrawlerMode"
                    ),
                    site_maps_configuration=kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                        site_maps=["siteMaps"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c90a23eeef0a23af52df460253f647effa981018e94e02c7b7f710d72f9d3ee)
                check_type(argname="argument seed_url_configuration", value=seed_url_configuration, expected_type=type_hints["seed_url_configuration"])
                check_type(argname="argument site_maps_configuration", value=site_maps_configuration, expected_type=type_hints["site_maps_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if seed_url_configuration is not None:
                self._values["seed_url_configuration"] = seed_url_configuration
            if site_maps_configuration is not None:
                self._values["site_maps_configuration"] = site_maps_configuration

        @builtins.property
        def seed_url_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.WebCrawlerSeedUrlConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration of the seed or starting point URLs of the websites you want to crawl.

            You can choose to crawl only the website host names, or the website host names with subdomains, or the website host names with subdomains and other domains that the webpages link to.

            You can list up to 100 seed URLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerurls.html#cfn-kendra-datasource-webcrawlerurls-seedurlconfiguration
            '''
            result = self._values.get("seed_url_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.WebCrawlerSeedUrlConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def site_maps_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnDataSource.WebCrawlerSiteMapsConfigurationProperty", _IResolvable_da3f097b]]:
            '''Configuration of the sitemap URLs of the websites you want to crawl.

            Only URLs belonging to the same website host names are crawled. You can list up to three sitemap URLs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-webcrawlerurls.html#cfn-kendra-datasource-webcrawlerurls-sitemapsconfiguration
            '''
            result = self._values.get("site_maps_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnDataSource.WebCrawlerSiteMapsConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerUrlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnDataSource.WorkDocsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "organization_id": "organizationId",
            "crawl_comments": "crawlComments",
            "exclusion_patterns": "exclusionPatterns",
            "field_mappings": "fieldMappings",
            "inclusion_patterns": "inclusionPatterns",
            "use_change_log": "useChangeLog",
        },
    )
    class WorkDocsConfigurationProperty:
        def __init__(
            self,
            *,
            organization_id: builtins.str,
            crawl_comments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
            inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            use_change_log: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information to connect to Amazon WorkDocs as your data source.

            Amazon WorkDocs connector is available in Oregon, North Virginia, Sydney, Singapore and Ireland regions.

            :param organization_id: The identifier of the directory corresponding to your Amazon WorkDocs site repository. You can find the organization ID in the `AWS Directory Service <https://docs.aws.amazon.com/directoryservicev2/>`_ by going to *Active Directory* , then *Directories* . Your Amazon WorkDocs site directory has an ID, which is the organization ID. You can also set up a new Amazon WorkDocs directory in the AWS Directory Service console and enable a Amazon WorkDocs site for the directory in the Amazon WorkDocs console.
            :param crawl_comments: ``TRUE`` to include comments on documents in your index. Including comments in your index means each comment is a document that can be searched on. The default is set to ``FALSE`` .
            :param exclusion_patterns: A list of regular expression patterns to exclude certain files in your Amazon WorkDocs site repository. Files that match the patterns are excluded from the index. Files that don’t match the patterns are included in the index. If a file matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the file isn't included in the index.
            :param field_mappings: A list of ``DataSourceToIndexFieldMapping`` objects that map Amazon WorkDocs data source attributes or field names to Amazon Kendra index field names. To create custom fields, use the ``UpdateIndex`` API before you map to Amazon WorkDocs fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Amazon WorkDocs data source field names must exist in your Amazon WorkDocs custom metadata.
            :param inclusion_patterns: A list of regular expression patterns to include certain files in your Amazon WorkDocs site repository. Files that match the patterns are included in the index. Files that don't match the patterns are excluded from the index. If a file matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the file isn't included in the index.
            :param use_change_log: ``TRUE`` to use the Amazon WorkDocs change log to determine which documents require updating in the index. Depending on the change log's size, it may take longer for Amazon Kendra to use the change log than to scan all of your documents in Amazon WorkDocs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                work_docs_configuration_property = kendra.CfnDataSource.WorkDocsConfigurationProperty(
                    organization_id="organizationId",
                
                    # the properties below are optional
                    crawl_comments=False,
                    exclusion_patterns=["exclusionPatterns"],
                    field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                        data_source_field_name="dataSourceFieldName",
                        index_field_name="indexFieldName",
                
                        # the properties below are optional
                        date_field_format="dateFieldFormat"
                    )],
                    inclusion_patterns=["inclusionPatterns"],
                    use_change_log=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c81f941a7e6027762047ba2a4dca2a80cd0266333586cd6278af4d285b4e5623)
                check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
                check_type(argname="argument crawl_comments", value=crawl_comments, expected_type=type_hints["crawl_comments"])
                check_type(argname="argument exclusion_patterns", value=exclusion_patterns, expected_type=type_hints["exclusion_patterns"])
                check_type(argname="argument field_mappings", value=field_mappings, expected_type=type_hints["field_mappings"])
                check_type(argname="argument inclusion_patterns", value=inclusion_patterns, expected_type=type_hints["inclusion_patterns"])
                check_type(argname="argument use_change_log", value=use_change_log, expected_type=type_hints["use_change_log"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "organization_id": organization_id,
            }
            if crawl_comments is not None:
                self._values["crawl_comments"] = crawl_comments
            if exclusion_patterns is not None:
                self._values["exclusion_patterns"] = exclusion_patterns
            if field_mappings is not None:
                self._values["field_mappings"] = field_mappings
            if inclusion_patterns is not None:
                self._values["inclusion_patterns"] = inclusion_patterns
            if use_change_log is not None:
                self._values["use_change_log"] = use_change_log

        @builtins.property
        def organization_id(self) -> builtins.str:
            '''The identifier of the directory corresponding to your Amazon WorkDocs site repository.

            You can find the organization ID in the `AWS Directory Service <https://docs.aws.amazon.com/directoryservicev2/>`_ by going to *Active Directory* , then *Directories* . Your Amazon WorkDocs site directory has an ID, which is the organization ID. You can also set up a new Amazon WorkDocs directory in the AWS Directory Service console and enable a Amazon WorkDocs site for the directory in the Amazon WorkDocs console.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-organizationid
            '''
            result = self._values.get("organization_id")
            assert result is not None, "Required property 'organization_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def crawl_comments(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to include comments on documents in your index.

            Including comments in your index means each comment is a document that can be searched on.

            The default is set to ``FALSE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-crawlcomments
            '''
            result = self._values.get("crawl_comments")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def exclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to exclude certain files in your Amazon WorkDocs site repository.

            Files that match the patterns are excluded from the index. Files that don’t match the patterns are included in the index. If a file matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the file isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-exclusionpatterns
            '''
            result = self._values.get("exclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field_mappings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]]:
            '''A list of ``DataSourceToIndexFieldMapping`` objects that map Amazon WorkDocs data source attributes or field names to Amazon Kendra index field names.

            To create custom fields, use the ``UpdateIndex`` API before you map to Amazon WorkDocs fields. For more information, see `Mapping data source fields <https://docs.aws.amazon.com/kendra/latest/dg/field-mapping.html>`_ . The Amazon WorkDocs data source field names must exist in your Amazon WorkDocs custom metadata.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-fieldmappings
            '''
            result = self._values.get("field_mappings")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnDataSource.DataSourceToIndexFieldMappingProperty", _IResolvable_da3f097b]]]], result)

        @builtins.property
        def inclusion_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of regular expression patterns to include certain files in your Amazon WorkDocs site repository.

            Files that match the patterns are included in the index. Files that don't match the patterns are excluded from the index. If a file matches both an inclusion and exclusion pattern, the exclusion pattern takes precedence and the file isn't included in the index.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-inclusionpatterns
            '''
            result = self._values.get("inclusion_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def use_change_log(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''``TRUE`` to use the Amazon WorkDocs change log to determine which documents require updating in the index.

            Depending on the change log's size, it may take longer for Amazon Kendra to use the change log than to scan all of your documents in Amazon WorkDocs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-datasource-workdocsconfiguration.html#cfn-kendra-datasource-workdocsconfiguration-usechangelog
            '''
            result = self._values.get("use_change_log")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkDocsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_kendra.CfnDataSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "index_id": "indexId",
        "name": "name",
        "type": "type",
        "custom_document_enrichment_configuration": "customDocumentEnrichmentConfiguration",
        "data_source_configuration": "dataSourceConfiguration",
        "description": "description",
        "role_arn": "roleArn",
        "schedule": "schedule",
        "tags": "tags",
    },
)
class CfnDataSourceProps:
    def __init__(
        self,
        *,
        index_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        custom_document_enrichment_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.CustomDocumentEnrichmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        data_source_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        description: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataSource``.

        :param index_id: The identifier of the index you want to use with the data source connector.
        :param name: The name of the data source.
        :param type: The type of the data source.
        :param custom_document_enrichment_configuration: Configuration information for altering document metadata and content during the document ingestion process.
        :param data_source_configuration: Configuration information for an Amazon Kendra data source. The contents of the configuration depend on the type of data source. You can only specify one type of data source in the configuration. You can't specify the ``Configuration`` parameter when the ``Type`` parameter is set to ``CUSTOM`` . The ``Configuration`` parameter is required for all other data sources.
        :param description: A description for the data source connector.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the data source. You can't specify the ``RoleArn`` parameter when the ``Type`` parameter is set to ``CUSTOM`` . The ``RoleArn`` parameter is required for all other data sources.
        :param schedule: Sets the frequency that Amazon Kendra checks the documents in your data source and updates the index. If you don't set a schedule, Amazon Kendra doesn't periodically update the index.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_kendra as kendra
            
            cfn_data_source_props = kendra.CfnDataSourceProps(
                index_id="indexId",
                name="name",
                type="type",
            
                # the properties below are optional
                custom_document_enrichment_configuration=kendra.CfnDataSource.CustomDocumentEnrichmentConfigurationProperty(
                    inline_configurations=[kendra.CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty(
                        condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            operator="operator",
            
                            # the properties below are optional
                            condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        ),
                        document_content_deletion=False,
                        target=kendra.CfnDataSource.DocumentAttributeTargetProperty(
                            target_document_attribute_key="targetDocumentAttributeKey",
            
                            # the properties below are optional
                            target_document_attribute_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            ),
                            target_document_attribute_value_deletion=False
                        )
                    )],
                    post_extraction_hook_configuration=kendra.CfnDataSource.HookConfigurationProperty(
                        lambda_arn="lambdaArn",
                        s3_bucket="s3Bucket",
            
                        # the properties below are optional
                        invocation_condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            operator="operator",
            
                            # the properties below are optional
                            condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        )
                    ),
                    pre_extraction_hook_configuration=kendra.CfnDataSource.HookConfigurationProperty(
                        lambda_arn="lambdaArn",
                        s3_bucket="s3Bucket",
            
                        # the properties below are optional
                        invocation_condition=kendra.CfnDataSource.DocumentAttributeConditionProperty(
                            condition_document_attribute_key="conditionDocumentAttributeKey",
                            operator="operator",
            
                            # the properties below are optional
                            condition_on_value=kendra.CfnDataSource.DocumentAttributeValueProperty(
                                date_value="dateValue",
                                long_value=123,
                                string_list_value=["stringListValue"],
                                string_value="stringValue"
                            )
                        )
                    ),
                    role_arn="roleArn"
                ),
                data_source_configuration=kendra.CfnDataSource.DataSourceConfigurationProperty(
                    confluence_configuration=kendra.CfnDataSource.ConfluenceConfigurationProperty(
                        secret_arn="secretArn",
                        server_url="serverUrl",
                        version="version",
            
                        # the properties below are optional
                        attachment_configuration=kendra.CfnDataSource.ConfluenceAttachmentConfigurationProperty(
                            attachment_field_mappings=[kendra.CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )],
                            crawl_attachments=False
                        ),
                        blog_configuration=kendra.CfnDataSource.ConfluenceBlogConfigurationProperty(
                            blog_field_mappings=[kendra.CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        exclusion_patterns=["exclusionPatterns"],
                        inclusion_patterns=["inclusionPatterns"],
                        page_configuration=kendra.CfnDataSource.ConfluencePageConfigurationProperty(
                            page_field_mappings=[kendra.CfnDataSource.ConfluencePageToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        space_configuration=kendra.CfnDataSource.ConfluenceSpaceConfigurationProperty(
                            crawl_archived_spaces=False,
                            crawl_personal_spaces=False,
                            exclude_spaces=["excludeSpaces"],
                            include_spaces=["includeSpaces"],
                            space_field_mappings=[kendra.CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    database_configuration=kendra.CfnDataSource.DatabaseConfigurationProperty(
                        column_configuration=kendra.CfnDataSource.ColumnConfigurationProperty(
                            change_detecting_columns=["changeDetectingColumns"],
                            document_data_column_name="documentDataColumnName",
                            document_id_column_name="documentIdColumnName",
            
                            # the properties below are optional
                            document_title_column_name="documentTitleColumnName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        connection_configuration=kendra.CfnDataSource.ConnectionConfigurationProperty(
                            database_host="databaseHost",
                            database_name="databaseName",
                            database_port=123,
                            secret_arn="secretArn",
                            table_name="tableName"
                        ),
                        database_engine_type="databaseEngineType",
            
                        # the properties below are optional
                        acl_configuration=kendra.CfnDataSource.AclConfigurationProperty(
                            allowed_groups_column_name="allowedGroupsColumnName"
                        ),
                        sql_configuration=kendra.CfnDataSource.SqlConfigurationProperty(
                            query_identifiers_enclosing_option="queryIdentifiersEnclosingOption"
                        ),
                        vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    google_drive_configuration=kendra.CfnDataSource.GoogleDriveConfigurationProperty(
                        secret_arn="secretArn",
            
                        # the properties below are optional
                        exclude_mime_types=["excludeMimeTypes"],
                        exclude_shared_drives=["excludeSharedDrives"],
                        exclude_user_accounts=["excludeUserAccounts"],
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
            
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        inclusion_patterns=["inclusionPatterns"]
                    ),
                    one_drive_configuration=kendra.CfnDataSource.OneDriveConfigurationProperty(
                        one_drive_users=kendra.CfnDataSource.OneDriveUsersProperty(
                            one_drive_user_list=["oneDriveUserList"],
                            one_drive_user_s3_path=kendra.CfnDataSource.S3PathProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        secret_arn="secretArn",
                        tenant_domain="tenantDomain",
            
                        # the properties below are optional
                        disable_local_groups=False,
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
            
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        inclusion_patterns=["inclusionPatterns"]
                    ),
                    s3_configuration=kendra.CfnDataSource.S3DataSourceConfigurationProperty(
                        bucket_name="bucketName",
            
                        # the properties below are optional
                        access_control_list_configuration=kendra.CfnDataSource.AccessControlListConfigurationProperty(
                            key_path="keyPath"
                        ),
                        documents_metadata_configuration=kendra.CfnDataSource.DocumentsMetadataConfigurationProperty(
                            s3_prefix="s3Prefix"
                        ),
                        exclusion_patterns=["exclusionPatterns"],
                        inclusion_patterns=["inclusionPatterns"],
                        inclusion_prefixes=["inclusionPrefixes"]
                    ),
                    salesforce_configuration=kendra.CfnDataSource.SalesforceConfigurationProperty(
                        secret_arn="secretArn",
                        server_url="serverUrl",
            
                        # the properties below are optional
                        chatter_feed_configuration=kendra.CfnDataSource.SalesforceChatterFeedConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
            
                            # the properties below are optional
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )],
                            include_filter_types=["includeFilterTypes"]
                        ),
                        crawl_attachments=False,
                        exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                        include_attachment_file_patterns=["includeAttachmentFilePatterns"],
                        knowledge_article_configuration=kendra.CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty(
                            included_states=["includedStates"],
            
                            # the properties below are optional
                            custom_knowledge_article_type_configurations=[kendra.CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty(
                                document_data_field_name="documentDataFieldName",
                                name="name",
            
                                # the properties below are optional
                                document_title_field_name="documentTitleFieldName",
                                field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                    data_source_field_name="dataSourceFieldName",
                                    index_field_name="indexFieldName",
            
                                    # the properties below are optional
                                    date_field_format="dateFieldFormat"
                                )]
                            )],
                            standard_knowledge_article_type_configuration=kendra.CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty(
                                document_data_field_name="documentDataFieldName",
            
                                # the properties below are optional
                                document_title_field_name="documentTitleFieldName",
                                field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                    data_source_field_name="dataSourceFieldName",
                                    index_field_name="indexFieldName",
            
                                    # the properties below are optional
                                    date_field_format="dateFieldFormat"
                                )]
                            )
                        ),
                        standard_object_attachment_configuration=kendra.CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty(
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        ),
                        standard_object_configurations=[kendra.CfnDataSource.SalesforceStandardObjectConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
                            name="name",
            
                            # the properties below are optional
                            document_title_field_name="documentTitleFieldName",
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )]
                        )]
                    ),
                    service_now_configuration=kendra.CfnDataSource.ServiceNowConfigurationProperty(
                        host_url="hostUrl",
                        secret_arn="secretArn",
                        service_now_build_version="serviceNowBuildVersion",
            
                        # the properties below are optional
                        authentication_type="authenticationType",
                        knowledge_article_configuration=kendra.CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
            
                            # the properties below are optional
                            crawl_attachments=False,
                            document_title_field_name="documentTitleFieldName",
                            exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )],
                            filter_query="filterQuery",
                            include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                        ),
                        service_catalog_configuration=kendra.CfnDataSource.ServiceNowServiceCatalogConfigurationProperty(
                            document_data_field_name="documentDataFieldName",
            
                            # the properties below are optional
                            crawl_attachments=False,
                            document_title_field_name="documentTitleFieldName",
                            exclude_attachment_file_patterns=["excludeAttachmentFilePatterns"],
                            field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                                data_source_field_name="dataSourceFieldName",
                                index_field_name="indexFieldName",
            
                                # the properties below are optional
                                date_field_format="dateFieldFormat"
                            )],
                            include_attachment_file_patterns=["includeAttachmentFilePatterns"]
                        )
                    ),
                    share_point_configuration=kendra.CfnDataSource.SharePointConfigurationProperty(
                        secret_arn="secretArn",
                        share_point_version="sharePointVersion",
                        urls=["urls"],
            
                        # the properties below are optional
                        crawl_attachments=False,
                        disable_local_groups=False,
                        document_title_field_name="documentTitleFieldName",
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
            
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        ssl_certificate_s3_path=kendra.CfnDataSource.S3PathProperty(
                            bucket="bucket",
                            key="key"
                        ),
                        use_change_log=False,
                        vpc_configuration=kendra.CfnDataSource.DataSourceVpcConfigurationProperty(
                            security_group_ids=["securityGroupIds"],
                            subnet_ids=["subnetIds"]
                        )
                    ),
                    web_crawler_configuration=kendra.CfnDataSource.WebCrawlerConfigurationProperty(
                        urls=kendra.CfnDataSource.WebCrawlerUrlsProperty(
                            seed_url_configuration=kendra.CfnDataSource.WebCrawlerSeedUrlConfigurationProperty(
                                seed_urls=["seedUrls"],
            
                                # the properties below are optional
                                web_crawler_mode="webCrawlerMode"
                            ),
                            site_maps_configuration=kendra.CfnDataSource.WebCrawlerSiteMapsConfigurationProperty(
                                site_maps=["siteMaps"]
                            )
                        ),
            
                        # the properties below are optional
                        authentication_configuration=kendra.CfnDataSource.WebCrawlerAuthenticationConfigurationProperty(
                            basic_authentication=[kendra.CfnDataSource.WebCrawlerBasicAuthenticationProperty(
                                credentials="credentials",
                                host="host",
                                port=123
                            )]
                        ),
                        crawl_depth=123,
                        max_content_size_per_page_in_mega_bytes=123,
                        max_links_per_page=123,
                        max_urls_per_minute_crawl_rate=123,
                        proxy_configuration=kendra.CfnDataSource.ProxyConfigurationProperty(
                            host="host",
                            port=123,
            
                            # the properties below are optional
                            credentials="credentials"
                        ),
                        url_exclusion_patterns=["urlExclusionPatterns"],
                        url_inclusion_patterns=["urlInclusionPatterns"]
                    ),
                    work_docs_configuration=kendra.CfnDataSource.WorkDocsConfigurationProperty(
                        organization_id="organizationId",
            
                        # the properties below are optional
                        crawl_comments=False,
                        exclusion_patterns=["exclusionPatterns"],
                        field_mappings=[kendra.CfnDataSource.DataSourceToIndexFieldMappingProperty(
                            data_source_field_name="dataSourceFieldName",
                            index_field_name="indexFieldName",
            
                            # the properties below are optional
                            date_field_format="dateFieldFormat"
                        )],
                        inclusion_patterns=["inclusionPatterns"],
                        use_change_log=False
                    )
                ),
                description="description",
                role_arn="roleArn",
                schedule="schedule",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9542f7b6e1451dc9177bf24b7be378edc74ce522d3fa3c567f3674a5f145a654)
            check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument custom_document_enrichment_configuration", value=custom_document_enrichment_configuration, expected_type=type_hints["custom_document_enrichment_configuration"])
            check_type(argname="argument data_source_configuration", value=data_source_configuration, expected_type=type_hints["data_source_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_id": index_id,
            "name": name,
            "type": type,
        }
        if custom_document_enrichment_configuration is not None:
            self._values["custom_document_enrichment_configuration"] = custom_document_enrichment_configuration
        if data_source_configuration is not None:
            self._values["data_source_configuration"] = data_source_configuration
        if description is not None:
            self._values["description"] = description
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if schedule is not None:
            self._values["schedule"] = schedule
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def index_id(self) -> builtins.str:
        '''The identifier of the index you want to use with the data source connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-indexid
        '''
        result = self._values.get("index_id")
        assert result is not None, "Required property 'index_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the data source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_document_enrichment_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.CustomDocumentEnrichmentConfigurationProperty, _IResolvable_da3f097b]]:
        '''Configuration information for altering document metadata and content during the document ingestion process.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-customdocumentenrichmentconfiguration
        '''
        result = self._values.get("custom_document_enrichment_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.CustomDocumentEnrichmentConfigurationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def data_source_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnDataSource.DataSourceConfigurationProperty, _IResolvable_da3f097b]]:
        '''Configuration information for an Amazon Kendra data source.

        The contents of the configuration depend on the type of data source. You can only specify one type of data source in the configuration.

        You can't specify the ``Configuration`` parameter when the ``Type`` parameter is set to ``CUSTOM`` .

        The ``Configuration`` parameter is required for all other data sources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-datasourceconfiguration
        '''
        result = self._values.get("data_source_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnDataSource.DataSourceConfigurationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the data source connector.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a role with permission to access the data source.

        You can't specify the ``RoleArn`` parameter when the ``Type`` parameter is set to ``CUSTOM`` .

        The ``RoleArn`` parameter is required for all other data sources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Sets the frequency that Amazon Kendra checks the documents in your data source and updates the index.

        If you don't set a schedule, Amazon Kendra doesn't periodically update the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-datasource.html#cfn-kendra-datasource-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnFaq(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_kendra.CfnFaq",
):
    '''A CloudFormation ``AWS::Kendra::Faq``.

    Creates an new set of frequently asked question (FAQ) questions and answers.

    :cloudformationResource: AWS::Kendra::Faq
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_kendra as kendra
        
        cfn_faq = kendra.CfnFaq(self, "MyCfnFaq",
            index_id="indexId",
            name="name",
            role_arn="roleArn",
            s3_path=kendra.CfnFaq.S3PathProperty(
                bucket="bucket",
                key="key"
            ),
        
            # the properties below are optional
            description="description",
            file_format="fileFormat",
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
        index_id: builtins.str,
        name: builtins.str,
        role_arn: builtins.str,
        s3_path: typing.Union[typing.Union["CfnFaq.S3PathProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        description: typing.Optional[builtins.str] = None,
        file_format: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Kendra::Faq``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param index_id: The identifier of the index that contains the FAQ.
        :param name: The name that you assigned the FAQ when you created or updated the FAQ.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the S3 bucket that contains the FAQ.
        :param s3_path: The Amazon Simple Storage Service (Amazon S3) location of the FAQ input data.
        :param description: A description for the FAQ.
        :param file_format: The format of the input file. You can choose between a basic CSV format, a CSV format that includes customs attributes in a header, and a JSON format that includes custom attributes. The format must match the format of the file stored in the S3 bucket identified in the S3Path parameter. Valid values are: - ``CSV`` - ``CSV_WITH_HEADER`` - ``JSON``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da52634bf448f13a8dfdf111b1193f46a241ac941af460a15585386c0620fb57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFaqProps(
            index_id=index_id,
            name=name,
            role_arn=role_arn,
            s3_path=s3_path,
            description=description,
            file_format=file_format,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11ca22cd6dac6125f6c23af39c883b9555dc5ca8feff5890bbf847c4d2ec1afa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3be9b6ec7b4902d9ec2eb28db705482668d74fecb5632459047a1859f7b8270)
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
        '''``arn:aws:kendra:us-west-2:111122223333:index/335c3741-41df-46a6-b5d3-61f85b787884/faq/f61995a6-cd5c-4e99-9cfc-58816d8bfaa7``.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier for the FAQ. For example:.

        ``f61995a6-cd5c-4e99-9cfc-58816d8bfaa7``

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="indexId")
    def index_id(self) -> builtins.str:
        '''The identifier of the index that contains the FAQ.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-indexid
        '''
        return typing.cast(builtins.str, jsii.get(self, "indexId"))

    @index_id.setter
    def index_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f1e70154142736744f66230e1c5b07df97f4a652446db44168d67c14beeea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name that you assigned the FAQ when you created or updated the FAQ.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b594acf6aecd343c9db04631030ca07304c2847b8ee62acf9027423dcc196ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of a role with permission to access the S3 bucket that contains the FAQ.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef4a3a137a43525f6d969da0db69ab6343d8d1b2954c1e827bc8a9161cefbf0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="s3Path")
    def s3_path(self) -> typing.Union["CfnFaq.S3PathProperty", _IResolvable_da3f097b]:
        '''The Amazon Simple Storage Service (Amazon S3) location of the FAQ input data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-s3path
        '''
        return typing.cast(typing.Union["CfnFaq.S3PathProperty", _IResolvable_da3f097b], jsii.get(self, "s3Path"))

    @s3_path.setter
    def s3_path(
        self,
        value: typing.Union["CfnFaq.S3PathProperty", _IResolvable_da3f097b],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1806afef94a938b4b58ebc0c38dcb5cddd53c1cee6e9ac50febc0bea90c9290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3Path", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the FAQ.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6fdcd3bb79f5f910c29a7243dd6f733e9edf684e556ed8d65538ed6d320d77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="fileFormat")
    def file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the input file.

        You can choose between a basic CSV format, a CSV format that includes customs attributes in a header, and a JSON format that includes custom attributes.

        The format must match the format of the file stored in the S3 bucket identified in the S3Path parameter.

        Valid values are:

        - ``CSV``
        - ``CSV_WITH_HEADER``
        - ``JSON``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-fileformat
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileFormat"))

    @file_format.setter
    def file_format(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c1da4741f70f3470f4ba1da7528d2bd5f61244bea5440442acec296bbd15b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileFormat", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnFaq.S3PathProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3PathProperty:
        def __init__(self, *, bucket: builtins.str, key: builtins.str) -> None:
            '''Information required to find a specific file in an Amazon S3 bucket.

            :param bucket: The name of the S3 bucket that contains the file.
            :param key: The name of the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-faq-s3path.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                s3_path_property = kendra.CfnFaq.S3PathProperty(
                    bucket="bucket",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c660660356fbb032dd86a92e34819e3494aa7fd2f3187fca1481c4c3aba2a3d)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket": bucket,
                "key": key,
            }

        @builtins.property
        def bucket(self) -> builtins.str:
            '''The name of the S3 bucket that contains the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-faq-s3path.html#cfn-kendra-faq-s3path-bucket
            '''
            result = self._values.get("bucket")
            assert result is not None, "Required property 'bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key(self) -> builtins.str:
            '''The name of the file.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-faq-s3path.html#cfn-kendra-faq-s3path-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3PathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_kendra.CfnFaqProps",
    jsii_struct_bases=[],
    name_mapping={
        "index_id": "indexId",
        "name": "name",
        "role_arn": "roleArn",
        "s3_path": "s3Path",
        "description": "description",
        "file_format": "fileFormat",
        "tags": "tags",
    },
)
class CfnFaqProps:
    def __init__(
        self,
        *,
        index_id: builtins.str,
        name: builtins.str,
        role_arn: builtins.str,
        s3_path: typing.Union[typing.Union[CfnFaq.S3PathProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
        description: typing.Optional[builtins.str] = None,
        file_format: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFaq``.

        :param index_id: The identifier of the index that contains the FAQ.
        :param name: The name that you assigned the FAQ when you created or updated the FAQ.
        :param role_arn: The Amazon Resource Name (ARN) of a role with permission to access the S3 bucket that contains the FAQ.
        :param s3_path: The Amazon Simple Storage Service (Amazon S3) location of the FAQ input data.
        :param description: A description for the FAQ.
        :param file_format: The format of the input file. You can choose between a basic CSV format, a CSV format that includes customs attributes in a header, and a JSON format that includes custom attributes. The format must match the format of the file stored in the S3 bucket identified in the S3Path parameter. Valid values are: - ``CSV`` - ``CSV_WITH_HEADER`` - ``JSON``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_kendra as kendra
            
            cfn_faq_props = kendra.CfnFaqProps(
                index_id="indexId",
                name="name",
                role_arn="roleArn",
                s3_path=kendra.CfnFaq.S3PathProperty(
                    bucket="bucket",
                    key="key"
                ),
            
                # the properties below are optional
                description="description",
                file_format="fileFormat",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d80eed0b304b1e2dc88b2a6b3ac2392e3650ef0ac292928d043232bd3fae1be)
            check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument s3_path", value=s3_path, expected_type=type_hints["s3_path"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "index_id": index_id,
            "name": name,
            "role_arn": role_arn,
            "s3_path": s3_path,
        }
        if description is not None:
            self._values["description"] = description
        if file_format is not None:
            self._values["file_format"] = file_format
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def index_id(self) -> builtins.str:
        '''The identifier of the index that contains the FAQ.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-indexid
        '''
        result = self._values.get("index_id")
        assert result is not None, "Required property 'index_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name that you assigned the FAQ when you created or updated the FAQ.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of a role with permission to access the S3 bucket that contains the FAQ.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_path(self) -> typing.Union[CfnFaq.S3PathProperty, _IResolvable_da3f097b]:
        '''The Amazon Simple Storage Service (Amazon S3) location of the FAQ input data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-s3path
        '''
        result = self._values.get("s3_path")
        assert result is not None, "Required property 's3_path' is missing"
        return typing.cast(typing.Union[CfnFaq.S3PathProperty, _IResolvable_da3f097b], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the FAQ.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the input file.

        You can choose between a basic CSV format, a CSV format that includes customs attributes in a header, and a JSON format that includes custom attributes.

        The format must match the format of the file stored in the S3 bucket identified in the S3Path parameter.

        Valid values are:

        - ``CSV``
        - ``CSV_WITH_HEADER``
        - ``JSON``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-fileformat
        '''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-faq.html#cfn-kendra-faq-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFaqProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_c2943556)
class CfnIndex(
    _CfnResource_9df397a6,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_kendra.CfnIndex",
):
    '''A CloudFormation ``AWS::Kendra::Index``.

    Creates an Amazon Kendra index

    Once the index is active you can add documents to your index using the `BatchPutDocument <https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html>`_ operation or using one of the supported data sources.

    :cloudformationResource: AWS::Kendra::Index
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_kendra as kendra
        
        cfn_index = kendra.CfnIndex(self, "MyCfnIndex",
            edition="edition",
            name="name",
            role_arn="roleArn",
        
            # the properties below are optional
            capacity_units=kendra.CfnIndex.CapacityUnitsConfigurationProperty(
                query_capacity_units=123,
                storage_capacity_units=123
            ),
            description="description",
            document_metadata_configurations=[kendra.CfnIndex.DocumentMetadataConfigurationProperty(
                name="name",
                type="type",
        
                # the properties below are optional
                relevance=kendra.CfnIndex.RelevanceProperty(
                    duration="duration",
                    freshness=False,
                    importance=123,
                    rank_order="rankOrder",
                    value_importance_items=[kendra.CfnIndex.ValueImportanceItemProperty(
                        key="key",
                        value=123
                    )]
                ),
                search=kendra.CfnIndex.SearchProperty(
                    displayable=False,
                    facetable=False,
                    searchable=False,
                    sortable=False
                )
            )],
            server_side_encryption_configuration=kendra.CfnIndex.ServerSideEncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_context_policy="userContextPolicy",
            user_token_configurations=[kendra.CfnIndex.UserTokenConfigurationProperty(
                json_token_type_configuration=kendra.CfnIndex.JsonTokenTypeConfigurationProperty(
                    group_attribute_field="groupAttributeField",
                    user_name_attribute_field="userNameAttributeField"
                ),
                jwt_token_type_configuration=kendra.CfnIndex.JwtTokenTypeConfigurationProperty(
                    key_location="keyLocation",
        
                    # the properties below are optional
                    claim_regex="claimRegex",
                    group_attribute_field="groupAttributeField",
                    issuer="issuer",
                    secret_manager_arn="secretManagerArn",
                    url="url",
                    user_name_attribute_field="userNameAttributeField"
                )
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        edition: builtins.str,
        name: builtins.str,
        role_arn: builtins.str,
        capacity_units: typing.Optional[typing.Union[typing.Union["CfnIndex.CapacityUnitsConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        description: typing.Optional[builtins.str] = None,
        document_metadata_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnIndex.DocumentMetadataConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[typing.Union["CfnIndex.ServerSideEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_context_policy: typing.Optional[builtins.str] = None,
        user_token_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnIndex.UserTokenConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Kendra::Index``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param edition: Indicates whether the index is a Enterprise Edition index or a Developer Edition index. Valid values are ``DEVELOPER_EDITION`` and ``ENTERPRISE_EDITION`` .
        :param name: The name of the index.
        :param role_arn: An IAM role that gives Amazon Kendra permissions to access your Amazon CloudWatch logs and metrics. This is also the role used when you use the `BatchPutDocument <https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html>`_ operation to index documents from an Amazon S3 bucket.
        :param capacity_units: ``AWS::Kendra::Index.CapacityUnits``.
        :param description: A description for the index.
        :param document_metadata_configurations: Specifies the properties of an index field. You can add either a custom or a built-in field. You can add and remove built-in fields at any time. When a built-in field is removed it's configuration reverts to the default for the field. Custom fields can't be removed from an index after they are added.
        :param server_side_encryption_configuration: The identifier of the AWS KMS customer managed key (CMK) to use to encrypt data indexed by Amazon Kendra. Amazon Kendra doesn't support asymmetric CMKs.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param user_context_policy: The user context policy. ATTRIBUTE_FILTER - All indexed content is searchable and displayable for all users. If you want to filter search results on user context, you can use the attribute filters of ``_user_id`` and ``_group_ids`` or you can provide user and group information in ``UserContext`` . USER_TOKEN - Enables token-based user access control to filter search results on user context. All documents with no access control and all documents accessible to the user will be searchable and displayable.
        :param user_token_configurations: Defines the type of user token used for the index.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1204970a88ec523311382503badf4dde293efe7a39dfb0456e1240724565fb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnIndexProps(
            edition=edition,
            name=name,
            role_arn=role_arn,
            capacity_units=capacity_units,
            description=description,
            document_metadata_configurations=document_metadata_configurations,
            server_side_encryption_configuration=server_side_encryption_configuration,
            tags=tags,
            user_context_policy=user_context_policy,
            user_token_configurations=user_token_configurations,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_488e0dd5) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540517a32fdcfcd298c87cf94ee56816edf19e0499b0f6948fee9fd23be529c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2df7cdccb6eab5e36f563831c237ba0ca6d01e47278e44ac46624c34c5638bc)
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
        '''The Amazon Resource Name (ARN) of the index.

        For example: ``arn:aws:kendra:us-west-2:111122223333:index/0123456789abcdef`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier for the index.

        For example: ``f4aeaa10-8056-4b2c-a343-522ca0f41234`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0a598cb3:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-tags
        '''
        return typing.cast(_TagManager_0a598cb3, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="edition")
    def edition(self) -> builtins.str:
        '''Indicates whether the index is a Enterprise Edition index or a Developer Edition index.

        Valid values are ``DEVELOPER_EDITION`` and ``ENTERPRISE_EDITION`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-edition
        '''
        return typing.cast(builtins.str, jsii.get(self, "edition"))

    @edition.setter
    def edition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c93239f3ae00e7cb944fd204cb022d7f5be68421fd79c69ed3f2763a51080330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edition", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8dbceb731e5a625527a5cc01b7c46b54b6616680debfa96e2ab053da367d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''An IAM role that gives Amazon Kendra permissions to access your Amazon CloudWatch logs and metrics.

        This is also the role used when you use the `BatchPutDocument <https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html>`_ operation to index documents from an Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8a890b398c997757af70a90887f07071ac0aff33283747ecb57cfbc966ef073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="capacityUnits")
    def capacity_units(
        self,
    ) -> typing.Optional[typing.Union["CfnIndex.CapacityUnitsConfigurationProperty", _IResolvable_da3f097b]]:
        '''``AWS::Kendra::Index.CapacityUnits``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-capacityunits
        '''
        return typing.cast(typing.Optional[typing.Union["CfnIndex.CapacityUnitsConfigurationProperty", _IResolvable_da3f097b]], jsii.get(self, "capacityUnits"))

    @capacity_units.setter
    def capacity_units(
        self,
        value: typing.Optional[typing.Union["CfnIndex.CapacityUnitsConfigurationProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf6edadfe64bf9cc89fb346617e7ebf299db00a7377538a0131f98173bfe1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityUnits", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75d78a23badee4ab3e1d5d8e4a54eeed850580bfffd42919232175a85362394b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="documentMetadataConfigurations")
    def document_metadata_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnIndex.DocumentMetadataConfigurationProperty", _IResolvable_da3f097b]]]]:
        '''Specifies the properties of an index field.

        You can add either a custom or a built-in field. You can add and remove built-in fields at any time. When a built-in field is removed it's configuration reverts to the default for the field. Custom fields can't be removed from an index after they are added.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-documentmetadataconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnIndex.DocumentMetadataConfigurationProperty", _IResolvable_da3f097b]]]], jsii.get(self, "documentMetadataConfigurations"))

    @document_metadata_configurations.setter
    def document_metadata_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnIndex.DocumentMetadataConfigurationProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6a2782afe74760aa4cd4a1e2c5389ae5d499b8e0b17c4f53326aba33c6a5ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "documentMetadataConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnIndex.ServerSideEncryptionConfigurationProperty", _IResolvable_da3f097b]]:
        '''The identifier of the AWS KMS customer managed key (CMK) to use to encrypt data indexed by Amazon Kendra.

        Amazon Kendra doesn't support asymmetric CMKs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-serversideencryptionconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnIndex.ServerSideEncryptionConfigurationProperty", _IResolvable_da3f097b]], jsii.get(self, "serverSideEncryptionConfiguration"))

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(
        self,
        value: typing.Optional[typing.Union["CfnIndex.ServerSideEncryptionConfigurationProperty", _IResolvable_da3f097b]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754853a1d856877c480ad0c2d5930ca3be45133cf17bdd2a002ec2af3d8c119d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverSideEncryptionConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="userContextPolicy")
    def user_context_policy(self) -> typing.Optional[builtins.str]:
        '''The user context policy.

        ATTRIBUTE_FILTER

        - All indexed content is searchable and displayable for all users. If you want to filter search results on user context, you can use the attribute filters of ``_user_id`` and ``_group_ids`` or you can provide user and group information in ``UserContext`` .

        USER_TOKEN

        - Enables token-based user access control to filter search results on user context. All documents with no access control and all documents accessible to the user will be searchable and displayable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-usercontextpolicy
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userContextPolicy"))

    @user_context_policy.setter
    def user_context_policy(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d813d698c8f17a6cd67584d63c8e7266087d6fa57cd89671e115048ddbfc3b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userContextPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="userTokenConfigurations")
    def user_token_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnIndex.UserTokenConfigurationProperty", _IResolvable_da3f097b]]]]:
        '''Defines the type of user token used for the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-usertokenconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnIndex.UserTokenConfigurationProperty", _IResolvable_da3f097b]]]], jsii.get(self, "userTokenConfigurations"))

    @user_token_configurations.setter
    def user_token_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnIndex.UserTokenConfigurationProperty", _IResolvable_da3f097b]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10cbdc54cc7ee0bf166d3e99163425e74855a9b539e601a9526126b7ad7f7b58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userTokenConfigurations", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.CapacityUnitsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_capacity_units": "queryCapacityUnits",
            "storage_capacity_units": "storageCapacityUnits",
        },
    )
    class CapacityUnitsConfigurationProperty:
        def __init__(
            self,
            *,
            query_capacity_units: jsii.Number,
            storage_capacity_units: jsii.Number,
        ) -> None:
            '''Specifies additional capacity units configured for your Enterprise Edition index.

            You can add and remove capacity units to fit your usage requirements.

            :param query_capacity_units: The amount of extra query capacity for an index and `GetQuerySuggestions <https://docs.aws.amazon.com/kendra/latest/dg/API_GetQuerySuggestions.html>`_ capacity. A single extra capacity unit for an index provides 0.1 queries per second or approximately 8,000 queries per day. You can add up to 100 extra capacity units. ``GetQuerySuggestions`` capacity is five times the provisioned query capacity for an index, or the base capacity of 2.5 calls per second, whichever is higher. For example, the base capacity for an index is 0.1 queries per second, and ``GetQuerySuggestions`` capacity has a base of 2.5 calls per second. If you add another 0.1 queries per second to total 0.2 queries per second for an index, the ``GetQuerySuggestions`` capacity is 2.5 calls per second (higher than five times 0.2 queries per second).
            :param storage_capacity_units: The amount of extra storage capacity for an index. A single capacity unit provides 30 GB of storage space or 100,000 documents, whichever is reached first. You can add up to 100 extra capacity units.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-capacityunitsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                capacity_units_configuration_property = kendra.CfnIndex.CapacityUnitsConfigurationProperty(
                    query_capacity_units=123,
                    storage_capacity_units=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7093c6b5e24a07c3c1a63e9139dde660572cc52116b64be9037e4edd6c4f67be)
                check_type(argname="argument query_capacity_units", value=query_capacity_units, expected_type=type_hints["query_capacity_units"])
                check_type(argname="argument storage_capacity_units", value=storage_capacity_units, expected_type=type_hints["storage_capacity_units"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "query_capacity_units": query_capacity_units,
                "storage_capacity_units": storage_capacity_units,
            }

        @builtins.property
        def query_capacity_units(self) -> jsii.Number:
            '''The amount of extra query capacity for an index and `GetQuerySuggestions <https://docs.aws.amazon.com/kendra/latest/dg/API_GetQuerySuggestions.html>`_ capacity.

            A single extra capacity unit for an index provides 0.1 queries per second or approximately 8,000 queries per day. You can add up to 100 extra capacity units.

            ``GetQuerySuggestions`` capacity is five times the provisioned query capacity for an index, or the base capacity of 2.5 calls per second, whichever is higher. For example, the base capacity for an index is 0.1 queries per second, and ``GetQuerySuggestions`` capacity has a base of 2.5 calls per second. If you add another 0.1 queries per second to total 0.2 queries per second for an index, the ``GetQuerySuggestions`` capacity is 2.5 calls per second (higher than five times 0.2 queries per second).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-capacityunitsconfiguration.html#cfn-kendra-index-capacityunitsconfiguration-querycapacityunits
            '''
            result = self._values.get("query_capacity_units")
            assert result is not None, "Required property 'query_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def storage_capacity_units(self) -> jsii.Number:
            '''The amount of extra storage capacity for an index.

            A single capacity unit provides 30 GB of storage space or 100,000 documents, whichever is reached first. You can add up to 100 extra capacity units.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-capacityunitsconfiguration.html#cfn-kendra-index-capacityunitsconfiguration-storagecapacityunits
            '''
            result = self._values.get("storage_capacity_units")
            assert result is not None, "Required property 'storage_capacity_units' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityUnitsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.DocumentMetadataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "type": "type",
            "relevance": "relevance",
            "search": "search",
        },
    )
    class DocumentMetadataConfigurationProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            type: builtins.str,
            relevance: typing.Optional[typing.Union[typing.Union["CfnIndex.RelevanceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            search: typing.Optional[typing.Union[typing.Union["CfnIndex.SearchProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Specifies the properties, such as relevance tuning and searchability, of an index field.

            :param name: The name of the index field.
            :param type: The data type of the index field.
            :param relevance: Provides tuning parameters to determine how the field affects the search results.
            :param search: Provides information about how the field is used during a search.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                document_metadata_configuration_property = kendra.CfnIndex.DocumentMetadataConfigurationProperty(
                    name="name",
                    type="type",
                
                    # the properties below are optional
                    relevance=kendra.CfnIndex.RelevanceProperty(
                        duration="duration",
                        freshness=False,
                        importance=123,
                        rank_order="rankOrder",
                        value_importance_items=[kendra.CfnIndex.ValueImportanceItemProperty(
                            key="key",
                            value=123
                        )]
                    ),
                    search=kendra.CfnIndex.SearchProperty(
                        displayable=False,
                        facetable=False,
                        searchable=False,
                        sortable=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__954dc04a56ef56fb898ce0f8582ed0990c0c46f17f7ca3f08d5016d39e3a463b)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument relevance", value=relevance, expected_type=type_hints["relevance"])
                check_type(argname="argument search", value=search, expected_type=type_hints["search"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "type": type,
            }
            if relevance is not None:
                self._values["relevance"] = relevance
            if search is not None:
                self._values["search"] = search

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the index field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html#cfn-kendra-index-documentmetadataconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The data type of the index field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html#cfn-kendra-index-documentmetadataconfiguration-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def relevance(
            self,
        ) -> typing.Optional[typing.Union["CfnIndex.RelevanceProperty", _IResolvable_da3f097b]]:
            '''Provides tuning parameters to determine how the field affects the search results.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html#cfn-kendra-index-documentmetadataconfiguration-relevance
            '''
            result = self._values.get("relevance")
            return typing.cast(typing.Optional[typing.Union["CfnIndex.RelevanceProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def search(
            self,
        ) -> typing.Optional[typing.Union["CfnIndex.SearchProperty", _IResolvable_da3f097b]]:
            '''Provides information about how the field is used during a search.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-documentmetadataconfiguration.html#cfn-kendra-index-documentmetadataconfiguration-search
            '''
            result = self._values.get("search")
            return typing.cast(typing.Optional[typing.Union["CfnIndex.SearchProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DocumentMetadataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.JsonTokenTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "group_attribute_field": "groupAttributeField",
            "user_name_attribute_field": "userNameAttributeField",
        },
    )
    class JsonTokenTypeConfigurationProperty:
        def __init__(
            self,
            *,
            group_attribute_field: builtins.str,
            user_name_attribute_field: builtins.str,
        ) -> None:
            '''Provides the configuration information for the JSON token type.

            :param group_attribute_field: The group attribute field.
            :param user_name_attribute_field: The user name attribute field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jsontokentypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                json_token_type_configuration_property = kendra.CfnIndex.JsonTokenTypeConfigurationProperty(
                    group_attribute_field="groupAttributeField",
                    user_name_attribute_field="userNameAttributeField"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6b8eb1909b62eab07efe488db208c9ecfe34acafbbeee38e4dea0fad0039e6d)
                check_type(argname="argument group_attribute_field", value=group_attribute_field, expected_type=type_hints["group_attribute_field"])
                check_type(argname="argument user_name_attribute_field", value=user_name_attribute_field, expected_type=type_hints["user_name_attribute_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "group_attribute_field": group_attribute_field,
                "user_name_attribute_field": user_name_attribute_field,
            }

        @builtins.property
        def group_attribute_field(self) -> builtins.str:
            '''The group attribute field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jsontokentypeconfiguration.html#cfn-kendra-index-jsontokentypeconfiguration-groupattributefield
            '''
            result = self._values.get("group_attribute_field")
            assert result is not None, "Required property 'group_attribute_field' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def user_name_attribute_field(self) -> builtins.str:
            '''The user name attribute field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jsontokentypeconfiguration.html#cfn-kendra-index-jsontokentypeconfiguration-usernameattributefield
            '''
            result = self._values.get("user_name_attribute_field")
            assert result is not None, "Required property 'user_name_attribute_field' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JsonTokenTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.JwtTokenTypeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key_location": "keyLocation",
            "claim_regex": "claimRegex",
            "group_attribute_field": "groupAttributeField",
            "issuer": "issuer",
            "secret_manager_arn": "secretManagerArn",
            "url": "url",
            "user_name_attribute_field": "userNameAttributeField",
        },
    )
    class JwtTokenTypeConfigurationProperty:
        def __init__(
            self,
            *,
            key_location: builtins.str,
            claim_regex: typing.Optional[builtins.str] = None,
            group_attribute_field: typing.Optional[builtins.str] = None,
            issuer: typing.Optional[builtins.str] = None,
            secret_manager_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
            user_name_attribute_field: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides the configuration information for the JWT token type.

            :param key_location: The location of the key.
            :param claim_regex: The regular expression that identifies the claim.
            :param group_attribute_field: The group attribute field.
            :param issuer: The issuer of the token.
            :param secret_manager_arn: The Amazon Resource Name (arn) of the secret.
            :param url: The signing key URL.
            :param user_name_attribute_field: The user name attribute field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                jwt_token_type_configuration_property = kendra.CfnIndex.JwtTokenTypeConfigurationProperty(
                    key_location="keyLocation",
                
                    # the properties below are optional
                    claim_regex="claimRegex",
                    group_attribute_field="groupAttributeField",
                    issuer="issuer",
                    secret_manager_arn="secretManagerArn",
                    url="url",
                    user_name_attribute_field="userNameAttributeField"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__643b3a2d709ad83dacc588a4aab7261225afdbf6c921738c4c323a1ee1ee5d21)
                check_type(argname="argument key_location", value=key_location, expected_type=type_hints["key_location"])
                check_type(argname="argument claim_regex", value=claim_regex, expected_type=type_hints["claim_regex"])
                check_type(argname="argument group_attribute_field", value=group_attribute_field, expected_type=type_hints["group_attribute_field"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
                check_type(argname="argument secret_manager_arn", value=secret_manager_arn, expected_type=type_hints["secret_manager_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
                check_type(argname="argument user_name_attribute_field", value=user_name_attribute_field, expected_type=type_hints["user_name_attribute_field"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key_location": key_location,
            }
            if claim_regex is not None:
                self._values["claim_regex"] = claim_regex
            if group_attribute_field is not None:
                self._values["group_attribute_field"] = group_attribute_field
            if issuer is not None:
                self._values["issuer"] = issuer
            if secret_manager_arn is not None:
                self._values["secret_manager_arn"] = secret_manager_arn
            if url is not None:
                self._values["url"] = url
            if user_name_attribute_field is not None:
                self._values["user_name_attribute_field"] = user_name_attribute_field

        @builtins.property
        def key_location(self) -> builtins.str:
            '''The location of the key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-keylocation
            '''
            result = self._values.get("key_location")
            assert result is not None, "Required property 'key_location' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def claim_regex(self) -> typing.Optional[builtins.str]:
            '''The regular expression that identifies the claim.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-claimregex
            '''
            result = self._values.get("claim_regex")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def group_attribute_field(self) -> typing.Optional[builtins.str]:
            '''The group attribute field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-groupattributefield
            '''
            result = self._values.get("group_attribute_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The issuer of the token.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_manager_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (arn) of the secret.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-secretmanagerarn
            '''
            result = self._values.get("secret_manager_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The signing key URL.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_name_attribute_field(self) -> typing.Optional[builtins.str]:
            '''The user name attribute field.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-jwttokentypeconfiguration.html#cfn-kendra-index-jwttokentypeconfiguration-usernameattributefield
            '''
            result = self._values.get("user_name_attribute_field")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JwtTokenTypeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.RelevanceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration": "duration",
            "freshness": "freshness",
            "importance": "importance",
            "rank_order": "rankOrder",
            "value_importance_items": "valueImportanceItems",
        },
    )
    class RelevanceProperty:
        def __init__(
            self,
            *,
            duration: typing.Optional[builtins.str] = None,
            freshness: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            importance: typing.Optional[jsii.Number] = None,
            rank_order: typing.Optional[builtins.str] = None,
            value_importance_items: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union["CfnIndex.ValueImportanceItemProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        ) -> None:
            '''Provides information for tuning the relevance of a field in a search.

            When a query includes terms that match the field, the results are given a boost in the response based on these tuning parameters.

            :param duration: Specifies the time period that the boost applies to. For example, to make the boost apply to documents with the field value within the last month, you would use "2628000s". Once the field value is beyond the specified range, the effect of the boost drops off. The higher the importance, the faster the effect drops off. If you don't specify a value, the default is 3 months. The value of the field is a numeric string followed by the character "s", for example "86400s" for one day, or "604800s" for one week. Only applies to ``DATE`` fields.
            :param freshness: Indicates that this field determines how "fresh" a document is. For example, if document 1 was created on November 5, and document 2 was created on October 31, document 1 is "fresher" than document 2. You can only set the ``Freshness`` field on one ``DATE`` type field. Only applies to ``DATE`` fields.
            :param importance: The relative importance of the field in the search. Larger numbers provide more of a boost than smaller numbers.
            :param rank_order: Determines how values should be interpreted. When the ``RankOrder`` field is ``ASCENDING`` , higher numbers are better. For example, a document with a rating score of 10 is higher ranking than a document with a rating score of 1. When the ``RankOrder`` field is ``DESCENDING`` , lower numbers are better. For example, in a task tracking application, a priority 1 task is more important than a priority 5 task. Only applies to ``LONG`` and ``DOUBLE`` fields.
            :param value_importance_items: An array of key-value pairs for different boosts when they appear in the search result list. For example, if you want to boost query terms that match the "department" field in the result, query terms that match this field are boosted in the result. You can add entries from the department field to boost documents with those values higher. For example, you can add entries to the map with names of departments. If you add "HR", 5 and "Legal",3 those departments are given special attention when they appear in the metadata of a document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                relevance_property = kendra.CfnIndex.RelevanceProperty(
                    duration="duration",
                    freshness=False,
                    importance=123,
                    rank_order="rankOrder",
                    value_importance_items=[kendra.CfnIndex.ValueImportanceItemProperty(
                        key="key",
                        value=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1accd841c4b5dd7504783ed3b5520e16e41f7c6efae6c85c12403238ea4d749)
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument freshness", value=freshness, expected_type=type_hints["freshness"])
                check_type(argname="argument importance", value=importance, expected_type=type_hints["importance"])
                check_type(argname="argument rank_order", value=rank_order, expected_type=type_hints["rank_order"])
                check_type(argname="argument value_importance_items", value=value_importance_items, expected_type=type_hints["value_importance_items"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration is not None:
                self._values["duration"] = duration
            if freshness is not None:
                self._values["freshness"] = freshness
            if importance is not None:
                self._values["importance"] = importance
            if rank_order is not None:
                self._values["rank_order"] = rank_order
            if value_importance_items is not None:
                self._values["value_importance_items"] = value_importance_items

        @builtins.property
        def duration(self) -> typing.Optional[builtins.str]:
            '''Specifies the time period that the boost applies to.

            For example, to make the boost apply to documents with the field value within the last month, you would use "2628000s". Once the field value is beyond the specified range, the effect of the boost drops off. The higher the importance, the faster the effect drops off. If you don't specify a value, the default is 3 months. The value of the field is a numeric string followed by the character "s", for example "86400s" for one day, or "604800s" for one week.

            Only applies to ``DATE`` fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-duration
            '''
            result = self._values.get("duration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def freshness(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''Indicates that this field determines how "fresh" a document is.

            For example, if document 1 was created on November 5, and document 2 was created on October 31, document 1 is "fresher" than document 2. You can only set the ``Freshness`` field on one ``DATE`` type field. Only applies to ``DATE`` fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-freshness
            '''
            result = self._values.get("freshness")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def importance(self) -> typing.Optional[jsii.Number]:
            '''The relative importance of the field in the search.

            Larger numbers provide more of a boost than smaller numbers.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-importance
            '''
            result = self._values.get("importance")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rank_order(self) -> typing.Optional[builtins.str]:
            '''Determines how values should be interpreted.

            When the ``RankOrder`` field is ``ASCENDING`` , higher numbers are better. For example, a document with a rating score of 10 is higher ranking than a document with a rating score of 1.

            When the ``RankOrder`` field is ``DESCENDING`` , lower numbers are better. For example, in a task tracking application, a priority 1 task is more important than a priority 5 task.

            Only applies to ``LONG`` and ``DOUBLE`` fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-rankorder
            '''
            result = self._values.get("rank_order")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_importance_items(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnIndex.ValueImportanceItemProperty", _IResolvable_da3f097b]]]]:
            '''An array of key-value pairs for different boosts when they appear in the search result list.

            For example, if you want to boost query terms that match the "department" field in the result, query terms that match this field are boosted in the result. You can add entries from the department field to boost documents with those values higher.

            For example, you can add entries to the map with names of departments. If you add "HR", 5 and "Legal",3 those departments are given special attention when they appear in the metadata of a document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-relevance.html#cfn-kendra-index-relevance-valueimportanceitems
            '''
            result = self._values.get("value_importance_items")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union["CfnIndex.ValueImportanceItemProperty", _IResolvable_da3f097b]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelevanceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.SearchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "displayable": "displayable",
            "facetable": "facetable",
            "searchable": "searchable",
            "sortable": "sortable",
        },
    )
    class SearchProperty:
        def __init__(
            self,
            *,
            displayable: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            facetable: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            searchable: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
            sortable: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides information about how a custom index field is used during a search.

            :param displayable: Determines whether the field is returned in the query response. The default is ``true`` .
            :param facetable: Indicates that the field can be used to create search facets, a count of results for each value in the field. The default is ``false`` .
            :param searchable: Determines whether the field is used in the search. If the ``Searchable`` field is ``true`` , you can use relevance tuning to manually tune how Amazon Kendra weights the field in the search. The default is ``true`` for string fields and ``false`` for number and date fields.
            :param sortable: Determines whether the field can be used to sort the results of a query. The default is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                search_property = kendra.CfnIndex.SearchProperty(
                    displayable=False,
                    facetable=False,
                    searchable=False,
                    sortable=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__43cf272f8362f07ccde026d4fb84d61b3747c6294923bb808e55f430dea22286)
                check_type(argname="argument displayable", value=displayable, expected_type=type_hints["displayable"])
                check_type(argname="argument facetable", value=facetable, expected_type=type_hints["facetable"])
                check_type(argname="argument searchable", value=searchable, expected_type=type_hints["searchable"])
                check_type(argname="argument sortable", value=sortable, expected_type=type_hints["sortable"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if displayable is not None:
                self._values["displayable"] = displayable
            if facetable is not None:
                self._values["facetable"] = facetable
            if searchable is not None:
                self._values["searchable"] = searchable
            if sortable is not None:
                self._values["sortable"] = sortable

        @builtins.property
        def displayable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''Determines whether the field is returned in the query response.

            The default is ``true`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html#cfn-kendra-index-search-displayable
            '''
            result = self._values.get("displayable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def facetable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''Indicates that the field can be used to create search facets, a count of results for each value in the field.

            The default is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html#cfn-kendra-index-search-facetable
            '''
            result = self._values.get("facetable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def searchable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''Determines whether the field is used in the search.

            If the ``Searchable`` field is ``true`` , you can use relevance tuning to manually tune how Amazon Kendra weights the field in the search. The default is ``true`` for string fields and ``false`` for number and date fields.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html#cfn-kendra-index-search-searchable
            '''
            result = self._values.get("searchable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        @builtins.property
        def sortable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]]:
            '''Determines whether the field can be used to sort the results of a query.

            The default is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-search.html#cfn-kendra-index-search-sortable
            '''
            result = self._values.get("sortable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SearchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''Provides the identifier of the AWS KMS customer master key (CMK) used to encrypt data indexed by Amazon Kendra.

            We suggest that you use a CMK from your account to help secure your index. Amazon Kendra doesn't support asymmetric CMKs.

            :param kms_key_id: The identifier of the AWS KMS key . Amazon Kendra doesn't support asymmetric keys.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-serversideencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                server_side_encryption_configuration_property = kendra.CfnIndex.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1e65adc615a3165ea9df85263340bfc45b9d851a47b778bd575d7c3b182639fa)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the AWS KMS key .

            Amazon Kendra doesn't support asymmetric keys.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-serversideencryptionconfiguration.html#cfn-kendra-index-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.UserTokenConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "json_token_type_configuration": "jsonTokenTypeConfiguration",
            "jwt_token_type_configuration": "jwtTokenTypeConfiguration",
        },
    )
    class UserTokenConfigurationProperty:
        def __init__(
            self,
            *,
            json_token_type_configuration: typing.Optional[typing.Union[typing.Union["CfnIndex.JsonTokenTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
            jwt_token_type_configuration: typing.Optional[typing.Union[typing.Union["CfnIndex.JwtTokenTypeConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        ) -> None:
            '''Provides the configuration information for a token.

            :param json_token_type_configuration: Information about the JSON token type configuration.
            :param jwt_token_type_configuration: Information about the JWT token type configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-usertokenconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                user_token_configuration_property = kendra.CfnIndex.UserTokenConfigurationProperty(
                    json_token_type_configuration=kendra.CfnIndex.JsonTokenTypeConfigurationProperty(
                        group_attribute_field="groupAttributeField",
                        user_name_attribute_field="userNameAttributeField"
                    ),
                    jwt_token_type_configuration=kendra.CfnIndex.JwtTokenTypeConfigurationProperty(
                        key_location="keyLocation",
                
                        # the properties below are optional
                        claim_regex="claimRegex",
                        group_attribute_field="groupAttributeField",
                        issuer="issuer",
                        secret_manager_arn="secretManagerArn",
                        url="url",
                        user_name_attribute_field="userNameAttributeField"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ef78732addd3b4dd02390dfc030b58c287a70690d2bae50aa573b05c819715b)
                check_type(argname="argument json_token_type_configuration", value=json_token_type_configuration, expected_type=type_hints["json_token_type_configuration"])
                check_type(argname="argument jwt_token_type_configuration", value=jwt_token_type_configuration, expected_type=type_hints["jwt_token_type_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if json_token_type_configuration is not None:
                self._values["json_token_type_configuration"] = json_token_type_configuration
            if jwt_token_type_configuration is not None:
                self._values["jwt_token_type_configuration"] = jwt_token_type_configuration

        @builtins.property
        def json_token_type_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnIndex.JsonTokenTypeConfigurationProperty", _IResolvable_da3f097b]]:
            '''Information about the JSON token type configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-usertokenconfiguration.html#cfn-kendra-index-usertokenconfiguration-jsontokentypeconfiguration
            '''
            result = self._values.get("json_token_type_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnIndex.JsonTokenTypeConfigurationProperty", _IResolvable_da3f097b]], result)

        @builtins.property
        def jwt_token_type_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnIndex.JwtTokenTypeConfigurationProperty", _IResolvable_da3f097b]]:
            '''Information about the JWT token type configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-usertokenconfiguration.html#cfn-kendra-index-usertokenconfiguration-jwttokentypeconfiguration
            '''
            result = self._values.get("jwt_token_type_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnIndex.JwtTokenTypeConfigurationProperty", _IResolvable_da3f097b]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserTokenConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_kendra.CfnIndex.ValueImportanceItemProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ValueImportanceItemProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies a key-value pair of the search boost value for a document when the key is part of the metadata of a document.

            :param key: The document metadata value used for the search boost.
            :param value: The boost value for a document when the key is part of the metadata of a document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-valueimportanceitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_kendra as kendra
                
                value_importance_item_property = kendra.CfnIndex.ValueImportanceItemProperty(
                    key="key",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__062de87b3e323244109a14768e5e37dc72be812535477b570bfaaad659cf4d85)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The document metadata value used for the search boost.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-valueimportanceitem.html#cfn-kendra-index-valueimportanceitem-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The boost value for a document when the key is part of the metadata of a document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kendra-index-valueimportanceitem.html#cfn-kendra-index-valueimportanceitem-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValueImportanceItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_kendra.CfnIndexProps",
    jsii_struct_bases=[],
    name_mapping={
        "edition": "edition",
        "name": "name",
        "role_arn": "roleArn",
        "capacity_units": "capacityUnits",
        "description": "description",
        "document_metadata_configurations": "documentMetadataConfigurations",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "tags": "tags",
        "user_context_policy": "userContextPolicy",
        "user_token_configurations": "userTokenConfigurations",
    },
)
class CfnIndexProps:
    def __init__(
        self,
        *,
        edition: builtins.str,
        name: builtins.str,
        role_arn: builtins.str,
        capacity_units: typing.Optional[typing.Union[typing.Union[CfnIndex.CapacityUnitsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        description: typing.Optional[builtins.str] = None,
        document_metadata_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnIndex.DocumentMetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[typing.Union[CfnIndex.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_context_policy: typing.Optional[builtins.str] = None,
        user_token_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnIndex.UserTokenConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnIndex``.

        :param edition: Indicates whether the index is a Enterprise Edition index or a Developer Edition index. Valid values are ``DEVELOPER_EDITION`` and ``ENTERPRISE_EDITION`` .
        :param name: The name of the index.
        :param role_arn: An IAM role that gives Amazon Kendra permissions to access your Amazon CloudWatch logs and metrics. This is also the role used when you use the `BatchPutDocument <https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html>`_ operation to index documents from an Amazon S3 bucket.
        :param capacity_units: ``AWS::Kendra::Index.CapacityUnits``.
        :param description: A description for the index.
        :param document_metadata_configurations: Specifies the properties of an index field. You can add either a custom or a built-in field. You can add and remove built-in fields at any time. When a built-in field is removed it's configuration reverts to the default for the field. Custom fields can't be removed from an index after they are added.
        :param server_side_encryption_configuration: The identifier of the AWS KMS customer managed key (CMK) to use to encrypt data indexed by Amazon Kendra. Amazon Kendra doesn't support asymmetric CMKs.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param user_context_policy: The user context policy. ATTRIBUTE_FILTER - All indexed content is searchable and displayable for all users. If you want to filter search results on user context, you can use the attribute filters of ``_user_id`` and ``_group_ids`` or you can provide user and group information in ``UserContext`` . USER_TOKEN - Enables token-based user access control to filter search results on user context. All documents with no access control and all documents accessible to the user will be searchable and displayable.
        :param user_token_configurations: Defines the type of user token used for the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_kendra as kendra
            
            cfn_index_props = kendra.CfnIndexProps(
                edition="edition",
                name="name",
                role_arn="roleArn",
            
                # the properties below are optional
                capacity_units=kendra.CfnIndex.CapacityUnitsConfigurationProperty(
                    query_capacity_units=123,
                    storage_capacity_units=123
                ),
                description="description",
                document_metadata_configurations=[kendra.CfnIndex.DocumentMetadataConfigurationProperty(
                    name="name",
                    type="type",
            
                    # the properties below are optional
                    relevance=kendra.CfnIndex.RelevanceProperty(
                        duration="duration",
                        freshness=False,
                        importance=123,
                        rank_order="rankOrder",
                        value_importance_items=[kendra.CfnIndex.ValueImportanceItemProperty(
                            key="key",
                            value=123
                        )]
                    ),
                    search=kendra.CfnIndex.SearchProperty(
                        displayable=False,
                        facetable=False,
                        searchable=False,
                        sortable=False
                    )
                )],
                server_side_encryption_configuration=kendra.CfnIndex.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_context_policy="userContextPolicy",
                user_token_configurations=[kendra.CfnIndex.UserTokenConfigurationProperty(
                    json_token_type_configuration=kendra.CfnIndex.JsonTokenTypeConfigurationProperty(
                        group_attribute_field="groupAttributeField",
                        user_name_attribute_field="userNameAttributeField"
                    ),
                    jwt_token_type_configuration=kendra.CfnIndex.JwtTokenTypeConfigurationProperty(
                        key_location="keyLocation",
            
                        # the properties below are optional
                        claim_regex="claimRegex",
                        group_attribute_field="groupAttributeField",
                        issuer="issuer",
                        secret_manager_arn="secretManagerArn",
                        url="url",
                        user_name_attribute_field="userNameAttributeField"
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ce90bfc8458d52938a1a8558591d2e8ee975572889b24651808cc701715add3)
            check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument capacity_units", value=capacity_units, expected_type=type_hints["capacity_units"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument document_metadata_configurations", value=document_metadata_configurations, expected_type=type_hints["document_metadata_configurations"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_context_policy", value=user_context_policy, expected_type=type_hints["user_context_policy"])
            check_type(argname="argument user_token_configurations", value=user_token_configurations, expected_type=type_hints["user_token_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edition": edition,
            "name": name,
            "role_arn": role_arn,
        }
        if capacity_units is not None:
            self._values["capacity_units"] = capacity_units
        if description is not None:
            self._values["description"] = description
        if document_metadata_configurations is not None:
            self._values["document_metadata_configurations"] = document_metadata_configurations
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if tags is not None:
            self._values["tags"] = tags
        if user_context_policy is not None:
            self._values["user_context_policy"] = user_context_policy
        if user_token_configurations is not None:
            self._values["user_token_configurations"] = user_token_configurations

    @builtins.property
    def edition(self) -> builtins.str:
        '''Indicates whether the index is a Enterprise Edition index or a Developer Edition index.

        Valid values are ``DEVELOPER_EDITION`` and ``ENTERPRISE_EDITION`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-edition
        '''
        result = self._values.get("edition")
        assert result is not None, "Required property 'edition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''An IAM role that gives Amazon Kendra permissions to access your Amazon CloudWatch logs and metrics.

        This is also the role used when you use the `BatchPutDocument <https://docs.aws.amazon.com/kendra/latest/dg/BatchPutDocument.html>`_ operation to index documents from an Amazon S3 bucket.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_units(
        self,
    ) -> typing.Optional[typing.Union[CfnIndex.CapacityUnitsConfigurationProperty, _IResolvable_da3f097b]]:
        '''``AWS::Kendra::Index.CapacityUnits``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-capacityunits
        '''
        result = self._values.get("capacity_units")
        return typing.cast(typing.Optional[typing.Union[CfnIndex.CapacityUnitsConfigurationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document_metadata_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnIndex.DocumentMetadataConfigurationProperty, _IResolvable_da3f097b]]]]:
        '''Specifies the properties of an index field.

        You can add either a custom or a built-in field. You can add and remove built-in fields at any time. When a built-in field is removed it's configuration reverts to the default for the field. Custom fields can't be removed from an index after they are added.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-documentmetadataconfigurations
        '''
        result = self._values.get("document_metadata_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnIndex.DocumentMetadataConfigurationProperty, _IResolvable_da3f097b]]]], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnIndex.ServerSideEncryptionConfigurationProperty, _IResolvable_da3f097b]]:
        '''The identifier of the AWS KMS customer managed key (CMK) to use to encrypt data indexed by Amazon Kendra.

        Amazon Kendra doesn't support asymmetric CMKs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnIndex.ServerSideEncryptionConfigurationProperty, _IResolvable_da3f097b]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_f6864754]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_f6864754]], result)

    @builtins.property
    def user_context_policy(self) -> typing.Optional[builtins.str]:
        '''The user context policy.

        ATTRIBUTE_FILTER

        - All indexed content is searchable and displayable for all users. If you want to filter search results on user context, you can use the attribute filters of ``_user_id`` and ``_group_ids`` or you can provide user and group information in ``UserContext`` .

        USER_TOKEN

        - Enables token-based user access control to filter search results on user context. All documents with no access control and all documents accessible to the user will be searchable and displayable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-usercontextpolicy
        '''
        result = self._values.get("user_context_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_token_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnIndex.UserTokenConfigurationProperty, _IResolvable_da3f097b]]]]:
        '''Defines the type of user token used for the index.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kendra-index.html#cfn-kendra-index-usertokenconfigurations
        '''
        result = self._values.get("user_token_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnIndex.UserTokenConfigurationProperty, _IResolvable_da3f097b]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDataSource",
    "CfnDataSourceProps",
    "CfnFaq",
    "CfnFaqProps",
    "CfnIndex",
    "CfnIndexProps",
]

publication.publish()

def _typecheckingstub__db7b870c602f215572ec4f7667cd46c2ae4e2c6035e16924c08cf6d68dc1e858(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    index_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    custom_document_enrichment_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.CustomDocumentEnrichmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    data_source_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    description: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__857c3d47368883ad30477d4c7721d4f448bafe37d7457ab7e8fa7ab0c70e6c2a(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4df69e7835817b60bff4c27a777904898be17518f1553fa5fd56e28c646990(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da518cc177b71ad2703234f2e02607e32d9ae04f8b106e8ef880eda822ebfbc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727aa22774141fa3563f0859859874f94f89dcfafca54202ef16cd4039fae247(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ff38538f8b7b5ad592fb8de907503bd940ef472178a94ea71872c5e0e52e36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13b151417bd0a802a711d66b55ba6494eed4691c8ad5b5af2f894a431892d5fb(
    value: typing.Optional[typing.Union[CfnDataSource.CustomDocumentEnrichmentConfigurationProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea79eed634a5ae09c1e689638d3ede50cbd8c33dae75c020cff75930d087664e(
    value: typing.Optional[typing.Union[CfnDataSource.DataSourceConfigurationProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3fe842db3dcb4fce0cdde73f8c5e1e2a0746c534ecd6c08bed0359e2beefe7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf11b1fe015a07a79a94cab233a319e551a36b06278e679c1bf6a049d269c0ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646a3352fddea09391f6d6bab4d6fa7a13f4b27c607bb5778a4fb3b77c8850b1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75a85e279b4b8eeb32b079b870a3a505c72193be98cbf8a512ba78fb2c7edaf(
    *,
    key_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49de6c4a08f15d0f081e52ec45a2bc4ccf3f2d2b5dd047fdd170d597181f21b2(
    *,
    allowed_groups_column_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cfb41c0445e5b29959324b1ac11eef70234922023e3fca11ee3192079da9e5c(
    *,
    change_detecting_columns: typing.Sequence[builtins.str],
    document_data_column_name: builtins.str,
    document_id_column_name: builtins.str,
    document_title_column_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6cfb9bb5093bde33f429779799db80d83d5393cdfc89e20b3430270efbe1e5(
    *,
    attachment_field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.ConfluenceAttachmentToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__529bdb052ea312464a1abde7c9704238bd18f7b0dd291c002a95313af6956988(
    *,
    data_source_field_name: builtins.str,
    index_field_name: builtins.str,
    date_field_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a264b7f2ddc83b3c490f89e320f16d205c5edb37049b498464df2b9eb674f1(
    *,
    blog_field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.ConfluenceBlogToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48a1e22fe3cbe861fbcbb273e85a7b63fd46b8626479abb9f9eb183a662b101f(
    *,
    data_source_field_name: builtins.str,
    index_field_name: builtins.str,
    date_field_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fc73a495264eef013dab776a4e7c3b95e5d3a9ae1ca4f62716fbbf86103e685(
    *,
    secret_arn: builtins.str,
    server_url: builtins.str,
    version: builtins.str,
    attachment_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ConfluenceAttachmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    blog_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ConfluenceBlogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    page_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ConfluencePageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    space_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ConfluenceSpaceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    vpc_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.DataSourceVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067682c93bcdb09a9f476748f97c89f1397c33c7f36fd58bb32a166d78fb3ce4(
    *,
    page_field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.ConfluencePageToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02db3b1eb2295ad6b3ca31a8a741242f9a81c7568d7e1cdd398ad8df1941bf58(
    *,
    data_source_field_name: builtins.str,
    index_field_name: builtins.str,
    date_field_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40a78d184b37483bcef61e3c4870f87360262d1fd7a7621e6a3a1ef3a7888c2(
    *,
    crawl_archived_spaces: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    crawl_personal_spaces: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    exclude_spaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_spaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    space_field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.ConfluenceSpaceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0000b03ae40dd75637e6d7b6c78c5df60c30c415f5ceda4611012d456c139d0(
    *,
    data_source_field_name: builtins.str,
    index_field_name: builtins.str,
    date_field_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__010dd9b2b9a8c77bfe2d4ed8e974fc62d5bb8091dd9fbf486410bd89c29b52f8(
    *,
    database_host: builtins.str,
    database_name: builtins.str,
    database_port: jsii.Number,
    secret_arn: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4048e2fee9d6603c2251b77fb03f4d3bb19fa55563651003cac3f2513230697f(
    *,
    inline_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.InlineCustomDocumentEnrichmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    post_extraction_hook_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.HookConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    pre_extraction_hook_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.HookConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f9c312cf9cd7088a9eba0183b5f0bf4960a0c56630a30d0a7208794a6863f3(
    *,
    confluence_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ConfluenceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    database_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.DatabaseConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    google_drive_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.GoogleDriveConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    one_drive_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.OneDriveConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    s3_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.S3DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    salesforce_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.SalesforceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    service_now_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ServiceNowConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    share_point_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.SharePointConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    web_crawler_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.WebCrawlerConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    work_docs_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.WorkDocsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8208bd51030836955a10bbcba314957eac24c0ca6dae40b87bfb3b46ccc25db5(
    *,
    data_source_field_name: builtins.str,
    index_field_name: builtins.str,
    date_field_format: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a29196b7634080fa4eab0118a19b31a589c1e30145e12231546ff92e046bd0(
    *,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5428173a27262b90e5499e20bdad87f915015d24730fdc55d29ea42f98f783f9(
    *,
    column_configuration: typing.Union[typing.Union[CfnDataSource.ColumnConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    connection_configuration: typing.Union[typing.Union[CfnDataSource.ConnectionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    database_engine_type: builtins.str,
    acl_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.AclConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    sql_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.SqlConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    vpc_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.DataSourceVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3be9f331fb30fc1120b64fb67b31c482fab661057041712cb9b0aa689b0c477(
    *,
    condition_document_attribute_key: builtins.str,
    operator: builtins.str,
    condition_on_value: typing.Optional[typing.Union[typing.Union[CfnDataSource.DocumentAttributeValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3693fd552c97d013bc352a51fe708bffae6e362b87808be7aee9daf036f228f5(
    *,
    target_document_attribute_key: builtins.str,
    target_document_attribute_value: typing.Optional[typing.Union[typing.Union[CfnDataSource.DocumentAttributeValueProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    target_document_attribute_value_deletion: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6664394a01ef732c5ed7f23d9d64a2dd01e3979fcbd6c750a603aa225b728522(
    *,
    date_value: typing.Optional[builtins.str] = None,
    long_value: typing.Optional[jsii.Number] = None,
    string_list_value: typing.Optional[typing.Sequence[builtins.str]] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63838fe65353180f3dde04339d577dd6cef52eeb9c6cb95bdd18eabb89519089(
    *,
    s3_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c923274fb398190dddefca2aff2f3ac3a6a978b70c7d65bb404d600266d9b1fc(
    *,
    secret_arn: builtins.str,
    exclude_mime_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_shared_drives: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclude_user_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b34e4d4b505681b8da4219b35bde24bf8a24d5dbe80f37f1c166073c9cbfd1(
    *,
    lambda_arn: builtins.str,
    s3_bucket: builtins.str,
    invocation_condition: typing.Optional[typing.Union[typing.Union[CfnDataSource.DocumentAttributeConditionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b4fdb9078ccf6b1abef814c1fa86146c3c7faee58757787d7e3ccd0de3b5eb(
    *,
    condition: typing.Optional[typing.Union[typing.Union[CfnDataSource.DocumentAttributeConditionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    document_content_deletion: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    target: typing.Optional[typing.Union[typing.Union[CfnDataSource.DocumentAttributeTargetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695d703d8c0b001be62c56ad50f3f4af915709c1284c26e428bfb6be0244d2ee(
    *,
    one_drive_users: typing.Union[typing.Union[CfnDataSource.OneDriveUsersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    secret_arn: builtins.str,
    tenant_domain: builtins.str,
    disable_local_groups: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b04aeb33b4fb722bc28444a3f3940da82f4017481948bf35f98659f0beb957(
    *,
    one_drive_user_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    one_drive_user_s3_path: typing.Optional[typing.Union[typing.Union[CfnDataSource.S3PathProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f669b52413aa28c0992bb60e68a3c50446a0d55409ec1ac95e949617563ad8(
    *,
    host: builtins.str,
    port: jsii.Number,
    credentials: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f41f6acb59e7453a4f264b5ea7dbe69a5cb3e25cbafd939a140f294a596121a(
    *,
    bucket_name: builtins.str,
    access_control_list_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.AccessControlListConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    documents_metadata_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.DocumentsMetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b4797593ba73adebab81646e1462689b8c7372f077d548f405b2bb475d02f9f(
    *,
    bucket: builtins.str,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6483dd014a4f5b7c359695864d6e8e429fff879adca08f318e87dc0a92a743(
    *,
    document_data_field_name: builtins.str,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    include_filter_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3f13b2ba7bea487e478e44d5d01f374af605ea8a37637189ddbfa2bada9ef3(
    *,
    secret_arn: builtins.str,
    server_url: builtins.str,
    chatter_feed_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.SalesforceChatterFeedConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    knowledge_article_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.SalesforceKnowledgeArticleConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    standard_object_attachment_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.SalesforceStandardObjectAttachmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    standard_object_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.SalesforceStandardObjectConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e689bb017a19a170b0a1a7f34277387cff6153267437b9bd2f64824f0a8fd6a(
    *,
    document_data_field_name: builtins.str,
    name: builtins.str,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d2256d2f21288201eab3a954f64ece169e7a95f3fb70d3ee8ca96627a377f6(
    *,
    included_states: typing.Sequence[builtins.str],
    custom_knowledge_article_type_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.SalesforceCustomKnowledgeArticleTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    standard_knowledge_article_type_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.SalesforceStandardKnowledgeArticleTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673113eebb1356ad8c49cba55bd0e063fede0e7da2dcadf3ade5650b7f4b2d0d(
    *,
    document_data_field_name: builtins.str,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7848e521c99f09cfcc736d593496d3342430c7a37a152f50ab8cb5d4a73b100(
    *,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258f4f94facbd694e75c4e33c31082f6986db4b3015b0e86ec9210f0a2da544a(
    *,
    document_data_field_name: builtins.str,
    name: builtins.str,
    document_title_field_name: typing.Optional[builtins.str] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6b2188dd486f22e5e5c83bbe485e54c8f2890629800d6adf78242466273d50(
    *,
    host_url: builtins.str,
    secret_arn: builtins.str,
    service_now_build_version: builtins.str,
    authentication_type: typing.Optional[builtins.str] = None,
    knowledge_article_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ServiceNowKnowledgeArticleConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    service_catalog_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ServiceNowServiceCatalogConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced55b5dbc1895241f7179622dbcc184de664555043b2f78674509174c9bda1d(
    *,
    document_data_field_name: builtins.str,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    filter_query: typing.Optional[builtins.str] = None,
    include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73feebbd1e46487ffa1b46b0644d23b18756aaeeb319992b0f2f62ba081b975d(
    *,
    document_data_field_name: builtins.str,
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    exclude_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    include_attachment_file_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90fb1a0d84aaf9de16cb7f8f2186dfcef612e5416777877db5790d0e7925997(
    *,
    secret_arn: builtins.str,
    share_point_version: builtins.str,
    urls: typing.Sequence[builtins.str],
    crawl_attachments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    disable_local_groups: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    document_title_field_name: typing.Optional[builtins.str] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssl_certificate_s3_path: typing.Optional[typing.Union[typing.Union[CfnDataSource.S3PathProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    use_change_log: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    vpc_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.DataSourceVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9058d8c99c505df3ace590b735e22ffca36be7920e96abbe2049836b6e0a93f1(
    *,
    query_identifiers_enclosing_option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78dcdcac178c8a64cb2a657a51649bac6d70ac8b2c0e4bc1b93bd0d4daabf383(
    *,
    basic_authentication: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.WebCrawlerBasicAuthenticationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff4b862a7ea02f0fb1b4bcbb9f7770d415fb18ebebd2dfa6134f78f04cad9a8(
    *,
    credentials: builtins.str,
    host: builtins.str,
    port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c76bcf4dccdbef664e3afaa154bc20afb0b322dd0a2e57fd1d5a36d14747ac(
    *,
    urls: typing.Union[typing.Union[CfnDataSource.WebCrawlerUrlsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    authentication_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.WebCrawlerAuthenticationConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    crawl_depth: typing.Optional[jsii.Number] = None,
    max_content_size_per_page_in_mega_bytes: typing.Optional[jsii.Number] = None,
    max_links_per_page: typing.Optional[jsii.Number] = None,
    max_urls_per_minute_crawl_rate: typing.Optional[jsii.Number] = None,
    proxy_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.ProxyConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    url_exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    url_inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba5c0e84e98f69ec08d299dd403c87e60f8a2ec725d88ba034022f6dddd20c0(
    *,
    seed_urls: typing.Sequence[builtins.str],
    web_crawler_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f9026e7358b434f219fc3e9bf3da50ec0a37eb8f00e193fa38cf66badfbde60(
    *,
    site_maps: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c90a23eeef0a23af52df460253f647effa981018e94e02c7b7f710d72f9d3ee(
    *,
    seed_url_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.WebCrawlerSeedUrlConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    site_maps_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.WebCrawlerSiteMapsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c81f941a7e6027762047ba2a4dca2a80cd0266333586cd6278af4d285b4e5623(
    *,
    organization_id: builtins.str,
    crawl_comments: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    exclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_mappings: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnDataSource.DataSourceToIndexFieldMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    inclusion_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    use_change_log: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9542f7b6e1451dc9177bf24b7be378edc74ce522d3fa3c567f3674a5f145a654(
    *,
    index_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    custom_document_enrichment_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.CustomDocumentEnrichmentConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    data_source_configuration: typing.Optional[typing.Union[typing.Union[CfnDataSource.DataSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    description: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da52634bf448f13a8dfdf111b1193f46a241ac941af460a15585386c0620fb57(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    index_id: builtins.str,
    name: builtins.str,
    role_arn: builtins.str,
    s3_path: typing.Union[typing.Union[CfnFaq.S3PathProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    description: typing.Optional[builtins.str] = None,
    file_format: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11ca22cd6dac6125f6c23af39c883b9555dc5ca8feff5890bbf847c4d2ec1afa(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3be9b6ec7b4902d9ec2eb28db705482668d74fecb5632459047a1859f7b8270(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f1e70154142736744f66230e1c5b07df97f4a652446db44168d67c14beeea5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b594acf6aecd343c9db04631030ca07304c2847b8ee62acf9027423dcc196ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef4a3a137a43525f6d969da0db69ab6343d8d1b2954c1e827bc8a9161cefbf0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1806afef94a938b4b58ebc0c38dcb5cddd53c1cee6e9ac50febc0bea90c9290(
    value: typing.Union[CfnFaq.S3PathProperty, _IResolvable_da3f097b],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6fdcd3bb79f5f910c29a7243dd6f733e9edf684e556ed8d65538ed6d320d77(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c1da4741f70f3470f4ba1da7528d2bd5f61244bea5440442acec296bbd15b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c660660356fbb032dd86a92e34819e3494aa7fd2f3187fca1481c4c3aba2a3d(
    *,
    bucket: builtins.str,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d80eed0b304b1e2dc88b2a6b3ac2392e3650ef0ac292928d043232bd3fae1be(
    *,
    index_id: builtins.str,
    name: builtins.str,
    role_arn: builtins.str,
    s3_path: typing.Union[typing.Union[CfnFaq.S3PathProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b],
    description: typing.Optional[builtins.str] = None,
    file_format: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1204970a88ec523311382503badf4dde293efe7a39dfb0456e1240724565fb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    edition: builtins.str,
    name: builtins.str,
    role_arn: builtins.str,
    capacity_units: typing.Optional[typing.Union[typing.Union[CfnIndex.CapacityUnitsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    description: typing.Optional[builtins.str] = None,
    document_metadata_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnIndex.DocumentMetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[typing.Union[CfnIndex.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_context_policy: typing.Optional[builtins.str] = None,
    user_token_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnIndex.UserTokenConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540517a32fdcfcd298c87cf94ee56816edf19e0499b0f6948fee9fd23be529c6(
    inspector: _TreeInspector_488e0dd5,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2df7cdccb6eab5e36f563831c237ba0ca6d01e47278e44ac46624c34c5638bc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c93239f3ae00e7cb944fd204cb022d7f5be68421fd79c69ed3f2763a51080330(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8dbceb731e5a625527a5cc01b7c46b54b6616680debfa96e2ab053da367d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8a890b398c997757af70a90887f07071ac0aff33283747ecb57cfbc966ef073(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf6edadfe64bf9cc89fb346617e7ebf299db00a7377538a0131f98173bfe1b5(
    value: typing.Optional[typing.Union[CfnIndex.CapacityUnitsConfigurationProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d78a23badee4ab3e1d5d8e4a54eeed850580bfffd42919232175a85362394b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6a2782afe74760aa4cd4a1e2c5389ae5d499b8e0b17c4f53326aba33c6a5ca(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnIndex.DocumentMetadataConfigurationProperty, _IResolvable_da3f097b]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754853a1d856877c480ad0c2d5930ca3be45133cf17bdd2a002ec2af3d8c119d(
    value: typing.Optional[typing.Union[CfnIndex.ServerSideEncryptionConfigurationProperty, _IResolvable_da3f097b]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d813d698c8f17a6cd67584d63c8e7266087d6fa57cd89671e115048ddbfc3b6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10cbdc54cc7ee0bf166d3e99163425e74855a9b539e601a9526126b7ad7f7b58(
    value: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.List[typing.Union[CfnIndex.UserTokenConfigurationProperty, _IResolvable_da3f097b]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7093c6b5e24a07c3c1a63e9139dde660572cc52116b64be9037e4edd6c4f67be(
    *,
    query_capacity_units: jsii.Number,
    storage_capacity_units: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954dc04a56ef56fb898ce0f8582ed0990c0c46f17f7ca3f08d5016d39e3a463b(
    *,
    name: builtins.str,
    type: builtins.str,
    relevance: typing.Optional[typing.Union[typing.Union[CfnIndex.RelevanceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    search: typing.Optional[typing.Union[typing.Union[CfnIndex.SearchProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b8eb1909b62eab07efe488db208c9ecfe34acafbbeee38e4dea0fad0039e6d(
    *,
    group_attribute_field: builtins.str,
    user_name_attribute_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643b3a2d709ad83dacc588a4aab7261225afdbf6c921738c4c323a1ee1ee5d21(
    *,
    key_location: builtins.str,
    claim_regex: typing.Optional[builtins.str] = None,
    group_attribute_field: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    secret_manager_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    user_name_attribute_field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1accd841c4b5dd7504783ed3b5520e16e41f7c6efae6c85c12403238ea4d749(
    *,
    duration: typing.Optional[builtins.str] = None,
    freshness: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    importance: typing.Optional[jsii.Number] = None,
    rank_order: typing.Optional[builtins.str] = None,
    value_importance_items: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnIndex.ValueImportanceItemProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43cf272f8362f07ccde026d4fb84d61b3747c6294923bb808e55f430dea22286(
    *,
    displayable: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    facetable: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    searchable: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
    sortable: typing.Optional[typing.Union[builtins.bool, _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e65adc615a3165ea9df85263340bfc45b9d851a47b778bd575d7c3b182639fa(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef78732addd3b4dd02390dfc030b58c287a70690d2bae50aa573b05c819715b(
    *,
    json_token_type_configuration: typing.Optional[typing.Union[typing.Union[CfnIndex.JsonTokenTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    jwt_token_type_configuration: typing.Optional[typing.Union[typing.Union[CfnIndex.JwtTokenTypeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062de87b3e323244109a14768e5e37dc72be812535477b570bfaaad659cf4d85(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ce90bfc8458d52938a1a8558591d2e8ee975572889b24651808cc701715add3(
    *,
    edition: builtins.str,
    name: builtins.str,
    role_arn: builtins.str,
    capacity_units: typing.Optional[typing.Union[typing.Union[CfnIndex.CapacityUnitsConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    description: typing.Optional[builtins.str] = None,
    document_metadata_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnIndex.DocumentMetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[typing.Union[CfnIndex.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_f6864754, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_context_policy: typing.Optional[builtins.str] = None,
    user_token_configurations: typing.Optional[typing.Union[_IResolvable_da3f097b, typing.Sequence[typing.Union[typing.Union[CfnIndex.UserTokenConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_da3f097b]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
