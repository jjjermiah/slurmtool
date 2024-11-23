import json
from dataclasses import dataclass

from rich import print
from rich.console import Console
from rich.table import Table

from slurmtools.helpers import execute_command_and_capture

def scontrol_partition():
    cmd = ['scontrol show partition --json']
    runcmd = ' '.join(cmd)
    print(f'Running command: {runcmd}')

    data = json.loads(execute_command_and_capture(runcmd)).get('partitions')

    return data


def scontrol_node():
    cmd = ['scontrol show node --json']
    runcmd = ' '.join(cmd)
    print(f'Running command: {runcmd}')

    data = json.loads(execute_command_and_capture(runcmd)).get('nodes')

    return data


@dataclass
class CPUInfo:
    total: int
    allocated: int
    free: int


@dataclass
class MemInfo:
    total: int
    allocated: int
    free: int

    def format(self) -> dict[str, str]:
        """Returns a dict with formatted memory information

        default is in MB, but if greater than 1024, will convert to GB
        """

        def MBtoGB(value) -> str:
            if value > 1024:
                return f'{value/1024:.2f} GB'
            return f'{value:.2f} MB'

        return {
            'total': MBtoGB(self.total),
            'allocated': MBtoGB(self.allocated),
            'free': MBtoGB(self.free),
        }


@dataclass
class GPUInfo:
    type: str
    total: int
    allocated: int
    free: int


@dataclass
class ScontrolNode:
    name: str
    hostname: str
    partitions: list[str]
    cpu: CPUInfo
    mem: MemInfo
    gpu: GPUInfo | None = None

    @classmethod
    def from_dict(cls, data) -> 'ScontrolNode':
        tmp = {}

        tmp['name'] = data.get('name')
        tmp['hostname'] = data.get('hostname')
        tmp['partitions'] = data.get('partitions')
        tmp['cpu'] = CPUInfo(
            total=data.get('cpus'),
            allocated=data.get('alloc_cpus'),
            free=data.get('alloc_idle_cpus'),
        )
        tmp['mem'] = MemInfo(
            total=data.get('real_memory'),
            allocated=data.get('alloc_memory'),
            free=data.get('real_memory') - data.get('alloc_memory'),
        )
        if data.get('gres').startswith('gpu'):
            # gres example is gpu:tesla_v100:4
            # gres_used example is gpu:tesla_v100:2(IDX:0-1)
            # extract this information

            gres = data.get('gres').split(':')
            type = gres[1]
            total = gres[2]
            used = data.get('gres_used').split(':')[2].split('(')[0]

            tmp['gpu'] = GPUInfo(
                type=type, total=total, allocated=used, free=int(total) - int(used)
            )
        return cls(**tmp)


@dataclass
class NodeList:
    nodes: list[ScontrolNode]

    def viz(self):
        console = Console()
        table = Table(show_header=True, header_style='bold magenta', expand=True)
        table.add_column('Node', style='red', width=8, justify='center')
        table.add_column('Total CPU', style='cyan', width=4, justify='center')
        table.add_column('Free CPU', style='cyan', width=4, justify='center')
        table.add_column('Total MEM', style='purple', width=8, justify='center')
        table.add_column('Free MEM', style='purple', width=8, justify='center')
        table.add_column('Total GPU', style='green', width=3, justify='center')
        table.add_column('Free GPU', style='green', width=3, justify='center')

        for node in self.nodes:
            table.add_row(
                node.hostname,
                str(node.cpu.total),
                str(node.cpu.free),
                node.mem.format().get('total'),
                node.mem.format().get('free'),
                str(node.gpu.total) if node.gpu else '',
                str(node.gpu.free) if node.gpu else '',
            )
        console.print(table)

    def groupby_partition(self) -> dict[str, 'NodeList']:
        """Returns an instance dict{str, list[ScontrolNode]}grouped by the key provided
        for example, passing 'partitions' will return a list of NodeList instances
        that all have the same partition name

        if a ScontrolNode has multiple partitions, it will be duplicated in each of the lists
        """
        allPartitions = set([partition for node in self.nodes for partition in node.partitions])
        grouped = {key: [] for key in allPartitions}

        # iterate over each partition, look for if the partition is in the list of partitions for each node
        for partition in allPartitions:
            for node in self.nodes:
                if partition in node.partitions:
                    grouped[partition].append(node)
        return {key: NodeList(nodes=value) for key, value in grouped.items()}


@dataclass
class ScontrolPartition:
    name: str
    nodes: list[str]
    total_cpus: int
    time: str = '00:00:00'

    @classmethod
    def from_dict(cls, data) -> 'ScontrolPartition':
        tmp = {}

        tmp['name'] = data.get('name')
        tmp['nodes'] = data.get('nodes').get('configured')
        tmp['total_cpus'] = data.get('cpus').get('total')

        # time in minutes
        time = data.get('maximums').get('time').get('number')
        # convert to D-HH:MM:SS i.e 5-00:00:00 for 5 days
        tmp['time'] = f'{time // 1440}-{(time % 1440) // 60:02d}:{(time % 60):02d}:00'

        return cls(**tmp)


def main():
    result = scontrol_partition()

    # [print(f"Partition: {partition.get('name')}") for partition in result]
    partitions = [ScontrolPartition.from_dict(partition) for partition in result]
    print(f'Found {len(partitions)} partitions')
    [print(partition) for partition in partitions]

    print(result[3])

    result = scontrol_node()
    print(f'Found {len(result)} nodes')
    nodes = NodeList(nodes=[ScontrolNode.from_dict(node) for node in result])
    # nodes.viz()

    grouped = nodes.groupby_partition()

    # for key, value in grouped.items():
    #   print(f"Partition: {key}")
    #   NodeList(nodes=value).viz()

    partition = 'himem'
    print(f'Partition: {partition}')
    grouped[partition].viz()


def gnodes():
    result = scontrol_node()
    nodes = NodeList(nodes=[ScontrolNode.from_dict(node) for node in result])


if __name__ == '__main__':
    main()
