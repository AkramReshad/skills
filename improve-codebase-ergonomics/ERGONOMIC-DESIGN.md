# Ergonomic Design

When the user wants to explore alternative organization or usage designs for a chosen ergonomics candidate, use this design-alternatives pattern. If the user explicitly asks for or authorizes parallel agents, run the sub-agent version below. Otherwise, produce the alternatives locally.

Uses the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **task**, **surface**, **friction**, **organization**, **convenience**, **canonical path**.

## Process

### 1. Frame the problem space

Before producing ergonomic alternatives, write a user-facing explanation of the problem space for the chosen candidate:

- The representative task and behaviour any new organization or usage design would need to preserve
- The friction it imposes, and which category it falls into (see [ERGONOMICS.md](ERGONOMICS.md))
- A rough illustrative task walkthrough or usage sketch to ground the constraints — not a proposal, just a way to make the friction concrete

Show this to the user, then immediately proceed to Step 2.

### 2. Produce ergonomic alternatives

Produce 3+ **radically different** organization or usage designs for the chosen candidate. Use sub-agents in parallel only when explicitly authorized.

Use a separate technical brief for each alternative: file paths, representative task, friction category from [ERGONOMICS.md](ERGONOMICS.md), preserved behaviour and ownership, and current ceremony. If using authorized sub-agents, prompt each sub-agent with one brief. If working locally, use each brief as a separate design pass. Give each pass a different design constraint:

- Agent 1: "Minimize the change — improve the current organization or usage surface with the smallest migration."
- Agent 2: "Maximize discoverability — make the canonical path obvious from domain vocabulary and nearby code."
- Agent 3: "Optimize for the most common task — make the default case trivial."
- Agent 4 (if applicable): "Minimize ceremony — compose stable setup and remove irrelevant choices."

Include both [LANGUAGE.md](LANGUAGE.md) vocabulary and `UBIQUITOUS_LANGUAGE.md` vocabulary so each design names things consistently with the ergonomics language and the project's domain language.

Each design outputs:

1. Organization or usage surface: locations, names, imports, entry points, defaults, and required choices
2. Task example showing how developers use it
3. Which friction the design removes
4. Canonical path, migration, and obsolete paths to delete
5. Preserved behaviour, ownership, and error modes
6. Trade-offs — where organization and convenience improve, where friction remains

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by **organization**, **convenience**, **discoverability**, **ceremony**, **cognitive load**, and migration cost.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
