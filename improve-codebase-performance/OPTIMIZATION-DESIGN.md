# Optimization Design

When the user wants to explore alternative optimizations for a chosen performance candidate, use this design-alternatives pattern. If the user explicitly asks for or authorizes parallel agents, run the sub-agent version below. Otherwise, produce the alternatives locally.

Uses the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **workload**, **cost**, **cost center**, **cost model**, **optimization**, **invariant**, **verification**.

## Process

### 1. Frame the problem space

Before producing optimization alternatives, write a user-facing explanation of the problem space for the chosen candidate:

- The representative workload and invariants every optimization must preserve
- The evidence and cost model for the cost center (see [OPTIMIZING.md](OPTIMIZING.md))
- A rough illustrative execution sketch to ground the cost model — not a proposal, just a way to make the mechanism concrete

Show this to the user, then immediately proceed to Step 2.

### 2. Produce optimization alternatives

Produce 3+ **radically different** optimizations for the chosen cost center. Use sub-agents in parallel only when explicitly authorized.

Use a separate technical brief for each alternative: file paths, workload, evidence category from [OPTIMIZING.md](OPTIMIZING.md), cost model, invariants, and verification surface. If using authorized sub-agents, prompt each sub-agent with one brief. If working locally, use each brief as a separate design pass. Give each pass a different design constraint:

- Agent 1: "Minimize the change — improve the implementation behind the existing seam."
- Agent 2: "Maximize scaling — reduce how cost grows with workload cardinality."
- Agent 3: "Optimize the most common workload — make the default path cheapest."
- Agent 4 (if applicable): "Optimize lifecycle or round trips — amortize valid setup and reduce crossings."

Include both [LANGUAGE.md](LANGUAGE.md) vocabulary and `UBIQUITOUS_LANGUAGE.md` vocabulary so each design names things consistently with the performance language and the project's domain language.

Each design outputs:

1. Optimization mechanism and affected implementation
2. Execution example showing how the workload changes
3. Which cost the implementation removes or reduces
4. Preserved invariants and error modes
5. Verification strategy matched to the mechanism
6. Trade-offs — expected effect, permanent complexity, and residual cost

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by expected cost reduction, scaling behaviour, implementation complexity, invariant risk, and strength of evidence.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
