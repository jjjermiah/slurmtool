import asyncio
import re
import time
from functools import lru_cache, wraps
from typing import Any, AsyncGenerator, Callable, Dict, Tuple, TypeVar

F = TypeVar('F', bound=Callable[..., Any])


@lru_cache(maxsize=None)
def extract(
    line: str,
    pattern: str = r'(\w+)=([\d.]+[A-Za-z]*)',
) -> dict[str, str]:
    """returns all key-value pairs in a line that match the pattern"""
    return dict(re.findall(pattern, line))


async def stripped_lines_from_cmd(cmd: list[str]) -> AsyncGenerator[str, None]:
    p = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    while True:
        line = await p.stdout.readline()
        if not line:
            break
        yield line.decode('utf-8').strip()
    await p.wait()


def parse_mem(string: str) -> int:
    if string.endswith('M'):
        return int(float(string[:-1])) * 1024 * 1024
    elif string.endswith('G'):
        return int(float(string[:-1])) * 1024 * 1024 * 1024
    else:
        return int(float(string))


def timer(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> F:  # type: ignore
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f'Execution time of {func.__name__}: {execution_time:.8f} seconds')
        return result

    return wrapper  # type: ignore


def parse_time_to_seconds(time_str: str) -> int:
    if '-' in time_str:
        days, time_part = time_str.split('-')
        hours, minutes, seconds = map(int, time_part.split(':'))
        return int(days) * 86400 + hours * 3600 + minutes * 60 + seconds
    else:
        hours, minutes, seconds = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds
