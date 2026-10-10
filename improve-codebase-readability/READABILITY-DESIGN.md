# Readability Design

When the user wants to explore alternative implementations for a chosen readability candidate, use this design-alternatives pattern. If the user explicitly asks for or authorizes parallel agents, run the sub-agent version below. Otherwise, produce the alternatives locally.

Uses the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **reading task**, **cognitive load**, **local reasoning**, **responsibility**, **state**, **contract**, **invariant**.

## Process

### 1. Frame the problem space

Before producing implementation alternatives, write a user-facing explanation of the problem space for the chosen candidate:

- The representative reading task and invariants every implementation must preserve
- The context the reader currently retains or reconstructs, and which friction category it falls into (see [READABILITY.md](READABILITY.md))
- A rough illustrative reading walkthrough or code sketch to ground the constraints

Show this to the user, then immediately proceed to Step 2.

### 2. Produce implementation alternatives

Produce 3+ **radically different** implementations for the chosen candidate. Use sub-agents in parallel only when explicitly authorized.

Use a separate technical brief for each alternative: file paths, representative reading task, friction category from [READABILITY.md](READABILITY.md), relevant contracts, state, ordering, and invariants. If using authorized sub-agents, prompt each sub-agent with one brief. If working locally, use each brief as a separate design pass. Give each pass a different design constraint:

- Agent 1: "Minimize the change — improve names, expressions, grouping, and local control flow within the current implementation."
- Agent 2: "Separate coherent responsibilities — expose the workflow through meaningful operations whose contracts reduce retained context."
- Agent 3: "Minimize interacting state — make value meanings, branch outcomes, and precedence explicit."
- Agent 4 (if applicable): "Minimize navigation — inline or regroup fragments so one coherent decision can be understood together."

Include both [LANGUAGE.md](LANGUAGE.md) vocabulary and `UBIQUITOUS_LANGUAGE.md` vocabulary so each design names things consistently with the readability language and the project's domain language.

Each design outputs:

1. Implementation sketch with names, responsibilities, and contracts
2. Reading walkthrough showing how the maintainer answers the same question
3. Which retained facts, implicit rules, or context switches the design removes
4. Added calls, contracts, and navigation the reader would need to learn
5. Preserved behaviour, ownership, ordering, and error modes
6. Verification strategy and trade-offs — where local reasoning improves and where cognitive load remains

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Compare by **local reasoning**, **cognitive load**, state tracking, contract complexity, navigation, and invariant risk.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
