---
name: codebase-map
description: Create or update docs/codebase_architecture.md as a high-level map of the repository organized by logical domains. Use when asked to map repo structure, refresh an architecture doc, or keep a domain-based codebase overview current.
metadata:
  short-description: Update a repo architecture map
---

# Codebase Map

Create or update a repository architecture document organized by logical business and engineering
responsibilities. Map each responsibility across its implementation layers.

Default output path: `docs/codebase_architecture.md`

Use a different output path only if the user explicitly asks for one.

## Goal

Produce a factual architecture map that helps another agent quickly understand:

- the main logical domains of the repo
- which files support each domain, including shared and overlapping ownership
- how the major runtime areas are split
- where the key entrypoints and boundaries live

This is a map, not a review.

- no recommendations
- no bug finding
- no cleanup advice
- no opinions

## Source Of Truth Order

Use these inputs in this order:

1. existing `docs/codebase_architecture.md`, if present
2. `docs/codebase_domains.md`, if present
3. `code_review/*_issues.md`, if present
4. the codebase itself

The job is usually an update, not a rewrite.
If `docs/codebase_architecture.md` exists, preserve its structure and improve it to match the current repo.
Preserve useful existing names and boundaries. Reassess the taxonomy when current repo evidence
shows that technical groupings obscure logical responsibilities.
If `docs/codebase_architecture.md` does not exist, do a full mapping and create it.

## Domain Rules

- Preserve useful established domain splits; additions need coherent responsibility and navigation value.
- Do not collapse existing canonical domains unless two are clearly duplicates.
- If `docs/codebase_domains.md` exists, treat it as the canonical domain seed file.
- If `docs/codebase_domains.md` does not exist, do a full mapping and create it.
- When `code_review/*_issues.md` exists, derive the initial domain list from those filenames by removing `_issues.md`.
- If repo evidence establishes a new domain under the Domain Additions and Splits criteria below, add it.
- Keep domain names repo-native. Do not replace them with generic labels.
- Prefer readable display names in `docs/codebase_domains.md`, not slug-only names.

## Domain Stability Policy

The goal is not perfect taxonomy purity. The goal is stable, useful domains that help future agents orient quickly and run unattended work reliably.

- Preserve existing domain names by default.
- Keep `docs/codebase_domains.md` as the stable seed for future runs.
- `docs/codebase_architecture.md` may be richer and more narrative, but it should stay close to the canonical domain doc.
- Do not rename an existing domain unless the rename is strongly justified by an actual repo rename or a clearly obsolete label.
- Prefer adding domains, splitting domains, or removing truly deleted domains over renaming active domains.
- Existing maps anchor names and scope; assess whether their entries express logical responsibilities or technical groupings. Explain evidence-backed restructuring when those groupings obscure ownership.
- Prefer adding or splitting domains over collapsing them when the repo already has an established split.
- If a repo has a substantial test surface, keep a separate test-focused domain and include domain-specific regression coverage within the responsibility it verifies.
- Only merge domains when they are clearly redundant and the split adds no navigation value.
- Avoid renaming domains unless the repo itself has clearly renamed the area and the old label is no longer useful.
- Avoid domain-name churn across runs. Stability is more important than finding the theoretically perfect taxonomy.
- If boundaries are fuzzy, preserve the current split and refine descriptions instead of reorganizing aggressively.

## Domain Additions and Splits

A domain owns a coherent business or engineering responsibility, including its concepts, rules,
workflows, and supporting implementation. Billing, Playlist Generation, Infrastructure, and Tests
are all valid kinds of domains. A domain can span frontend code, APIs, services, jobs, models,
repositories, and tests.

Files can belong to multiple domains. Billing can own core billing logic, multiple billing API
surfaces, billing models, settlement jobs, and `tests/billing/`. Those tests also belong to Tests,
which owns test organization, fixtures, isolation, execution, and verification conventions.
Describe the responsibility of each overlap; domain file lists need not be disjoint.

Discover responsibilities before assigning implementation files. Add a domain when repo evidence
establishes independently coherent concepts and rules, with enough scope to make separate
navigation useful. This may expose a responsibility currently distributed across technical layers
or split an existing broad domain. Existing file ownership does not preclude a logical domain.

A capability or analytical method can remain within a broader domain when it shares that domain's
concepts and rules. Size is supporting evidence, not the deciding criterion. Check candidates
against comparable responsibilities and apply a consistent level of abstraction. When ownership
remains fuzzy, preserve the existing split and refine its description.

For each addition or split, show its responsibility, concepts and governing rules, interfaces with
other domains, and supporting implementation across relevant layers, including regression coverage
where present. A route, service declaration, directory, or file count alone establishes location,
not the domain boundary. Separate the runtime-shape inventory from logical domain discovery.

