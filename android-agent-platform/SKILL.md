---
name: android-agent-platform
description: Operate Android emulators with `android-use` / `agentctl`. Trigger when the user asks to use or control an Android emulator, run or debug Android flows, boot or reset an AVD, restore/save snapshots, launch an automation APK, inspect app state, drive Android UI with Appium, collect artifacts, or troubleshoot `adb`, `android-use`, `agentctl`, provisioning, clock skew, stale automation tokens, or snapshot-state failures.
---

# Android Agent Platform

Last updated: 2026-04-26

## Defaults

- Prefer `android-use` for agent workflows.
- Use raw `agentctl` only for android-agent-platform development or protocol-level debugging.
- Use plain `android-use ...`; the shim activates the platform runtime and config applies SDK paths.
- Before repo-specific flows, check:
```bash
<repo>/.android-use.json
<repo>/.android-use.toml
<repo>/scripts/android-use/
```
- Also check Make/package scripts named for Android verification.
- Do not hardcode machine paths into commands when repo config or scripts exist.

## Session Flow

```bash
android-use ready
android-use state --json
android-use wait --jsonpath '$.startup_state' --equals Ready --timeout 30s
android-use assert --jsonpath '$.network_errors' --empty
```

Later commands auto-use the current active session. If multiple active sessions exist, pass `--session <id>`.

## Generic Primitives

```bash
android-use call POST /control/reset
android-use call POST /viewer/override --body '{"state":"present"}'
android-use logcat --package --since 2m
android-use events --since 2m
android-use mark "before pickup trigger"
android-use gps set --lat 33.776 --lng -118.244
android-use gps verify --timeout 10s
android-use artifact collect
android-use artifact bundle
```

`call` is app-agnostic. Route names and domain semantics belong to the target repo.

## Step Runner

Use repo-owned YAML for repeatable flows:

```bash
android-use run scripts/android-use/smoke-active-ride.yml
```

Supported step actions:
- `call`
- `wait`
- `assert`
- `gps`
- `screenshot`
- `collect`

## UI

Use state/API validation first. Use UI automation when the behavior is visual or interaction-specific:

```bash
android-use ui tree
android-use ui tap --text-selector "Continue"
android-use ui tap --x 540 --y 960
android-use ui type --resource-id "com.example:id/name" --text "Ada"
android-use ui assert --text-selector "Ready"
```

## Machine Contract

- `--json` works on every `android-use` command.
- JSON envelope includes `ok`, `session_id`, `device_serial`, `app_package`, `state`, `artifacts`, and `error`.
- Exit codes:
  - `0` success
  - `10` app assertion failed
  - `20` app unhealthy
  - `30` device/emulator infra
  - `40` timeout
  - `50` tool/config error
- Failed commands auto-collect state, events, logcat where possible, screenshot/UI tree where possible, manifest, and a bundle.

## Config

`android-use` reads:
- shared/user Context tools config
- nearest `.context-tools.toml`
- nearest `.android-use.toml` or `.android-use.json`

Repo-local config can define:
- default AVD
- package/component/main activity
- automation APK variants
- automation port/path
- platform home/artifact dir
- SDK paths
- known snapshots

## Repo-Specific Flows

For repo-specific Android flows, use scripts in the repo:

```bash
<repo>/scripts/android-use/
```

For `nemtadplayer`, use:

```bash
make smoke-playback
make smoke-active-ride
make reset-local-scenario
```

or the direct scripts:

```bash
scripts/android-use/smoke-playback.sh
scripts/android-use/smoke-active-ride.sh
scripts/android-use/reset-local-scenario.sh
```

## Failure Triage

- Start with `android-use state --json`, `android-use events --since 2m`, and `android-use logcat --package --since 2m`.
- If auth/state looks stale after snapshot restore, relaunch through `android-use ready` or `android-use app stop && android-use app launch`.
- If Appium commands fail, run `android-use doctor`; prefer API/state primitives unless UI evidence is needed.
- Before mutating more state after a failure, run `android-use artifact collect`.

## Finish

End the session when done:

```bash
android-use session end
```
