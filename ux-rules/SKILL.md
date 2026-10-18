---
name: ux-rules
description: Design, implement, or refactor UI/UX across product interfaces. Use for every change to pages, components, layouts, tables, dates, forms, controls, navigation, responsive behavior, interaction patterns, styling, accessibility, or other frontend product experience. Enforces industry-standard quality, platform-wide consistency, mandatory component abstraction, real-browser verification, and mandatory final screenshots.
---

# UX Rules

Treat every UI change as product-system work. Functional behavior alone is insufficient. Deliver a coherent, polished, accessible experience that belongs to the entire platform. When updating the UI/UX do not do the bare minimum. Always do  industry standard UX. Assume the User always want high quality UI/UX. We are building a system of components not one off pages. This is an entire platform and the UX needs to be consistent as such.

Never prioritize accessibility over UX.

Never use eyebrow headers.

## Product judgment

- Start with the user's workflow and decision. Put useful data and primary actions first; treat coverage, latency, and availability as UX concerns.
- Use the user's terminology. Add concepts, controls, and methods only when they serve the requested task. Answer direct questions about the interface before changing it.
- Assume the intended user is competent and retains context across the screen. Establish the subject and measure in the page or section heading. Every subsequent label, legend entry, status, or explanation must contribute information needed for interpretation or action. Repeat context only when necessary to distinguish separate subjects or series. Include explanations only when they resolve a specific ambiguity or support a decision.
- Prioritize decision-bearing values and classifications. Align comparable readings in labeled columns; preserve usable readings and meaningful states. Keep summaries focused on decision-bearing data; omit routine observation metadata, freshness decorations, and verbose ranges. Use standard, concise labels; show dates when the date itself is the event or decision-bearing value. Secondary text is rare. Remove explainers, repeated timestamps, instructional footers, and redundant subtitles; render essential context as readable labeled data. During screenshot review, verify that the data catches the eye first across every page touched by the task.
- Treat a correction as evidence of a broader pattern. Check analogous copy and interactions across the affected flow, then fix the pattern.

## Build a component system

Always build UI through abstracted components, starting with the first occurrence:

- Reuse or extend existing platform components before creating new ones.
- Extract new UI elements and interaction patterns into focused components with explicit contracts, even with a single caller.
- Compose pages from these components. Keep styling and behavior in the components that own them.
- Migrate affected callers to the abstraction in the same change.

Place abstractions at the narrowest correct scope:

- Cross-platform primitives: `apps/web/components/ui`.
- Domain-wide components: the relevant `apps/web/components/<domain>` directory.
- Route composition: thin App Router files.

Do not create a shared component without migrating its real callers. Do not force unrelated behavior into one abstraction merely because it looks similar.

## Quality standard

Complete every relevant state:

- default, hover, focus-visible, active, disabled;
- loading, success, error, empty, unavailable;
- keyboard operation and accessible names;
- focus entry, trapping, dismissal, and restoration for dialogs;
- desktop, tablet, and mobile layout behavior;
- long text, large values, overflow, and narrow-width behavior;
- pending-action feedback without layout shift or stale controls.

Maintain platform consistency in typography, spacing, density, icon semantics, action hierarchy, surface treatment, and responsive behavior. Prefer existing design tokens and shared CSS. Avoid page-specific duplication that introduces a second visual language.

## Visual acceptance

- Review visible copy across the assembled screen. Reject duplicated meaning across headings, metrics, legends, statuses, and explanatory text—including repetition phrased differently. For every repeated phrase or explanation, identify the additional information it contributes; remove it when there is none.
- Review the whole affected view, including hierarchy, density, spacing, typography, alignment, balanced grids, control sizing, and interaction feedback.
- Removing or changing an element includes rebalancing the remaining composition. Resolve awkward gaps, oversized controls, repeated headings, and misaligned values introduced or exposed by the change.
- Check analogous shared views and fix the pattern within the affected flow. Preserve established visual treatments and explicit user preferences unless the user changes them.
- Inspect the rendered result and refine visible problems before handoff. Passing tests and browser diagnostics establishes functional evidence; visual acceptance also requires direct review of composition and interaction quality.
- Do not stop at the smallest functional edit while the affected experience remains visibly unfinished.

## Verification and screenshot gate

Run `pnpm design:export` after adding, renaming, moving, or removing an exported frontend component. Run `pnpm design:check` before handoff.

For any UI change:

1. Run focused tests during implementation.
2. Use the repository-configured `browser-use` workflow for live browser verification. Read the `browser-use` skill before operating it.
3. Select representative shared compositions, relevant states, and viewport boundaries. Shared components do not require screenshots of every route; expand coverage for distinct rendering behavior or unresolved risk.
4. Check browser console, page, and network issues attributable to the change.
5. Save at least one final screenshot after data and fonts have loaded. Capture both desktop and mobile when responsive behavior materially changed.
6. Visually inspect every screenshot and verify relevant interactions before handoff. Resolve visible defects before declaring completion.

The task is incomplete without a final screenshot. Never claim the UI work is finished, complete, fixed, shipped, or ready unless the final response embeds the verified screenshot using its absolute path. If screenshot capture is blocked, report the exact blocker and leave the work explicitly incomplete.
