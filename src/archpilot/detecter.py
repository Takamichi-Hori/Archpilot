import os

from archpilot.commands import run_command
from archpilot.models import (
    CPUInfo,
    DiskInfo,
    GPUInfo,
    MemoryInfo,
    SystemInfo,
)

def detect_cpu() -> CPUInfo:
    output = run_command(["lscpu"])

    values: dict[str, str] = {}

    for line in output.splitlines():
        if ":" not in line:
            continue
        
        key, value = line.split(":", 1)

        values[key.strip()] = value.strip()

    model = values.get("Model name", "Unknown CPU")
    architecture = values.get("Architecture", "unknown")

    try:
        core_per_socket = int(values.get("Core(s) per socket", "0"))
        sockets =  int(values.get("Socket(s)", "1"))

        cores = core_per_socket * sockets

    except ValueError:
        cores = 0
    
    try:
        threads = int(values.get("CPU(s)", "0"))

    except ValueError:
        threads = 0
    
    return CPUInfo(
        model=model,
        architecture=architecture,
        cores=cores,
        threads=threads,
    )