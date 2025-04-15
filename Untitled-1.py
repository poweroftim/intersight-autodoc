
import os
import json
import requests
from intersight_auth import IntersightAuth
from docx import Document

# Create an AUTH object
AUTH = IntersightAuth(
    secret_key_filename='./API-Key-27JAN-SecretKey.txt',
    api_key_id='6064aebf7564612d332da45c/677bfe2775646133014d720f/6797ab91756461330151b3c2'
)

# Intersight REST API Base URL
BURL = 'https://www.intersight.com/api/v1/'

def get_server_profiles():
    response = requests.get(
        f"{BURL}server/Profiles",
        auth=AUTH
    )
    #print(f"Server Profiles Response: {response.status_code}, {response.text}")  # Debug print
    if response.status_code == 200:
        return response.json().get('Results', [])
    else:
        print(f"Failed to get server profiles: {response.status_code}")
        return []
    
def get_vnics_for_server_profile(profile_moid):
    response = requests.get(
        f"{BURL}server/Profiles/{profile_moid}?$expand=PolicyBucket",
        auth=AUTH
    )
    if response.status_code == 200:
        profile_data = response.json()
        policy_bucket = profile_data.get('PolicyBucket', [])
        vnics = []
        for policy in policy_bucket:
            eth_ifs = policy.get('EthIfs', [])
            for eth_if in eth_ifs:
                # Expand EthIfs by making an additional API call
                eth_if_response = requests.get(
                    f"{BURL}vnic/EthIfs/{eth_if['Moid']}",
                    auth=AUTH
                )
                if eth_if_response.status_code == 200:
                    eth_if_details = eth_if_response.json()
                    vnic_details = {
                        "Name": eth_if_details.get('Name'),
                        "Order": eth_if_details.get('Order')
                    }
                    vnics.append(vnic_details)
                    
                    # Check if FabricEthNetworkGroupPolicy is a list
                    fabric_policies = eth_if_details.get('FabricEthNetworkGroupPolicy', [])
                    if isinstance(fabric_policies, list):
                        for fabric_policy in fabric_policies:
                            fabric_policy_moid = fabric_policy.get('Moid')
                            if fabric_policy_moid:
                                fabric_policy_response = requests.get(
                                    f"{BURL}fabric/EthNetworkGroupPolicies/{fabric_policy_moid}",
                                    auth=AUTH
                                )
                                if fabric_policy_response.status_code == 200:
                                    fabric_policy_details = fabric_policy_response.json()
                                    vlan_settings = fabric_policy_details.get('VlanSettings', {})
                                    vnic_details = {
                                        "Name": fabric_policy_details.get('Name'),  # Extract Name from FabricEthNetworkGroupPolicy
                                        "AllowedVlans": vlan_settings.get('AllowedVlans', [])  # Extract AllowedVlans from VlanSettings
                                    }
                                    vnics.append(vnic_details)
                                else:
                                    print(f"Failed to expand FabricEthNetworkGroupPolicy {fabric_policy_moid}: {fabric_policy_response.status_code}")
                            else:
                                print(f"FabricEthNetworkGroupPolicy Moid is missing for EthIf: {eth_if['Moid']}")
                    else:
                        print(f"FabricEthNetworkGroupPolicy is not a list for EthIf: {eth_if['Moid']}")
                else:
                    print(f"Failed to expand EthIf {eth_if['Moid']}: {eth_if_response.status_code}")
        return vnics
    else:
        print(f"Failed to get vNICs for profile {profile_moid}: {response.status_code}")
        return []
    
def get_vnics_for_all_server_profiles():
    server_profiles = get_server_profiles()
    all_vnics = {}
    for profile in server_profiles:
        profile_moid = profile['Moid']
        vnics = get_vnics_for_server_profile(profile_moid)
        all_vnics[profile['Name']] = vnics
    return all_vnics

if __name__ == "__main__":
    vnics_for_all_profiles = get_vnics_for_all_server_profiles()
    print(json.dumps(vnics_for_all_profiles, indent=4))