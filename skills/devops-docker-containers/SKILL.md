---
name: devops-docker-containers
title: "Docker Containers: Dockerfile & Compose Hardening"
description: "Build and harden containers: Dockerfiles, multi-stage builds, Compose stacks, image scanning and non-root defaults. Use for Docker builds and failures."
license: Apache-2.0
compatibility: "Needs the Docker CLI with buildx and compose; image scanning uses Docker Scout or Trivy when installed."
domains: devops
capabilities: docker
rules:
  - match((?i)\b(dockerfile|docker[\s-]compose|compose\.ya?ml|docker\s+build|multi[\s-]stage|\.dockerignore|buildkit|docker\s+scout|trivy)\b)
  - match((?i)\b(container|image|docker)\b.{0,40}\b(too\s+big|too\s+large|slow\s+build|vulnerab\w+|cve|non[\s-]root|harden\w*|exits?|crash\w*|won'?t\s+start)\b)
  - match((?i)\b(write|build|optimi[sz]e|shrink|harden|secure|fix)\s+(an?\s+|the\s+|my\s+)?(\w+\s+){0,2}(docker\s*file|container\s+image|docker\s+image|compose\s+stack)\b)
  - semantic(make my docker image smaller and more secure)
---

## Overview

Use this skill to build, optimize and secure container images and local Compose stacks. Images are small, secure, reproducible and disposable. One concern per container, logs to stdout, state in volumes, and changes ship as a rebuild and redeploy, never as edits to a running container.

## Mental model

A container problem lives in one of three places: the build, the container runtime, or the Compose service graph. Find which before editing. The installed engine decides which behavior applies, so check it first.

## Rules

### Method

1. Inspect the relevant definitions and project conventions. Batch independent discovery and reproduce reported failures before editing.
2. Identify whether the failure is in the build, the container runtime, or the Compose service graph. Verify image tags against the registry and derive directives from the installed engine version. Inspect resulting images or Compose configuration when local tools are available. Check the non-root user, the pinned base and `.dockerignore`.
3. For multi-step interactive changes, confirm the plan. For autonomous local definition edits, record assumptions and proceed within the brief. Report the evidence and request explicit approval for production or destructive actions.

Check the live environment before applying any version fact below: `docker version`, `docker info` (image store, storage driver, cgroup version), `docker compose version`, `docker buildx version`. The installed engine wins over this list.

### Engine and registry facts (2026)

- Docker Engine 29 (29.x current): fresh installs use the containerd image store (multi-platform images and attestations kept locally); upgraded hosts may still run a graph driver. The daemon's minimum API version rose (1.44 in 29.0, back to 1.40 in 29.3), so old SDKs and CI clients can fail with API-version errors.
- containerd 2.x lowered the default container `nofile` ulimit to 1024. Databases and proxies may need `--ulimit nofile=` or `default-ulimits` in `daemon.json`.
- cgroup v1 is deprecated. The nftables firewall backend is experimental and does not enable IP forwarding for you. Docker Content Trust is gone from the CLI; sign images with cosign or Notation.
- Docker Hub limits: 100 pulls per 6 h per IP unauthenticated, 200 for Personal accounts. Authenticate CI and use a pull-through mirror.
- BuildKit is the default builder. Compose is the `docker compose` plugin; the Python `docker-compose` v1 is dead.

### Base images

- Use minimal, maintained bases: Docker Hardened Images (free and Apache-2.0 since Dec 2025), distroless, Chainguard, or `-slim`. Alpine only when musl suits the workload (native wheels, glibc-only binaries).
- Production pins a version tag plus digest: `FROM python:3.14-slim@sha256:<digest>`. Let Renovate or Dependabot bump digests. No `:latest`.
- Rebuild when the base image ships CVE fixes; `docker build --pull` refreshes it.

### Dockerfile

- Start with `# syntax=docker/dockerfile:1` and run `docker build --check` in CI.
- Order layers rarely-changing first. Copy lockfiles before source. `.dockerignore` excludes `.git`, `node_modules`, `.env` and build output. Add `.dockerignore` alongside every Dockerfile.
- Prefer cache mounts over cleanup tricks: `RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt`. For apt: `apt-get install -y --no-install-recommends ... && rm -rf /var/lib/apt/lists/*`.
- Build secrets only via `RUN --mount=type=secret,id=npmrc,target=/root/.npmrc` or `--mount=type=ssh`. ARG and ENV values persist in image history and metadata.
- Exec-form ENTRYPOINT and CMD, explicit WORKDIR, ENV for runtime and ARG for build time, `COPY --chown` and `--chmod` instead of an extra chown layer.

```dockerfile
# syntax=docker/dockerfile:1
# Node 24 = LTS line at time of writing; confirm the current LTS before pinning
FROM node:24-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build && npm prune --omit=dev

FROM node:24-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Hardening and supply chain

- Use a numeric non-root `USER` (for example 10001) so Kubernetes `runAsNonRoot` can verify it, and no SUID or SGID binaries in custom layers. At runtime: `--read-only`, `--cap-drop ALL`, `--security-opt no-new-privileges`, then add back only what is needed.
- HEALTHCHECK must use a binary the image contains (curl is absent from distroless and hardened images). Set `--start-period` for slow starters.
- Attach attestations: `docker buildx build --sbom=true --provenance=mode=max --push`. Sign and deploy by digest.
- Scan with `docker scout cves` or Trivy. For pinning scanners and CI actions, token permissions and OIDC, use the `ci-cd-pipelines` skill.
- Multi-arch: `docker buildx build --platform linux/amd64,linux/arm64`.

### Compose

- File name `compose.yaml`; the top-level `version:` key is obsolete. Validate with `docker compose config`.
- Use `depends_on` with `condition: service_healthy` plus real healthchecks, named networks that split frontend and backend, ports published on `127.0.0.1` unless external access is required, named volumes for data, bind mounts for dev source. `deploy.resources.limits` is honored by `docker compose up`.
- Secrets go through top-level `secrets:` (mounted under `/run/secrets`), not `environment:`. `.env` is for non-secret interpolation.
- Use `profiles` for optional services, `include:` for multi-file projects, `develop.watch` (`docker compose watch`) for dev sync and rebuild, and `compose.override.yaml` for local overrides.

### Operations

- Inspect with `docker history`, `docker inspect`, `docker stats`, `docker system df`, `docker compose logs -f <service>`.
- `docker system prune -af`, `docker compose down -v` and volume removal delete data. Propose them; don't run them unprompted.

### Common requests

| Request | Response |
|---|---|
| "X not working" | Clarify: build failure, runtime error, performance, or security? |
| Question | Answer directly. |
| Empty or irrelevant results twice | Stop and ask for direction. |

### Guards

- Don't reference an image, tag or base you haven't verified exists. Exact image names come from a registry or documentation lookup, not memory.
- Don't use `:latest` in production Dockerfiles.
- Don't bake secrets into images through ARG, ENV, COPY, or a RUN without a secret mount.
- Don't run containers as root unless explicitly required.
- Don't use shell-form CMD or ENTRYPOINT in production.
- Pin base images (tag plus digest) in production Dockerfiles and check the live engine version before relying on version-specific behavior.

### Scope limits

Cluster orchestration, Helm and deployments, and cloud infrastructure provisioning are not covered here. This skill builds and secures the image and the local Compose stack.

## Output format

Report in the fewest words that carry the evidence: for example "Image built. 3 layers. 45MB. No critical CVEs." No explanations unless asked, and no duplicated docker output.

## Checklist

- [ ] The engine and Compose versions were read from the live environment.
- [ ] Base image is minimal, pinned by tag and digest, and exists in the registry.
- [ ] Final stage runs as a numeric non-root user.
- [ ] No secret reaches ARG, ENV, COPY or an unmounted RUN.
- [ ] `.dockerignore` exists beside the Dockerfile.
- [ ] Image scan result is reported.
- [ ] Destructive cleanup commands were proposed, not run.

## Composition / References

- `infrastructure-change` covers the shared plan-and-verify procedure.
- `ci-cd-pipelines` covers pinning scanners and CI trust setup.
- `devops-kubernetes-operations` covers running the image on a cluster.
