#!/usr/bin/env python
import time
import math
import asyncio
from node.engine.ws.task import Task as Agent
from naptha_sdk.schemas import ModuleRunInput
from naptha_sdk.utils import get_logger, load_yaml
from random_number_protocol_ws.schemas import InputSchema

logger = get_logger(__name__)

async def run_agent(agent, name):
    response = await agent(agent_name=name)
    return response

async def run(inputs, worker_nodes=None, orchestrator_node=None, flow_run=None, cfg=None):
    logger.info(f"Inputs: {inputs}")

    num_nodes = len(worker_nodes)
    num_agents = inputs.num_agents
    agents_per_node = math.ceil(num_agents / num_nodes)

    ist = time.time()
    logger.info(f"Running {num_agents} agents...")
    tasks = []
    results = []
    for i in range(num_agents):
        node_index = min(i // agents_per_node, num_nodes - 1)
        name = f"Agent_{i}"
        agent = Agent(name=name, fn="random_number_agent", worker_node=worker_nodes[node_index], orchestrator_node=orchestrator_node, flow_run=flow_run)
        tasks.append(run_agent(agent, name))

    results = await asyncio.gather(*tasks)

    iet = time.time()
    logger.info(f"[Run time: {iet - ist} s]")

    logger.info(f"Results: {results}")

    return results 