import asyncio

from rich import print

from .models import (
    timer,
)
from .models.scontrol_node import NodeList
from .models.scontrol_partition import PartitionList

@timer
async def get_nodes_partitions():
    node_task = asyncio.create_task(NodeList.fetch())
    partition_task = asyncio.create_task(PartitionList.fetch())
    
    nodes, partitions = await asyncio.gather(node_task, partition_task)
    print(nodes[0])
    print(partitions[0])

@timer
def main() -> None:
    asyncio.run(get_nodes_partitions())

if __name__ == '__main__':
    main()
