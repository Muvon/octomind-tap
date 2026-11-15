---
name: e2e-testing
title: "End-to-End Testing: Playwright and UI Tests"
description: "Write stable browser and mobile UI tests: locators, auth-state reuse, data isolation, flake triage, visual snapshots, sharding. Use for Playwright suites."
license: Apache-2.0
compatibility: "Requires Node.js for Playwright; mobile flows need a simulator or emulator."
domains: developer
rules:
  - file(playwright.config.ts)
  - file(playwright.config.js)
  - file(cypress.config.ts)
  - file(cypress.config.js)
  - file(.maestro)
  - content(playwright)
  - content(cypress)
  - content(e2e)
  - content(maestro)
  - match((?i)\b(end[\s-]?to[\s-]?end|e2e|ui|browser)\s+tests?\b)
  - match((?i)\b(flaky|flakey|unstable)\s+(e2e|ui|browser|playwright|cypress|tests?)\b)
  - match((?i)\b(visual\s+regression|screenshot\s+tests?|page\s+object|data-testid|getByRole|detox|appium|xcuitest|espresso)\b)
---

## Overview

Use this skill to write, repair or review tests that drive the real UI of a web or mobile app. The deliverable is a suite that fails when a user flow breaks, passes when it does not, and tells the next reader why it failed. Keep the project's framework (Playwright, Cypress, Maestro or other); the mechanics below are written for Playwright because its current documentation was checked, and the principles carry over. As of 2026-11, Playwright is at 1.65 and no longer supports Node.js 20; read the installed version and its release notes before using an API.

## Mental model

An end-to-end test is the most expensive test you own: slow, shared with every layer, and the likeliest to flake. Spend it on the few flows where the integration itself is the risk (sign-up, checkout, the core workflow), and cover logic below the UI with unit and integration tests. Each test must start from a known state, act as a user would, and assert what the user sees.

## Rules

### Locators

Order of preference (Playwright documentation): `getByRole` with the accessible name, then `getByText` for non-interactive text, `getByLabel`, `getByPlaceholder`, `getByAltText`, `getByTitle`, and `getByTestId` (a `data-testid` contract) when no user-facing handle is stable.

- Avoid CSS and XPath chains tied to DOM structure; they break when markup changes.
- Locators are strict: an action matching several elements throws. Narrow with `filter({ hasText })` or `filter({ has })` rather than `first()` or `nth()`.
- If no role or label finds the element, the app has an accessibility gap; report it, because the same gap affects real users.

### Assertions and waiting

- Use web-first assertions (`await expect(locator).toBeVisible()`, `toHaveText`, `toHaveURL`); they retry until the condition holds or the timeout ends.
- Never use fixed sleeps. Wait for a condition the user could observe: an element, a URL, a network response (`page.waitForResponse`) tied to the action.
- Do not assert on a snapshot of a value (`expect(await locator.isVisible())`); that skips the retry.
- Enable the `@typescript-eslint/no-floating-promises` lint rule and run `tsc --noEmit` so a missing `await` fails CI.

### Isolation and test data

- Each test runs independently with its own storage, cookies and data; tests do not depend on order.
- Create data through the API or database seed, not through ten UI steps, and clean it up or use unique names (a run id) so parallel workers never collide.
- Do not depend on third-party services you do not control; fulfill their responses with `page.route`. Test against a staging environment with stable data.

### Authentication state

- Log in once in a setup project, save the state with `storageState`, and let other projects depend on the setup project.
- When tests change server-side state, use one account per worker (select it with `testInfo.parallelIndex`); a shared account is only for read-only tests.
- Where an API login exists, authenticate with `request` and save `request.storageState()`; it is faster than the UI.
- Store state files under `playwright/.auth` and add the folder to `.gitignore`: they hold cookies that can impersonate the account. Saved state expires; regenerate it. Session storage and IndexedDB-based auth need extra handling.

### Flaky tests

