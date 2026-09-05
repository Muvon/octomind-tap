---
name: os-alpine
title: "Alpine Linux Operations"
description: "Operate Alpine hosts and images with musl ABI awareness, apk repository discipline, OpenRC services, and persistent configuration."
license: Apache-2.0
compatibility: "An Alpine Linux target with its installed apk/BusyBox tools; OpenRC applies to booted systems that use it."
domains: devops
rules:
  - content(alpine)
  - content(musl)
---

## Overview

Use for Alpine Linux systems, container images, and Alpine-related musl compatibility issues. Read the [Linux foundation](../os-linux/SKILL.md) for target identification and shared diagnostic contracts. Musl is a C library, not a distribution; a musl binary does not prove the target is Alpine.

## Mental model

Alpine combines musl libc, BusyBox utilities, apk packages, and normally OpenRC on booted hosts. A small image trades GNU/glibc assumptions for different interfaces; making it behave like another distribution through compatibility patches is not automatically the simplest solution.

## Release and current changes

- Verified 2026-09-05: Alpine 3.24 is the current stable branch; `edge` is rolling development. Check the release table again before selecting a base image or upgrade path.
- Support differs by repository: `main` is typically supported for two years, while `community` is supported until the next stable release. An otherwise supported branch can contain community packages that no longer receive that coverage.
- Alpine 3.23 introduced apk-tools v3. Check `apk --version` and local help before relying on newer commands, configuration, or parsed output; apk tool version and repository/package format version are different facts.
- Alpine 3.24 deprecates `qemu-binfmt` in favor of user-mode QEMU `binfmt.d` configuration and the `binfmt` service. For emulation failures, check installed registration and host ownership rather than starting the obsolete service.
- Its setuptools 82 package removes `pkg_resources`; a tool broken after upgrading may need a supported dependency/code update, not a system-wide Python downgrade.

## ABI and tool compatibility

- Prefer musl-compatible artifacts or build against the actual target. A glibc-linked executable can report “not found” even when the file exists because its ELF interpreter is unavailable. Inspect architecture and ELF interpreter/dependencies with trusted inspection tools before diagnosing PATH.
- `gcompat` implements a subset of glibc-compatible APIs; it is not a replacement glibc installation or a guarantee that arbitrary vendor binaries work. If upstream supports only glibc, a supported glibc-based image may be the correct deployment choice. Don't invent loader symlinks or fetch unofficial libc packages to suppress an error.
- BusyBox `sh` is normally ash. Check applet help; don't assume Bash syntax or GNU options for `sed`, `date`, `find`, or `ps`. Add a declared tool dependency only when the operation requires it.
- Check Python wheel/native-addon availability for musl and the target architecture. A smaller base image can trigger source builds and additional build dependencies; judge the complete deliverable, not only compressed base size.

## apk and repository state

- Inspect `/etc/apk/repositories`, `/etc/apk/world`, installed versions, and package policy. Keep repositories on the same stable branch; `testing` belongs to edge. Don't combine stable and edge as a generic missing-package fallback.
- World records requested package constraints, not just installed files. Resolve conflicts against those constraints; don't use force flags that discard requirements merely to make the solver succeed.
- `apk update` refreshes indexes; `apk upgrade` changes installed packages. Review branch-upgrade instructions separately: `--available` reconciles against available repository versions and can downgrade packages. It is not a harmless diagnostic flag.
- Keep package signing enabled. Investigate keys, clock, index freshness, mirrors, and branch consistency on verification failure. Do not routinely use `--allow-untrusted` or turn HTTPS verification off.
- For images, declare runtime packages explicitly and isolate build dependencies in a stage or a named virtual dependency group. Removing a build group must leave required shared libraries available. Treat an image's mutable tag and immutable digest differently; rebuild deliberately for security updates.
- Preserve modified configuration and review `.apk-new` files. A successful package transaction does not show that a daemon loaded the intended configuration.

## Services and persistence

- On an OpenRC host, use `rc-service name status`, `rc-status`, and `rc-update show` to inspect state. Starting a service now differs from adding it to a runlevel; inspect `/etc/init.d` and `/etc/conf.d` for the actual service configuration.
- OpenRC defaults to cgroup v2 in Alpine 3.19+; user services are available in 3.22+. Check the actual manager and cgroup setup rather than translating systemd commands mechanically. Ordinary Alpine containers often have no OpenRC boot lifecycle.
- Distinguish disk-backed installations from diskless/data modes. For diskless setups, inspect `lbu` inclusion and persistence configuration; approved changes may need `lbu commit` and package-cache handling to survive reboot. This overlay is not automatically a backup of all application data.
- Before a host release upgrade, review bootloader and filesystem notes and establish recovery access. GRUB updates can require installation to the actual boot device/EFI target; do not copy a generic device path into a command.

## Example

Read Alpine package identity without refreshing indexes or changing packages:

```sh
set -eu
cat /etc/alpine-release
apk --version
apk --print-arch
apk info -v musl busybox apk-tools
apk policy musl
```

Policy reflects available local metadata; it is not evidence that repositories were refreshed or the package is the latest security revision.

## Checklist

- [ ] Branch, repository support, architecture, libc, and apk version are identified.
- [ ] Binary and shell assumptions fit musl/BusyBox; compatibility failures stay visible.
- [ ] Package constraints, trust, runtime dependencies, and configuration are preserved.
- [ ] Init and persistence match the deployment mode; verification limits are stated.

## References

- [Release support](https://alpinelinux.org/releases/) and [3.24 release announcement](https://lists.alpinelinux.org/~alpine/announce/%3C20260609230455.2543c365%40ncopa-desktop.lan%3E).
- [apk behavior](https://wiki.alpinelinux.org/wiki/Alpine_Package_Keeper), [package/repository model](https://docs.alpinelinux.org/user-handbook/0.1a/Working/apk.html).
- [glibc compatibility](https://wiki.alpinelinux.org/wiki/Running_glibc_programs), [BusyBox](https://wiki.alpinelinux.org/wiki/BusyBox).
- [OpenRC](https://wiki.alpinelinux.org/wiki/OpenRC) and [diskless persistence](https://wiki.alpinelinux.org/wiki/Alpine_local_backup).
