# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from msrestazure.azure_cloud import AZURE_CHINA_CLOUD
from azure.identity import ClientSecretCredential
from azure.identity import AzureAuthorityHosts
from azure.mgmt.network import NetworkManagementClient

SUBSCRIPTION_ID = "xxx"
TENANT_ID = "xxx"
CLIENT_ID = "xxx"
CLIENT_SECRET = "xxx"

def azurearm_credentials():
    credentials = ClientSecretCredential(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        tenant_id=TENANT_ID,
        authority=AzureAuthorityHosts.AZURE_CHINA
    )
    return credentials

def main():

    GROUP_NAME = "cmb-rg"
    NETWORK_INTERFACE = "cmb-demo-vm1495"
    NSG_NAME = "cmb-specific-nsg"

    credentials = azurearm_credentials()
    
    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    network_client = NetworkManagementClient(credentials, SUBSCRIPTION_ID,base_url=AZURE_CHINA_CLOUD.endpoints.resource_manager, credential_scopes = [AZURE_CHINA_CLOUD.endpoints.resource_manager + "/.default"])

    # Get network interface
    network_interface = network_client.network_interfaces.get(
        GROUP_NAME,
        NETWORK_INTERFACE
    )
    print("Get network interface:\n{}".format(network_interface))

    nsg = network_client.network_security_groups.get(
        GROUP_NAME,
        NSG_NAME
    )

    print("Get network security group:\n{}".format(nsg))

    network_interface.network_security_group = nsg
    # Update network interface
    network_client.network_interfaces.begin_create_or_update(
        GROUP_NAME,
        NETWORK_INTERFACE,
        network_interface
    )
    print("Get network interface:\n{}".format(network_interface))

if __name__ == "__main__":
    main()