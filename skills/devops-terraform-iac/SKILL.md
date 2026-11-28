---
name: devops-terraform-iac
title: "Terraform & OpenTofu: Modules, State & Drift"
description: "Write and manage Terraform or OpenTofu: HCL modules, remote state with locking, plan and apply workflow, imports, drift detection and IaC security."
license: Apache-2.0
compatibility: "Needs the terraform or tofu binary; linting uses tflint and Checkov or Trivy when installed. Registry lookups need network access."
domains: devops
rules:
  - match((?i)\b(terraform|opentofu|terragrunt|tfstate|tflint|hcl)\b)
  - match((?i)\w+\.tf\b|\.tfvars\b)
  - match((?i)\b(infrastructure\s+as\s+code|iac)\b.{0,40}\b(modules?|state|drift|plans?|apply|import)\w*)
  - match((?i)\b(state\s+lock|remote\s+state|configuration\s+drift|drift\s+detection)\b)
  - semantic(write a reusable infrastructure as code module)
---

## Overview

Use this skill to design, write and manage production infrastructure as code with Terraform and OpenTofu: HCL, module design, state backends and locking, provider configuration, plan and apply workflow, drift detection, imports and state operations, testing and IaC security. Infrastructure code is production code: review, test, version and document it with the same rigor.

## Mental model

State is the record of what exists, and it is a secret store. The plan is the contract between the code and the real world. Nothing is applied that was not planned, shown and approved, and the repository's pinned versions decide which features exist.

## Rules

### Method

1. Inspect the relevant definitions and project conventions. Batch independent discovery and reproduce reported failures before editing.
2. Identify Terraform or OpenTofu, the target workspace and backend, and the pinned versions. Use versioned modules and locking for shared state. Format and validate locally, review the saved plan, and check variable types and descriptions before presenting it. Require approval before apply or destroy.
3. For multi-step interactive changes, confirm the plan. For autonomous local definition edits, record assumptions and proceed within the brief. Report the evidence and request explicit approval for production or destructive actions.

Check the live toolchain before applying any version fact below: `terraform version` or `tofu version`, `required_version`, `.terraform.lock.hcl`, the backend block, and the CI image. The repo's pinned versions win over this list.

### Terraform and OpenTofu (2026)

- Terraform (BSL, HashiCorp/IBM): 1.16 is current (Aug 2026), 1.15 the previous minor. OpenTofu (MPL, Linux Foundation): 1.12 is current.
- Identify which binary the repo uses (`.terraform-version` or `.opentofu-version`, `*.tofu` files, CI image, lock-file provider hosts). Switching binaries on shared state is a migration, not a command swap: features diverge (OpenTofu state encryption and the `enabled` meta-argument; Terraform actions and `terraform query`).
- Feature floors: S3-native locking `use_lockfile` (TF 1.10, Tofu 1.10); ephemeral resources and variables (TF 1.10, Tofu 1.11); write-only arguments (TF 1.11, Tofu 1.11); variables in module `source` and `version` (TF 1.15, Tofu 1.8); `import` blocks inside modules (TF 1.16).

### Layout and naming

- One root module per environment per component (`environments/<env>/<component>`) calling versioned `modules/<component>`. One state each, never a monolith.
- Files: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf` (terraform and required_providers), plus `locals.tf` and `data.tf` when large.
- snake_case everywhere. Name a module's single primary resource `this`. Outputs say what they expose (`vpc_id`, `subnet_ids`).
- Tags from one `local.common_tags` map (Environment, Team, ManagedBy=terraform, Repository), applied through AWS `default_tags` or merged per resource.
- Separate directories or state per environment. Use CLI workspaces only for short-lived copies of identical config (PR previews).
- Every variable has `description` and `type`. Add `validation` for constrained inputs, `sensitive = true` for secrets, `nullable = false` where null is meaningless, and `deprecated` (TF 1.15) when retiring inputs or outputs.

### Versions and modules

- Pin `required_version` and providers on the major with `~>` (2026: hashicorp/aws is 6.x; check the registry for others). Commit `.terraform.lock.hcl`. For mixed-OS teams run `terraform providers lock -platform=linux_amd64 -platform=darwin_arm64`.
- Pin registry modules with `version`; internal modules by git tag (`?ref=v1.2.0`) or commit SHA.
- One module is one logical component. Accept `tags`, output what callers need, use `for_each` over `count` for named instances, and `count` (or OpenTofu `enabled`) only for 0-or-1 toggles.

```hcl
terraform {
  required_version = "~> 1.15"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
  backend "s3" {
    bucket       = "myorg-terraform-state"
    key          = "prod/networking/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true # S3-native locking; dynamodb_table is deprecated
  }
}
```

### State and secrets

- State is a secret store: encrypted backend, versioned bucket, tight access, locking on (S3 `use_lockfile`; GCS and azurerm lock natively). Share outputs with `terraform_remote_state` or data sources, never by reading state files by hand.
- Keep secrets out of state, not just out of code: ephemeral resources and variables feed write-only arguments, and only the version attribute is stored.

```hcl
ephemeral "random_password" "db" {
  length = 32
}

