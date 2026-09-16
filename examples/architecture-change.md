# Architecture change

**User:** “Use our backend domain skill with $closed-loop-companion to move invoice rendering to a queue. Preserve ordering and the existing retry guarantee.”

**Route:** FULL — architecture, failure handling and observable behavior change.

**Flow:** the domain skill proposes implementation; Codex checks constraints and records acceptance criteria; the companion requires failure/ordering evidence and independent direction review. Consequential unresolved tradeoffs return to the user.

**Outcome:** READY_FOR_USER_ACCEPTANCE after current evidence and reviews pass. A direction conflict or missing required evidence keeps the gate closed; repeated failure triggers reassessment, not endless patches.
