# Language

Shared vocabulary for every suggestion this skill makes. Use these terms exactly. Preserve canonical repo-local and domain vocabulary.

## Terms

**Reading task**
A representative question a maintainer must answer about behaviour. Examples include determining which fallback wins, when a database write occurs, how an error propagates, or which consequences follow from changing one decision. Ground the question in current code and a plausible maintenance task.

**Cognitive load**
The concepts, choices, context switches, and hidden facts a developer must hold to complete a task correctly.

**Local reasoning**
Understanding a decision and its consequences from a small, coherent body of code and explicit contracts. Relevant context may include callers and dependencies; identify the context the decision actually requires.

**Responsibility**
A coherent purpose with its own rules and reasons to change. Loading evidence, resolving fallback precedence, persisting a result, and constructing a response may have distinct responsibilities even when they participate in one workflow.

**State**
Values and effects whose current meaning depends on the execution path so far. Includes reassigned variables, partially assembled results, shared mutable objects, and transaction progress. Difficulty grows when the reader must track their interactions across distant statements.

**Abstraction level**
The level of detail at which code describes intent, policy, orchestration, or mechanics. A coherent passage lets the reader follow its purpose without repeatedly reconstructing that purpose from lower-level detail.

**Contract**
What a reader must know about an operation: inputs, results, effects, ordering, invariants, and error modes. A useful contract lets the reader reason about the calling code without opening the implementation to discover essential consequences.

**Invariant**
Behaviour that must remain unchanged by a readability refactor. Includes results, ordering, isolation, transaction semantics, error modes, freshness, determinism, and other task-specific contracts.

**Verification**
Evidence that the same reading task requires less retained or reconstructed context while behaviour and ownership remain intact. Explain the specific burden removed; correctness checks establish preserved behaviour.

## Principles

- **The change-context test.** "To change this decision safely, how much unrelated code must I understand?"
- **The reading walkthrough.** Trace the same question before and after the proposed change. Identify facts held in working memory, rules inferred from order, and implementations opened to discover essential consequences.
- **The responsibility test.** Identify coherent purposes and their rules. A useful separation lets readers understand one decision without learning unrelated mechanics.
- **The state test.** Give values stable meanings and keep their lifetimes close to their use. Make transitions explicit when mutation is essential to the workflow.
- **The ordering test.** Make precedence, sequencing, and transaction rules visible while preserving their actual execution semantics.
- **The abstraction-level test.** Keep each passage coherent in its level of detail. Extract or inline where doing so helps readers retain the larger purpose.
- **The naming test.** Names should identify the domain role, decision, or effect. Expand dense expressions when named intermediate concepts clarify the rules.
- **The extraction test.** A helper earns its place when its name and contract let the reader understand the caller without reconstructing its implementation. Include parameters, shared state, navigation, and error handling in the assessment.
- **Behaviour and ownership are invariants.** A readability improvement must preserve runtime behaviour and documented ownership unless the user explicitly accepts a broader change.
- **Verification matches the friction.** State which facts the reader can stop retaining, which rules become explicit, and which navigation becomes unnecessary. Then verify preserved behaviour through the repository's correctness gate.

## Relationships

- A **Reading task** requires understanding responsibilities, decisions, and their consequences.
- Interacting **State**, implicit ordering, mixed **Abstraction levels**, and unclear **Contracts** increase **Cognitive load**.
- Coherent **Responsibilities** and explicit **Contracts** support **Local reasoning**.
- **Verification** establishes that the reading task became easier and the **Invariants** survived.

## Assessment limits

- Length, branch counts, and complexity metrics are discovery aids. Explain the reading difficulty supported by the code.
- Long, regular mappings and cohesive algorithms may already be readable. Short functions can still require substantial hidden context.
- Helper extraction may increase navigation and contract complexity. Assess the complete reading task, including the new calls.
- Comments can explain a necessary constraint or rationale. Assess whether the code itself can express the rule more directly before relying on narration.
- Easier reasoning is a plausible benefit for AI agents. Claims of improved agent accuracy or speed require evidence from agent tasks.
