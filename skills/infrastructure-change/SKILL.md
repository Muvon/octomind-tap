---
name: infrastructure-change
title: "Infrastructure Change Planning and Verification"
description: "Plan and verify Docker, Kubernetes, or Terraform changes with the correct target, explicit approvals, and evidence from the current environment."
license: Apache-2.0
domains: devops
rules:
  - session(tap-devops-docker-)
  - session(tap-devops-kubernetes-)
  - session(tap-devops-terraform-)
  - match((?i)\b(edit|update|fix|configure|refactor|migrate)\b.{0,40}\b(dockerfile|compose|kubernetes|helm|terraform|opentofu)\b)
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
