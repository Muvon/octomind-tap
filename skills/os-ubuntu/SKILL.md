---
name: os-ubuntu
title: "Ubuntu Operations"
description: "Diagnose and maintain Ubuntu systems: LTS support, APT repositories, phased updates, Netplan, package isolation, service persistence, and release upgrades."
license: Apache-2.0
compatibility: "Ubuntu userspace; commands depend on installed tools and privileges."
domains: devops
rules:
  - content(ubuntu)
---

## Overview

Operate the installed Ubuntu release using its supported repositories and management tools. Baseline checked 2026-09-05: Ubuntu 26.04 LTS “Resolute Raccoon” is current; recheck release status before lifecycle decisions. Read `/etc/os-release`, package architecture, image definition, and repository configuration. Apply [shared Linux guidance](../os-linux/SKILL.md) for host/container boundaries and general service diagnostics.

## Mental model

Ubuntu release, kernel flavour, package channel, and subscription coverage are independent. A newer HWE kernel does not upgrade the userspace release. An Ubuntu container may share another distribution's kernel and lack systemd. Diagnose the running service and its persistent configuration separately from installed package state.

## Releases and coverage

- LTS releases receive five years of standard security maintenance; interim releases receive nine months. Ubuntu 26.04 LTS has standard maintenance through May 2031. An LTS point release refreshes media and accumulated updates; it is not a new release series.
- Check coverage by package/component. Standard maintenance does not mean every Universe package is covered. Ubuntu Pro adds ESM coverage for eligible Main/Universe packages; the Legacy add-on extends eligible coverage further. Subscription entitlement and enabled services must be verified, not inferred from the Ubuntu version.
- Ubuntu 25.10's support ended in July 2026. Recheck interim-release and flavour-specific support; an old article calling a release newest is insufficient.

## Ubuntu 26.04 compatibility changes

- `sudo-rs` is the default sudo provider, introduced in 25.10. Check installed options and sudoers support before reusing advanced policy or Expect automation: prompts differ, and logging/LDAP features are not interchangeable with `sudo.ws`. Preserve required controls rather than silently switching providers.
- Many core commands now come from `rust-coreutils`; GNU compatibility is incomplete, and `cp`, `mv`, and `rm` remain GNU in the documented default set. Inspect the actual command provider and test relied-on flags/output; use a documented `gnu`-prefixed command only for an explicit compatibility need, not an automatic global replacement.

## Repositories and package failures

- Ubuntu 24.04+ defaults to deb822 `/etc/apt/sources.list.d/ubuntu.sources`: `Types`, `URIs`, `Suites`, `Components`, `Signed-By`. Inspect retained `.list` files too.
- Keep suites tied to the installed codename: release, `-updates`, and `-security`, with optional `-backports` for an identified need. Match mirrors to architecture; don't replace a ports mirror with an amd64 archive blindly. Don't mix Debian packages, another Ubuntu series, or `-proposed` into routine production sources.
- Use per-repository `Signed-By`: `/usr/share/keyrings` for package-managed keys, `/etc/apt/keyrings` for operator-managed keys, readable by `_apt`. Verify publisher identity and supported series for third-party repositories or PPAs. Don't bypass errors with global `apt-key` trust, `trusted=yes`, disabled TLS verification, or unsigned packages.
- Use `apt` interactively and `apt-get` in scripts. Refresh package indexes successfully before installs; preserve update failures instead of falling back to stale metadata. `-y` and command-scoped `DEBIAN_FRONTEND=noninteractive` do not resolve every conffile decision or prevent service restarts.
- Diagnose candidates with `apt-cache policy PACKAGE`, holds with `apt-mark showhold`, and incomplete transactions with `dpkg --audit`. Read `/var/log/apt/history.log`, `/var/log/apt/term.log`, and `/var/log/dpkg.log`. Don't delete active locks or force unexplained dependency repairs.
- Kept-back packages may reflect phased updates, explicit holds, or dependency constraints. Confirm the cause before acting; security updates are not phased. Don't routinely bypass phasing. A release-upgrade procedure may require installing phased updates first; follow that documented exception deliberately.

## Network and service persistence

- Netplan is the configuration frontend; discover whether NetworkManager or systemd-networkd manages the interface. Inspect `/etc/netplan/` and image/cloud-init ownership. Don't edit generated backend files or run competing managers on the same interface.
- Before remote network changes, retain recovery access. `netplan try` applies a temporary configuration pending confirmation; it is not read-only validation. Verify rollback after timeout because known cases may not revert fully. Confirm on-disk configuration before rebooting.
- Inspect resolver ownership before changing DNS; a generated `/etc/resolv.conf` is not the durable source. Verify address, route, and name resolution separately.
- On systemd hosts, inspect the effective unit and journal; put overrides under `/etc/systemd/system/UNIT.d/`. A definition reload does not restart the service. Verify health, startup enablement, and data mounts independently. Diagnose AppArmor/firewall denials rather than disabling protection globally.
- Preserve externally managed system Python. Use distro packages for OS integration, virtual environments for applications, and pipx for CLI isolation; don't replace system Python or bypass PEP 668 as a routine installation fix.

## Release upgrades

Use `do-release-upgrade` for supported server/cloud release transitions, not codename substitution in sources. Follow the supported sequential or next-LTS route and release notes. LTS-to-LTS availability normally follows the first point release; don't use `-d` to bypass production rollout gates. Review backups, disk space, third-party packages, conffile decisions, and recovery access; verify services and data after the required reboot.

## Read-only diagnostic example

Inspect userspace, package origin, and transaction state without updating indexes:

```sh
cat /etc/os-release
dpkg --print-architecture
apt-cache policy openssh-server
apt-mark showhold
dpkg --audit
```

The package candidate uses cached indexes; it does not establish current security coverage.

## Checklist

- [ ] Release, architecture, deployment boundary, and package coverage are known.
- [ ] Repository trust and package-selection causes are verified; errors remain visible.
- [ ] Network/service changes persist through the relevant restart or recreation.
- [ ] Report changes, observed results, and outstanding verification separately.

## References

- [Ubuntu lifecycle](https://ubuntu.com/about/release-cycle) and [release list](https://ubuntu.com/project/docs/release-team/list-of-releases/).
- [26.04 changes for LTS users](https://documentation.ubuntu.com/release-notes/26.04/summary-for-lts-users/) and [sudo-rs compatibility](https://ubuntu.com/server/docs/reference/other-tools/sudo-rs/).
- [Package management](https://ubuntu.com/server/docs/how-to/software/package-management/), [third-party repositories](https://ubuntu.com/server/docs/explanation/software/third-party-repository-usage/), and [phased updates](https://ubuntu.com/server/docs/about-apt-upgrade-and-phased-updates/).
- [Network configuration](https://ubuntu.com/server/docs/explanation/networking/configuring-networks/) and [Netplan try caveats](https://netplan.readthedocs.io/en/stable/netplan-try/).
- [Release upgrades](https://ubuntu.com/server/docs/how-to/software/upgrade-your-release/) and [externally managed Python](https://packaging.python.org/en/latest/specifications/externally-managed-environments/).
