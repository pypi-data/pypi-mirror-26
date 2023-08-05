# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from .resource import Resource


class OperationalizationCluster(Resource):
    """Instance of an Azure ML Operationalization Cluster resource.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: Specifies the resource ID.
    :vartype id: str
    :ivar name: Specifies the name of the resource.
    :vartype name: str
    :param location: Specifies the location of the resource.
    :type location: str
    :ivar type: Specifies the type of the resource.
    :vartype type: str
    :param tags: Contains resource tags defined as key/value pairs.
    :type tags: dict
    :param description: The description of the cluster.
    :type description: str
    :ivar created_on: The date and time when the cluster was created.
    :vartype created_on: datetime
    :ivar modified_on: The date and time when the cluster was last modified.
    :vartype modified_on: datetime
    :ivar provisioning_state: The provision state of the cluster. Valid values
     are Unknown, Updating, Provisioning, Succeeded, and Failed. Possible
     values include: 'Unknown', 'Updating', 'Creating', 'Deleting',
     'Succeeded', 'Failed', 'Canceled'
    :vartype provisioning_state: str or :class:`OperationStatus
     <azure.mgmt.machinelearningcompute.models.OperationStatus>`
    :ivar provisioning_errors: List of provisioning errors reported by the
     resource provider.
    :vartype provisioning_errors: list of :class:`ErrorResponseWrapper
     <azure.mgmt.machinelearningcompute.models.ErrorResponseWrapper>`
    :param cluster_type: The cluster type. Possible values include: 'ACS',
     'Local'
    :type cluster_type: str or :class:`ClusterType
     <azure.mgmt.machinelearningcompute.models.ClusterType>`
    :param storage_account: Storage Account properties.
    :type storage_account: :class:`StorageAccountProperties
     <azure.mgmt.machinelearningcompute.models.StorageAccountProperties>`
    :param container_registry: Container Registry properties.
    :type container_registry: :class:`ContainerRegistryProperties
     <azure.mgmt.machinelearningcompute.models.ContainerRegistryProperties>`
    :param container_service: Parameters for the Azure Container Service
     cluster.
    :type container_service: :class:`AcsClusterProperties
     <azure.mgmt.machinelearningcompute.models.AcsClusterProperties>`
    :param app_insights: AppInsights configuration.
    :type app_insights: :class:`AppInsightsProperties
     <azure.mgmt.machinelearningcompute.models.AppInsightsProperties>`
    :param global_service_configuration: Contains global configuration for the
     web services in the cluster.
    :type global_service_configuration: :class:`GlobalServiceConfiguration
     <azure.mgmt.machinelearningcompute.models.GlobalServiceConfiguration>`
    """

    _validation = {
        'id': {'readonly': True},
        'name': {'readonly': True},
        'location': {'required': True},
        'type': {'readonly': True},
        'created_on': {'readonly': True},
        'modified_on': {'readonly': True},
        'provisioning_state': {'readonly': True},
        'provisioning_errors': {'readonly': True},
        'cluster_type': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'description': {'key': 'properties.description', 'type': 'str'},
        'created_on': {'key': 'properties.createdOn', 'type': 'iso-8601'},
        'modified_on': {'key': 'properties.modifiedOn', 'type': 'iso-8601'},
        'provisioning_state': {'key': 'properties.provisioningState', 'type': 'str'},
        'provisioning_errors': {'key': 'properties.provisioningErrors', 'type': '[ErrorResponseWrapper]'},
        'cluster_type': {'key': 'properties.clusterType', 'type': 'str'},
        'storage_account': {'key': 'properties.storageAccount', 'type': 'StorageAccountProperties'},
        'container_registry': {'key': 'properties.containerRegistry', 'type': 'ContainerRegistryProperties'},
        'container_service': {'key': 'properties.containerService', 'type': 'AcsClusterProperties'},
        'app_insights': {'key': 'properties.appInsights', 'type': 'AppInsightsProperties'},
        'global_service_configuration': {'key': 'properties.globalServiceConfiguration', 'type': 'GlobalServiceConfiguration'},
    }

    def __init__(self, location, cluster_type, tags=None, description=None, storage_account=None, container_registry=None, container_service=None, app_insights=None, global_service_configuration=None):
        super(OperationalizationCluster, self).__init__(location=location, tags=tags)
        self.description = description
        self.created_on = None
        self.modified_on = None
        self.provisioning_state = None
        self.provisioning_errors = None
        self.cluster_type = cluster_type
        self.storage_account = storage_account
        self.container_registry = container_registry
        self.container_service = container_service
        self.app_insights = app_insights
        self.global_service_configuration = global_service_configuration
