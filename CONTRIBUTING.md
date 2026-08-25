# Contributing to ArchPilot

Thank you for your interest in contributing to ArchPilot.

ArchPilot is an open-source project that aims to make Arch Linux easier to adopt by analyzing a user's hardware and intended use case, then generating an appropriate system configuration.

The project is still in early development, so contributions that improve correctness, safety, testing, documentation, and hardware compatibility are especially valuable.

## Current Project Status

ArchPilot is currently at **v0.1**.

The current version supports:

* CPU detection
* GPU vendor detection
* Memory detection
* Physical disk detection
* UEFI detection
* Virtualization detection
* Gaming recommendations
* Development recommendations
* Everyday-use recommendations
* Safe installation-plan generation

ArchPilot does **not currently perform destructive installation operations**.

The following remain intentionally disabled:

```text
Disk partitioning
Filesystem formatting
Partition deletion
Bootloader installation
Real Arch Linux installation
```

Please do not submit changes that enable destructive operations without prior discussion.

---

## Ways to Contribute

Contributions are welcome in many areas.

### Hardware Detection

Examples:

* Improve GPU detection
* Handle multiple GPUs
* Support hybrid graphics
* Improve disk detection
* Detect additional hardware
* Add PCI-based device identification

### Recommendation Engine

Examples:

* Improve AMD recommendations
* Improve Intel recommendations
* Improve NVIDIA recommendations
* Add better gaming configurations
* Add development tools
* Add desktop-use packages

### Profiles

Future versions of ArchPilot are intended to support community-maintained profiles.

Possible profiles include:

```text
Gaming
Development
Everyday
Content creation
Minimal desktop
Laptop
Handheld gaming
Workstation
```

Profile contributions should avoid unnecessary packages and clearly explain why each package is recommended.

### Testing

Testing contributions are especially welcome.

Useful areas include:

* Additional GPU vendor cases
* Unexpected command output
* Missing Linux utilities
* Multiple GPUs
* Virtual machines
* Invalid JSON from system utilities
* Recommendation edge cases
* Safety regression tests

### Documentation

Documentation contributions include:

* Fixing unclear explanations
* Improving installation instructions
* Adding examples
* Improving architecture documentation
* Correcting grammar
* Documenting supported hardware
* Adding troubleshooting information

---

## Development Setup

### Requirements

You will need:

* Linux
* Python 3.11 or newer
* Git
* `lscpu`
* `lspci`
* `lsblk`
* `systemd-detect-virt`

Clone the repository:

```bash
git clone <repository-url>
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

Install development dependencies:

```bash
pip install pytest ruff
```

Verify your environment:

```bash
archpilot doctor
```

---

## Running ArchPilot

Analyze your system:

```bash
archpilot analyze
```

Generate JSON output:

```bash
archpilot analyze --json
```

Generate a recommendation:

```bash
archpilot recommend --use-case gaming
```

Generate a safe installation plan:

```bash
archpilot plan --use-case gaming
```

---

## Running Tests

Before submitting a pull request, run:

```bash
pytest
```

All tests should pass.

Then run Ruff:

```bash
ruff check src tests
```

You can automatically fix some Ruff issues with:

```bash
ruff check src tests --fix
```

Format the code with:

```bash
ruff format src tests
```

Before submitting your contribution, the following should both succeed:

```bash
ruff check src tests
pytest
```

---

## Project Architecture

The current architecture separates system interaction from decision-making.

```text
CLI
 │
 ├── Detector
 │      │
 │      └── Commands
 │
 ├── Recommender
 │
 └── Planner
```

### `commands.py`

Handles interaction with external system commands.

Examples:

```text
lscpu
lspci
lsblk
systemd-detect-virt
```

Avoid adding direct `subprocess` calls throughout the project when the operation belongs in the command abstraction layer.

### `detector.py`

Collects facts about the system.

The detector should answer questions such as:

```text
What GPU is installed?
How much memory exists?
Is the system booted using UEFI?
What physical disks are available?
```

The detector should avoid making configuration decisions whenever possible.

### `recommender.py`

Turns system facts and the user's intended use case into configuration decisions.

For example:

```text
AMD GPU
+
Gaming profile