- Playwright reports a test as flaky when it fails first and passes on retry. Retries are a detector and a stopgap, not a fix: every flaky test gets an owner and a root cause.
- Collect traces on the first retry (`trace: 'on-first-retry'`) in CI rather than on every test, which is slow. Open the trace viewer, find the first action whose state differs from expectation.
- Common causes: asserting before the app settled, shared data between tests, order dependence, animations, real network or clock dependence, and genuine race conditions in the product (a product bug, not a test bug).
- Quarantine a flaky test out of the blocking gate the same day, with an exit date, instead of letting people learn to rerun.
- After a failure Playwright discards the worker and its browser and starts a new one; `testInfo.retry` lets a test clean server state before a retry.

### Visual regression

- `await expect(page).toHaveScreenshot()` writes baselines on the first run into a snapshot folder next to the test; commit it. File names include the browser and platform, so baselines are per platform.
- Rendering varies with operating system, hardware and headless mode: generate and compare baselines in the same environment, normally the CI image, and update with `--update-snapshots` only after reviewing the diff.
- Tune `threshold` (per-pixel color tolerance, default 0.2) and `maxDiffPixels` per assertion; hide volatile regions with `stylePath`; move the pointer away (`page.mouse.move(-1, -1)`) to avoid hover states.
- Snapshot stable components, not whole pages with dates or ads.

### CI

- Run on every pull request, on Linux, installing only the browsers used.
- Split a suite across machines with `--shard=1/4` through `--shard=4/4`. Set `fullyParallel: true` so shards balance by test, not by file. Use the `blob` reporter in CI and combine the shard reports with `npx playwright merge-reports --reporter html ./all-blob-reports`.
- Since 1.65 a sharded run that matches no tests fails unless `--pass-with-no-tests` is set.
- Keep Playwright updated; new browser releases can break old versions.

### Mobile UI tests

- Maestro describes a flow in YAML (`appId`, then commands such as `launchApp`, `tapOn`, `inputText`, `assertVisible`, `runFlow`), and runs on an iOS Simulator or Android Emulator. Keep shared steps (login) in a subflow called with `runFlow`.
- For native frameworks (XCUITest on iOS, Espresso on Android) and other tools, read the platform documentation through the docs tool; do not guess API names.
- Give every interactive element an accessibility identifier or label; tests and screen readers use the same handle.

## Examples

Bad: sleep, brittle selector, shared state.

```ts
await page.click('div.container > div:nth-child(3) button');
await page.waitForTimeout(3000);
expect(await page.locator('.total').innerText()).toBe('42');
```

Good: user-facing locator, web-first assertion, seeded data.

```ts
import { test, expect } from '@playwright/test';

test('checkout shows the order total', async ({ page, request }) => {
  const order = await request.post('/api/test/orders', { data: { items: 2 } });
  const { id } = await order.json();
  await page.goto(`/orders/${id}`);
  await page.getByRole('button', { name: 'Pay now' }).click();
  await expect(page.getByTestId('order-total')).toHaveText('$42.00');
});
```

## Checklist

- Each test is independent, creates its own data, and passes when run alone and in parallel.
- Locators are role, label or test id based; no fixed sleeps.
- Auth state comes from a setup project, is gitignored, and is per worker where tests write data.
- Traces are collected on first retry; every flaky test has an owner and a root cause, or is quarantined.
- Visual baselines were generated in the CI environment and reviewed.
- The suite was run (and sharded runs merged) or the report says it was not.

## References

- [Playwright best practices](https://playwright.dev/docs/best-practices), [locators](https://playwright.dev/docs/locators), [authentication](https://playwright.dev/docs/auth)
- [Retries](https://playwright.dev/docs/test-retries), [visual comparisons](https://playwright.dev/docs/test-snapshots), [sharding](https://playwright.dev/docs/test-sharding)
- [Playwright release notes](https://playwright.dev/docs/release-notes)
- [Maestro](https://maestro.dev/)
