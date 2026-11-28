---
name: devops-kubernetes-operations
title: "Kubernetes Operations: kubectl, Helm & Manifests"
description: "Manage Kubernetes workloads with kubectl and Helm: deployments, services, RBAC, network policies, autoscaling and cluster debugging."
license: Apache-2.0
compatibility: "Needs kubectl access to a cluster and, for charts, Helm; manifest validation uses kubeconform when installed."
capabilities: kubernetes codesearch-structural codesearch-graph
rules:
  - match((?i)\b(kubectl|helm|kustomize|kubeconform|argo\s*cd|fluxcd?|gateway\s+api|ingress|configmap|statefulset|daemonset|network\s*polic\w+|poddisruptionbudget)\b)
  - match((?i)\b(kubernetes|k8s|k3s|eks|gke|aks)\b.{0,60}\b(deploy\w*|cluster|pods?|manifests?|rbac|autoscal\w+|hpa|upgrade|rollout|namespace)\b)
  - match((?i)\b(crashloopbackoff|imagepullbackoff|oomkilled|pending\s+pods?|evicted)\b)
  - semantic(my pods keep restarting in the cluster)
---

## Overview

Use this skill for Kubernetes day-2 work: kubectl and Helm operations, deployments, services, ingress and Gateway API, config and secrets, RBAC, network policies, storage, autoscaling and production cluster operations. Manifests should be easy to understand, modify and debug. Pragmatic means delivering value without creating technical debt.

## Mental model

The cluster is the source of live facts and the repository is the source of intent. Check the live cluster before applying any version fact, confirm the context and namespace before any mutation, and keep one source of truth per object (GitOps).

## Rules

### Method

1. Inspect the relevant definitions and project conventions. Batch independent discovery and reproduce reported failures before editing.
2. Confirm the current cluster context and namespace before operations. Prefer versioned declarative manifests for workloads. Check resource requests, probes, least-privilege RBAC and network policy. Render or validate manifests locally, then review the target and proposed changes before a cluster mutation.
3. For multi-step interactive changes, confirm the plan. For autonomous local definition edits, record assumptions and proceed within the brief. Report the evidence and request explicit approval for production or destructive actions.

Check the live cluster before applying any version fact below: `kubectl version` (client within one minor of the server), `kubectl api-resources`, deprecation warnings in command output, and the managed provider's supported versions, which lag upstream.

### Platform facts (2026)

- Upstream supports the newest three minors: 1.37 (Aug 2026), 1.36, 1.35. 1.34 reached end of life on 2026-10-27; 1.38 is planned for 2026-12-16.
- The ingress-nginx controller was retired in March 2026 and gets no security fixes. Put new HTTP routing on Gateway API (v1.5 standard channel: Gateway, HTTPRoute, GRPCRoute, TLSRoute, ListenerSet) through a maintained implementation, and migrate existing Ingress objects with ingress2gateway. The Ingress API remains but is feature-frozen.
- Nodes need cgroup v2: since 1.35 the kubelet refuses to start on cgroup v1 by default. kube-proxy IPVS mode is deprecated in favor of nftables mode. kube-dns is being retired for CoreDNS.
- Helm 4 (Nov 2025) is current: server-side apply for new releases, `--atomic` became `--rollback-on-failure`, `--force` became `--force-replace`, post-renderers are plugins. Helm 3 gets security fixes only until 2027-02-10.
- Stable features to use: native sidecars (init containers with `restartPolicy: Always`, 1.33) and in-place Pod resize (1.35). HPA scale-to-zero is beta in 1.37.

### Workloads

- Deployments for stateless, StatefulSets for stateful. Set `revisionHistoryLimit` and rolling-update `maxSurge` and `maxUnavailable` deliberately.
- Requests on every container. Memory limit equal to the request for predictable OOM behavior. CPU limits only when a hard cap is required, since they throttle.
- readinessProbe gates traffic, livenessProbe stays cheap and free of dependency checks, startupProbe covers slow starts.
- HA: two or more replicas, a PodDisruptionBudget, and `topologySpreadConstraints` across zones and nodes.
- Autoscaling: HPA on CPU or custom metrics; VPA or in-place resize for right-sizing. Don't run HPA and VPA on the same resource metric.

### Security

- Label namespaces with Pod Security Admission `restricted`. securityContext: `runAsNonRoot`, `readOnlyRootFilesystem`, `allowPrivilegeEscalation: false`, capabilities drop ALL, `seccompProfile: RuntimeDefault`.
- `automountServiceAccountToken: false` unless the pod calls the API. Roles scoped to a namespace before ClusterRoles. No wildcard verbs.
- Default-deny NetworkPolicy per namespace, then explicit allows (including DNS egress).
- Secrets come from External Secrets Operator or the Secrets Store CSI driver, with encryption at rest enabled. Secrets in Git only encrypted (SOPS, Sealed Secrets). Reference images by digest.

### Delivery and validation

- GitOps (Argo CD or Flux) with Kustomize overlays or Helm charts; one source of truth per object.
- Before applying: `kubectl diff -f`, `kubectl apply --server-side --dry-run=server -f`, `helm template | kubeconform`, `helm lint`.
- Add a service mesh only when mTLS or traffic policy needs justify the operational cost.

### Debugging

`kubectl get` and `describe`, `kubectl events --for <kind>/<name>`, `kubectl logs --previous`, `kubectl debug` (ephemeral containers) for distroless pods, `kubectl rollout status|history|undo`, `kubectl top`.

### Implementation principles

KISS, DRY through Kustomize or Helm rather than copy-paste, YAGNI, no dead manifests, named values in ConfigMaps instead of magic numbers, comments that explain why, fail fast through probes and validation, and clarify unclear intent instead of assuming.

### Common requests

| Request | Response |
|---|---|
| Question | Answer directly. |
| Ambiguous | Ask one clarifying question. |
| Empty or irrelevant results twice | Stop and ask for direction. |

### Guards

- Don't run a mutating kubectl or helm command before confirming the current context and namespace match the intended cluster.
- Don't reference a Helm chart, repo, image or API version you haven't verified exists. Exact names come from a registry or documentation lookup, not memory.
- Don't propose a root cause you cannot trace directly.
- Don't implement multi-step interactive work before confirming the plan.
- Don't add unrequested features or create documentation files unless asked.

### Scope limits

Authoring the container image and local Compose stacks, and provisioning the cloud infrastructure the cluster runs on, are not covered here. This skill orchestrates workloads on the cluster.

## Output format

Report in the fewest words that carry the evidence: for example "Deployment ready. 3 replicas running." No explanations unless asked, and no duplicated kubectl output.

## Checklist

- [ ] Context and namespace were confirmed before any mutation.
- [ ] Version facts were checked against the live cluster.
- [ ] Manifests have requests, probes, a security context and a default-deny policy.
- [ ] `kubectl diff` or a server-side dry run was reviewed before apply.
- [ ] Chart, image and API names were verified, not recalled.
- [ ] Production or destructive actions have explicit approval.

## Composition / References

- `infrastructure-change` covers the shared plan-and-verify procedure.
- `devops-docker-containers` covers building and hardening the image.
- `devops-incident-response` covers live incidents.
