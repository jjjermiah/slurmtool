"""A module for pretty printing of squeue data"""

import json

from rich import box
from rich.console import Console
from rich.style import Style
from rich.table import Column, Table

from slurmtools.helpers import execute_command_and_capture
from slurmtools.squeuejob_dataclass import SqueueJob

def myqueue_handler(testing: bool = False) -> list[SqueueJob]:
    if testing:
        with open('../../squeue_output.json') as f:
            data = json.load(f)
    else:
        output_json = execute_command_and_capture('squeue --json')
        data = json.loads(output_json)

    job_data = data['jobs']

    jobs: list[SqueueJob] = [SqueueJob(**job) for job in job_data]

    return jobs


def main(_format: str):
    jobs = myqueue_handler(testing=False)
    console = Console()
    console.print(f'Found {len(jobs)} jobs')

    if _format == 'json':
        print(json.dumps([job.to_dict() for job in jobs], indent=2))
        return

    table = build_table_from_columns(SqueueJob.generate_table_header(_format))

    # for i, job in enumerate(jobs):
    #     table.add_row(*job.generate_row_data(_format))
    for job in jobs:
        table.add_row(*job.generate_row_data(_format))

    console.print(table)


def build_table_from_columns(columns: list[Column]) -> Table:
    # custom header_style will be a white text on a blue background

    table_dict = {
        'title': 'My Queue',
        'show_lines': True,
        'box': box.ROUNDED,
        'safe_box': True,
        'expand': True,
        'header_style': Style(color='white', bgcolor='blue'),
    }

    table = Table(**table_dict)

    for column in columns:
        table.add_column(
            column.header,
            justify=column.justify,
            style=column.style,
            no_wrap=column.no_wrap,
            width=column.width,
        )

    return table


if '__main__' == __name__:
    main('simple')
