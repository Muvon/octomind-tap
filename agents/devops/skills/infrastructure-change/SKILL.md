---
name: infrastructure-change
title: "Infrastructure Change Planning and Verification"
description: "Plan and verify Docker, Kubernetes, or Terraform changes with the correct target, explicit approvals, and evidence from the current environment."
license: Apache-2.0
rules:
  - match((?i)\b(edit|update|fix|configure|refactor|migrate|write|rewrite|build|need|convert|harden|shrink|create|draft|implement|add|make|set\s+up)\b.{0,60}\b(dockerfile|docker[\s-]?compose|compose\s+(stack|file|setup)|helm|terraform|opentofu|rbac|network\s*polic\w+|ingress|hpa|statefulset|manifests?|poddisruptionbudget|persistentvolumeclaim|dockerignore)\b)
  - match((?i)\b(dockerfile|dockerignore|multi[\s-]stage|trivy|distroless|docker-compose\.ya?ml|compose\.ya?ml|docker[\s-]compose\s+(file|stack))\b)
  - match((?i)\b(compose|containers?)\b.{0,60}\b(can'?t|cannot|unable)\b.{0,30}\b(talk|reach|connect)\b)
  - match((?i)\b(diagnose|debug|troubleshoot|investigate|roll\s*out)\b.{0,50}\b(kubernetes|k8s|helm|terraform|opentofu)\b)
  - match((?i)\b(apply|deploy|roll\s*out|upgrade)\b.{0,40}\b(helm\s+(chart|release)|manifests?|terraform\s+plan|kubectl)\b)
  - match((?i)\b(terraform|opentofu|tfstate|hcl|main\.tf)\b)
  - match((?i)\b(rbac|roles?bindings?|network\s*policies|hpa|poddisruptionbudgets?|persistentvolumeclaims?|statefulsets?|configmaps?|kustomize)\b)
  - match((?i)\b(image|container|compose\s+stack)\b.{0,50}\b(non[\s-]root|unprivileged|healthchecks?|registry|published\s+on\s+the\s+host|reachable\s+only)\b)
  - semantic(plan and apply a terraform change safely, 0.75)
  - semantic(update the kubernetes deployment and verify the rollout, 0.75)
  - semantic(change our docker setup and confirm it on the right environment, 0.75)
  - semantic(which cluster is this command pointed at before I apply, 0.75)
---

## Overview

Use this procedure when changing infrastructure definitions or diagnosing their behavior. Determine the target and approval requirements before making changes.

## Rules

1. Identify the desired outcome, environment and version. Inspect relevant configuration and prior decisions. For a failure, locate the first failing operation and verify the symptom before editing.
2. Keep read-only investigations separate from changes. For multi-step interactive work, present the scoped plan and get confirmation. An autonomous brief may authorize local definition edits. Production mutations, destructive operations and registry pushes require separately authorized actions.
3. Batch independent discovery. Make the smallest coherent change consistent with existing definitions. Check the cluster context and namespace, IaC workspace and state backend, or registry target as relevant.
4. Run the available local validation and review the resulting diff or plan. Report the exact evidence, unresolved risks and any operation awaiting approval. Store durable project conventions only when relevant, after checking existing memory.

## Checklist

- [ ] Target and authority verified.
- [ ] Diff or plan stays within the requested scope.
- [ ] Verification evidence and remaining operations are explicit.
