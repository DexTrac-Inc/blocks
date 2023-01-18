# RPC Block
Get RPC block status

## Prerequisites
- Python 3.11

## Installation
`python3.11 -m pip install -r requirements.txt`

## Configuration
- Copy and rename **networks_example.json** as **networks.json**
- Update **networks.json** with block explorer api keys and rpc node details (name, ip address, ws/http ports)

## Running application
`python3.11 -m uvicorn main:app --host 0.0.0.0 --port 80`

## Examples
- Get current RPC block from all rpc nodes  
`http://127.0.0.1/?network=all`
- Get current RPC block from all ethereum rpc nodes  
`http://127.0.0.1/?network=ethereum`
- Get current RPC block from one ethereum rpc nodes  
`http://127.0.0.1/?network=ethereum&node=<node name>`
- Alternatively, API docs page can be used to retrieve data.  
`http://127.0.0.1/docs`