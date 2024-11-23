from dataclasses import dataclass
from typing import Callable, Dict, Generator, Type

from slurmtools.proper.models.utils import extract, parse_mem

@dataclass
class TRES:
    cpu: int
    mem: int
    gpu: int

    @classmethod
    def from_str(cls: Type['TRES'], s: str) -> 'TRES':
        return cls(*cls.parse_tres(s))

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

    def __str__(self) -> str:
        return f'{self.cpu} CPUs, {self.mem} memory, {self.gpu} GPUs'

    def __repr__(self) -> str:
        return f'TRES({self.cpu}, {self.mem}, {self.gpu})'

    def __add__(self, other: 'TRES') -> 'TRES':
        return TRES(self.cpu + other.cpu, self.mem + other.mem, self.gpu + other.gpu)

    def __sub__(self, other: 'TRES') -> 'TRES':
        return TRES(self.cpu - other.cpu, self.mem - other.mem, self.gpu - other.gpu)

    def __mul__(self, other: int) -> 'TRES':
        return TRES(self.cpu * other, self.mem * other, self.gpu * other)

    def __truediv__(self, other: int) -> 'TRES':
        return TRES(self.cpu / other, self.mem / other, self.gpu / other)

    def __floordiv__(self, other: int) -> 'TRES':
        return TRES(self.cpu // other, self.mem // other, self.gpu // other)

    def __mod__(self, other: int) -> 'TRES':
        return TRES(self.cpu % other, self.mem % other, self.gpu % other)

    def __eq__(self, other: 'TRES') -> bool:
        return self.cpu == other.cpu and self.mem == other.mem and self.gpu == other.gpu

    def __ne__(self, other: 'TRES') -> bool:
        return not self == other

    def __lt__(self, other: 'TRES') -> bool:
        return self.cpu < other.cpu and self.mem < other.mem and self.gpu < other.gpu

    def __le__(self, other: 'TRES') -> bool:
        return self.cpu <= other.cpu and self.mem <= other.mem and self.gpu <= other.gpu

    def __gt__(self, other: 'TRES') -> bool:
        return self.cpu > other.cpu and self.mem > other.mem and self.gpu > other.gpu

    def __ge__(self, other: 'TRES') -> bool:
        return self.cpu >= other.cpu and self.mem >= other.mem and self.gpu >= other.gpu

    def __bool__(self) -> bool:
        return self.cpu or self.mem or self.gpu

    def __abs__(self) -> 'TRES':
        return TRES(abs(self.cpu), abs(self.mem), abs(self.gpu))

    def __neg__(self) -> 'TRES':
        return TRES(-self.cpu, -self.mem, -self.gpu)

    def __pos__(self) -> 'TRES':
        return TRES(+self.cpu, +self.mem, +self.gpu)