## Workflow

### 1. Read the current map first

If `docs/codebase_architecture.md` exists:

- read it first
- keep the overall shape if it is useful
- treat it as the preferred output style for that repo

The target is to replicate and refresh the established architecture-doc style, not invent a new format each run.

### 2. Read the domain seed file

Look for `docs/codebase_domains.md`.

- If present, use it to anchor the domain sections.
- If missing, create it before finishing.

If `code_review/*_issues.md` exists, use those filenames to seed or confirm the domain list.
Make the canonical domain doc readable and actionable for future runs.
Use a markdown table with:

- domain display name
- senior engineer persona for that domain
- short scope
- key files/directories to inspect

When tests are substantial, prefer a separate test-focused domain such as `Tests` or `Test & Debug`.
Include resource-specific tests in their owning domains as well; overlapping references are expected.

### 3. Map the repo thoroughly

Read the root config files to understand language, framework, runtime, and entrypoints.
Identify implemented business and engineering responsibilities from product concepts, rules, and
workflows. Trace each across the major runtime directories and compare it with the canonical map.
Record the runtime areas separately; shared layers can support several logical domains.

Focus on executable code first:

- entrypoints
- routes/controllers/activities/handlers
- services/use-cases
- models/entities
- persistence/data access
- workers/background jobs
- shared infrastructure/framework glue
- tests
- deployment/infra files

Treat `docs/`, `notes/`, generated assets, and review artifacts as supporting material unless they define runtime behavior.

### 4. Use subagents when available

When subagents are available, spawn multiple explorer-style subagents in parallel for major top-level runtime areas or established domain slices. Have each subagent:

- read the relevant files
- summarize the domain purpose
- identify its concepts, governing rules, and workflows
- identify key files and boundaries
- report interfaces and overlapping responsibilities with other domains, including shared tests

Then merge the results into one consistent architecture document.

Do not delegate the final synthesis. The main agent owns the final structure and wording.

### 5. Update the architecture doc

Write or update `docs/codebase_architecture.md`.
If the file already exists, update it in place to preserve a familiar structure where possible.
If it does not exist, create it from a full repo mapping.

## Output Requirements

The document should:

- lead with a short project identity summary
- organize the main body by logical domains
- include enough file references for each domain to be navigable
- explain governing rules and interfaces for new or split domains, with evidence across relevant layers
- describe overlapping ownership where the same files support multiple responsibilities
- preserve established repo domain splits when present
- include a brief summary of supporting material separately from runtime domains
- include a small statistics section at the end when useful

Use clear headings and separators.
Prefer the existing repo-local style if one already exists.

## Minimum Section Shape

Use this when no strong existing structure is present:

```md
# {Repo} Codebase Architecture Overview

> Auto-generated: YYYY-MM-DD

{1-2 sentence project identity}

---

## Logical Domains

### 1. {domain_name}

**Purpose:** {what it owns}

**Concepts & Rules:** {governing concepts, lifecycle, calculations, or operational policy}

**Key Directories & Files:**

- `path` - {role}
- `path` - {role}

**Entrypoints / Interfaces:**

- `path`
- `path`

**Related Areas:** {interfaces and overlapping responsibilities with other domains}

---

## Supporting Material

- `docs/` - supporting documentation
- `docs/codebase_domains.md` - canonical domain seed
- `notes/` - agent memory / implementation notes
- `code_review/` - review artifacts

---

## Key Statistics

| Category    | Count |
| ----------- | ----- |
| Domains     | N     |
| Entrypoints | N     |
```

## Writing Rules

- Stay factual.
- Keep descriptions short and concrete.
- Do not turn the output into a raw directory dump.
- Do not let supporting folders dominate the architecture.
- Include domain-specific regression coverage alongside shared test-domain references.
- Prefer preserving and refining an existing good architecture doc over reformatting it unnecessarily.

## Notes File Format

When creating or updating `docs/codebase_domains.md`, use this shape:

```md
| #   | Domain          | Persona                 | Scope                             | Key Files/Dirs       |
| --- | --------------- | ----------------------- | --------------------------------- | -------------------- |
| 1   | **Domain Name** | Senior Engineer Persona | Short description of what it owns | `path/`, `path/file` |
```

Use readable names such as `Analytics Services`, not slug-only forms such as `analytics_services`, unless the repo itself clearly uses the slug as the display name.
Preserve existing persona text by default. If the file is being created from scratch, assign a sensible senior-level persona for each domain, such as `Database Architect`, `Senior Infrastructure Engineer`, `Senior Android Engineer`, `Senior Backend Engineer`, `Senior Frontend Engineer`, `Senior Security Engineer`, or `Senior QA / Test Engineer`.
