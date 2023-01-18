#!/usr/bin/env python3
import json
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from block import get_network, get_all_network, network_names, node_names

app = FastAPI(
    title='RPC Blocks',
    description='Get RPC block status',
    version='0.1.0'
    )

@app.get("/", tags=["blocks"])
async def get_blocks(network: str = Query("all", enum=network_names()), node: str | None = None):
    if network == 'all':
        return JSONResponse(jsonable_encoder(get_all_network()))
    else:
        if not node == None:
            if node in node_names(network):
                return JSONResponse((get_network(network, node))[-1])
            else:
                return JSONResponse({"error": "invalid node name"})
        else:
            return JSONResponse((get_network(network))[-1])