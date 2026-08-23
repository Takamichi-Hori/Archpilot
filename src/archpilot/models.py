from dataclasses import asdict, dataclass, field
from typing import Any

@dataclass
class CPUInfo:
    model: str
    architecture: str
    cores: int
    threads: int

@dataclass
class GPUInfo:
    vendor: str
    model: str

@dataclass
class MemoryInfo:
    total_gb: float

@dataclass
class DiskInfo:
    name: str
    size: str
    disk_type: str

@dataclass
class SystemInfo:
    cpu: CPUInfo
    gpus: list[GPUInfo]
    memory: MemoryInfo
    disks: list[DiskInfo]

    uefi: bool
    virtualization: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)