resource "aws_db_instance" "main" {
  # ...
  password_wo         = ephemeral.random_password.db.result
  password_wo_version = 1 # bump to rotate
}
```

- Otherwise use `sensitive = true`, `TF_VAR_*` injection, Vault or Secrets Manager (a data source's value still lands in state), and SOPS for encrypted tfvars.

### Refactors and imports

- Use `import` blocks with `terraform plan -generate-config-out=generated.tf` instead of the `terraform import` CLI. On TF 1.14+, `terraform query` with `*.tfquery.hcl` list blocks discovers existing resources in bulk.
- Use `moved` blocks for renames and module moves, and `removed` blocks with `lifecycle { destroy = false }` to forget a resource without destroying it. Use `terraform state mv` and `state rm` only when blocks can't express the change, after `terraform state pull > backup.tfstate`.
- `-target` and `-replace` are surgical exceptions, not a workflow.

### Workflow and verification

```bash
terraform fmt -recursive && terraform validate
terraform plan -out=tfplan        # review, then
terraform apply tfplan
terraform plan -refresh-only      # drift detection, changes nothing
```

- Test and lint with `terraform test` (`.tftest.hcl`, mock providers), tflint, and Checkov or Trivy config scanning (tfsec now lives in Trivy).
- CI plans every PR. One pipeline identity applies, authenticated by OIDC federation instead of long-lived keys. Use the `ci-cd-pipelines` skill for pinning those tools and the pipeline trust setup. A scheduled `plan -detailed-exitcode` (exit 2 means changes) catches drift.

### Cloud security baseline

- A dedicated least-privilege role per environment via provider `assume_role` or OIDC, with audit logging on.
- Private subnets for compute, public only for load balancers, deny-by-default security groups, VPC endpoints and flow logs.

### Common requests

| Request | Response |
|---|---|
| Question | Answer directly. |
| Ambiguous | Ask one clarifying question. |
| Empty or irrelevant results twice | Stop and ask for direction. |

### Guards

- Don't run `terraform apply` without showing the plan first.
- Don't implement multi-step interactive work before confirming the plan.
- Don't hardcode secrets, account IDs or credentials in `.tf` files.
- Don't use local state for team environments.
- Don't use `count` for named resources; use `for_each`.
- Don't ignore `.terraform.lock.hcl`; commit it.
- Don't add unrequested resources or modules.
- Don't reference a provider, module or resource type you haven't verified exists in the registry. Exact names come from a lookup, not memory.
- Run `terraform fmt` before committing any `.tf` files.

### Scope limits

Container images and Compose stacks, orchestrating workloads on a cluster, and live incident response are not covered here. This skill provisions the infrastructure.

## Output format

Report in the fewest words that carry the evidence: for example "3 resources added. Plan shows +2 ~1 -0. Ready to apply." No explanations unless asked, and no duplicated plan output.

## Checklist

- [ ] The binary, workspace, backend and pinned versions were identified.
- [ ] `fmt` and `validate` pass, and the saved plan was reviewed.
- [ ] No secrets in code; state backend is encrypted and locked.
- [ ] Provider, module and resource names were verified in the registry.
- [ ] `.terraform.lock.hcl` is committed.
- [ ] Apply or destroy has explicit approval of the shown plan.

## Composition / References

- `infrastructure-change` covers the shared plan-and-verify procedure.
- `ci-cd-pipelines` covers pipeline trust setup and tool pinning.
- `devops-cloud-engineering` covers IAM, network and cost questions on the target cloud.
