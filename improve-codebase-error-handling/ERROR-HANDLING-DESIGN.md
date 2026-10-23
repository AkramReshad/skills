# Error Handling Design

When the user wants to explore alternative handling designs for a chosen error-handling candidate, use this design-alternatives pattern. If the user explicitly asks for or authorizes parallel agents, run the sub-agent version below. Otherwise, produce the alternatives locally.

Uses the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **failure**, **failure path**, **observer**, **handler**, **owning layer**, **error shape**, **cause**, **invariant**.

## Process

### 1. Frame the problem space

Before producing handling alternatives, write a user-facing explanation of the problem space for the chosen candidate:

- The failure path, its observer, and the invariants every design must preserve
- What the observer currently receives, and which defect category it falls into (see [ERROR-HANDLING.md](ERROR-HANDLING.md))
- A rough illustrative failure walkthrough or code sketch to ground the constraints — not a proposal, just a way to make the defect concrete

Show this to the user, then immediately proceed to Step 2.

### 2. Produce handling alternatives

Produce 3+ **radically different** handling designs for the chosen failure path. Use sub-agents in parallel only when explicitly authorized.

Use a separate technical brief for each alternative: file paths, failure path, defect category from [ERROR-HANDLING.md](ERROR-HANDLING.md), owning layer, error shape, and invariants. If using authorized sub-agents, prompt each sub-agent with one brief. If working locally, use each brief as a separate design pass. Give each pass a different design constraint:

- Agent 1: "Minimize the change — correct the defective handler in place."
- Agent 2: "Move the decision to the owning layer — remove handlers below it and let the failure propagate."
- Agent 3: "Standardize the shape — express the failure through the domain's established error shape and translate once at the seam."
- Agent 4 (if applicable): "Make the outcome explicit in the result — represent failure, absence, fallback, and partial success as distinct results."

Include both [LANGUAGE.md](LANGUAGE.md) vocabulary and `UBIQUITOUS_LANGUAGE.md` vocabulary so each design names things consistently with the error-handling language and the project's domain language.

Each design outputs:

1. Handling design: origin, handlers, owning layer, and error shape
2. Failure walkthrough showing what the observer receives
3. Which defect the design removes
4. Cause preservation and translation points
5. Preserved invariants and success-path behaviour
6. Verification strategy and trade-offs — where explicitness improves and where handling burden remains

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by explicitness, cause preservation, shape consistency, ownership, caller burden, and invariant risk.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
