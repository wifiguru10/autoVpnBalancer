#!/usr/bin/python3 

import meraki
#import copy
import asyncio
import os
import copy

from time import *

from meraki import aio
import tqdm.asyncio

#import time
import get_keys as g
import datetime
import random

import batch_helper

#import click
#from deepdiff import DeepDiff

#import inspect 

############################################################### USER CONFIGURABLE SECTION ###########################
TAG_GOLDEN = 'golden'
TAG_NAMES = [ 'AVB_GROUP1', 'AVB_GROUP2', 'AVB_GROUP3', 'AVB_GROUP4' ]
TAGS = {}

WRITE=True  #Set this to TRUE to write changes, otherwise it'll just run through the process read-only.

#Action batch settings
USE_ACTION_BATCH = True
batchSize = 5
linearBatch = False #set this to TRUE if you want it to run sequentially, or FALSE if you want it to run all at once. 
#Above linearBatch, setting to False makes it run fast AF. But might break if your doing ALOT of locations. There's no validation/verification, so use with caution.

#asyncio settings
USE_ASYNCIO = False

#####################################################################################################################

log_dir = os.path.join(os.getcwd(), "Logs/")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


#Main dashboard object
db = meraki.DashboardAPI(
            api_key=g.get_api_key(), 
            base_url='https://api.meraki.com/api/v1/', 
            output_log=True,
            log_file_prefix=os.path.basename(__file__)[:-3],
            log_path='Logs/',
            print_console=False)

#Loads whilelist from disk if it's available, otherwise the script will span ALL organizations your API key has access to
orgs_whitelist = []
file_whitelist = 'org_whitelist.txt'
if os.path.exists(file_whitelist):
    f = open(file_whitelist)
    wl_orgs = f.readlines()
    for o in wl_orgs:
        if len(o.strip()) > 0:
            orgs_whitelist.append(o.strip())

### ASYNC SECTION

async def getOrg_Networks(aio, org_id):
    result = await aio.organizations.getOrganizationNetworks(org_id,perPage=1000, total_pages='all')
    return org_id, "networks", result

async def getOrg_Devices(aio, org_id):
    result = await aio.organizations.getOrganizationDevicesStatuses(org_id,perPage=1000, total_pages='all')
    return org_id, "devices", result

async def getOrg_Templates(aio, org_id):
    result = await aio.organizations.getOrganizationConfigTemplates(org_id)
    return org_id, "templates", result

async def getSwitchStatuses_Device(aio, serial):
    result = await aio.switch.getDeviceSwitchPortsStatuses(serial)
    return serial, "statuses", result

async def getSwitchPorts_Device(aio, serial):
    result = await aio.switch.getDeviceSwitchPorts(serial)
    return serial, "switchports", result

async def getNetworkApplianceVpnSiteToSiteVpn_Network(aio, net_id):
    result = await aio.network.getNetworkApplianceVpnSiteToSiteVpn(net_id)
    return netid, "VPNsit2site", result


async def getEverything():
    async with meraki.aio.AsyncDashboardAPI(
                api_key=g.get_api_key(),
                base_url="https://api.meraki.com/api/v1",
                output_log=True,
                log_file_prefix=os.path.basename(__file__)[:-3],
                log_path='Logs/',
                maximum_concurrent_requests=10,
                maximum_retries= 100,
                nginx_429_retry_wait_time=60,
                wait_on_rate_limit=True,
                print_console=False,
                
        ) as aio:
            orgs_raw = await aio.organizations.getOrganizations()
            orgs = {}
            for o in orgs_raw:
                if len(orgs_whitelist) == 0:
                    if o['api']['enabled']:
                        orgs[o['id']] = o
                elif o['id'] in orgs_whitelist:
                    orgs[o['id']] = o
            
            org_networks = {}
            org_devices = {}
            org_templates = {}
            getTasks = []
            for o in orgs:
                getTasks.append(getOrg_Networks(aio, o))
                getTasks.append(getOrg_Devices(aio, o))
                #getTasks.append(getOrg_Templates(aio, o))

            for task in tqdm.tqdm(asyncio.as_completed(getTasks), total=len(getTasks), colour='green'):
                oid, action, result = await task
                if action == "devices":
                    org_devices[oid] = result
                elif action == "networks":
                    org_networks[oid] = result
                elif action == "templates":
                    org_templates[oid] = result

            
            print("DONE")
            return org_devices, org_networks, org_templates
    ##return

