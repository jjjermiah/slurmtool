from dataclasses import dataclass, field
from typing import Callable, Dict, Generator, List

from .base import ScontrolBase, ListBase
from .tres import TRES
from .utils import extract, parse_mem, stripped_lines_from_cmd

NODE_CMD = ['scontrol', 'show', 'node', '-a', '--oneliner']

@dataclass
class ScontrolNode(ScontrolBase):
    NodeName: str
    State: str
    Partitions: List[str] = field(default_factory=list)
    CfgTRES: TRES = field(default='', repr=True)
    AllocTRES: TRES = field(default='', repr=True)

    def __post_init__(self) -> None:
        if self.CfgTRES:
            self.CfgTRES = TRES.from_str(self.CfgTRES)
        if self.AllocTRES:
            self.AllocTRES = TRES.from_str(self.AllocTRES)
        if isinstance(self.Partitions, str):
            self.Partitions = self.Partitions.split(',')

    @staticmethod
    def parse_tres(
        tres_str: str,
        flds: Dict[str, Callable[[str], int]] | None = None,
    ) -> Generator[int, None, None]:
        if flds is None:
            flds = {'cpu': int, 'mem': parse_mem, 'gpu': int}
        extracted_dict = extract(tres_str)
        for fld, transformer in flds.items():
            yield transformer(extracted_dict.get(fld, '0'))

@dataclass
class NodeList(ListBase):
    nodes: List[ScontrolNode]

    @classmethod
    async def fetch(cls: type['NodeList']) -> 'NodeList':
        return cls(await fetch_nodes())

    def __getitem__(self, index: int) -> ScontrolNode:
        return self.nodes[index]

async def fetch_nodes() -> list[str]:
    return [ScontrolNode.from_line(line) async for line in stripped_lines_from_cmd(NODE_CMD)]
