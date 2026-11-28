---
name: performance-profiling
title: "Performance Profiling and Load Testing"
description: "Find where time and memory go: profiler per runtime, flame graphs, benchmark statistics, k6 load-test design. Use for slow code, memory leaks, latency."
license: Apache-2.0
compatibility: "Requires a shell and the runtime's own profiler; k6 for load tests."
rules:
  - content(profiling)
  - content(flamegraph)
  - content(latency)
  - content(bottleneck)
  - content(benchmark)
  - content(k6)
  - match((?i)\b(memory\s+(leak|usage|growth|bloat)|leaking\s+memory|out\s+of\s+memory|oom|load\s+tests?|stress\s+tests?|soak\s+tests?|p99|p95|too\s+slow|performance\s+(regression|issue|problem)s?|high\s+cpu|cpu\s+spike)\b)
  - match((?i)\b(speed\s+up|takes\s+(forever|too\s+long)|getting\s+slower|runs?\s+slow(ly)?|slow\s+(query|endpoint|request|response|startup|build))\b)
---

## Overview

Use this skill when something is slow, uses too much memory, or must be shown to hold under load. The deliverable is evidence: a profile or measurement that names the bottleneck, a change, and a before-and-after comparison with the numbers. Measure first; do not optimize from reading code. The method is the same in every language: state the target, reproduce, profile, change one thing, re-measure.

## Mental model

A profile answers "where is the time (or memory) going", not "what is wrong". Samples from a profiler show where the program was when sampled; the widest frames are the candidates. A load test answers a different question: how the system behaves at a given arrival rate. Mixing them up wastes days: profile a single process to find the hot code, load-test the deployed system to find capacity and the shape of failure.

## Rules

### Workflow

1. Write the target as a number with a percentile and a condition ("p95 under 300 ms at 200 requests per second"). "Fast" is not testable.
2. Reproduce on a fixed input and a quiet machine; record the baseline before touching code.
3. Profile CPU first when the process is busy; profile wall-clock or off-CPU when it is waiting; profile allocations when memory or garbage collection is the symptom.
4. Change one thing, then repeat the same measurement. Keep the change only if the comparison shows it helps against the target.
5. Keep the result as a regression guard (a benchmark, or a load-test threshold in CI).

### Profiler by runtime

| Runtime | CPU | Memory | Notes |
|---|---|---|---|
| Go | `go test -cpuprofile`, or `net/http/pprof` served under `/debug/pprof/profile` (30 s sample); `go tool pprof` | `/debug/pprof/heap`, `go test -memprofile` | `top` sorts by flat time, `top -cum` by cumulative; `list <func>` shows source lines. Heap samples are about one per half megabyte, so the numbers are approximate |
| Node.js | `node --cpu-prof app.js`, open the `.cpuprofile` in Chrome DevTools | heap snapshots: `--heapsnapshot-signal=SIGUSR2`, `v8.writeHeapSnapshot()`, or `--inspect` | Snapshots pause the process and can roughly double memory use |
| JVM | async-profiler: `asprof -d 30 -f flamegraph.html <pid>`; events include CPU, heap allocations, native memory, contended locks | async-profiler allocation and native-memory events | async-profiler does not have the safepoint-bias problem of many Java profilers; official builds cover Linux and macOS on x64 and arm64 |
| Other | Use the runtime's own sampling profiler; confirm its name and flags from its documentation before running | | |

Run profilers on a build close to production (same optimization level, same data size). A debug build or a tiny dataset gives a different bottleneck.

### Reading a flame graph

- The x-axis is not time. Stacks are sorted alphabetically, and a frame's width is the share of samples that contained it.
- The y-axis is stack depth; the top edge is what was running, the frames below are its callers.
- Look for wide plateaus near the top: functions where the time is spent. A wide frame lower down with narrow children means the cost is spread among callees.
- A CPU flame graph shows nothing about waiting. If CPU is low while latency is high, collect an off-CPU or wall-clock profile, or trace the calls (database, network, locks).
- To check a fix, compare a differential flame graph or the same hot function's share before and after.