async def getEverythingDevice(device_list):
    async with meraki.aio.AsyncDashboardAPI(
                api_key=g.get_api_key(),
                base_url="https://api.meraki.com/api/v1",
                output_log=True,
                log_file_prefix=os.path.basename(__file__)[:-3],
                log_path='Logs/',
                maximum_concurrent_requests=10,
                maximum_retries= 100,
                wait_on_rate_limit=True,
                print_console=False,
                
        ) as aio:
            getTasks = []
            for d in device_list:
                #getTasks.append(getSwitchPorts_Device(aio, d['serial']))
                getTasks.append(getSwitchStatuses_Device(aio, d['serial']))
                

            switches_statuses = {}
            switches_switchports = {}
            for task in tqdm.tqdm(asyncio.as_completed(getTasks), total=len(getTasks), colour='green'):
                serial, action, result = await task
                if action == 'statuses':
                    switches_statuses[serial] = result
                elif action == 'switchports':
                    switches_switchports[serial] = result
                    
                
            
            print("DONE")
            return switches_switchports, switches_statuses

### /ASYNC SECTION   



orgs = db.organizations.getOrganizations()

### This section returns all Devices, Networks and Templates in all the orgs you have access to
loop = asyncio.get_event_loop()
start_time = time()
org_devices, org_networks, org_templates = loop.run_until_complete(getEverything())
end_time = time()
elapsed_time = round(end_time-start_time,2)

print(f"Loaded Everything took [{elapsed_time}] seconds")
print()
### end-of Devices/Networks/Templates

def getDevice(serial):
    for o in org_devices:
        devs = org_devices[o]
        for d in devs:
            if serial == d['serial']:
                return d
    return

def getNetwork(netID):
    for o in org_networks:
        nets = org_networks[o]
        for n in nets:
            if netID == n['id']:
                return n
    return

def getOrg(orgID):
    for o in orgs:
        if orgID == o['id']:
            return o
    return

### This section returns all SwitchPorts and SwitchPort Statuses
MS_online = []
for o in org_devices:
    for d in org_devices[o]:
        if d['status'] == 'online' and 'MS' in d['model'][:2]:
            d['org_id'] = o
            MS_online.append(copy.deepcopy(d))


start_time = time()
#switches_switchports, switches_statuses = loop.run_until_complete(getEverythingDevice(MS_online))
end_time = time()
elapsed_time = round(end_time-start_time,2)
print()
print(f"Loaded Everything took [{elapsed_time}] seconds")
print()
### end-of SwitchPorts / Statuses

def getInscope(tags):
    for t in tags:
        if t in TAG_NAMES:
            return t
    return 

MXnets = []
for o in org_networks:
    nets = org_networks[o]
    for n in nets:
        if 'appliance' in n['productTypes']:
            n['org_id'] = o
            MXnets.append(copy.deepcopy(n))

MXnets_inscope = []
for mx in MXnets:
    Keeper = False
    tag_count = 0
    for t in mx['tags']:
        if t in TAG_NAMES:
            tag_count += 1
            Keeper = True
    if Keeper and tag_count == 1:
        MXnets_inscope.append(copy.deepcopy(mx))

