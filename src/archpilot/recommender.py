from archpilot.models import Recommendation, SystemInfo

BASE_PACKAGES = [
    "base",
    "linux",
    "linux-firmware",
    "networkmanager",
    "pipewire",
    "pipewire-pulse",
]

KDE_PACKAGES = [
    "plasma-meta",
    "konsole",
    "dolphin",
]

GAMING_PACKAGES = [
    "steam",
    "gamemode",
    "gamescope",
    "mangohud",
]

def gpu_packages(system: SystemInfo) -> tuple[list[str], list[str]]:
    packages: list[str] = []
    warnings: list[str] = []

    for gpu in system.gpus:
        if gpu.vendor == "AMD":
            packages.extend(
                ["mesa", "vulkan-radeon", "lib32-mesa", "lib32-vulkan-radeon",]
            )

        elif gpu.vendor == "Intel":
            packages.extend(
                ["mesa", "vulkan-intel", "lib32-mesa", "lib32-vulkan-intel"]
            )
        
        elif gpu.vendor == "NVIDIA":
            packages.extend(
                ["nvidia-utils", "lib32-nvidia-utils"]
            )

            warnings.append(
                "NVIDIA kernel driver package must be resolved "
                "for the exact GPU generation and kernel."
            )

    return packages, warnings

