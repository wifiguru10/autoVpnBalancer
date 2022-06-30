#!/usr/bin/ipython3 -i 

import meraki
import copy
import os
import pickle
import get_keys as g
import random
import sys
import datetime
from time import *

a = {'number': 1,
 'name': 'OpenRoaming',
 'enabled': True,
 'splashPage': 'None',
 'ssidAdminAccessible': False,
 'authMode': '8021x-radius',
 'dot11w': {'enabled': False, 'required': False},
 'dot11r': {'enabled': False, 'adaptive': False},
 'encryptionMode': 'wpa-eap',
 'wpaEncryptionMode': 'WPA2 only',
 'radiusServers': [{'host': '56.43.23.23',
   'port': 1812,
   'id': '577586652211294136',
   'openRoamingCertificateId': None,
   'caCertificate': None}],
 'radiusAccountingEnabled': True,
 'radiusAccountingServers': [{'host': '56.43.23.23',
   'port': 1812,
   'id': '577586652211294139',
   'openRoamingCertificateId': None,
   'caCertificate': None}],
 'radiusTestingEnabled': False,
 'radiusProxyEnabled': True,
 'radiusCoaEnabled': False,
 'radiusCalledStationId': '$NODE_MAC$:$VAP_NAME$',
 'radiusAuthenticationNasId': '$NODE_MAC$:$VAP_NUM$',
 'radiusAttributeForGroupPolicies': 'Filter-Id',
 'radiusFailoverPolicy': None,
 'radiusLoadBalancingPolicy': None,
 'ipAssignmentMode': 'Bridge mode',
 'useVlanTagging': False,
 'radiusOverride': False,
 'minBitrate': 12,
 'bandSelection': 'Dual band operation',
 'perClientBandwidthLimitUp': 0,
 'perClientBandwidthLimitDown': 0,
 'perSsidBandwidthLimitUp': 0,
 'perSsidBandwidthLimitDown': 0,
 'mandatoryDhcpEnabled': False,
 'lanIsolationEnabled': False,
 'visible': True,
 'availableOnAllAps': False,
 'availabilityTags': ['secure']}

b = {'number': 1,
 'name': 'OpenRoaming',
 'enabled': True,
 'splashPage': 'None',
 'ssidAdminAccessible': False,
 'authMode': '8021x-radius',
 'dot11w': {'enabled': False, 'required': False},
 'dot11r': {'enabled': False, 'adaptive': False},
 'encryptionMode': 'wpa-eap',
 'wpaEncryptionMode': 'WPA2 only',
 'radiusServers': [{'host': '56.43.23.23',
   'port': 1812,
   'id': '577586652210346715',
   'radsecEnabled': False,
   'openRoamingCertificateId': None,
   'caCertificate': None}],
 'radiusAccountingEnabled': True,
 'radiusAccountingServers': [{'host': '56.43.23.23',
   'port': 1812,
   'id': '577586652210346716',
   'radsecEnabled': False,
   'openRoamingCertificateId': None,
   'caCertificate': None}],
 'radiusTestingEnabled': False,
 'radiusServerTimeout': 1,
 'radiusServerAttemptsLimit': 3,
 'radiusFallbackEnabled': False,
 'radiusAccountingInterimInterval': 1200,
 'radiusProxyEnabled': True,
 'radiusCoaEnabled': False,
 'radiusCalledStationId': '$NODE_MAC$:$VAP_NAME$',
 'radiusAuthenticationNasId': '$NODE_MAC$:$VAP_NUM$',
 'radiusAttributeForGroupPolicies': 'Filter-Id',
 'radiusFailoverPolicy': None,
 'radiusLoadBalancingPolicy': None,
 'ipAssignmentMode': 'Bridge mode',
 'useVlanTagging': False,
 'radiusOverride': False,
 'minBitrate': 12,
 'bandSelection': 'Dual band operation',
 'perClientBandwidthLimitUp': 0,
 'perClientBandwidthLimitDown': 0,
 'perSsidBandwidthLimitUp': 0,
 'perSsidBandwidthLimitDown': 0,
 'mandatoryDhcpEnabled': False,
 'lanIsolationEnabled': False,
 'visible': True,
 'availableOnAllAps': False,
 'availabilityTags': ['secure']}

