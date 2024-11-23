from dataclasses import dataclass

# from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from rich.table import Column

from slurmtools.enums import JobState
from slurmtools.helpers import format_memory as _format_memory

@dataclass
class ReturnCode:
    set: bool
    infinite: bool
    number: int


@dataclass
class Signal:
    id: ReturnCode
    name: str

    def __post_init__(self):
        self.id = ReturnCode(**self.id)


@dataclass
class DerivedExitCode:
    status: List[str]
    return_code: ReturnCode
    signal: Signal

    def __post_init__(self):
        self.return_code = ReturnCode(**self.return_code)
        self.signal = Signal(**self.signal)


@dataclass
class Time:
    seconds: int
    microseconds: int


@dataclass
class TimeLimit:
    set: bool
    infinite: bool
    number: int


@dataclass
class JobTime:
    elapsed: int
    eligible: int
    end: int
    start: int
    submission: int
    suspended: int
    system: Time
    limit: TimeLimit
    total: Time
    user: Time

    def __post_init__(self):
        self.system = Time(**self.system)
        self.total = Time(**self.total)
        self.user = Time(**self.user)
        self.limit = TimeLimit(**self.limit)


@dataclass
class ExitCode:
    status: List[str]
    return_code: ReturnCode
    signal: Signal

    def __post_init__(self):
        self.return_code = ReturnCode(**self.return_code)
        self.signal = Signal(**self.signal)


@dataclass
class JobComment:
    administrator: str
    job: str
    system: str


@dataclass
class JobArrayTaskID:
    set: bool
    infinite: bool
    number: int


@dataclass
class JobArray:
    job_id: int
    limits: Dict
    task_id: JobArrayTaskID
    task: str

    def __post_init__(self):
        self.task_id = JobArrayTaskID(**self.task_id)


@dataclass
class JobAssociation:
    account: str
    cluster: str
    partition: str
    user: str
    id: int


@dataclass
class JobReservation:
    id: int
    name: str


@dataclass
class JobRequiredMemory:
    set: bool
    infinite: bool
    number: int


@dataclass
class JobRequired:
    CPUs: int
    memory_per_cpu: JobRequiredMemory
    memory_per_node: JobRequiredMemory

    def __post_init__(self):
        self.memory_per_cpu = JobRequiredMemory(**self.memory_per_cpu)
        self.memory_per_node = JobRequiredMemory(**self.memory_per_node)


@dataclass
class JobStep:
    set: bool
    infinite: bool
    number: int


@dataclass
class JobStepsTime:
    elapsed: int
    end: JobStep
    start: JobStep
    suspended: int
    system: Time
    total: Time
    user: Time

    def __post_init__(self):
        self.end = JobStep(**self.end)
        self.start = JobStep(**self.start)
        self.system = Time(**self.system)
        self.total = Time(**self.total)
        self.user = Time(**self.user)


@dataclass
class JobStatisticsCPU:
    actual_frequency: int


@dataclass
class JobStatisticsEnergy:
    set: bool
    infinite: bool
    number: int


@dataclass
class JobStatistics:
    CPU: JobStatisticsCPU
    energy: JobStatisticsEnergy

    def __post_init__(self):
        self.CPU = JobStatisticsCPU(**self.CPU)
        self.energy = JobStatisticsEnergy(**self.energy)


@dataclass
class JobStepTask:
    distribution: str


@dataclass
class JobStepTRESAllocated:
    type: str
    name: str
    id: int
    count: int


@dataclass
class JobStepTRES:
    requested: List[JobStepTRESAllocated]
    consumed: List[JobStepTRESAllocated]
    allocated: List[JobStepTRESAllocated]

    def __post_init__(self):
        self.requested = [JobStepTRESAllocated(**tres) for tres in self.requested]
        self.consumed = [JobStepTRESAllocated(**tres) for tres in self.consumed]
        self.allocated = [JobStepTRESAllocated(**tres) for tres in self.allocated]


@dataclass
class JobStep:
    time: JobStepsTime
    exit_code: ExitCode
    nodes: JobStepsTime
    tasks: JobStepsTime
    pid: str
    CPU: JobStepsTime
    kill_request_user: str
    state: List[str]
    statistics: JobStatistics
    step: JobStepTask
    task: JobStepTask
    tres: JobStepTRES


