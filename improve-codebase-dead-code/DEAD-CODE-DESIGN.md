# Dead Code Design

When the user wants to explore alternative removal designs for a chosen dead-code candidate, use this design-alternatives pattern. If the user explicitly asks for or authorizes parallel agents, run the sub-agent version below. Otherwise, produce the alternatives locally.

Uses the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **element**, **entry point**, **live**, **dynamic reference**, **dead closure**, **residue**, **invariant**.

## Process

### 1. Frame the problem space

Before producing removal alternatives, write a user-facing explanation of the problem space for the chosen candidate:

- The element, the entry points checked, and the invariants every removal must preserve
- The reachability evidence, and which category the element falls into (see [DEAD-CODE.md](DEAD-CODE.md))
- A rough illustrative reachability walkthrough or code sketch to ground the constraints — not a proposal, just a way to make the dead code concrete

Show this to the user, then immediately proceed to Step 2.

### 2. Produce removal alternatives

Produce 3+ **radically different** removal designs for the chosen element. Use sub-agents in parallel only when explicitly authorized.

Use a separate technical brief for each alternative: file paths, element, category from [DEAD-CODE.md](DEAD-CODE.md), entry points, static and dynamic references, and invariants. If using authorized sub-agents, prompt each sub-agent with one brief. If working locally, use each brief as a separate design pass. Give each pass a different design constraint:

- Agent 1: "Minimize the change — remove only the dead element."
- Agent 2: "Remove the full dead closure — the element and everything only it reaches."
- Agent 3: "Retire the decision — remove a settled flag or impossible condition together with its dead branch."
- Agent 4 (if applicable): "Make reachability provable — replace dynamic references with static ones so remaining dead elements can be shown dead."

Include both [LANGUAGE.md](LANGUAGE.md) vocabulary and `UBIQUITOUS_LANGUAGE.md` vocabulary so each design names things consistently with the dead-code language and the project's domain language.

Each design outputs:

1. Removal set: elements, dead closure, and affected files
2. Reachability walkthrough showing no live entry point loses behaviour
3. Which dead code the design removes
4. Dynamic references ruled out and how
5. Preserved invariants and live behaviour
6. Verification strategy and trade-offs — what is removed and what dead code remains

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by removed surface, strength of reachability proof, invariant risk, and migration cost.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
