---
name: os-debian
title: "Debian Operations"
description: "Diagnose and maintain Debian systems: release support, APT sources, package failures, service persistence, networking, and supported upgrades. Use for Debian hosts and Debian-based images."
license: Apache-2.0
compatibility: "Debian userspace; commands depend on installed tools and privileges."
domains: devops
rules:
  - content(debian)
---

## Overview

Operate Debian according to its installed release and package policy. Baseline checked 2026-09-05: Debian 13 “trixie” is stable; Debian 14 “forky” is testing. Recheck release and security notices before lifecycle decisions. Read `/etc/os-release`, package architecture, repository suites, and deployment configuration before choosing commands. Apply [shared Linux guidance](../os-linux/SKILL.md) for host/container boundaries and general service diagnostics.

## Mental model

Debian's userspace release, running kernel, package candidates, and active configuration are separate facts. A Debian container can run on another distribution's kernel. A successful package installation does not prove that a service started, uses the intended configuration, or will survive recreation.

## Releases and support

- Prefer a supported stable release for new general-purpose production deployments. Stable receives backported fixes; an older upstream version string alone does not prove a missing security fix. Check the Debian package revision and security tracker.
- Debian 13 has regular support through August 2028 and LTS through June 2030. LTS has package and architecture limits; it is not blanket coverage for every installed package. Inspect `check-support-status` when available.
- Debian 12 is in LTS; Debian 11's LTS ended 2026-08-31. Third-party extended LTS is a separate arrangement. Use published dates when a status label on an older page conflicts with the calendar.
- Pin the intended codename in managed sources. The alias `stable` moves to a new major release. Point releases collect updates within one release; they are not separate upgrade channels.

## Debian 13 compatibility changes

- `i386` now serves legacy userspace on amd64: there is no official i386 kernel or installer. Don't upgrade a standalone Debian 12 i386 system to trixie; plan an amd64 reinstall where hardware permits.
- All architectures except i386 now use 64-bit `time_t`. On `armel`/`armhf`, library ABIs changed without necessarily changing sonames. Rebuild third-party native packages and test data exchange before deployment; a binary loading successfully does not establish compatibility or rule out silent data loss.

## APT sources and transactions

- For new source entries, use deb822 `.sources` stanzas under `/etc/apt/sources.list.d/`: `Types`, `URIs`, `Suites`, `Components`, and `Signed-By`. Inspect existing `.list` files too; duplicate entries and mismatched options can break updates.
- Keep `trixie`, `trixie-updates`, and `trixie-security` coherent with the installed release; security uses the Debian security archive. Enable only required components, including `non-free-firmware` when needed. Use release-matched backports selectively; don't mix testing, unstable, Ubuntu repositories, or PPAs into stable to obtain one package.
- Scope repository trust with `Signed-By`. Package-managed keyrings belong in `/usr/share/keyrings`; operator-managed ones in `/etc/apt/keyrings`, readable by `_apt`. Obtain keys from the repository publisher and verify identity. Don't use global `apt-key` trust, `trusted=yes`, or disabled signature checks to bypass a failure.
- Use `apt` interactively and `apt-get` in scripts. Refresh indexes before resolving new installs; where supported, `apt-get update --error-on=any` makes partial download failures explicit. Stop on errors instead of silently using stale indexes or switching mirrors/releases.
- `-y` answers APT questions; `DEBIAN_FRONTEND=noninteractive` selects debconf defaults. Neither defines every conffile decision or prevents service restarts. Scope automation settings to the command and make configuration/restart policy deliberate.
- Diagnose with `apt-cache policy PACKAGE`, `apt-mark showhold`, `dpkg --audit`, and APT/dpkg logs. Review `apt-get -s` simulations before removals or dependency repairs. `dist-upgrade` may remove packages; don't use it, `autoremove`, or forced dpkg options as unexplained repairs. Never delete an active package-manager lock.

## Services, networking, and Python

- Check PID 1 before using systemd. Inspect `systemctl cat UNIT`, status, and the unit journal; use `/etc/systemd/system/UNIT.d/` overrides rather than editing packaged unit files. Reloading unit definitions does not restart a running service. Verify runtime behavior and boot enablement separately.
- Discover the manager for the affected interface: ifupdown (`/etc/network/interfaces`), NetworkManager, systemd-networkd, or image-managed configuration. Don't assume Netplan or systemd-resolved is installed. Avoid competing managers and edits to generated resolver files; temporary `ip` changes don't persist.
- Keep Debian's externally managed Python intact. Use distro packages for OS integration, virtual environments for applications, and pipx for isolated Python CLIs. Don't replace `/usr/bin/python3`, remove the external-management marker, or use `--break-system-packages` as a routine fix.

## Release upgrades

Follow the target release notes; Debian 13 supports upgrading from Debian 12, not skipping older releases. Check third-party packages, holds, disk space, backups, recovery access, and service downtime first. Apply the documented staged upgrade and review conffile changes. Verify boot, services, mounts, and application data afterward; an APT exit code alone is insufficient.

## Read-only diagnostic example

Inspect package state without refreshing indexes or changing packages:

```sh
cat /etc/os-release
dpkg --print-architecture
apt-cache policy openssl
apt-mark showhold
dpkg --audit
```

Candidates reflect cached indexes; report their freshness separately.

## Checklist

- [ ] Release, architecture, support coverage, and execution boundary are established.
- [ ] Sources and keys match the intended release; failures remain visible.
- [ ] Dependency changes, restarts, and persistent configuration match the task.
- [ ] Report observed results, changes performed, and unverified runtime behavior separately.

## References

- [Debian releases](https://www.debian.org/releases/), [security tracker](https://security-tracker.debian.org/tracker/), and [LTS package coverage](https://wiki.debian.org/LTS/Using).
- [Debian 13 ABI changes](https://www.debian.org/releases/trixie/release-notes/whats-new.html#bit-time-t-abi-transition) and [i386 restrictions](https://www.debian.org/releases/trixie/release-notes/issues.html#reduced-support-for-i386).
- [APT sources](https://manpages.debian.org/trixie/apt/sources.list.5.en.html), [apt-get](https://manpages.debian.org/trixie/apt/apt-get.8.en.html), and [debconf](https://manpages.debian.org/trixie/debconf-doc/debconf.7.en.html).
- [Debian 13 upgrade procedure](https://www.debian.org/releases/trixie/release-notes/upgrading.html) and [network configuration](https://www.debian.org/doc/manuals/debian-reference/ch05.en.html).
- [Externally managed Python](https://packaging.python.org/en/latest/specifications/externally-managed-environments/).
