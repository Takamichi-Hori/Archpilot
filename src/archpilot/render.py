from archpilot.models import SystemInfo


def render_system(system: SystemInfo) -> str:
    lines: list[str] = []

    lines.append("ArchPilot System Analysis")
    lines.append("")
    lines.append(f"CPU: {system.cpu.model}")
    lines.append(f"Architecture: {system.cpu.architecture}")
    lines.append(f"Cores: {system.cpu.cores}")
    lines.append(f"Threads: {system.cpu.threads}")
    lines.append("")

    if system.gpus:
        lines.append("GPU:")

        for gpu in system.gpus:
            lines.append(
                f"  - {gpu.vendor}: {gpu.model}"
            )

    else:
        lines.append("GPU: Not detected")

    lines.append("")
    lines.append(f"RAM: {system.memory.total_gb} GB")
    lines.append("")
    lines.append("Disks:")

    for disk in system.disks:
        lines.append(
            f"  - /dev/{disk.name}: {disk.size}"
        )

    lines.append("")
    lines.append(f"UEFI: {'Yes' if system.uefi else 'No'}")

    lines.append(f"Virtualization: {system.virtualization or 'None'}")

    return "\n".join(lines)