"""A module for extracting versions"""

import subprocess

def get_slurm_version():
    info = subprocess.Popen(['sinfo', '--version'], stdout=subprocess.PIPE)
    for line in info.stdout:
        slurm, version = line.decode('utf-8').strip().split()
    return tuple(version.strip()[:5].split('.'))
