#!/usr/bin/env python3

import json
from typing import OrderedDict
import requests
from web3 import Web3
from web3.middleware import geth_poa_middleware
from datetime import datetime, timezone
from time import sleep, time

with open('networks.json', 'r') as networks_file:
    network_data = json.dumps(json.loads(networks_file.read()), sort_keys=True)
networks = json.loads(network_data)['networks']
nodes = json.loads(network_data)['nodes']

def get_explorer_block(network, url, api_key):
    def check_success(results):
        for i in results:
            if i['isError'] == '1':
                continue
            else:
                return i
        raise Exception

    session = requests.Session()
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    
    if network == 'metis':
        api_url = f"{url}?module=block&action=eth_block_number"
    else:
        api_url = f"{url}?action=eth_blockNumber&module=proxy&apikey={api_key}"

    try:
        response = session.get(api_url, headers=headers, timeout=5)
    except Exception:
        pass
    else:
        if response.status_code == 200 and 'result' in response.json():
            block_number = response.json()['result']
            return int(block_number, 16)
    return int('0x0', 16)

def get_node_block(ip):
    node_info = nodes[ip]
    url = f"http://{ip}:{node_info['httpPort']}{node_info['httpAddtlUrl']}"
    # print(url)
    w3 = Web3(Web3.HTTPProvider(url, request_kwargs={'timeout': 3}))
    
    if w3.is_connected() == True:
        if not node_info['network'] == 'ethereum':
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        syncing = w3.eth._syncing()
        latest = w3.eth.get_block('latest')
        
        if syncing == None:
            sync_status = "not supported"
        elif syncing == False:
            sync_status = 'synched'
        else:
            sync_status = 'syncing'
        return int(latest['number']), sync_status
    return 0, 'Failed to connect'

def get_network(network, node=None):
    network_status = []
    node_status = []
    explorer_block = get_explorer_block(network, networks[network]['explorer']['api'], networks[network]['explorer']['apiKey'])
    for ip in nodes:
        if network == nodes[ip]['network']:
            if not node == None:
                if nodes[ip]['name'] == node:
                    node_block, sync = get_node_block(ip)
                else:
                    continue
            else:
                node_block, sync = get_node_block(ip)
            
            node_status.append({
                nodes[ip]['name']: {
                    "nodeBlock": node_block,
                    "syncStatus": sync,
                    "upToDate": block_check(explorer_block, node_block)
                }
                })
    network_status.append({
            network: {
            "explorerBlock": explorer_block,
            "nodes": node_status
            }
        })
    return network_status

def get_all_network():
    network_status = []
    for network in networks:
        # print(network)
        node_status = []
        explorer_block = get_explorer_block(network, networks[network]['explorer']['api'], networks[network]['explorer']['apiKey'])
        for ip in nodes:
            # print(ip)
            if network == nodes[ip]['network']:
                node_block, sync = get_node_block(ip)
                node_status.append({
                    nodes[ip]['name']: {
                        "nodeBlock": node_block,
                        "syncStatus": sync,
                        "upToDate": block_check(explorer_block, node_block)
                    }
                    })
        network_status.append({
            network: {
            "explorerBlock": explorer_block,
            "nodes": node_status
            }
        })
    return network_status

def block_check(explorer_block, node_block):
    if (node_block > explorer_block) or abs(explorer_block - node_block) <= 10:
        return True
    return False

def network_names():
    net_names = [x for x in networks]
    net_names.append('all')
    return net_names

def node_names(network):
    node_names = [nodes[x]['name'] for x in nodes if nodes[x]['network'] == network] 
    return node_names