---
name: os-fedora
title: "Fedora Operations"
description: "Diagnose and maintain Fedora systems with release-aware DNF5, Atomic deployment, SELinux, networking, and rootless container guidance."
license: Apache-2.0
compatibility: "Requires access to the target Fedora system or its configuration and logs; administrative changes require appropriate privileges."
domains: devops
rules:
  - content(fedora)
  - content(silverblue)
  - content(kinoite)
---

## Overview

Research baseline: 2026-09-05, Fedora Linux 44 stable; Fedora 45 remains prerelease. Recheck release status before upgrades. Apply the [Linux baseline](../os-linux/SKILL.md) for shared host/container, systemd, and resource diagnostics.

## Mental model

Fedora is a short-lifecycle distribution with multiple deployment models. Identify the installed edition, release, repository/image origin, and booted deployment before choosing commands. Traditional RPM hosts, Atomic desktops, CoreOS, and bootc-derived images do not share one universal update procedure.

## Releases and DNF5

- Fedora releases receive approximately thirteen months of updates. Check the target's support status rather than assuming an installed release remains maintained. Rawhide, Branched, beta, and updates-testing are separate development/testing choices, not repair repositories.
- Traditional Fedora uses DNF5 by default since Fedora 41. Check `dnf --version` and installed command help; DNF4 Python APIs, plugins, options, and history behavior are not interchangeable with DNF5.
- Query installed packages and enabled repository configuration before a transaction. Preserve signatures, release matching, and intentional third-party sources. A missing dependency is a reason to inspect provenance and availability, not mix Fedora versions or RHEL/EPEL packages.
- DNF5 `check-upgrade` returns 100 when upgrades are available and 0 when none are found. Treat real errors separately; `|| true` hides failed checks. Repository queries may refresh metadata, so prefer installed-package queries for strictly local inventory.
- Major release upgrades use the documented upgrade workflow, not a routine package refresh. Review proposed removals and third-party compatibility; flags such as `--allowerasing` can change the outcome substantially.
- Keep a known bootable kernel/deployment and account for out-of-tree module compatibility when planning updates. Do not remove older kernels or disable Secure Boot simply because a driver failed to load.

## Atomic and image deployments

- Fedora Atomic Desktop 44 still documents rpm-ostree layering; bootable-container work does not mean every installation has switched to bootc. Inspect `rpm-ostree status` and, where available, `bootc status --format=json` before choosing a mutation tool.
- An installed bootc binary alone is not deployment evidence. Inspect the booted image and any incompatibility flag; layered packages can require rpm-ostree for mutations even when bootc is present.
- For an rpm-ostree deployment, distinguish booted, pending, and rollback deployments. Package layering creates a new deployment; do not repeatedly reinstall into the running root because the pending change is not yet active.
- For an image-managed deployment, update the intended image source/digest through its existing pipeline. Do not convert the machine's update model or switch its image origin as incidental troubleshooting.
- Use Flatpak for suitable desktop applications and Toolbx/containers for development dependencies where that matches the deployment. Reserve host layering for software that needs host integration. Toolbx is an integrated environment, not a strong sandbox for untrusted code.
- Rollback restores OS deployment content, not arbitrary user/database data. Persistent `/var` state is shared across deployments; schema migrations and application downgrades need their own compatibility plan.
- A read-only system path may be intentional. Modify image/build configuration or supported persistent configuration rather than remounting the system writable to bypass its model.

## Diagnose the failing layer

- Query NetworkManager's active profile, routes, and DNS ownership before changing settings. A profile edit does not necessarily alter the currently active connection; protect remote management access when applying changes.
- Correlate application logs with SELinux AVC records, ownership, mount flags, and file labels. Fix a documented label/boolean/port mismatch when justified; do not disable SELinux, firewalling, or signature verification as a default remedy.
- For rootless Podman, inspect the user's storage, UID mapping, volume labels, and cgroup delegation. Sudo selects a different container context, not a transparent permission fix.
- Check the installed runtime and network backend rather than importing older Docker/CNI recipes. Confirm service restart behavior and persistent volumes independently of a successful container start.

## Diagnostic example

Read-only local inventory on a Fedora host with these utilities installed:

```sh
cat /etc/os-release
uname -r
rpm -q fedora-release dnf5 rpm-ostree bootc
findmnt /
nmcli connection show --active
getenforce
```

An absent package is evidence, not an instruction to install it. Inspect deployment status next only with the relevant installed tool; retain failures rather than silently selecting another updater.

## Checklist

- Confirm supported release and stable versus development content.
- Identify traditional or image deployment and the actual booted/pending state.
- Preserve package/image provenance and review transaction removals.
- Diagnose security, network, and rootless permissions without blanket bypasses.
- State what was observed, what changed, and whether reboot, rollback, and application behavior were verified.

## References

- [Fedora 44 release](https://fedoramagazine.org/announcing-fedora-linux-44/) and [release support duration](https://fedoraproject.org/workstation/)
- [Fedora 45 scheduled milestones](https://fedoraproject.org/wiki/I18N/Meetings/2026-08-17)
- [Fedora's DNF5 transition](https://fedoraproject.org/wiki/Changes/SwitchToDnf5)
- [DNF5 reference](https://dnf5.readthedocs.io/en/latest/dnf5.8.html) and [check-upgrade exit status](https://dnf5.readthedocs.io/en/latest/commands/check-upgrade.8.html)
- [Atomic Desktop 44 deployment status](https://fedoramagazine.org/whats-new-fedora-atomic-desktops-in-fedora-linux-44/)
- [bootc deployment detection](https://bootc.dev/bootc/man/bootc-status.8.html) and [persistent filesystem semantics](https://bootc.dev/bootc/filesystem.html)
- [NetworkManager](https://networkmanager.dev/docs/api/latest/nmcli.html) and [rootless Podman](https://docs.podman.io/en/latest/markdown/podman.1.html)
- [Toolbx host integration](https://containertoolbx.org/)
