from datetime import datetime

from rich import box, print
from rich.console import Console
from rich.style import Style
from rich.table import Table

from slurmtools.helpers import execute_command_and_capture
from slurmtools.sacctjob_dataclass import SacctJob

def jobhist_handler(
    starttime: datetime | None = None,
) -> list[SacctJob]:
    cmd = [
        'sacct',
        '--json',
        # should be of format YYYY-MM-DD-HH:MM:SS
        f"--starttime={starttime.strftime("%Y-%m-%d-%H:%M:%S")}" if starttime else '',
    ]

    runcmd = ' '.join(cmd)
    print(f'Running command: {runcmd}')
    import json

    data = json.loads(execute_command_and_capture(runcmd)).get('jobs')

    return [SacctJob(**job) for job in data]


def main(starttime: datetime | None = None, debug: bool = False, state: list[str] | None = None):
    jobs: list[SacctJob] = jobhist_handler(starttime=starttime)

    console = Console()

    table_dict = {
        'title': 'My Job History',
        'show_lines': True,
        'box': box.ROUNDED,
        'safe_box': True,
        'expand': True,
        'header_style': Style(
            color='white',
            bold=True,
        ),
    }

    table = Table(**table_dict)

    for column in SacctJob.generate_table_header(table):
        table.add_column(
            column.header,
            style=column.style,
            no_wrap=column.no_wrap,
            width=column.width,
            justify=column.justify,
        )

    filters = {'state': state}

    # j.state.current is a List[str]
    # filter by checking if any of the states are in the filters.state list
    if filters.get('state'):
        jobs_filtered: list[SacctJob] = [
            job
            for job in jobs
            if any(state in job.state.current for state in filters.get('state', []))
        ]
        console.print(
            f"Found {len(jobs_filtered)} / {len(jobs)} jobs with state {filters.get('state')}"
        )
    else:
        jobs_filtered = jobs
        console.print(f'Found {len(jobs)} jobs')

    for i, job in enumerate(jobs_filtered):
        if debug and (i == 0 or i == 1):
            print(job)

        table.add_row(*job.generate_row_data())

    console.print(table)
