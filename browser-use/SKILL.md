---
name: browser-use
description: "Use the browser-use CLI for agent browser workflows: opening app routes, inspecting summaries/snapshots, clicking/filling/selecting/pressing/waiting, screenshots, issue checks, auth-profile status, and app-specific browser-flow discovery. Use when Codex needs browser verification or interaction for any repo, especially local web apps."
---

# Browser Use

Use `browser-use` for routine browser work. Use raw `browserctl` only for browser-runtime development or explicit protocol debugging.

## Device Profiles

List the available device profiles before choosing one when mobile or tablet behavior matters:

```bash
browser-use devices list <workspace-alias>
```

Use the semantic aliases `desktop`, `mobile` (iPhone 15 Pro), and `tablet` (iPad gen 11), or pass any Playwright descriptor returned by the list command:

```bash
browser-use open <workspace-alias> /target --device-preset mobile
browser-use open <workspace-alias> /target --device-preset "Galaxy S24"
```

Set a workspace default with `device_preset` in `.context-tools.toml`. For reusable workspace-specific names, define `devices` in `browser.config.ts`; a preset can inherit a Playwright descriptor with `device: "iPhone 15 Pro"` and override individual context options.

## Invocation

Invoke the CLI by command name:

```bash
browser-use <command> ...
```

Run it from the target repository so it discovers `.context-tools.toml` from the current directory upward. Do not use an absolute path to the `browser-use` executable. Pass `--config` only for a non-discoverable config or when automatic discovery is unavailable.

## Standard Loop

```bash
browser-use open <workspace-alias> /target
browser-use summary <workspace-alias> --url /target --brief
browser-use quick-snapshot <workspace-alias> --url /target
browser-use fill <workspace-alias> "#selector-or-name" "..."
browser-use click <workspace-alias> "#selector-or-name"
browser-use wait <workspace-alias> --url-contains "/target" --return-current
browser-use assert-url <workspace-alias> /target
browser-use assert-text <workspace-alias> "Ready"
browser-use screenshot <workspace-alias> --url /target --annotated
browser-use assert-no-page-errors <workspace-alias> --url /target
```

Use `browser-use fill|click|press|select|wait` for routine UI interaction.

`browser-use` discovers `.context-tools.toml` from the current directory upward.

Use `browser-use current <workspace-alias>` when page/session ids are needed. When more than one active context/page exists, pass `--auth-profile`, `--context`, `--page`, or `--url`; `browser-use` fails with candidates instead of guessing. Use `--url` with an absolute URL or a workspace-relative path such as `/dashboard`; it selects an already-active page and does not open a new one.

Never call `browser-runtime/node_modules/.bin/tsx browser-runtime/packages/cli/src/bin.ts ...` from agent work.

## Repo-Specific Flows

For repo-specific browser flows, check:

```bash
<repo>/scripts/browser-use/
```

Also check package scripts named:

```bash
browser-use:*
```

Shared `browser-use` stays generic. Login helpers, upload smokes, checkout flows, and domain assertions belong in the app repo.

If browser work fails because of authentication, stale storage state, missing credentials, signin redirects, or profile mismatch, inspect `<repo>/scripts/browser-use/` before manual troubleshooting. Repos should keep authentication scripts there and expose them with `browser-use:*` package scripts when useful.

## Auth Profiles

`browser-use open` reports auth state. If it reports stale or missing auth, check `<repo>/scripts/browser-use/` and `browser-use:*` package scripts before doing a manual login flow.

Generic auth lifecycle:

```bash
browser-use auth status <workspace-alias> --auth-profile admin
browser-use auth save <workspace-alias> --auth-profile admin
browser-use auth clear <workspace-alias> --auth-profile admin
```

Runtime cleanup:

```bash
browser-use clean <workspace-alias>
browser-use clean <workspace-alias> --include-auth
```

Repo convention checks:

```bash
browser-use script doctor <workspace-alias>
browser-use script doctor <workspace-alias> --route /auth/signin --selector '#email'
```

## Guardrails

- Use `browser-use --json` when scripting.
- Prefer `browser-use quick-snapshot` before raw protocol inspection.
- Use refs from the latest snapshot when available.
- Prefer exact `--selector`, `--ref`, `--label`, `--placeholder`, or `--name`; use `--name-regex` or `--fuzzy` only when exact matching is not stable.
- Capture screenshots when visual state matters.
- Default artifacts are temporary and disappear when the daemon exits; use `screenshot --output <path>` or configure `artifactDir` when they must persist.
- Saved auth profiles belong in the target repo `.browser-runtime/auth/`.
