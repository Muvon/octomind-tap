---
name: os-rhel
title: "RHEL Operations"
description: "Diagnose and maintain Red Hat Enterprise Linux hosts and images with release-aware repositories, networking, SELinux, and container operations."
license: Apache-2.0
compatibility: "Requires access to the target RHEL system or its configuration and logs; administrative changes require appropriate privileges."
domains: devops
rules:
  - content(rhel)
  - content(redhat)
  - content(red) content(hat)
---

## Overview

Apply RHEL-specific operational rules after establishing the target environment. Research baseline: 2026-09-05, RHEL 10.2 stable; maintained older branches require their own documentation. Use the [Linux baseline](../os-linux/SKILL.md) for shared host/container, systemd, and resource diagnostics. Do not infer that a compatible derivative, Fedora installation, or UBI container has RHEL host support or identical tooling.

## Mental model

The installed major/minor release, architecture, content source, and deployment mode jointly define what is supported. Diagnose the failing layer before changing it: registration is not repository availability, a denied file access is not necessarily Unix permissions, and a container's userspace is not its host kernel.

## Release and content boundaries

- RHEL 10 minimum architecture levels are x86-64-v3, ARMv8.0-A, little-endian POWER10, and IBM Z z15. Verify actual CPU features exposed to a VM before upgrading; an `x86_64` label alone is insufficient. Treat RISC-V developer previews separately from supported production architectures.
- Identify package mode versus an image-managed deployment before proposing updates. Package-mode hosts use DNF transactions; image-mode hosts follow their bootc/image pipeline. Having DNF installed does not authorize changing the running image.
- RHEL 10 ships DNF 4, unlike current Fedora's DNF 5. Check `dnf --version` and installed help before reusing plugins, flags, or automation.
- BaseOS and AppStream form the normal content foundation. Application Streams can expire before the OS; inspect the selected runtime's lifecycle separately. RHEL 10 distributes no modular AppStream content, so old `dnf module enable` recipes do not select its language runtimes.
- For missing packages or CDN failures, inspect the target's registration, enabled repository IDs, release locks, architecture, and content source, including Satellite or cloud RHUI where applicable. Do not disable subscription plugins, mix another major release, or add Fedora repositories to make resolution succeed.
- Evaluate CodeReady Linux Builder and external repositories explicitly. Availability in CRB does not imply Red Hat support for its packages. Preserve package signatures and repository provenance.
- UBI provides redistributable images and a public package subset, not every RHEL package or host entitlement. Check whether a build used subscription-only repositories before claiming it is freely redistributable. Minimal UBI uses `microdnf`; do not assume systemd, Python, or full diagnostic utilities are present.

## Networking and access failures

- Use NetworkManager connection profiles and `nmcli`; RHEL 10 removed ifcfg-format support and `dhclient`. Inspect active profile, address, route, and DNS ownership before editing generated files.
- For remote connection changes, account for the management route and a recovery path. A persistent profile change and the active device configuration can differ; verify both.
- Inspect service logs and SELinux AVC records alongside ownership, mode, mounts, and labels. Correct the path's persistent file-context mapping, intended port type, or documented boolean when evidence supports it. Do not disable SELinux or generate a broad allow policy as the first fix.
- Separate listening address, firewall zone/rules, routing, DNS, and TLS errors. Keep firewalld runtime and permanent configuration consistent for the intended persistence; opening a port cannot fix a process that never bound it.

## Containers and lifecycle

- RHEL 10 boots with cgroup v2. Check the actual controller/delegation setup before applying resource-limit advice from older hosts.
- Rootless Podman state belongs to its user; running the same command with sudo selects different storage and containers. Check UID mappings, bind-mount labels, and user-service lifetime instead of escalating containers to privileged mode.
- Current RHEL 10 defaults include Netavark, pasta for rootless networking, and crun. Older CNI/runc instructions require a planned migration, not an improvised runtime fallback.
- Use the deployment's existing systemd/Quadlet conventions for persistent services. A running container is not proof of restart behavior, health, or durable data placement.

## Diagnostic example

Read-only inventory on a RHEL host with these tools installed:

```sh
cat /etc/os-release
uname -m
lscpu
rpm -q redhat-release dnf NetworkManager selinux-policy
nmcli connection show --active
getenforce
findmnt -t cgroup2
```

Retain missing-package and permission diagnostics; do not install utilities or suppress failures just to complete the inventory.

## Checklist

- Confirm release, CPU baseline, host/container scope, and deployment mode.
- Verify repository provenance, access mechanism, and component support lifetime.
- Diagnose network ownership and SELinux denials before changing policy.
- Check reboot, user-service, and persistent-data consequences of authorized changes.
- Report observed evidence, the exact proposed/applied change, and any unverified recovery or runtime behavior.

## References

- [RHEL 10.2 release](https://www.redhat.com/en/blog/rhel-102-and-98-intelligent-evolution-enterprise-linux)
- [RHEL 10 architecture and migration changes](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/considerations_in_adopting_rhel_10/index)
- [DNF and content management](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/managing_software_with_the_dnf_tool/index)
- [Current UBI 10 DNF packages](https://cdn-ubi.redhat.com/content/public/ubi/dist/ubi10/10/x86_64/baseos/os/Packages/d/)
- [UBI content and redistribution](https://developers.redhat.com/articles/ubi-faq)
- [RHEL container management](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/building_running_and_managing_containers/index)
- [SELinux diagnosis](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html-single/using_selinux/index)
- [NetworkManager command reference](https://networkmanager.dev/docs/api/latest/nmcli.html)
