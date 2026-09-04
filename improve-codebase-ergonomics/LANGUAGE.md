# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly — don't substitute vague labels such as "cleanup," "polish," or "developer experience." Consistent language is the whole point.

## Terms

**Task**
A representative developer action in the codebase. Deliberately scale-agnostic — applies equally to finding an implementation, adding a caller, constructing test state, changing configuration, or invoking a common operation.

**Surface**
Everything a developer must find, understand, choose, and do to complete a task correctly. Includes file placement, names, imports, arguments, ordering, defaults, configuration, and required setup.

**Friction**
Effort imposed by the surface beyond the task's essential complexity. Friction must be grounded in a representative task rather than personal aesthetic preference.

**Organization**
Placement, grouping, naming, and import structure that makes code predictable to find and change. Good organization follows domain vocabulary and established ownership.

**Convenience**
Useful defaults, helpers, composition, or entry points that reduce repeated ceremony for common tasks. Convenience earns its place when it makes the correct path easier without creating a competing path.

**Ceremony**
Required steps, arguments, imports, conversions, or setup that do not express the developer's intent. Necessary domain choices and explicit invariants are not ceremony.

**Discoverability**
How readily the correct code or usage path can be found from the task, surrounding code, and domain vocabulary.

**Cognitive load**
The concepts, choices, context switches, and hidden facts a developer must hold to complete a task correctly.

**Canonical path**
The single expected location or usage path for a task. A canonical path may be a module location, import, command, helper, builder, or common-case entry point.

**Verification**
Evidence that an ergonomics improvement reduced friction for its representative task while preserving behaviour, ownership, and required explicit choices.

## Principles

- **The task walkthrough.** Trace a representative task from intent to completion. Count what must be found, learned, chosen, repeated, and kept in working memory.
- **The canonical-path test.** A developer starting from domain vocabulary and nearby callers should encounter one obvious location or usage path.
- **The organization test.** Code should live where its domain meaning and ownership predict. Moving code without improving predictability is churn.
- **The discoverability test.** Names, exports, placement, and examples should lead developers toward correct usage without requiring repository archaeology.
- **The ceremony test.** Repeated steps that do not express intent should be removed, defaulted, composed, or hidden when the correct behaviour is stable.
- **The choice test.** Preserve choices that carry domain meaning or invariants. Remove choices that merely expose implementation detail or repeat a stable default.
- **The common-path test.** Make the frequent correct task direct. Less-common variants may remain explicit when their differences matter.
- **The residue test.** After establishing a canonical path, migrate callers and delete obsolete aliases, wrappers, helpers, exports, and documentation. A new convenience layered beside old paths increases friction.
- **Behaviour and ownership are invariants.** An ergonomics improvement must preserve runtime behaviour and documented ownership unless the user explicitly accepts a broader change.
- **Verification matches the friction.** Use the narrowest reliable evidence: fewer imports, steps, arguments, choices, context switches, touched files, or plausible locations, plus the repository correctness gate.

## Relationships

- A **Task** is completed through a **Surface**.
- A **Surface** imposes **Friction** through poor **Organization**, weak **Discoverability**, excess **Ceremony**, or unnecessary choices.
- **Convenience** reduces ceremony for a common task.
- **Organization** and **Discoverability** lead developers toward a **Canonical path**.
- Reduced **Friction** lowers **Cognitive load**.
- **Verification** shows that the task became easier while behaviour and ownership remained intact.

## Rejected framings

- **Ergonomics as aesthetic cleanup**: formatting preference, symmetry, and personal taste do not establish task friction.
- **Convenience as more helpers**: an additional helper is valuable only when it becomes the canonical path and obsolete paths can be removed.
- **Organization as moving files**: relocation is useful only when placement becomes more predictable from domain vocabulary and ownership.
- **Fewer lines as proof**: line count may fall while choices, hidden facts, or context switches increase. Verify the representative task.
