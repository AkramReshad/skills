# Codebase entropy

## Philosophy

Codebases tend toward disorder as changes accumulate. Individually reasonable changes can leave behind unclear responsibilities, fragmented logic, duplication, inefficient operations, difficult code, and maintenance tooling that no longer fits the system. Sustained development requires deliberate effort to constrain and remove that disorder.

The need for engineering guardrails grows with the rate of meaningful changes and the burden of coordinating them. Headcount has historically been a useful proxy for that pressure. AI agents weaken the relationship between headcount and output: a solo developer can now generate changes at a pace previously associated with a much larger team.

Commit counts are an illustration of change volume, assuming meaningful commits without gaming. They are not a productivity target or a precise threshold for adopting a particular process.

## Why engineering organizations build guardrails

As engineering organizations grow, personal familiarity becomes insufficient to maintain a shared codebase. Reviews, tests, CI/CD, repository scripts, domain ownership, and infrastructure teams help coordinate changes and preserve quality. Large organizations invest in internal engineering platforms because people who have never met must safely change related systems.

These practices also supply judgment: a reviewer notices that a function is inefficient, a service is hard to understand, modules should be combined, or scripts should become reusable tooling. Periodic maintenance creates time to remove dead code, address deferred work, and improve the system's structure.

The underlying pressure is the volume of changes that must be understood and reconciled. A small team using many AI agents can encounter that pressure without acquiring the review capacity and maintenance practices that traditionally grew alongside a larger engineering team.

## The AI development problem

Rapid implementation can outrun understanding. One observed example was a staff engineer producing roughly 2,000 commits in three weeks through extensive parallel agent work. The resulting codebase was difficult to maintain. The missing ingredient was sustained scrutiny of the accumulated result: readability, architecture, reuse, performance, and overall coherence.

The operating belief is that AI-assisted development needs maintenance capacity that scales with its output. Passing automated checks does not by itself supply all the engineering judgment needed to keep a codebase understandable and adaptable.

## Maintenance skills

The maintenance skills provide recurring, focused engineering scrutiny:

- Architecture examines responsibilities, interfaces, and how knowledge is distributed.
- Readability examines the effort required to understand behavior and safely change it.
- Performance examines unnecessary computational and operational cost.
- Ergonomics examines friction in working with and reusing the codebase.

Test-suite maintenance and repository-layout maintenance address additional sources of accumulated disorder.

Each skill has a distinct purpose. Minimal overlap is desirable, while useful changes remain possible where concerns intersect. Readability improvements may include proportional structural changes when those changes directly make behavior easier to follow.

Skills guide model attention and judgment. Model quality still matters; a skill cannot guarantee good findings or good implementation.

## Run order

Run the workflows in this order. Each pass treats the results of earlier passes as settled.

1. Dead code (`prune-codebase-workflow`). Remove unreachable code first so every later pass reviews, fixes, and restructures only live code.
2. Quality (`repair-codebase-workflow`). Fix real bugs so later passes start from code that works and tests that can be trusted.
3. Coverage (`cover-codebase-workflow`). Add tests for correct behaviour after the bugs are fixed, so later structural passes have a safety net. Tests target contracts through interfaces, so most survive refactors.
4. Architecture (`deepen-codebase-workflow`). Make the largest structural moves before anything polishes code that might then move.
5. Repository layout. Once ownership has settled, put files where their owners predict.
6. Error handling (`surface-codebase-workflow`). Handle failures at the layers Architecture settled.
7. Typing (`tighten-codebase-workflow`). Make declared types true for the settled structure and error handling.
8. Contracts (`align-codebase-workflow`). Align consumers with producers once types are true and error shapes are stable.
9. Ergonomics (`streamline-codebase-workflow`). Smooth how the settled pieces are found and called.
10. Performance (`optimize-codebase-workflow`). Optimize the final structure against code that will not be reshuffled afterwards.
11. Readability (`clarify-codebase-workflow`). Make the final code, including optimizations, easy to read without changing runtime cost.
12. Test suite. Prune last, after every earlier pass has added or replaced tests.

Ergonomics, Performance, and Readability preserve types, contracts, and error modes as invariants, so those must be correct before they run.