### Benchmarks and statistics

- Run a benchmark many times and compare distributions. For Go: `go test -run='^$' -bench=. -count=10` before and after, then `benchstat old.txt new.txt`. A `~` in the delta column means no statistically significant difference; a significant result can still be too small to matter, so check the size against the target.
- Do not rerun until a change appears; at the default 0.05 significance level about 5 percent of comparisons show a change when none exists.
- Fix the environment: same machine, no other load, power and CPU frequency settings stable. Report the median and the spread, not one run.

### Load-test design

- Pick the workload model. A closed model (a fixed pool of virtual users, each waiting for its response) slows its own request rate when the system slows, which hides the problem; this is coordinated omission. An open model starts requests at a fixed rate regardless of response time. To test a target arrival rate, use an open model: in k6 the `constant-arrival-rate` or `ramping-arrival-rate` executor, with `rate`, `timeUnit`, `duration`, `preAllocatedVUs` and `maxVUs` set high enough to hold the rate.
- Choose the test type for the question:

| Type | Question | Shape |
|---|---|---|
| Smoke | Does the script and system work at minimal load | seconds to minutes, low load |
| Average load | Does it meet the target at normal traffic | 5 to 60 minutes at production-level load |
| Stress | How does it behave above normal | 5 to 60 minutes at high load |
| Spike | Does it survive a sudden surge | a few minutes at very high load |
| Soak | Does it stay stable over time (leaks, pool exhaustion) | average load for hours |
| Breakpoint | Where does it fail | load raised gradually until failure |

- Keep the shape simple: ramp up, plateau, ramp down. Start with a smoke test before anything larger.
- Gate with thresholds, so the run fails when the target is missed: for example `http_req_duration: ['p(95)<200']` and `http_req_failed: ['rate<0.01']`; k6 exits non-zero when a threshold fails. Use `abortOnFail` with `delayAbortEval` to stop a doomed run without reacting to warm-up samples. Tag requests to set thresholds per endpoint.
- Test against a production-like environment with representative data volume. Do not load-test a system you do not own or a live production system without the owner's approval and a stop condition.
- Report percentiles per endpoint, error rate, throughput, and resource use (CPU, memory, connections) at each load step. Do not average percentiles across instances or intervals; merge the raw samples or histograms.

### Memory leaks

Confirm a leak with a trend (memory after garbage collection rising over hours at constant load), not one reading. For snapshot-based runtimes: warm up, exercise the suspect action once, take snapshot A, repeat the action many times, take snapshot B, and compare B against A for large positive deltas and what retains them. Typical retainers: unbounded caches, listeners never removed, closures holding large objects, global maps keyed by request.

## Examples

Bad: change code on a guess, report "feels faster".

Good: "Baseline p95 412 ms at 200 req/s (k6 `constant-arrival-rate`, 10 min). CPU profile shows 38 percent in `encodeJSON`, called per row. Batched the call. Same test: p95 211 ms, error rate 0.0 percent. Threshold `p(95)<300` now passes in CI."

## Checklist

- The target is a number with a percentile and a load.
- Baseline and result use the same input, environment and command, and both are recorded.
- The profile type matches the symptom (CPU, wall-clock, allocation).
- Benchmark comparisons use repeated runs and a significance check.
- The load model is open when a target arrival rate is tested; thresholds fail the run.
- Every command was run, or the report says which were not.

## References

- [k6 open and closed models](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/), [thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/), [constant-arrival-rate](https://grafana.com/docs/k6/latest/using-k6/scenarios/executors/constant-arrival-rate/), [test types](https://grafana.com/docs/k6/latest/testing-guides/test-types/)
- [Profiling Go programs](https://go.dev/blog/pprof) and [benchstat](https://pkg.go.dev/golang.org/x/perf/cmd/benchstat)
- [async-profiler](https://github.com/async-profiler/async-profiler)
- [Node.js heap snapshots](https://nodejs.org/en/learn/diagnostics/memory/using-heap-snapshot)
- [Flame graphs](https://www.brendangregg.com/flamegraphs.html)
