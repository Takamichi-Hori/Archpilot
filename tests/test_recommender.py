from archpilot.models import (CPUInfo, GPUInfo, MemoryInfo, SystemInfo,)
from archpilot.recommender import recommend

def make_system(vendor: str) -> SystemInfo:

    return SystemInfo(
        cpu=CPUInfo(
            model="Test CPU",
            architecture="x86_64",
            cores=8,
            threads=16,
        ),
        gpus=[
            GPUInfo(
                vendor=vendor,
                model="Test GPU",
            )
        ],
        memory=MemoryInfo(
            total_gb=32,
        ),
        disks=[],
        uefi=True,
        virtualization=None,
    )

def test_amd_gaming_profile():
    system = make_system("AMD")

    result = recommend(
        system,
        "gaming",
    )

    assert "staem" in result.packages
    assert "vulkan-radeon" in result.packages
    assert result.desktop_environment == "KDE Plasma"

