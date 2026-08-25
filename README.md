# ArchPilot

**ArchPilot is a hardware-aware Arch Linux environment planner designed to make Arch Linux more approachable for everyday users, gamers, and developers.**

Instead of requiring users to manually research hardware drivers, packages, desktop environments, and system configuration, ArchPilot aims to analyze the computer and the user's intended use case, then generate a suitable Arch Linux configuration automatically.

> **Current status: v0.1 — early development**
>
> ArchPilot currently analyzes hardware and generates a safe installation plan.
> It **does not modify disks or install Arch Linux yet**.

---

## Why ArchPilot?

Arch Linux gives users a high degree of control, but getting from a blank installation to a fully configured desktop often requires knowledge of:

* GPU drivers
* Filesystems
* Desktop environments
* Audio systems
* Networking
* Gaming packages
* Development tools
* Hardware-specific configuration

For experienced Linux users, that flexibility is a strength.

For someone who simply wants a fast gaming PC, development environment, or everyday Linux desktop, it can be a significant barrier.

ArchPilot explores a different workflow:

```text
Hardware
   +
User's intended use
        │
        ▼
System Analysis
        │
        ▼
Recommendation Engine
        │
        ▼
Arch Configuration
        │
        ▼
Installation Plan
```

The long-term goal is to turn this into a safe migration and installation tool capable of taking a user from an existing operating system to a ready-to-use Arch Linux environment.

---

## Current Features

### Hardware Detection

ArchPilot v0.1 can detect:

* CPU model
* CPU architecture
* Core and thread count
* GPU vendor

  * AMD
  * Intel
  * NVIDIA
* Installed memory
* Physical disks
* UEFI availability
* Virtualization environment

Hardware information is collected using Linux system interfaces and utilities including:

```text
lscpu
lspci
lsblk
/proc/meminfo
/sys
systemd-detect-virt
```

---

## Hardware-Aware Recommendations

ArchPilot separates hardware detection from configuration decisions.

For example:

```text
AMD GPU
   │
   ▼
mesa
vulkan-radeon
lib32-mesa
lib32-vulkan-radeon
```

while NVIDIA hardware produces a different package set.

When ArchPilot cannot make a decision safely, it reports the unresolved decision instead of guessing.

This is currently used for some NVIDIA driver decisions where the correct kernel module may depend on the GPU generation and selected kernel.

---

## Usage Profiles

ArchPilot v0.1 provides three initial profiles.

### Gaming

Designed for users building a Linux gaming environment.

Recommendations may include:

```text
Steam
GameMode
gamescope
MangoHud
Mesa / Vulkan packages
GPU-specific packages
PipeWire
```

### Development

Designed for software development environments.

Recommendations may include:

```text
Git
Docker
Python
Node.js
Go
KDE Plasma
```

### Everyday

Designed for general desktop use.

Recommendations may include:

```text
Firefox
VLC
LibreOffice
KDE Plasma
```

More profiles are planned, and the profile system is intended to eventually support community contributions.

---

## Safety First

ArchPilot is intended to eventually perform operations that can modify disks and operating systems.

Because those operations can destroy user data if implemented incorrectly, v0.1 deliberately stops before execution.

The following operations are currently blocked:

```text
Disk partitioning        BLOCKED
Filesystem formatting    BLOCKED
Partition deletion       BLOCKED
Bootloader installation  BLOCKED
Real OS installation     BLOCKED
```

The current pipeline is:

```text
Detect
  ↓
Analyze
  ↓
Recommend
  ↓
Plan
  ↓
STOP
```

Future execution functionality will first be developed and tested against virtual disks using QEMU before support for physical disks is considered.

---

## Architecture

ArchPilot currently separates system interaction, hardware detection, recommendation logic, and planning.

```text
                    CLI
                     │
        ┌────────────┼────────────┐
        │            │            │
     analyze      recommend      plan
        │            │            │
        ▼            ▼            ▼
    Detector ──► Recommender ──► Planner
        │
        ▼
    Commands
        │
        ▼
Linux system interfaces
```

### Project Structure

```text
src/archpilot/
├── __main__.py
├── cli.py
├── commands.py
├── detector.py
├── models.py
├── planner.py
├── recommender.py
└── render.py
```

### Detector

Collects facts about the system.

```text
Hardware → facts
```

Examples:

```text
GPU: AMD Radeon
RAM: 32 GB
Firmware: UEFI
```

### Recommender

Turns detected facts and user intent into configuration decisions.

```text
Facts + use case → recommendation
```

### Planner

Converts a recommendation into an installation plan.

