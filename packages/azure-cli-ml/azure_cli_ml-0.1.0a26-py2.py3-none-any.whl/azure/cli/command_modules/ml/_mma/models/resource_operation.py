# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 1.1.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ResourceOperation(Model):
    """Resource operation.

    :param name: Name of this operation.
    :type name: str
    :param display: Display of the operation
    :type display: :class:`ResourceOperationDisplay
     <modelmanagementaccounts.models.ResourceOperationDisplay>`
    :param origin: The operation origin
    :type origin: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'display': {'key': 'display', 'type': 'ResourceOperationDisplay'},
        'origin': {'key': 'origin', 'type': 'str'},
    }

    def __init__(self, name=None, display=None, origin=None):
        self.name = name
        self.display = display
        self.origin = origin
