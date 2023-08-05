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


class Subscription(Model):
    """Subscription information.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: The fully qualified ID for the subscription. For example,
     /subscriptions/00000000-0000-0000-0000-000000000000.
    :vartype id: str
    :ivar subscription_id: The subscription ID.
    :vartype subscription_id: str
    :ivar display_name: The subscription display name.
    :vartype display_name: str
    :ivar state: The subscription state. Possible values are Enabled, Warned,
     PastDue, Disabled, and Deleted. Possible values include: 'Enabled',
     'Warned', 'PastDue', 'Disabled', 'Deleted'
    :vartype state: str or
     ~azure.mgmt.resource.subscriptions.v2016_06_01.models.SubscriptionState
    :param subscription_policies: The subscription policies.
    :type subscription_policies:
     ~azure.mgmt.resource.subscriptions.v2016_06_01.models.SubscriptionPolicies
    :param authorization_source: The authorization source of the request.
     Valid values are one or more combinations of Legacy, RoleBased, Bypassed,
     Direct and Management. For example, 'Legacy, RoleBased'.
    :type authorization_source: str
    """

    _validation = {
        'id': {'readonly': True},
        'subscription_id': {'readonly': True},
        'display_name': {'readonly': True},
        'state': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'subscription_id': {'key': 'subscriptionId', 'type': 'str'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'state': {'key': 'state', 'type': 'SubscriptionState'},
        'subscription_policies': {'key': 'subscriptionPolicies', 'type': 'SubscriptionPolicies'},
        'authorization_source': {'key': 'authorizationSource', 'type': 'str'},
    }

    def __init__(self, subscription_policies=None, authorization_source=None):
        self.id = None
        self.subscription_id = None
        self.display_name = None
        self.state = None
        self.subscription_policies = subscription_policies
        self.authorization_source = authorization_source
