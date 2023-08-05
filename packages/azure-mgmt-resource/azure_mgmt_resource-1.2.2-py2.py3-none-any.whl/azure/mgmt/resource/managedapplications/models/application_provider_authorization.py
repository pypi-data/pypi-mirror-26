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


class ApplicationProviderAuthorization(Model):
    """The managed application provider authorization.

    :param principal_id: The provider's principal identifier. This is the
     identity that the provider will use to call ARM to manage the managed
     application resources.
    :type principal_id: str
    :param role_definition_id: The provider's role definition identifier. This
     role will define all the permissions that the provider must have on the
     managed application's container resource group. This role definition
     cannot have permission to delete the resource group.
    :type role_definition_id: str
    """

    _validation = {
        'principal_id': {'required': True},
        'role_definition_id': {'required': True},
    }

    _attribute_map = {
        'principal_id': {'key': 'principalId', 'type': 'str'},
        'role_definition_id': {'key': 'roleDefinitionId', 'type': 'str'},
    }

    def __init__(self, principal_id, role_definition_id):
        self.principal_id = principal_id
        self.role_definition_id = role_definition_id
