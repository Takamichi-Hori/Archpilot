# Security Policy

Security and data safety are core requirements of ArchPilot.

ArchPilot is intended to eventually interact with disks, partitions, filesystems, bootloaders, operating-system installation processes, and user data.

A mistake in these areas could result in permanent data loss or an unbootable system.

For that reason, security and safety issues are treated seriously even during early development.

## Current Security Scope

ArchPilot v0.1 is a non-destructive prototype.

It currently supports:

* Hardware detection
* System analysis
* Hardware-aware recommendations
* Installation-plan generation

ArchPilot v0.1 does **not** intentionally perform:

```text
Disk partitioning
Filesystem formatting
Partition deletion
Bootloader installation
Operating-system installation
User-data migration
Backup restoration
```

If the current version unexpectedly performs or allows any destructive operation, please treat that as a security issue.

---

## Supported Versions

ArchPilot is currently under active early development.

| Version                     | Supported |
| --------------------------- | --------- |
| 0.1.x                       | Yes       |
| Older development snapshots | No        |

Only the latest development release is expected to receive security fixes during the early stages of the project.

---

## Reporting a Vulnerability

Please **do not open a public GitHub issue** for vulnerabilities that could expose user data, execute unintended commands, escalate privileges, or cause destructive system changes.

Preferred reporting method:

**Use GitHub Private Vulnerability Reporting for this repository.**

If Private Vulnerability Reporting is unavailable, contact the project maintainer through a private communication channel listed on the repository profile rather than publishing exploit details publicly.

A useful report should include:

* Description of the vulnerability
* Affected ArchPilot version
* Operating system and environment
* Steps to reproduce
* Expected behavior
* Actual behavior
* Potential security or data-loss impact
* Relevant logs or command output
* Suggested mitigation, if known

Please remove secrets and personal information before including logs.

---

## Examples of Security Issues

Security reports are especially important for issues involving:

### Destructive Disk Operations

Examples:

* Wrong disk selected for installation
* Existing partitions unexpectedly deleted
* Filesystem formatted without explicit authorization
* Incorrect device path resolution
* Installation plan targeting the wrong physical drive

### Command Injection

ArchPilot interacts with operating-system commands.

Any situation where untrusted input could alter a command or execute arbitrary commands should be reported.

Examples include unsafe construction involving:

```text
subprocess
shell=True
user-provided package names
device paths
configuration files
profile definitions
```

### Privilege Escalation

Future ArchPilot versions may require elevated permissions for selected operations.

Report issues where:

* Commands receive more privileges than necessary
* Unprivileged users can trigger privileged operations
* Environment variables affect privileged execution unexpectedly
* Writable files are trusted by privileged processes

### Path Traversal

Report situations where user-controlled paths can cause ArchPilot to read from or write to unintended locations.

Examples:

```text
../../etc/passwd
symlink-based path escapes
unsafe restore destinations
```

### Backup and Migration Safety

Future migration features may handle sensitive user data.

Report vulnerabilities involving:

* Backups containing unintended files
* Data restored to incorrect users or paths
* Checksum verification bypass
* Sensitive files copied without explicit approval
* Incomplete backup reported as successful
* Existing data silently overwritten

### Secrets

Future migration functionality may encounter:

```text
SSH private keys
API tokens
.env files
browser credentials
Git credentials
cloud credentials
```

Sensitive credentials must never be silently migrated or exposed in logs.

Any such behavior should be reported.

### Unsafe Hardware Detection

Hardware detection normally should not be destructive.

However, report cases where malformed or unexpected system information can:

* Crash privileged components
* Cause arbitrary command execution
* Produce an unsafe installation target
* Bypass safety checks

### Community Profiles

Future versions may support community-provided configuration profiles.

Profiles must eventually be treated as untrusted input.

Potential issues include:

* Arbitrary command execution
* Untrusted package sources
* Shell injection
* Privileged script execution
* Malicious configuration values

---

## Security Design Principles

ArchPilot follows several security principles.

### Safety Over Automation

If ArchPilot cannot confidently determine what should happen, it should stop or request user input.

It should not guess when the consequence could affect user data.

```text
Uncertain
   ↓
STOP / WARN

not

Uncertain
   ↓
Guess
   ↓
Modify disk
```

---

### Plan Before Execution

Potentially destructive operations should first produce an inspectable plan.

The intended architecture is:

```text
Detection
    ↓
Recommendation
    ↓
Plan
    ↓
Safety Validation
    ↓
Explicit Approval
    ↓
Execution
```

Planning and execution should remain separate components.

---

### Least Privilege

ArchPilot should run without root privileges whenever possible.

Only operations that genuinely require elevated permissions should be executed with elevated privileges.

Future privileged components should be kept as small and isolated as possible.

---

### No Shell Unless Necessary

Prefer structured subprocess execution:

```python
subprocess.run(
    ["command", "argument"],
    check=True,
)
```

instead of:

```python
subprocess.run(
    f"command {user_input}",
    shell=True,
)
```

Use of `shell=True` should be avoided wherever possible.

---

### Explicit Device Identity

Future destructive operations should never rely only on unstable or ambiguous assumptions.

Disk selection should consider information such as:

```text
Device path
Model
Serial
Capacity
Partition table
Existing filesystems
```

A device should be revalidated immediately before any destructive operation.

---

### Verify Before Destroying

Before destructive disk operations are eventually introduced, ArchPilot should verify:

```text
Correct target device
Backup status
Expected partition state
Power conditions where relevant
Encryption state
Mount state
User confirmation
```

---

### Test Destructive Workflows Virtually

New installation functionality must be developed against virtual machines and virtual disks first.

The intended progression is:

```text
Unit tests
    ↓
Integration tests
    ↓
QEMU virtual disks
    ↓
Automated installation
    ↓
Boot verification
    ↓
Physical hardware testing
```

Physical-disk support should not be the first testing environment for destructive features.

---

## Sensitive Logging

Logs should never intentionally contain:

* Passwords
* Authentication tokens
* Private SSH keys
* Recovery keys
* Browser credentials
* Full secret environment variables

Future debugging modes should follow the same rule.

Device metadata and filesystem paths may themselves reveal private information, so security reports should redact unnecessary personal data.

---

## Dependencies

Dependencies should be kept minimal.

When adding a dependency, contributors should consider:

* Whether the dependency is necessary
* Whether it executes privileged operations
* Its maintenance status
* Its license
* Its security history
* Whether equivalent functionality exists in Python or trusted system utilities

Security updates to dependencies should be applied promptly where practical.

---

## Third-Party Components

ArchPilot may eventually integrate with third-party components such as `archinstall`.

A vulnerability originating from a third-party component should still be reported if ArchPilot exposes or amplifies its impact.

When appropriate, the issue may also need to be coordinated with the upstream project.

---

## Disclosure

Please allow reasonable time for a vulnerability to be investigated and fixed before publishing technical details publicly.

Once a fix is available, a security advisory may include:

* Affected versions
* Impact
* Fixed version
* Mitigation
* Credit to the reporter, if desired

ArchPilot aims to handle vulnerability reports respectfully and transparently.

---

## Security Is Part of Correctness

For ArchPilot, a configuration that appears to work but risks destroying user data is not considered correct behavior.

Any feature involving:

```text
root privileges
partitions
filesystems
bootloaders
encryption
backups
migration
```

should be designed with failure scenarios in mind before implementation.

When in doubt, ArchPilot should fail safely.