c = {'id': '577586652210697357', 'networkId': 'L_577586652210278168', 'name': 'Auditorium', 'clientBalancingEnabled': True, 'minBitrateType': 'band', 'bandSelectionType': 'ap', 'apBandSettings': {'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, 'twoFourGhzSettings': {'maxPower': 11, 'minPower': 5, 'minBitrate': 24, 'rxsop': None, 'validAutoChannels': [1, 6, 11], 'axEnabled': True}, 'fiveGhzSettings': {'maxPower': 14, 'minPower': 8, 'minBitrate': 24, 'rxsop': None, 'validAutoChannels': [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165], 'channelWidth': '20'}, 'perSsidSettings': {'0': {'name': 'GUEST', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '1': {'name': 'OpenRoaming', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '2': {'name': 'CORP_DOT1X', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '3': {'name': 'CORP_WPA', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '4': {'name': 'CORP_WPA2', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '5': {'name': 'CORP_WPA1_WPA2', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '6': {'name': 'iPSK_Radius', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '7': {'name': 'iPSK_Static', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '8': {'name': 'Unconfigured SSID 9', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '9': {'name': 'Unconfigured SSID 10', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '10': {'name': 'Unconfigured SSID 11', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '11': {'name': 'Unconfigured SSID 12', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '12': {'name': 'Unconfigured SSID 13', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '13': {'name': 'Unconfigured SSID 14', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '14': {'name': 'Unconfigured SSID 15', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}}}
d = {'id': '577586652210269967', 'networkId': 'N_577586652210343146', 'name': 'Auditorium', 'clientBalancingEnabled': True, 'minBitrateType': 'band', 'bandSelectionType': 'ap', 'apBandSettings': {'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, 'twoFourGhzSettings': {'maxPower': 11, 'minPower': 5, 'minBitrate': 24, 'rxsop': None, 'validAutoChannels': [1, 6, 11], 'axEnabled': True}, 'fiveGhzSettings': {'maxPower': 14, 'minPower': 8, 'minBitrate': 24, 'rxsop': None, 'validAutoChannels': [36, 40, 44, 48, 52, 56, 60, 64, 100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144, 149, 153, 157, 161, 165], 'channelWidth': '20'}, 'perSsidSettings': {'0': {'name': 'GUEST', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '1': {'name': 'OpenRoaming', 'minBitrate': 12, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '2': {'name': 'CORP_DOT1X', 'minBitrate': 12, 'bandOperationMode': '5Ghz', 'bandSteeringEnabled': False}, '3': {'name': 'CORP_WPA', 'minBitrate': 24, 'bandOperationMode': '5Ghz', 'bandSteeringEnabled': False}, '4': {'name': 'CORP_WPA2', 'minBitrate': 1, 'bandOperationMode': '5Ghz', 'bandSteeringEnabled': False}, '5': {'name': 'CORP_WPA1_WPA2', 'minBitrate': 11, 'bandOperationMode': '5Ghz', 'bandSteeringEnabled': False}, '6': {'name': 'iPSK_Radius', 'minBitrate': 24, 'bandOperationMode': '5Ghz', 'bandSteeringEnabled': False}, '7': {'name': 'iPSK_Static', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '8': {'name': 'Unconfigured SSID 9', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '9': {'name': 'Unconfigured SSID 10', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '10': {'name': 'Unconfigured SSID 11', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '11': {'name': 'Unconfigured SSID 12', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '12': {'name': 'Unconfigured SSID 13', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '13': {'name': 'Unconfigured SSID 14', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}, '14': {'name': 'Unconfigured SSID 15', 'minBitrate': 11, 'bandOperationMode': 'dual', 'bandSteeringEnabled': False}}}
gp = {'name': 'GP_ACL1',
 'scheduling': {'enabled': False,
  'monday': {'active': True, 'from': '00:00', 'to': '24:00'},
  'tuesday': {'active': True, 'from': '00:00', 'to': '24:00'},
  'wednesday': {'active': True, 'from': '00:00', 'to': '24:00'},
  'thursday': {'active': True, 'from': '00:00', 'to': '24:00'},
  'friday': {'active': True, 'from': '00:00', 'to': '24:00'},
  'saturday': {'active': True, 'from': '00:00', 'to': '24:00'},
  'sunday': {'active': True, 'from': '00:00', 'to': '24:00'}},
 'bandwidth': {'settings': 'network default',
  'bandwidthLimits': {'limitUp': None, 'limitDown': None}},
 'firewallAndTrafficShaping': {'settings': 'custom',
  'trafficShapingRules': [],
  'l3FirewallRules': [{'comment': 'block 10/8',
    'policy': 'deny',
    'protocol': 'any',
    'destPort': 'Any',
    'destCidr': '10.0.0.0/8'},
   {'comment': 'allow DNS',
    'policy': 'allow',
    'protocol': 'udp',
    'destPort': '53',
    'destCidr': 'Any'}],
  'l7FirewallRules': []},
 'splashAuthSettings': 'network default',
 'vlanTagging': {'settings': 'network default'},
 'bonjourForwarding': {'settings': 'network default', 'rules': []}}

#same as compare() but strips out ID/networkID for profiles/group policies etc
def soft_compare(A, B):
    t_A = copy.deepcopy(A)
    t_B = copy.deepcopy(B)
    delete_keys1 = ['id', 'networkId', 'groupPolicyId', 'dnsRewrite', 'adultContentFilteringEnabled', 'roles'] # 'radiusServerTimeout', 'radiusServerAttemptsLimit', 'radiusFallbackEnabled', 'radiusAccountingInterimInterval' ]
    for dk in delete_keys1:
        if dk in t_A: t_A.pop(dk)
        if dk in t_B: t_B.pop(dk)

    #This bit of code should "true up" both objects by removing uncomming keys, similar to the static removal of keys above, but dynamic
    toRemove = []
    if len(t_A) > len(t_B) and len(t_B) > 0:
        for k in t_A:
            if not k in t_B:
                toRemove.append(k)
        for tr in toRemove:
            if not type(tr) == dict: t_A.pop(tr)
    elif len(t_B) > len(t_A) and len(t_A) > 0:
        for k in t_B:
            if not k in t_A:
                toRemove.append(k)
        for tr in toRemove:
            if not type(tr) == dict: t_B.pop(tr)

    if not len(t_A) == len(t_B):
        print("Both objects aren't equal.... somethings wrong...")


    delete_keys2 = [ 'id', 'radsecEnabled' , 'openRoamingCertificateId', 'caCertificate']
    #had to add some logic to pop the "id" and "radsecEnabled". 'id' is unique and 'radsecEnabled' is beta for openroaming
    if 'radiusServers' in t_A:
        for radServ in t_A['radiusServers']:
            for dk in delete_keys2:
                if dk in radServ: radServ.pop(dk)
            #radServ.pop('id')
            #if 'radsecEnabled' in radServ: radServ.pop('radsecEnabled')
        #t_A['radiusServers'][0].pop('id')
        #if 'radsecEnabled' in t_A['radiusServers'][0]: t_A['radiusServers'][0].pop('radsecEnabled')

    if 'radiusAccountingServers' in t_A: 
        for radACC in t_A['radiusAccountingServers']:
            for dk in delete_keys2:
                if dk in radACC: radACC.pop(dk)   

    if 'radiusServers' in t_B:
        for radServ in t_B['radiusServers']:
            for dk in delete_keys2:
                if dk in radServ: radServ.pop(dk)

    if 'radiusAccountingServers' in t_B:
        for radACC in t_B['radiusAccountingServers']:
            for dk in delete_keys2:
                if dk in radACC: radACC.pop(dk) 
        
    result = compare(t_A, t_B)
    if not result:
        a = 0 #really just a placeholder for breakpoint
    return result

 #compares JSON objects, directionarys and unordered lists will be equal 
def compare(A, B):
    result = True
    if A == None and B == None: 
        return True

    if A == B:
        return True

    if not type(A) == type(B): 
        #print(f"Wrong type")
        return False

    #try:
    
    if not type(A) == int and not type(A) == str and not type(A) == float and not type(A) == bool and not type(A) == dict and not type(A) == list: 
        print(f'Wierd Compare type of [{type(A)}] Contents[{A}]')
        return False
    
    #except:
    #    print()
    
    if type(A) == dict:
        for a in A:
            #if a in B and not self.compare(A[a],B[a]):
            #    return False
            result = compare(A[a],B[a])
            if a in B and not compare(A[a],B[a]):
                return False
    elif type(A) == list:
        found = 0
        for a in A:
            if type(a) == dict:
                for b in B:
                    if compare(a,b):
                        found += 1
            #elif A == B:
                #return True
            elif not a in B:
                return False
        #if found == len(A) and len(A) > 0:
            #print("YEAH")
        if A == B:
            return True
        elif not found == len(A):
            return False             
        
    else:
        if not A == B:
            return False
    if 'name' in A and 'number' in A:
        print()  
    return result
##END-OF COMPARE

def findName(list_of_things, target_name):
    res = []
    for o in list_of_things:
        if target_name in o['name']:
            res.append(o)
    return res

db = meraki.DashboardAPI(api_key=g.get_api_key(), base_url='https://api.meraki.com/api/v1/', maximum_retries=50, print_console=False)

orgs = db.organizations.getOrganizations()

org_id = '121177'

nix = findName(orgs, "Nix")

devs = db.organizations.getOrganizationDevices(org_id)


# TODO: Test....

# TODO: inspected.stack() - inter tools - https://docs.python.org/3/library/itertools.html

# TODO: GPC - https://developer.cisco.com/meraki/api-v1/#!get-device-switch-ports-statuses
