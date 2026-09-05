---
name: os-macos
title: "macOS Operations"
description: "macOS administration: hardware and release detection, launchd domains, managed updates, security boundaries, packages, diagnostics, and recovery."
license: Apache-2.0
compatibility: "Requires access to the target Mac through supported shell or device-management tools."
domains: devops
rules:
  - content(macos)
  - content(osx)
  - match(mac.*administration|mac.*diagnostics|mac.*maintenance)
---

## Overview

Use for Mac administration, troubleshooting, updates, and automation. Identify the target and its management policy; local tools do not establish remote capabilities.

## Mental model

macOS combines Unix permissions, signed system software, privacy controls, sessions, and device management. Root does not bypass every boundary. Installed files, service registration, permission to run, and health are distinct states.

## Release and hardware gate

Verified 2026-09-05: macOS Tahoe 26 is the current stable family; Apple's security page lists 26.6.2. macOS 27 remains prerelease. Older Sequoia 15 and Sonoma 14 receive listed updates, but don't infer identical security coverage or guaranteed support dates from a three-release rule.

- Record product version/build, model, Intel versus Apple silicon, native/process architecture, logged-in user, shell, and enrollment status. macOS has no Windows-style Home/Pro editions; release, hardware eligibility, and management enrollment are the relevant distinctions.
- Rosetta can make an Apple-silicon process report x86_64. Prefer native compatible tools, and inspect binary architecture and dependencies before choosing Intel packages. Translation availability is version-specific, not a permanent fallback guarantee.
- macOS command-line utilities often use BSD behavior. Check the target's manual before importing GNU flags; don't replace system tools or rewrite global PATH merely to make a Linux command work.
- Interactive shell startup files do not define a launchd job's environment. Use explicit executable paths, arguments, working directory, and required environment for unattended work.

## Services and launchd domains

- Distinguish system daemons from per-user agents. Third-party locations are `/Library/LaunchDaemons`, `/Library/LaunchAgents`, and `~/Library/LaunchAgents`; leave Apple-owned `/System/Library` jobs alone.
- Select the actual launchctl domain: `system`, `user/<uid>`, or `gui/<uid>`. User and GUI domains are not interchangeable; an SSH/root shell does not imply the console user's GUI session exists.
- Inspect the exact service label/domain before changing it. Use the target's current `launchctl` manual for `print`, `bootstrap`, `bootout`, and `kickstart`; registration/removal, enabled state, and starting a process are different operations.
- Validate plist syntax, executable ownership/access, arguments, output paths, and the service's own logs. ProgramArguments is an argument array, not an implicit shell command: pipes, redirects, globbing, and variable expansion need explicit handling.
- Don't use permanent KeepAlive restart loops to conceal invalid configuration. A demand-start job without a PID can be healthy; validate its trigger and actual output rather than requiring every registered service to run continuously.
- Modern login/background items can also require user approval or management policy. Inspect the application's registration and managed-login-item rules; don't repeatedly re-enable a user-disabled helper.

## Packages and managed updates

- Preserve the established source: Apple Software Update, App Store, signed vendor package, or existing package manager. Verify publisher/signature, architecture, version, destination, and update owner before installing. Package receipts do not prove every installed file remains healthy.
- Do not assume Homebrew exists or manages every app. Avoid introducing another installation path for the same tool; identify the executable actually resolved by the failing service.
- On managed Macs, inspect effective update declarations, deferrals, deadlines, and reported status. Declarative management can take precedence over similar commands; don't fight policy with repeated `softwareupdate` invocations.
- Apple-silicon update authorization can involve volume ownership and an escrowed bootstrap token. Being an administrator or using sudo is not equivalent to satisfying that authorization.
- Separate OS upgrades, minor/security updates, background security improvements, and third-party app updates. Before an authorized upgrade, verify hardware support, free space, power, backup/recovery readiness, and reboot impact; afterward verify build and workload health.

## Security, diagnostics, and recovery

- Distinguish Unix/ACL permissions, TCC privacy consent, sandbox restrictions, Gatekeeper, SIP, and FileVault. Diagnose the failing layer; don't broadly remove quarantine, grant Full Disk Access, or disable protections as a generic repair.
- Use the approved management/privacy-consent mechanism for unattended software. Don't edit privacy databases, managed profiles, or protected system files to bypass ownership.
- Filter unified logs by time and relevant process/subsystem; correlate service state, crashes, storage pressure, and network symptoms. Preserve the original exit/error details and avoid collecting unrelated personal data or credentials.
- Make one attributable change, with bounded retries and a recovery path. Stop when the same permanent denial or configuration failure repeats. Never convert inaccessible data into empty output or delete a store/cache without establishing its ownership and recoverability.
- Reinstallation, erase, and downgrade are separate recovery operations. A backup is not proof that an older OS can restore everything; verify hardware/OS compatibility and the intended data-restoration path first.

## Example

Read-only inventory in the intended target session:

```sh
/usr/bin/sw_vers
/usr/bin/uname -m
/usr/sbin/system_profiler SPSoftwareDataType SPHardwareDataType -detailLevel mini
```

Compare hardware chip/processor information with the process architecture. System Profiler may include machine identifiers: keep raw output local and share only fields relevant to the diagnosis.

## Checklist

- [ ] Target release/build, hardware, identity, session, and management are known.
- [ ] Correct launchd domain and package/update owner are identified.
- [ ] Permission failures are diagnosed without silently weakening controls.
- [ ] Changes have explicit completion evidence, retry bounds, and recovery.
- [ ] Observed results and unverified assumptions are reported separately.

## References

- [Security releases](https://support.apple.com/en-us/100100) and [Rosetta](https://support.apple.com/en-us/102527)
- [launchd management](https://support.apple.com/guide/terminal/script-management-with-launchd-apdc6c1077b-5d5d-4d35-9c19-60f2397b2369/mac)
- [Login/background items](https://support.apple.com/guide/deployment/manage-login-items-background-tasks-mac-depdca572563/web)
- [Managed updates](https://developer.apple.com/documentation/devicemanagement/deploying-software-updates-using-declarative-management)
- [Tokens and ownership](https://support.apple.com/guide/deployment/use-secure-and-bootstrap-tokens-dep24dbdcf9e/web)
- [System Integrity Protection](https://support.apple.com/en-us/102149) and [Console diagnostics](https://support.apple.com/guide/console/view-log-messages-cnsl1012/mac)
