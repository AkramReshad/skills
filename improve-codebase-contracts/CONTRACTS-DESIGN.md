# Contracts Design

When the user wants to explore alternative contract designs for a chosen contract-consistency candidate, use this design-alternatives pattern. If the user explicitly asks for or authorizes parallel agents, run the sub-agent version below. Otherwise, produce the alternatives locally.

Uses the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **boundary contract**, **producer**, **consumer**, **definition**, **drift**, **source of truth**, **invariant**.

## Process

### 1. Frame the problem space

Before producing contract alternatives, write a user-facing explanation of the problem space for the chosen candidate:

- The boundary contract, its producer and consumers, and the invariants every design must preserve
- Where each consumer disagrees with real producer output, and which drift category it falls into (see [CONTRACTS.md](CONTRACTS.md))
- A rough illustrative contract trace or payload sketch to ground the constraints — not a proposal, just a way to make the drift concrete

Show this to the user, then immediately proceed to Step 2.

### 2. Produce contract alternatives

Produce 3+ **radically different** contract designs for the chosen boundary contract. Use sub-agents in parallel only when explicitly authorized.

Use a separate technical brief for each alternative: file paths, boundary contract, drift category from [CONTRACTS.md](CONTRACTS.md), producer definition and output, consumer definitions, and invariants. If using authorized sub-agents, prompt each sub-agent with one brief. If working locally, use each brief as a separate design pass. Give each pass a different design constraint:

- Agent 1: "Minimize the change — correct the drifting consumer definition in place."
- Agent 2: "Derive from one definition — generate or derive consumer definitions from the producer's."
- Agent 3: "Parse at the boundary — make the consumer validate producer output at runtime against the corrected definition."
- Agent 4 (if applicable): "Pin the contract with real output — verify every consumer against recorded producer output."

Include both [LANGUAGE.md](LANGUAGE.md) vocabulary and `UBIQUITOUS_LANGUAGE.md` vocabulary so each design names things consistently with the contract language and the project's domain language.

Each design outputs:

1. Contract design: producer definition, consumer definitions, and how they relate
2. Contract trace showing the corrected agreement with real producer output
3. Which drift the design removes
4. Source of truth and derivation points
5. Preserved producer output and compatibility for other consumers
6. Verification strategy and trade-offs — where agreement becomes durable and where drift can recur

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by agreement, durability against future drift, runtime safety, migration cost, and invariant risk.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