@dataclass
class JobTRES:
    allocated: List[JobStepTRESAllocated]
    requested: List[JobStepTRESAllocated]

    def __post_init__(self):
        self.allocated = [JobStepTRESAllocated(**tres) for tres in self.allocated]
        self.requested = [JobStepTRESAllocated(**tres) for tres in self.requested]

    def memory(self, alloc_or_req: str = 'requested'):
        """filter each JobStepTRESAllocated object by type to find type = 'mem' and return the count."""
        filtered = filter(lambda x: x.type == 'mem', getattr(self, alloc_or_req))

        return _format_memory(next(filtered).count)

    def cpu(self, alloc_or_req: str = 'requested'):
        """filter each JobStepTRESAllocated object by type to find type = 'cpu' and return the count."""
        filtered = filter(lambda x: x.type == 'cpu', getattr(self, alloc_or_req))

        return str(next(filtered).count)


@dataclass
class State:
    current: List[str]
    reason: str

    def format(self) -> str:
        return JobState[self.current[0]].format()


@dataclass
class SacctJob:
    account: str
    comment: JobComment
    allocation_nodes: int
    array: JobArray
    association: JobAssociation
    block: str
    cluster: str
    constraints: str
    container: str
    derived_exit_code: DerivedExitCode
    time: JobTime
    exit_code: ExitCode
    extra: str
    failed_node: str
    flags: List[str]
    group: str
    het: JobArray
    job_id: int
    name: str
    licenses: str
    mcs: JobComment
    nodes: str
    partition: str
    priority: ReturnCode
    qos: str
    required: JobRequired
    kill_request_user: str
    reservation: JobReservation
    script: str
    state: State
    steps: List[JobStep]
    submit_line: str
    tres: JobTRES
    used_gres: str
    user: str
    wckey: JobComment
    working_directory: str

    def __post_init__(self):
        """Since the object might be created from a dictionary, we need to convert nested dictionaries to dataclasses."""
        self.derived_exit_code = DerivedExitCode(**self.derived_exit_code)
        self.time = JobTime(**self.time)
        self.exit_code = ExitCode(**self.exit_code)
        self.array = JobArray(**self.array)
        self.association = JobAssociation(**self.association)
        self.reservation = JobReservation(**self.reservation)
        self.required = JobRequired(**self.required)
        self.state = State(**self.state)
        self.steps = [JobStep(**step) for step in self.steps]
        self.tres = JobTRES(**self.tres)

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def generate_table_header(_format: str) -> List[Column]:
        columns = [
            Column(
                'JobID',
                no_wrap=True,
                style='cyan',
                width=6,
                justify='center',
            ),
            Column('Name', style='magenta', no_wrap=True),
            Column('State', style='yellow', no_wrap=True),
            Column('Partition', style='blue', no_wrap=True),
            Column('CPUs', style='green', no_wrap=True, justify='center', width=3),
            Column('Memory', style='cyan', no_wrap=True, justify='right', width=5),
            Column('Start Time', style='magenta', no_wrap=True, justify='center', width=15),
            Column('Limit', style='yellow', no_wrap=True, justify='center'),
            Column('Elapsed', style='green', no_wrap=True, justify='center'),
        ]

        return columns

    def generate_row_data(self) -> List[str]:
        row_data = [
            str(self.job_id),
            self.generate_name(),
            self.state.format(),
            self.partition,
            self.tres.cpu(),
            self.tres.memory(),
            datetime.fromtimestamp(self.time.start).strftime('%Y-%m-%d %H:%M:%S'),
            self.format_time_limit(),
            self.format_time_elapsed(),
        ]

        return row_data

    def is_running(self):
        return self.state.status == 'RUNNING'

    def generate_name(self) -> str:
        """If the name is longer than 20 characters, it will be truncated."""
        if len(self.name) <= 20:
            return self.name

        # check if the name is a path and if so, only show the last part
        if '/' in self.name:
            return self.name.split('/')[-1]

        # return 17 characters of the name and add '...'
        return self.name[:17] + '...'

    def format_time_limit(self) -> str:
        """time_limit.number is in total minutes. We want to convert it to HH:MM."""
        # return datetime.fromtimestamp(self.time['limit']["number"] * 60).strftime("%H:%M")
        return datetime.fromtimestamp(self.time.limit.number * 60).strftime('%HH:%MM')

    def format_time_elapsed(self) -> str:
        # return datetime.fromtimestamp(self.time['elapsed']).strftime("%H:%M:%S")
        return datetime.fromtimestamp(self.time.elapsed).strftime('%HH:%MM')
