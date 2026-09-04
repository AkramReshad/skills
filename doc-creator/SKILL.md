---
name: doc-creator
description: Create and update concise, standalone Markdown project docs. Use when Codex needs to write, revise, organize, or relocate docs while preserving truth, matching repository conventions, and avoiding conversational artifacts.
---

# Doc Creator

## Priorities

1. Truth. Document only facts, decisions, requirements, constraints, and rationale supported by the user, the repo, or cited source material.
2. Succinctness. Write the shortest doc that carries the needed meaning. Remove redundancy, filler, and boilerplate sections.
3. Standalone clarity. Make the doc understandable without the chat, meeting, prompt, or agent reasoning that led to it.

Do not record major decisions, architecture, vendors, dates, owners, metrics, requirements, or roadmap claims unless they are explicit or the user has given permission to decide for that repo. Ask when a missing decision blocks the doc. Otherwise mark it as an open question.

## Workflow

1. Inspect existing docs with `rg --files` and `rg --files docs`.
2. Use the user-provided path when given.
3. If no path is given, use `docs/` when it exists. Ask before creating `docs/`.
4. Use the closest existing domain folder. Ask before creating a new domain folder.
5. Check nearby docs or templates for naming, section order, and tone.
6. Write or edit only the content needed.
7. Run the final checks.

Common folder names such as `docs/business`, `docs/infra`, `docs/architecture`, `docs/product`, `docs/hardware`, `docs/research`, and `docs/operations` are examples, not standards. Follow the repo's existing taxonomy.

## Naming

Treat path, filename, title, and scope as one contract. Do not materially change that contract. If
requested content exceeds it, decide whether to rename, split, or create another document; update
references.

## Writing Rules

Define project-specific terms the first time they appear.

Prefer direct durable statements:

- "Decision: API clients authenticate with OAuth 2.0."
- "Open question: production rollback owner."

Avoid unsupported specificity:

- Do not turn plausible assumptions into decisions.
- Do not invent details to make the doc feel complete.
- Do not add timelines, owners, metrics, vendors, or implementation choices without support.

Avoid conversational artifacts:

- "as discussed"
- "as requested"
- "the user wants"
- "we talked about"
- "from the conversation"
- "this thread"
- "I think"
- "you said"

Avoid unnecessary meta-commentary:

- intended reader statements
- drafting-process notes
- agent handoff notes
- explanations of what the doc is doing instead of the content itself
- TODOs caused only by missing author context

Use only headings that earn their place. Prefer compact sections such as `Decision`, `Rationale`, `Scope`, `Definitions`, `Requirements`, `Open Questions`, or domain-specific equivalents.

## Final Checks

Confirm:

- the path, filename, title, and scope agree
- material claims are supported or marked as open questions
- the doc is standalone
- redundant sections and repeated points are removed
- conversational artifacts are gone

Useful residue scan:

```bash
rg -n "as discussed|as requested|conversation|thread|the user|you said|we talked|I think|from chat|intended reader|this document|this doc" <doc-path>
```

Treat matches as review prompts, not automatic failures.

Report the final path and any placement decision that matters.
