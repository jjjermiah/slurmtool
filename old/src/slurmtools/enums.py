"""Some enums for slurmtools"""

from enum import Enum

class JobState(Enum):
    """Enum for job states"""

    BOOT_FAIL = 'BF'
    CANCELLED = ':no_entry: [bold red strike]CANCELLED[/bold red strike]'  # 'CA'
    COMPLETED = ':white_check_mark: [bold green]COMPLETED[/bold green]'  #'CD'
    CONFIGURING = 'CF'
    COMPLETING = 'CG'
    DEADLINE = 'DL'
    FAILED = ':x: [bold red]FAILED[/bold red]'  # 'F'
    NODE_FAIL = 'NF'
    OUT_OF_MEMORY = 'OOM'
    PENDING = ':hourglass_flowing_sand: [bold yellow]PENDING[/bold yellow]'  # 'PD'
    PREEMPTED = 'PR'
    RUNNING = '[bold orange]RUNNING[/bold orange]'  # 'R'
    RESV_DEL_HOLD = 'RD'
    REQUEUE_HOLD = 'RH'
    REQUEUED = 'RQ'
    RESIZING = 'RS'
    REVOKED = 'RV'
    SIGNALING = 'SI'
    SPECIAL_EXIT = 'SE'
    STAGE_OUT = 'SO'
    STOPPED = 'ST'
    SUSPENDED = 'S'
    TIMEOUT = ':alarm_clock: [bold red]TIMEOUT[/bold red]'  #'TO'

    def format(self):
        return self.value

    # def format(self):
    #     """format
    #     """
    #     if self == JobState.FAILED:
    #         return f
    #     elif self == JobState.COMPLETED:
    #         return
    #     elif self == JobState.PENDING:
    #         return
    #     elif self == JobState.RUNNING:
    #         return
    #     elif self == JobState.CANCELLED:
    #         return
    #     elif self == JobState.TIMEOUT:
    #         return
    #     else:
    #         return self.name
