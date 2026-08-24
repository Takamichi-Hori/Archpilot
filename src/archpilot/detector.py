import os
import json

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



def detect_gpus() -> list[GPUInfo]:
    output = run_command(["lspci"])

    gpus: list[GPUInfo] = []

    for line in output.splitlines():
        lower = line.lower()

        if not any(
            keyword in lower
            for keyword in ("vga compatible controller", "3d controller", "display controller")
        ):
            continue

        if "nvidia" in lower:
            vendor = "NVIDIA"

        elif "advanced micro devices" in lower or "amd/ati" in lower:
            vendor = "AMD"

        elif "intel corporation" in lower:
            vendor = "Intel"

        else:
            vendor = "Unknown"

        if ": " in line:
            model = line.split(": ", 1)[1]
        
        else:
            model = line

        gpus.append(
            GPUInfo(
                vendor=vendor,
                model=model,
            )
        )

    return gpus



def detect_memory() -> MemoryInfo:
    try:
        with open("/proc/meminfo", encoding="utf-8") as file:
            first_line = file.readline()

        parts = first_line.split()

        memory_kb = int(parts[1])

        memory_gb = memory_kb / 1024 / 1024

        return MemoryInfo(
            total_gb=round(memory_gb, 1)
        )

    except (OSError, ValueError, IndexError):
        return MemoryInfo(total_gb=0.0)



def detect_disks() -> list[DiskInfo]:
    output = run_command( ["lsblk", "-J", "-o", "NAME, SIZE, TYPE"])

    if not output:
        return []

    try:
        data = json.loads(output)

    except json.JSONDecodeError:
        return []

    disks: list[DiskInfo] = []

    for device in data.get("blockdevices", []):
        if device.get("type") != "disk":
            continue

        disks.append(
            DiskInfo(
                name=device.get("name", "unknown"),
                size=device.get("size", "unknown"),
                disk_type=device.get("type", "disk"),
            )
        )

    return disks




def detect_uefi() -> bool:
    return os.path.exists("/sys/firmware/efi")




def detect_virtualization() -> str | None:
    output = run_command(["systemd-detect-virt"])

    if not output or output == "none":
        return None

    return output