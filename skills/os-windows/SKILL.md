---
name: os-windows
title: "Windows Operations"
description: "Windows client/server operations: release channels, PowerShell context, services, updates, permissions, WSL boundaries, and evidence-based recovery."
license: Apache-2.0
compatibility: "Requires access to the target Windows system through its supported shell or management tools."
domains: devops
rules:
  - content(windows)
  - content(win11)
  - content(win10)
  - content(windowsserver)
  - content(wsl)
---

## Overview

Use for Windows administration, diagnostics, and automation. Determine the target and management authority; local tools do not establish remote capabilities.

## Mental model

Windows behavior depends on edition, channel, identity, and execution context. A successful command or running process does not prove service health.

## Release and execution gate

Verified 2026-09-05: Windows 11 25H2 is the general feature-update baseline. Released 26H1 serves specific new hardware and is not an in-place upgrade from 24H2/25H2. Windows Server 2025 is the current LTSC release. Recheck release health and edition-specific lifecycle dates before prescribing an upgrade; Insider and optional preview updates are different channels.

- Identify client versus Server, edition, display version, full build/revision, architecture, and installation type. Server Core, desktop clients, Enterprise LTSC, and IoT Enterprise LTSC have different component availability and support terms.
- Windows 10 22H2 standard support ended in October 2025; verify ESU enrollment where applicable. Don't apply that lifecycle blindly to Windows 10 LTSC products.
- Distinguish native architecture from process bitness/emulation. A 32-bit shell on 64-bit Windows can see redirected filesystem/registry locations; ARM64 machines may run emulated x64 tools.
- Windows PowerShell 5.1 uses `powershell.exe`; PowerShell 7 uses `pwsh.exe` and installs alongside it. PowerShell 7.6 is current LTS; 7.7 is preview. Check `$PSVersionTable`, module compatibility, and remoting endpoint rather than assuming Terminal selects PowerShell 7.
- Preserve argument boundaries with PowerShell arrays and `-LiteralPath` where appropriate. Explicitly use `sc.exe` for the service utility: `sc` can resolve to a PowerShell alias.

## Services and scheduled work

- Inspect Service Control Manager configuration before changing it: service name, account, binary arguments, dependencies, start mode, recovery actions, and current state. A display name is not a stable service identifier.
- Keep long-lived services under their service manager; use Task Scheduler for scheduled jobs with explicit user, logon requirements, working directory, overlap policy, and exit handling. Interactive success does not prove unattended success.
- A stopped demand-start service may be normal. Before restarting, inspect scoped event logs and dependency failures; don't turn every service to Automatic or loop restarts against a persistent configuration error.
- For an authorized restart, bound waiting, observe the final state, and check the actual endpoint/workload. Record pending reboot or partial failure instead of reporting success from command acceptance alone.

## Packages and update lifecycle

- Use the host's existing management channel. WinGet supports modern Windows clients and Server 2025, but availability depends on App Installer and context; don't bootstrap a second manager just because the command is absent.
- Resolve exact package ID, source, publisher, architecture, version, and user/machine scope before installation. Preserve installer exit codes and restart requirements; a PATH change may require a new process.
- Respect Intune/Group Policy/WSUS controls and update rings. Check known issues, safeguard holds, reboot windows, and recovery options before feature updates; don't bypass a managed deferral by manually installing another channel.
- OS servicing, Store apps, WinGet applications, and PowerShell have separate update lifecycles. Verify the changed component after reboot; an empty query or pending installation is not proof of compliance.

## Privilege, WSL, and failure handling

- Use the least-privileged identity that can perform the operation. Elevation, service-account rights, NTFS/share permissions, and remote authorization are separate; diagnose the denied boundary instead of granting broad Full Control.
- Execution policy is a scripting guardrail, not a security boundary. Don't disable Defender, firewall, UAC, application control, or certificate validation to make an unexplained failure disappear.
- Record WSL distribution, WSL version, and WSL 1/2 mode separately from Windows. WSL 2 has a Linux kernel in a managed VM; networking, service lifetime, and mounted Windows-file permissions differ from a standalone Linux server.
- `-ErrorAction Stop` promotes cmdlet errors for handling; native utilities need exit-code checks under the selected PowerShell behavior. Some tools define nonzero success/status codes: interpret their contract rather than treating every nonzero value identically.
- Capture the failing operation, timestamp, target, and relevant event IDs before changing state. Use bounded, targeted diagnostics; don't dump credentials or entire event stores. Retry only identified transient failures; preserve prior configuration for recovery.

## Example

Read-only target inventory, compatible with Windows PowerShell 5.1 and PowerShell 7:

```powershell
$PSVersionTable
Get-CimInstance Win32_OperatingSystem -ErrorAction Stop |
    Select-Object Caption, Version, BuildNumber, OSArchitecture
Get-CimInstance Win32_Processor -ErrorAction Stop |
    Select-Object Name, Architecture
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' -ErrorAction Stop |
    Select-Object EditionID, DisplayVersion, CurrentBuildNumber, UBR
```

Processor architecture codes include 9 for x64 and 12 for ARM64. Run in the intended target session; these values alone do not prove patch support or service health.

## Checklist

- [ ] Target, edition/channel, build, architecture, identity, and shell are known.
- [ ] Service/package/update ownership and reboot consequences are explicit.
- [ ] Failures remain visible; retries and recovery have stopping conditions.
- [ ] Post-change evidence verifies the requested behavior, not just command exit.
- [ ] Executed checks and remaining unknowns are reported separately.

## References

- [Windows 11 releases](https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information) and [Server releases](https://learn.microsoft.com/en-us/windows/release-health/windows-server-release-info)
- [PowerShell lifecycle](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle) and [5.1/7 differences](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell)
- [Service Control Manager](https://learn.microsoft.com/en-us/windows/win32/services/service-control-manager) and [WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
- [WSL versions](https://learn.microsoft.com/en-us/windows/wsl/compare-versions) and [execution policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies)
- [PowerShell errors](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_error_handling) and [processor architecture](https://learn.microsoft.com/en-us/windows/win32/cimwin32prov/win32-processor)
