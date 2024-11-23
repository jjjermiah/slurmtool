import asyncio
from dataclasses import dataclass, fields
from typing import Type

from rich import print
from .models.tres import TRES
from slurmtools.proper.models.utils import stripped_lines_from_cmd

def process_job_line(line: str) -> list[str]:
    """lines are separated by a `|` character and end in a |"""
    return line.strip().split('|')[:-1]

async def fetch_jobs(command: list[str]) -> tuple[list[str], list[list[str]]]:
    return [process_job_line(line) async for line in stripped_lines_from_cmd(command)]

@dataclass
class SacctJob:
    JobID: str
    JobName: str
    User: str
    Account: str
    WorkDir: str
    Cluster: str
    Partition: str
    NNodes: str
    NodeList: str
    AllocTRES: TRES
    State: str
    ExitCode: str
    Submit: str
    Start: str
    End: str
    Planned: str
    Timelimit: str
    Elapsed: str
    CPUTime: str
    TotalCPU: str
    UserCPU: str
    SystemCPU: str
    CPUTimeRAW: str
    ReqMem: str

    def __post_init__(self):
        self.AllocTRES = TRES.from_str(self.AllocTRES)

    @classmethod
    def flds(cls: Type['SacctJob']) -> list[str]:
        return [f.name for f in fields(cls)]

@dataclass
class JobList:
    jobs : list[SacctJob]
    
    @classmethod
    def initialize(cls: Type['JobList']) -> 'JobList':
        cmd = ['sacct', '--format=%s' % ','.join(SacctJob.flds()), '--parsable']

        (keys, *values) = asyncio.run(fetch_jobs(cmd))
        jobs = []
        for job in values:
            if len(job) != len(keys):
                raise ValueError('Job and keys have different lengths')
            jobs.append(SacctJob(**dict(zip(keys, job))))
        return cls(jobs=jobs)

def main() -> None:
    sacctJobs = JobList.initialize()
    
    filtered = [job for job in sacctJobs.jobs if not '.' in job.JobID] 
    print(f"Found {len(filtered)} jobs")
    print(filtered[0])

if __name__ == '__main__':
    main()
