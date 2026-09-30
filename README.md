# ArchPilot

**A hardware-aware Arch Linux environment planner built with Python.**

ArchPilot analyzes a Linux machine's hardware and a selected use case, then generates package recommendations and a safe Arch Linux installation plan.

> **Status: v0.1**
>
> ArchPilot currently performs system analysis, recommendations, and planning. It intentionally does not modify disks or install an operating system.

---

## What It Does

Arch Linux installations often require users to manually determine GPU drivers, system packages, desktop environments, and hardware-specific configuration.

ArchPilot turns this into a simple pipeline:

```text
Hardware + Use Case
        │
        ▼
   System Detection
        │
        ▼
   Recommendation
        │
        ▼
 Installation Plan
```

The goal of the project is to separate hardware detection, configuration decisions, and potentially destructive system operations into clearly defined layers.

---

## Features

### Hardware Detection

ArchPilot detects:

- CPU model and architecture
- CPU cores and threads
- AMD, Intel, and NVIDIA GPUs
- installed memory
- physical disks
- UEFI availability
- virtualization environment

It uses standard Linux interfaces and utilities including:

```text
lscpu
lspci
lsblk
/proc/meminfo
/sys
systemd-detect-virt
```

### Hardware-Aware Recommendations

Recommendations depend on the detected hardware.

For example, an AMD GPU may produce:

```text
mesa
vulkan-radeon
lib32-mesa
lib32-vulkan-radeon
```

while Intel and NVIDIA hardware receive different package recommendations.

If ArchPilot cannot safely determine a configuration, it produces a warning instead of guessing.

### Usage Profiles

Three profiles are currently supported:

**Gaming**

```text
Steam
GameMode
gamescope
MangoHud
GPU-specific Vulkan packages
```

**Developer**

```text
Git
Docker
Python
Node.js
npm
Go
```

**Everyday**

```text
Firefox
VLC
LibreOffice
```

---

## Architecture

The project separates system interaction from decision-making.

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

Collects facts about the current machine without making configuration decisions.

### Recommender

Combines hardware information with the selected use case to determine packages, services, and warnings.

### Planner

Converts recommendations into an inspectable plan.

The current version explicitly disables destructive operations.

### Commands

Linux commands are accessed through a small abstraction instead of direct subprocess calls throughout the application.

This keeps system interaction isolated and makes the application easier to test.

---

## Safety

Operating-system installation tools can destroy data if something goes wrong.

For that reason, ArchPilot v0.1 deliberately stops before execution:

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

Operations such as disk formatting, partition deletion, and bootloader installation are not performed.

Future installation functionality would first be tested using virtual machines and virtual disks.

---

## Installation

Requirements:

- Linux
- Python 3.11+
- `lscpu`
- `lspci`
- `lsblk`
- `systemd-detect-virt`

```bash
git clone https://github.com/Takamichi-Hori/Archpilot.git
cd Archpilot

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

Check dependencies:

```bash
archpilot doctor
```

---

## Usage

Analyze the current machine:

```bash
archpilot analyze
```

JSON output:

```bash
archpilot analyze --json
```

Generate recommendations:

```bash
archpilot recommend --use-case gaming
archpilot recommend --use-case developer
archpilot recommend --use-case everyday
```

Generate an installation plan:

```bash
archpilot plan --use-case gaming
```

Save it as JSON:

```bash
archpilot plan \
  --use-case gaming \
  --output archpilot-plan.json
```

---

## Testing

ArchPilot uses `pytest` for unit testing and `ruff` for static analysis.

```bash
pip install pytest ruff

ruff check src tests
pytest
```

GitHub Actions automatically runs both checks on pushes and pull requests.

Tests cover hardware classification, hardware-aware recommendations, usage profiles, and safety constraints.

---

## Design Decisions

**Separate facts from decisions**

```text
Detection → Facts
Recommendation → Decisions
Planning → Actions
```

Hardware detection does not decide which configuration should be installed.

**Fail safely**

When the available information is insufficient for a reliable decision, ArchPilot reports the unresolved configuration instead of guessing.

**Plan before execution**

Potentially destructive operations should have an inspectable plan before any system changes occur.

**Keep system interaction isolated**

External Linux commands are accessed through a dedicated layer so the core application logic remains easier to test and maintain.

---

## Future Improvements

- QEMU-based integration testing
- virtual disk and partition planning
- improved NVIDIA driver resolution
- network preflight checks
- installation logging
- automated boot verification
- terminal or graphical user interface

---