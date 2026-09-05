---
name: os-linux
title: "Linux Operations Foundation"
description: "Identify and operate Linux hosts, VMs, and containers: distro and ABI boundaries, services, resource limits, networking, and evidence-based recovery."
license: Apache-2.0
compatibility: "A Linux target and its available administration tools; target access may be local or remote."
domains: devops
rules:
  - content(linux)
  - content(alpine)
  - content(musl)
  - content(rhel)
  - content(redhat)
  - content(red) content(hat)
  - content(fedora)
  - content(debian)
  - content(ubuntu)
---

## Overview

Use for Linux administration, troubleshooting, and deployment work. Establish what system the commands will affect, then use its distribution guide for package and release details. This foundation covers shared operational contracts, not a universal installer.

## Mental model

Kernel, distribution userspace, libc, service manager, and deployment boundary are separate facts. A container shares a kernel while carrying different userspace; its root user, filesystem, and resource limits need not describe the host.

## Identify the target

- Guidance checked 2026-09-05 against current kernel and systemd documentation. Distribution-supported kernels often backport fixes; an older upstream version string alone does not prove an unpatched vulnerability. Check the vendor advisory and installed package revision.
- Record the target host/container, effective identity, distribution `ID`/`VERSION_ID`, architecture, libc, init/service manager, and deployment mode before changing state. The workstation running the assistant is not necessarily the target.
- Read `/etc/os-release`, or `/usr/lib/os-release` only when the former is absent. Do not merge both files. `ID_LIKE` suggests ancestry, not interchangeable repositories or upgrade paths.
- `uname` reports the running kernel and machine architecture, not the distribution release, package architecture, CPU feature baseline, or glibc/musl ABI. Inspect the artifact and target before selecting binaries.
- Check PID 1, mounts, namespaces, and the runtime's metadata. A present `systemctl` binary does not prove systemd is managing this environment. WSL, containers, chroots, image builds, and full hosts have different lifecycle owners.

## Services and configuration

- Use the active manager: systemd, OpenRC, or the container supervisor. Don't install another init system merely because a familiar command fails.
- On systemd, inspect the exact unit and its drop-ins with `systemctl cat`/`show`, plus bounded `journalctl -u` output. Check the correct system or user manager; service names vary by distro.
- Keep site overrides in supported configuration/drop-in locations instead of editing vendor files. Validate application configuration before activating it.
- `daemon-reload` rereads systemd units; service `reload` rereads application configuration only when supported; `restart` stops and starts the service. `enable` changes boot activation and does not itself start the service. Choose the operation the change needs.
- A process being active or a port listening is not application readiness. Verify the original symptom, dependency behavior, and an appropriate health request after a change.

## Resource and network diagnosis

- Identify the process's actual cgroup before interpreting memory or CPU pressure. On cgroup v2, inspect effective limits and relevant `memory.events`, `memory.current`, `memory.max`, and `cpu.stat`; ancestor limits also apply. Host-wide free memory does not rule out a container OOM.
- Use pressure-stall information when available to distinguish resource stalls from simple utilization. Correlate events over time; one CPU or memory snapshot is weak evidence.
- Check both filesystem space and inodes, mount options, quotas, and deleted-but-open files. `du` and `df` answer different questions. Don't delete logs, volumes, or caches indiscriminately to make a metric look healthy.
- Separate listener, DNS, routing, firewall, TLS, and upstream failure. Use the target's network namespace and resolver configuration; public DNS success does not prove application resolution works.
- Identify the owning network/firewall stack before edits: NetworkManager, networkd, Netplan, firewalld, nftables, or another manager. Editing a generated file or an underlying ruleset can be overwritten or conflict with its owner. Preserve a recovery path when changing remote connectivity.

## Changes and failure contracts

- Keep package sources, signing trust, architecture, and release consistent. Installed state differs from fresh repository metadata; report which evidence a query used. Do not bypass signature checks or mix release repositories to satisfy a missing dependency.
- Diagnose Unix permissions, ACLs, mount restrictions, capabilities, and SELinux/AppArmor policy separately. Don't replace a precise fix with `chmod -R 777`, privileged containers, or disabled enforcement.
- Match shell syntax and utilities to the target. BusyBox and GNU flags differ; `sh` is not necessarily Bash. Preserve command exit status and stderr instead of chaining unrelated fallback commands until one succeeds.
- Work within the authorized target and change scope. Before a disruptive change, establish the affected service/data, configuration owner, rollback or recovery method, and verification. A snapshot is not a proven application-consistent backup; package rollback does not reverse a data migration.

## Example

Read identity inside the intended Linux target, with `/proc` mounted:

```sh
set -eu
if [ -r /etc/os-release ]; then
    cat /etc/os-release
elif [ ! -e /etc/os-release ] && [ -r /usr/lib/os-release ]; then
    cat /usr/lib/os-release
else
    printf '%s\n' 'OS identity unavailable; do not guess a distribution.' >&2
    exit 1
fi
uname -sr
uname -m
cat /proc/1/comm
cat /proc/self/cgroup
```

This identifies context; it does not prove the target is the host or a service is healthy. Missing tools, denied access, and absent procfs data remain explicit evidence gaps.

## Checklist

- [ ] Target, userspace, ABI, manager, and host/container boundary are established.
- [ ] Diagnosis cites actual evidence and distinguishes uncertainty from absence.
- [ ] Proposed changes preserve package trust, security controls, data, and remote access.
- [ ] Verification checks the original behavior; unexecuted checks are stated.

## References

- [OS identity format](https://manpages.debian.org/trixie/systemd/os-release.5.en.html), [systemctl semantics](https://manpages.debian.org/trixie/systemd/systemctl.1.en.html).
- [Kernel cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html), [systemd delegation](https://systemd.io/CGROUP_DELEGATION/), [pressure-stall information](https://docs.kernel.org/accounting/psi.html).
- [Container resource limits](https://docs.docker.com/engine/containers/resource_constraints/).
- Distribution-specific operations: [Alpine](../os-alpine/SKILL.md), [RHEL](../os-rhel/SKILL.md), [Fedora](../os-fedora/SKILL.md), [Debian](../os-debian/SKILL.md), [Ubuntu](../os-ubuntu/SKILL.md).
