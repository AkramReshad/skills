# Typing Design

When the user wants to explore alternative typing designs for a chosen typing candidate, use this design-alternatives pattern. If the user explicitly asks for or authorizes parallel agents, run the sub-agent version below. Otherwise, produce the alternatives locally.

Uses the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **value flow**, **entry**, **declared type**, **runtime value**, **boundary**, **parse**, **escape**, **invariant**.

## Process

### 1. Frame the problem space

Before producing typing alternatives, write a user-facing explanation of the problem space for the chosen candidate:

- The value flow, its entry, and the invariants every design must preserve
- Where the declared type and the runtime value can disagree, and which defect category it falls into (see [TYPING.md](TYPING.md))
- A rough illustrative type walkthrough or code sketch to ground the constraints — not a proposal, just a way to make the defect concrete

Show this to the user, then immediately proceed to Step 2.

### 2. Produce typing alternatives

Produce 3+ **radically different** typing designs for the chosen value flow. Use sub-agents in parallel only when explicitly authorized.

Use a separate technical brief for each alternative: file paths, value flow, defect category from [TYPING.md](TYPING.md), entry, declared types, escapes, and invariants. If using authorized sub-agents, prompt each sub-agent with one brief. If working locally, use each brief as a separate design pass. Give each pass a different design constraint:

- Agent 1: "Minimize the change — correct the declared type or remove the escape in place."
- Agent 2: "Parse at the boundary — establish the type once where the value enters and let downstream code rely on it."
- Agent 3: "Fix at the source — correct the imprecise type where it originates and let inference carry it."
- Agent 4 (if applicable): "Maximize precision — state the known set of runtime values as a union, literal set, or structured type."

Include both [LANGUAGE.md](LANGUAGE.md) vocabulary and `UBIQUITOUS_LANGUAGE.md` vocabulary so each design names things consistently with the typing language and the project's domain language.

Each design outputs:

1. Typing design: entry, parse point, declared types, and removed escapes
2. Type walkthrough showing the declared type at each step of the value flow
3. Which defect the design removes
4. Behaviour for invalid input at the boundary
5. Preserved invariants and valid-input behaviour
6. Verification strategy and trade-offs — where type truth improves and where escapes remain

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by type truth, boundary coverage, remaining escapes, caller burden, and invariant risk.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