In v0.1, the planner explicitly prevents destructive operations.

### Commands

Provides a small abstraction around external Linux utilities instead of spreading direct subprocess calls throughout the codebase.

This makes system-dependent code easier to test and replace.

---

## Installation

### Requirements

* Linux
* Python 3.11+
* `lscpu`
* `lspci`
* `lsblk`
* `systemd-detect-virt`

Clone the repository:

```bash
git clone <your-repository>
cd archpilot
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install ArchPilot in editable mode:

```bash
pip install -e .
```

---

## Usage

### Check dependencies

```bash
archpilot doctor
```

### Analyze the current PC

```bash
archpilot analyze
```

JSON output:

```bash
archpilot analyze --json
```

### Generate a gaming recommendation

```bash
archpilot recommend --use-case gaming
```

### Generate a development recommendation

```bash
archpilot recommend --use-case developer
```

### Generate an everyday-use recommendation

```bash
archpilot recommend --use-case everyday
```

### Generate an installation plan

```bash
archpilot plan --use-case gaming
```

Save the plan:

```bash
archpilot plan \
  --use-case gaming \
  --output archpilot-plan.json
```

---

## Testing

Install development tools:

```bash
pip install pytest ruff
```

Run the test suite:

```bash
pytest
```

Run static analysis:

```bash
ruff check src tests
```

Current tests cover areas including:

* NVIDIA GPU vendor detection
* AMD GPU vendor detection
* Intel GPU vendor detection
* Hardware-aware gaming recommendations
* Prevention of destructive disk operations

---

## Roadmap

### v0.1 — Hardware-Aware Planner

* [x] CPU detection
* [x] GPU detection
* [x] Memory detection
* [x] Disk detection
* [x] UEFI detection
* [x] Virtualization detection
* [x] Gaming profile
* [x] Development profile
* [x] Everyday profile
* [x] Hardware-aware package recommendations
* [x] Safe installation plan
* [x] Unit tests

### v0.2 — Virtual Installation

* [ ] QEMU-based test environment
* [ ] Virtual disk inspection
* [ ] Partition planning
* [ ] Network preflight checks
* [ ] `archinstall` integration
* [ ] Installation logging
* [ ] Automated boot verification
* [ ] Improved NVIDIA driver resolution

### v0.3 — Migration Analysis

* [ ] Windows system analysis
* [ ] Installed application detection
* [ ] Linux application equivalents
* [ ] User-data inventory
* [ ] BitLocker detection
* [ ] Windows Fast Startup detection
* [ ] Migration manifests

### Future

* [ ] Backup verification
* [ ] Restore engine
* [ ] Dual-boot support
* [ ] Bootable ArchPilot ISO
* [ ] Graphical interface
* [ ] Community profiles
* [ ] Hardware-specific community configurations

---

## Contributing

ArchPilot is being developed as an open-source project, and contributions are welcome.

Useful contributions include:

* Hardware detection improvements
* Support for additional GPUs and devices
* New usage profiles
* Package recommendations
* Tests
* Documentation
* Linux compatibility fixes
* QEMU test infrastructure
* UI/UX ideas

If you are new to open source, documentation, tests, and additional hardware-detection cases are good places to start.

Before submitting a pull request:

```bash
ruff check src tests
pytest
```

Both should pass.

A dedicated `CONTRIBUTING.md` with contribution guidelines will be maintained as the project grows.

---

## Design Principles

ArchPilot follows several principles:

### Safety over automation

If ArchPilot cannot determine an operation safely, it should stop instead of guessing.

### Plan before execution

Potentially destructive operations should have an inspectable plan before they are executed.

### Hardware-aware, not one-size-fits-all

Recommendations should be based on the actual machine whenever possible.

### Test destructive workflows virtually first

Disk and installation functionality should be validated against virtual machines and virtual disks before physical hardware.

### Keep the core independent from the interface

Hardware detection and recommendation logic should not depend on whether ArchPilot eventually uses a CLI, TUI, or GUI.

---

## License

ArchPilot is licensed under the **GNU General Public License v3.0 only (GPL-3.0-only)**.

You may use, study, modify, and redistribute ArchPilot under the terms of the GPLv3.

See the `LICENSE` file for the complete license text.

---

## Disclaimer

ArchPilot is experimental software under active development.

Future versions may perform operations involving partitions, filesystems, bootloaders, and operating-system installation. Such operations can result in permanent data loss if something goes wrong.

Always maintain verified backups of important data.

**ArchPilot is an independent community project and is not affiliated with or endorsed by Arch Linux.**
