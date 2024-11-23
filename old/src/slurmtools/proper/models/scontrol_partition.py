from dataclasses import dataclass, field
from typing import Type

from .base import ScontrolBase, ListBase
from .utils import parse_time_to_seconds, stripped_lines_from_cmd

PARTITION_CMD = ['scontrol', 'show', 'partition', '-a', '--oneliner']

@dataclass
class ScontrolPartition(ScontrolBase):
    PartitionName: str
    Nodes: str = ''
    State: str = ''
    TotalCPUs: int = 0
    TotalNodes: int = 0
    MaxMemPerNode: int = 0
    MaxTime: int = field(default=0)
    DefaultTime: int = field(default=0)

    def __post_init__(self) -> None:
        if isinstance(self.MaxTime, str):
            self.MaxTime = parse_time_to_seconds(self.MaxTime)
        if isinstance(self.DefaultTime, str):
            self.DefaultTime = parse_time_to_seconds(self.DefaultTime)
        if isinstance(self.TotalCPUs, str):
            self.TotalCPUs = int(self.TotalCPUs)
        if isinstance(self.TotalNodes, str):
            self.TotalNodes = int(self.TotalNodes)

@dataclass
class PartitionList(ListBase):
    partitions: list[ScontrolPartition]

    @classmethod
    async def fetch(cls: Type['PartitionList']) -> 'PartitionList':
        return cls(await fetch_partitions())
    
    def __getitem__(self, index: int) -> ScontrolPartition:
        return self.partitions[index]


async def fetch_partitions() -> list['ScontrolPartition']:
    return [
        ScontrolPartition.from_line(line) async for line in stripped_lines_from_cmd(PARTITION_CMD)
    ]
