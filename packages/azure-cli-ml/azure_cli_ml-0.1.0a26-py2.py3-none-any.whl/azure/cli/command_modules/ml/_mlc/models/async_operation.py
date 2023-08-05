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

from msrest.serialization import Model


class AsyncOperation(Model):
    """Azure async operation details.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param id: Async operation id.
    :type id: str
    :param name: Async operation name.
    :type name: str
    :ivar status: The provisioning state of the cluster. Possible values
     include: 'Unknown', 'Updating', 'Creating', 'Deleting', 'Succeeded',
     'Failed', 'Canceled'
    :vartype status: str or :class:`OperationStatus
     <azure.mgmt.machinelearningcompute.models.OperationStatus>`
    :ivar start_time: The date time that the async operation started.
    :vartype start_time: datetime
    :ivar end_time: The date time that the async operation finished.
    :vartype end_time: datetime
    :param percent_complete: Async operation progress.
    :type percent_complete: float
    :param error: If the async operation fails, this structure contains the
     error details.
    :type error: :class:`ErrorResponseWrapper
     <azure.mgmt.machinelearningcompute.models.ErrorResponseWrapper>`
    """

    _validation = {
        'status': {'readonly': True},
        'start_time': {'readonly': True},
        'end_time': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'status': {'key': 'status', 'type': 'str'},
        'start_time': {'key': 'startTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
        'percent_complete': {'key': 'percentComplete', 'type': 'float'},
        'error': {'key': 'error', 'type': 'ErrorResponseWrapper'},
    }

    def __init__(self, id=None, name=None, percent_complete=None, error=None):
        self.id = id
        self.name = name
        self.status = None
        self.start_time = None
        self.end_time = None
        self.percent_complete = percent_complete
        self.error = error