for mx in MXnets_inscope:
    if 'golden' in mx['tags']:
        groupTag = getInscope(mx['tags'])
        if not groupTag == None:
            if not groupTag in TAGS:
                TAGS[groupTag] = db.appliance.getNetworkApplianceVpnSiteToSiteVpn(mx['id'])
                if 'subnets' in TAGS[groupTag]: TAGS[groupTag].pop('subnets') #remove localy significant subnets, get just the hubIDs

print()
print(f"Active Tags:")
for tag in TAGS:
    print(f"\t[{tag}]")
    print(f"\t\tSpoke Configuration[{TAGS[tag]}]")

print()
print(f"Tagged Networks:")
for tag in TAGS:
    print(f"\t[{tag}]")
    currentNets = []
    for mx in MXnets_inscope:
        if tag in mx['tags']:
            currentNets.append(mx['name'])
    print(f"\t\tNetworks Tagged {currentNets} ")    

#Quick sort'n'shuffle to make sure 
nets_online = []
nets_offline = []
nets_other = []
orgs_inscope = []
for oid in org_devices:
    for d in org_devices[oid]:
        netId = d['networkId']
        if d['status'] == 'online':
            if not netId in nets_online: nets_online.append(netId)
            if netId in nets_offline: nets_offline.remove(netId)
            if netId in nets_other: nets_other.remove(netId)
        elif d['status'] == 'offline' or d['status'] == 'dormant':
            if not netId in nets_offline and not netId in nets_online and not netId in nets_other: nets_offline.append(netId)
        else:
            print(f"Status is unknown[{d['status']}] in network[{netId}]")
            if not netId in nets_other and not netId in nets_online: 
                nets_other.append(netId)
            if netId in nets_offline: nets_offline.remove(netId)

            

random.shuffle(nets_online)
random.shuffle(nets_offline)
random.shuffle(nets_other)

#Make a quick list of all the networkIDs in scope
MXNets_inscope_ids = []
for mx in MXnets_inscope: MXNets_inscope_ids.append(mx['id'])

MXnets_inscope = []
for n in nets_online:
    if n in MXNets_inscope_ids: MXnets_inscope.append(getNetwork(n))
for n in nets_other:
    if n in MXNets_inscope_ids: MXnets_inscope.append(getNetwork(n))
for n in nets_offline:
    if n in MXNets_inscope_ids: MXnets_inscope.append(getNetwork(n))


target_orgID = None
if USE_ACTION_BATCH:
    all_actions = []
    
    total_nets = len(MXnets_inscope)
    count = 0
    for mx in MXnets_inscope:
        
        if target_orgID == None:
            target_orgID = mx['org_id']
        if not 'golden' in mx['tags']:
            groupTag = getInscope(mx['tags'])
            currentVPN = None
            if not groupTag == None:
                currentVPN = db.appliance.getNetworkApplianceVpnSiteToSiteVpn(mx['id'])
                if 'subnets' in currentVPN: currentVPN.pop('subnets')
            targetVPN = TAGS[groupTag]
            if not currentVPN == None:
                if not currentVPN == targetVPN:
                    print()
                    print(f"Current VPN doesn't match target")
                    if WRITE:
                        all_actions.append(db.batch.appliance.updateNetworkApplianceVpnSiteToSiteVpn(mx['id'], **targetVPN))
                    else:
                        print("<NO WRITE PERFORMED>")
                    count += 1
                    print(f"Configured Network {mx['name']} With tags[{mx['tags']}] Network#{count} out of {total_nets}")

    test_helper = batch_helper.BatchHelper(db, target_orgID, all_actions, linear_new_batches=linearBatch, actions_per_new_batch=batchSize)
    test_helper.prepare()
    test_helper.generate_preview()
    test_helper.execute()

    all_AB = db.organizations.getOrganizationActionBatches(target_orgID)
    for ab in all_AB:
        if ab['status']['failed']: #the the AB failed
            print(f"Action Batch[{ab['id']}] Failed with errors[{ab['status']['errors']}]")


else:
    print("Using AsyncIO")

print()
print(f"DONE")



        



