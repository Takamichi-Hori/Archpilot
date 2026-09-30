from archpilot.models import (
    CPUInfo,
    GPUInfo,
    MemoryInfo,
    SystemInfo,
)
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

    assert "steam" in result.packages
    assert "vulkan-radeon" in result.packages
    assert "lib32-vulkan-radeon" in result.packages
    assert result.desktop_environment == "KDE Plasma"


def test_intel_gpu_packages():
    system = make_system("Intel")

    result = recommend(
        system,
        "gaming",
    )

    assert "vulkan-intel" in result.packages
    assert "lib32-vulkan-intel" in result.packages


def test_nvidia_gpu_packages_and_warning():
    system = make_system("NVIDIA")

    result = recommend(
        system,
        "gaming",
    )

    assert "nvidia-utils" in result.packages
    assert "lib32-nvidia-utils" in result.packages
    assert result.warnings


def test_developer_profile():
    system = make_system("AMD")

    result = recommend(
        system,
        "developer",
    )

    assert "git" in result.packages
    assert "docker" in result.packages
    assert "python" in result.packages
    assert "nodejs" in result.packages
    assert "go" in result.packages
    assert "docker" in result.services


def test_everyday_profile():
    system = make_system("Intel")

    result = recommend(
        system,
        "everyday",
    )

    assert "firefox" in result.packages
    assert "vlc" in result.packages
    assert "libreoffice-fresh" in result.packages