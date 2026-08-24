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

def recommend(system: SystemInfo, use_case: str,) -> Recommendation:

    packages = BASE_PACKAGES.copy()

    packages.extend(KDE_PACKAGES)

    services = ["NetworkManager", "bluetooth",]

    warnings: list[str] = []

    gpu_pkgs, gpu_warnings = gpu_packages(system)

    packages.extend(gpu_pkgs)
    warnings.extend(gpu_warnings)

    if use_case == "gaming":
        packages.extend(GAMING_PACKAGES)

    elif use_case == "developer":
        packages.extend(
            ["git", "docker", "python", "nodejs", "npm", "go",]
        )

        services.append("docker")

    elif use_case == "everyday":
        packages.extend(
            ["firefox", "vlc", "libreoffice-fresh",]
        )

    else:
        raise ValueError(f"Unknown use case: {use_case}")

    packages = sorted(set(packages))
    services = sorted(set(services))

    return Recommendation(
        use_case=use_case,
        desktop_environment="KDE Plasma",
        packages=packages,
        services=services,
        warnings=warnings,
    )