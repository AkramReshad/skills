# Coverage Design

When the user wants to explore alternative test designs for a chosen coverage candidate, use this design-alternatives pattern. If the user explicitly asks for or authorizes parallel agents, run the sub-agent version below. Otherwise, produce the alternatives locally.

Uses the vocabulary in [LANGUAGE.md](LANGUAGE.md) — **contract**, **caller**, **test surface**, **gap**, **mutation**, **assertion**, **invariant**.

## Process

### 1. Frame the problem space

Before producing test alternatives, write a user-facing explanation of the problem space for the chosen candidate:

- The contract, its callers, and the production behaviour every design must leave unchanged
- The mutation that currently survives, and which gap category it falls into (see [COVERAGE.md](COVERAGE.md))
- A rough illustrative contract walkthrough or test sketch to ground the constraints — not a proposal, just a way to make the gap concrete

Show this to the user, then immediately proceed to Step 2.

### 2. Produce test alternatives

Produce 3+ **radically different** test designs for the chosen contract. Use sub-agents in parallel only when explicitly authorized.

Use a separate technical brief for each alternative: file paths, contract, gap category from [COVERAGE.md](COVERAGE.md), callers, test surface, and existing tests. If using authorized sub-agents, prompt each sub-agent with one brief. If working locally, use each brief as a separate design pass. Give each pass a different design constraint:

- Agent 1: "Minimize the change — add the assertion to the closest existing test."
- Agent 2: "Test through the outermost interface the contract's callers use."
- Agent 3: "Cover the contract as a table of inputs and outcomes, including its edges and error modes."
- Agent 4 (if applicable): "Isolate the contract at the nearest existing seam with the repository's existing test stand-ins."

Include both [LANGUAGE.md](LANGUAGE.md) vocabulary and `UBIQUITOUS_LANGUAGE.md` vocabulary so each design names things consistently with the coverage language and the project's domain language.

Each design outputs:

1. Test design: test surface, setup, inputs, and assertions
2. Contract walkthrough showing which mutations the tests catch
3. Which gap the design closes
4. Fixtures and test stand-ins used
5. Preserved production behaviour
6. Verification strategy and trade-offs — mutations caught, brittleness, test runtime, and maintenance

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose. Contrast by mutations caught, interface fidelity, brittleness, test runtime, and maintenance.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated — the user wants a strong read, not a menu.
