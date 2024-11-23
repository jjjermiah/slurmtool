from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict, List, Union

from dataclasses_json import dataclass_json
from rich.table import Column

from slurmtools.helpers import format_memory as _format_memory

@dataclass_json
@dataclass
class SqueueJobSpec:
    set: bool
    infinite: bool
    number: int

    def __getitem__(self, key):
        return getattr(self, key)


@dataclass_json
@dataclass
class Status:
    status: List[str]
    return_code: Dict[str, Union[bool, int]]
    signal: Dict[str, Union[bool, int, str]]


@dataclass_json
@dataclass
class AllocatedNodes:
    sockets: Dict[str, Dict[str, str]]
    nodename: str
    cpus_used: int
    memory_used: int
    memory_allocated: int

    def __getitem__(self, key):
        return getattr(self, key)


@dataclass_json
@dataclass
class JobResources:
    nodes: str
    allocated_cores: int
    allocated_cpus: int
    allocated_hosts: int
    allocated_nodes: List[AllocatedNodes]

    def __getitem__(self, key):
        return getattr(self, key)


@dataclass
class SqueueJob:
    account: str
    admin_comment: str
    allocating_node: str
    array_task_string: str
    association_id: int
    batch_features: str
    batch_flag: bool
    batch_host: str
    burst_buffer: str
    burst_buffer_state: str
    cluster: str
    cluster_features: str
    command: str
    comment: str
    container: str
    container_id: str
    contiguous: bool
    core_spec: int
    thread_spec: int
    cpus_per_tres: str
    cron: str
    dependency: str
    derived_exit_code: Status
    excluded_nodes: str
    exit_code: Status
    extra: str
    flags: List[str]
    failed_node: str
    features: str
    federation_origin: str
    federation_siblings_active: str
    federation_siblings_viable: str
    gres_detail: List[str]
    group_id: int
    group_name: str
    het_job_id_set: str
    job_id: int
    job_resources: JobResources
    job_size_str: List[str]
    job_state: List[str]
    licenses: str
    mail_type: List[str]
    mail_user: str
    mcs_label: str
    memory_per_tres: str
    name: str
    network: str
    nodes: str
    nice: int
    partition: str
    prefer: str
    power: Dict[str, List[str]]
    profile: List[str]
    qos: str
    reboot: bool
    required_nodes: str
    minimum_switches: int
    requeue: bool
    restart_cnt: int
    resv_name: str
    scheduled_nodes: str
    selinux_context: str
    shared: List[str]
    exclusive: List[str]
    oversubscribe: bool
    show_flags: List[str]
    sockets_per_board: int
    state_description: str
    state_reason: str
    standard_error: str
    standard_input: str
    standard_output: str
    system_comment: str
    tres_bind: str
    tres_freq: str
    tres_per_job: str
    tres_per_node: str
    tres_per_socket: str
    tres_per_task: str
    tres_req_str: str
    tres_alloc_str: str
    user_id: int
    user_name: str
    maximum_switch_wait_time: int
    wckey: str
    current_working_directory: str
    accrue_time: SqueueJobSpec
    array_job_id: SqueueJobSpec
    array_task_id: SqueueJobSpec
    array_max_tasks: SqueueJobSpec
    cores_per_socket: SqueueJobSpec
    billable_tres: SqueueJobSpec
    cpus_per_task: SqueueJobSpec
    cpu_frequency_minimum: SqueueJobSpec
    cpu_frequency_maximum: SqueueJobSpec
    cpu_frequency_governor: SqueueJobSpec
    deadline: SqueueJobSpec
    delay_boot: SqueueJobSpec
    eligible_time: SqueueJobSpec
    end_time: SqueueJobSpec
    het_job_id: SqueueJobSpec
    het_job_offset: SqueueJobSpec
    last_sched_evaluation: SqueueJobSpec
    max_cpus: SqueueJobSpec
    max_nodes: SqueueJobSpec
    tasks_per_core: SqueueJobSpec
    tasks_per_tres: SqueueJobSpec
    tasks_per_node: SqueueJobSpec
    tasks_per_socket: SqueueJobSpec
    tasks_per_board: SqueueJobSpec
    cpus: SqueueJobSpec
    node_count: SqueueJobSpec
    tasks: SqueueJobSpec
    memory_per_cpu: SqueueJobSpec
    memory_per_node: SqueueJobSpec
    minimum_cpus_per_node: SqueueJobSpec
    minimum_tmp_disk_per_node: SqueueJobSpec
    preempt_time: SqueueJobSpec
    preemptable_time: SqueueJobSpec
    pre_sus_time: SqueueJobSpec
    priority: SqueueJobSpec
    resize_time: SqueueJobSpec
    sockets_per_node: SqueueJobSpec
    start_time: SqueueJobSpec
    submit_time: SqueueJobSpec
    suspend_time: SqueueJobSpec
    time_limit: SqueueJobSpec
    time_minimum: SqueueJobSpec
    threads_per_core: SqueueJobSpec

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def generate_table_header(_format: str) -> list[Column]:
        columns = [
            Column(
                'Job ID',
                no_wrap=True,
                style='cyan',
                width=6,
                justify='center',
            ),
            Column('Name', style='magenta'),
            Column('Partition', style='green', justify='center'),
            Column('State', style='yellow', justify='center', width=6),
            Column('Elapsed', style='blue', justify='center', width=5),
            Column('Limit', style='red', justify='center', width=5),
        ]

        if _format == 'spec':
            columns.extend(
                [
                    Column('CPU x Mem', style='cyan', justify='center'),
                    Column('Node x Mem', style='yellow', justify='center'),
                ]
            )
        elif _format == 'debug':
            columns.extend(
                [
                    Column('stderr', style='red', justify='center', width=6),
                    Column('stdout', style='green', justify='center', width=6),
                ]
            )
        elif _format == 'long':
            pass

        return columns

    def generate_row_data(self, _format: str) -> list[str]:
        row_data = [
            str(self.job_id),
            self.generate_name(),
            self.partition,
            self.job_state[0],
            self.format_elapsed_time(),
            self.format_time_limit(),
        ]

        if _format == 'spec':
            row_data.extend(
                [
                    self.generate_cpu_mem(),
                    self.generate_node_mem(),
                ]
            )
        elif _format == 'debug':
            row_data.extend(self.generate_err_out_links())
        elif _format == 'long':
            pass

        return row_data

    def total_memory_used(self):
        return sum(node.memory_used for node in self.job_resources.allocated_nodes)

    def is_pending(self) -> bool:
        return self.job_state[0] == 'PENDING'

    def is_running(self) -> bool:
        return self.job_state[0] == 'RUNNING'

    def is_completed(self) -> bool:
        return self.job_state[0] == 'COMPLETED'

    def is_failed(self) -> bool:
        return self.job_state[0] == 'FAILED'

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
        return datetime.fromtimestamp(self.time_limit['number'] * 60).strftime('%H:%M')

    def format_elapsed_time(self) -> str:
        if self.is_pending():
            return '0:00'
        else:
            return datetime.fromtimestamp(
                self['start_time']['number'] - datetime.now().timestamp()
            ).strftime('%H:%M')

    def generate_cpu_mem(self) -> str:
        cpu = f"{self.cpus['number']}{'*' if self.cpus['infinite'] else ''}"
        mem = f"{_format_memory(self.memory_per_cpu['number'])}{'*' if self.memory_per_cpu['infinite'] else ''}"
        return f'{cpu} x {mem}'

    def generate_node_mem(self) -> str:
        node = f"{self.node_count['number']}{'*' if self.node_count['infinite'] else ''}"
        mem = f"{_format_memory(self.memory_per_node['number'])}{'*' if self.memory_per_node['infinite'] else ''}"
        return f'{node} x {mem}'

    def generate_err_out_links(self) -> list[str]:
        if self.standard_error == '' and self.standard_output == '':
            return ['N/A', 'N/A']

        err = f'[link=file://{self.standard_error}]stderr[/link]'
        out = f'[link=file://{self.standard_output}]stdout[/link]'

        return [err, out]
