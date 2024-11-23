from dataclasses import dataclass, fields
from typing import Type

from .utils import extract

@dataclass
class ScontrolBase:
    pass

    @classmethod
    def from_line(cls: Type['ScontrolBase'], line: str) -> 'ScontrolBase':
        return cls(
            **{
                k: v
                for k, v in extract(line, pattern=r'(\w+)=([^\s]+)').items()
                if k in cls.flds()
            }
        )

    @classmethod
    def flds(cls: Type['ScontrolBase']) -> list[str]:
        return [field.name for field in fields(cls)]


@dataclass
class ListBase:
    pass

    def __getitem__(self, index: int):
        raise NotImplementedError