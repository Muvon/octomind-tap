---
name: observability-setup
title: "Observability and Alerting Setup"
description: "Set up metrics, logs, traces and alerts: SLI and SLO definition, burn-rate alerts, Prometheus cardinality limits, OpenTelemetry Collector and dashboards."
license: Apache-2.0
compatibility: "Prometheus-style metrics, OpenTelemetry Collector, any log backend. Needs access to the service's metrics endpoint or config."
rules:
  - content(prometheus)
  - content(grafana)
  - content(opentelemetry)
  - content(otel)
  - content(alerting)
  - content(slo)
  - content(observability)
  - content(monitoring) content(alerts)
  - match((?i)\b(set\s*up|setup|add|configure|create|build|improve)\b.{0,30}\b(monitoring|alerts?|alerting|dashboards?|observability|tracing)\b)
  - match((?i)\b(alert\s+fatigue|noisy\s+alerts?|too\s+many\s+alerts|burn[\s-]?rate|error\s+budgets?|slis?|service\s+level\s+(objective|indicator)s?|golden\s+signals)\b)
  - match((?i)\bhow\s+(do|should|can)\s+(i|we)\s+monitor\b)
---

## Overview

Use this when you add monitoring to a service, review an alerting setup, or cut alert noise. The outcome is a short list of service-level indicators (SLIs), a target for each, alerts that fire on user-visible symptoms, a telemetry pipeline with bounded cost, and a dashboard that answers "is it broken, where, since when" in that order.

## Mental model

Telemetry has three jobs: tell you users are hurting (alerts), tell you where (dashboards, traces), and tell you why (logs, traces, profiles). Alert on symptoms and diagnose with causes. Every metric and label has a storage cost that grows with the number of distinct label combinations, so each one must earn its place.

## Rules

### Define SLIs and SLOs first

1. List the user journeys (login, checkout, API call). Pick at most two SLIs per journey.
2. Use the ratio form: good events divided by valid events. Availability SLI: non-5xx requests over all requests. Latency SLI: requests faster than a threshold over all requests (a threshold, not an average).
3. Set an SLO target and a window (for example 99.9 percent over 30 days). The error budget is 100 percent minus the target; 99.9 percent leaves 0.1 percent.
4. Write the SLO down with its owner and what happens when the budget is spent (feature freeze, reliability work).

### Alert on symptoms, with burn rates

- Page on user-visible errors and latency, high in the stack, at one point per request path. Put causes (CPU, queue depth, disk) on the dashboard, not in pages, unless they predict an imminent outage. Every page needs an action a human can take; an alert without one is a ticket or deleted.
- Use multiwindow, multi-burn-rate alerts. Starting values for a 99.9 percent SLO (Google SRE Workbook, table 5-8):

| Severity | Long window | Short window | Burn rate | Budget used |
|---|---|---|---|---|
| Page | 1 h | 5 min | 14.4 | 2% |
| Page | 6 h | 30 min | 6 | 5% |
| Ticket | 3 days | 6 h | 1 | 10% |

The alert fires when both windows exceed the burn rate; the short window makes it reset quickly. Example for a 99.9 percent availability SLO, in PromQL:

```
(
  sum(rate(http_requests_total{code=~"5.."}[1h])) / sum(rate(http_requests_total[1h])) > (14.4 * 0.001)
and
  sum(rate(http_requests_total{code=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > (14.4 * 0.001)
)
```

- Batch jobs: alert when the job has not succeeded within at least two full run cycles (a job that runs every 4 hours and takes 1 hour: 10 hours).
- Alert on the monitoring itself (Prometheus up, Alertmanager reachable) and add one external blackbox probe, because internal monitoring cannot see its own outage.
- Every alert links to its dashboard and runbook, and has a name that states the symptom.

### Metrics and cardinality

- Counters only go up (use `rate()`); gauges go up and down (never `rate()`); use histograms for latency so you can compute percentiles across instances.
- Cardinality: Prometheus guidance is to keep most metrics under 10 label combinations and to rethink any metric that reaches 100 series. Never use user ID, request ID, email, full URL or raw error message as a label. Normalize paths to route templates (`/users/:id`).
- Name metrics `<namespace>_<what>_<unit>` with base units (seconds, bytes) and `_total` on counters.
- Check growth: `topk(10, count by (__name__)({__name__=~".+"}))` shows the heaviest metric names; alert when series count grows faster than traffic.

### Logs

- Structured (JSON) logs with timestamp (UTC), level, service, trace ID and a request ID. One event per line. Never log secrets or full personal data.
- Pipeline: collector at the node or sidecar, parse and drop at the collector, store by tier. Set retention per tier by purpose (debug logs days, audit logs as the compliance rule requires) and write the number down; unlimited retention is a cost, not a default.
- Sample or drop high-volume low-value lines (health checks, debug) at the collector.

### Traces and the OpenTelemetry Collector

- Instrument with OpenTelemetry SDKs; export OTLP to a Collector rather than directly to the backend, so you can change backends and drop data in one place.
- A Collector config has five parts: receivers (collect), processors (modify, in listed order), exporters (send), connectors (join pipelines), extensions (health checks). A component that is configured but not named in `service.pipelines` is inactive.

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
processors:
  memory_limiter: {check_interval: 1s, limit_mib: 512}
  batch: {}
exporters:
  otlp_grpc:
    endpoint: ${env:BACKEND_ENDPOINT}
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp_grpc]
```

- Put `memory_limiter` first and `batch` last among processors. Read secrets and endpoints with `${env:NAME}`. Check the Collector release you run for the exact component names; they change between versions.
- Sample traces at the Collector (keep all errors and slow traces, a fraction of the rest) and state the rate.

### Dashboard layout

Top row: the SLI and the error-budget remaining. Second row: RED for each service (rate, errors, duration percentiles). Third row: USE per resource (utilization, saturation, errors). Bottom: dependencies and deploy markers. One dashboard per service with the same layout, so on-call knows where to look.

## Examples

Bad alert: `node_cpu_seconds_total` above 80 percent for 5 minutes pages the team at night; users saw nothing.

Good: page on the checkout availability burn rate (14.4 over 1 h and 5 min); CPU is a panel on the service dashboard linked from the page.

## Checklist

- [ ] Each journey has at most two SLIs, a target, a window, and an owner.
- [ ] Pages fire on burn rate or a symptom, with a runbook link; causes are on dashboards.
- [ ] No unbounded label; series count checked after the change.
- [ ] Logs are structured, carry a trace ID, and have a written retention per tier.
- [ ] Collector pipeline names every component it configures; `memory_limiter` first, `batch` last.
- [ ] Monitoring itself is monitored and one external probe exists.
- [ ] Windows and thresholds quoted from a source are marked as starting values to tune against real traffic.

## References

- [Google SRE Workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)
- [Prometheus: alerting practices](https://prometheus.io/docs/practices/alerting/) and [instrumentation practices](https://prometheus.io/docs/practices/instrumentation/)
- [OpenTelemetry Collector configuration](https://opentelemetry.io/docs/collector/configuration/) and [memory limiter processor](https://pkg.go.dev/go.opentelemetry.io/collector/processor/memorylimiterprocessor)
