# Workflows

Workflows are external pipelines stored as `workflows/<name>.toml` and run with:

```bash
octomind workflow <name>
```

Start from `templates/workflow.toml`. Workflows may reference installed roles
and public tap agent tags; they never belong inside agent manifests.