↓

Mesa
Vulkan Radeon
Steam
GameMode
```

Keep hardware detection and recommendation logic separate.

### `planner.py`

Creates an installation plan.

The planner must remain non-destructive in v0.1.

---

## Safety Requirements

Safety is a core design requirement of ArchPilot.

Changes involving any of the following require extra review:

* Disk partitions
* Filesystem creation
* Filesystem formatting
* Bootloaders
* Mount operations
* Encryption
* Root privileges
* User-data migration
* Backup and restore
* Operating-system installation

Do not introduce commands such as:

```text
mkfs
fdisk
parted
wipefs
dd
```

into executable ArchPilot workflows without prior discussion and dedicated safety tests.

Destructive functionality must not be introduced casually as part of an unrelated pull request.

---

## Testing Hardware-Dependent Code

Whenever possible, separate parsing and decision logic from actual hardware access.

For example, prefer:

```text
lspci output
    ↓
parser
    ↓
GPU classification
```

instead of writing code that can only be tested on one physical computer.

Hardware classification functions should accept deterministic input so they can be tested using fixed examples.

Do not assume that all machines contain:

* One GPU
* One disk
* UEFI
* NVIDIA, AMD, or Intel hardware
* A specific Linux distribution
* A physical machine rather than a VM

---

## Error Handling

ArchPilot should fail safely.

Prefer:

```text
Unknown hardware
→ report uncertainty
→ continue safely or stop
```

over:

```text
Unknown hardware
→ guess configuration
→ perform destructive operation
```

When hardware cannot be identified reliably, return an explicit unknown or unresolved state.

---

## Coding Guidelines

Use:

* Python type hints
* Clear function names
* Small focused functions
* `dataclass` models where appropriate
* Explicit error handling
* Tests for new behavior

Avoid:

* Large functions that mix detection and decision logic
* Silent exception handling
* Hard-coded machine-specific paths unless they are Linux interfaces
* Unnecessary dependencies
* Destructive shell commands
* Platform assumptions without checks

Prefer readable code over clever code.

---

## Creating an Issue

Before opening an issue:

1. Search existing issues.
2. Confirm that the issue can still be reproduced.
3. Include relevant environment information.

Useful information includes:

```text
ArchPilot version
Linux distribution
Python version
CPU
GPU
Relevant command output
Expected behavior
Actual behavior
```

Do not include passwords, private keys, authentication tokens, or other secrets.

For security vulnerabilities, follow `SECURITY.md` instead of opening a public issue.

---

## Pull Requests

Keep pull requests focused.

A good pull request should:

* Solve one clearly defined problem
* Explain why the change is needed
* Include tests where appropriate
* Pass the existing test suite
* Pass Ruff checks
* Avoid unrelated formatting changes

A pull request description should explain:

```text
What changed?
Why was it changed?
How was it tested?
Are there any safety implications?
```

For hardware-related changes, include example hardware or command output when possible.

---

## Commit Messages

Clear commit messages are encouraged.

Examples:

```text
feat: add Intel GPU package recommendations

fix: prevent false AMD GPU detection

test: add hybrid graphics detection cases

docs: document QEMU testing workflow

refactor: separate GPU parsing from hardware access
```

Small, understandable commits make reviews easier.

---

## Major Changes

Please open an issue or discussion before starting major architectural work such as:

* Real disk partitioning
* `archinstall` integration
* Bootloader management
* Windows migration
* Backup and restore
* GUI architecture
* Plugin systems
* Community profile formats

This helps avoid duplicated work and allows safety requirements to be discussed before implementation begins.

---

## License

By contributing to ArchPilot, you agree that your contributions will be licensed under the project's **GNU General Public License v3.0 only (GPL-3.0-only)**.

---

## First-Time Contributors

First-time open-source contributors are welcome.

Good starting points include:

* Documentation fixes
* Additional test cases
* Hardware detection examples
* Error-message improvements
* Small recommendation improvements

Look for issues labeled:

```text
good first issue
help wanted
documentation
testing
```

If none are available yet, feel free to open an issue proposing a small improvement before starting implementation.

Thank you for helping make ArchPilot safer and easier to use.
