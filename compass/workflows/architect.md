# Workflow — Architect

Use when the user asks to design a system, choose an architecture, or plan a new feature's structure.

## Process

### 1. Discover the system class

Ask the user (or infer from context):

- Is this **mission-critical** (Type A — life/finance), **commercial** (Type B), or **casual** (Type C)?
- New project or feature inside an existing system?
- Expected scale (users, traffic, data volume)?
- Team size + experience with distributed systems?

### 2. Run the architectural heuristics in order

Follow [reference/architectural-heuristics.md](../reference/architectural-heuristics.md):

1. Nature & criticality → 2. Decomposition → 3. Relevance filter → 4. Tech stack → 5. Scaling needs → 6. Distributed-system capability → 7. Sync vs async → 8. UI ↔ domain isolation → 9. Pattern injection check.

### 3. Stack conversation

If the user hasn't named a stack:

- Ask what stacks they know.
- Discuss fit with the project (latency, scale, ecosystem, team familiarity).
- **Defer to the user's final choice.** After choice, optimize patterns and folder structure for that stack.

### 4. Pick the paradigm

Match the system to a paradigm using [reference/architecture-paradigms.md](../reference/architecture-paradigms.md):

- Single-machine app → Layered or MVC
- Multi-team independent deploys → Microservices
- Cross-system reactive workflows → Pub/Sub
- Decoupled background ops → Message Queue

Mix is fine: microservices internally Layered, exchanging events via Pub/Sub.

### 5. Define quality targets

Pick 2–3 from [reference/quality-criteria.md](../reference/quality-criteria.md) that matter most for this system class. State them explicitly. They're inputs to the ADR and the code review later.

### 6. Produce the design output

Deliver, in this order:

1. **One-paragraph summary** — what is being built and why.
2. **Decomposition diagram** (text or Mermaid) — modules + their responsibilities.
3. **Paradigm + key trade-offs** — why this paradigm, what's deliberately sacrificed.
4. **Stack choice** — confirm + justify the user's pick.
5. **Quality targets** — measurable.
6. **ADR draft** — fill [checklists/adr.md](../checklists/adr.md).
7. **First slice** — smallest end-to-end vertical that proves the architecture.

### 6.5. Design checklist

Walk [checklists/design.md](../checklists/design.md) before declaring the design done. Each unchecked box is either a gap to fill or an explicit waiver to record in the ADR.

### 7. Simplicity gate

Before output, run [reference/simplicity-guard.md](../reference/simplicity-guard.md) over the design:

- Could a single service / single file / single function meet the stated requirements? If yes, present that first.
- Each module, layer, queue, cache, service boundary must answer to a **named present force** (scale, team split, regulatory, measured perf). Strip the rest.
- No speculative microservice splits, no "we'll add Kafka later", no plugin points without a second consumer today.
- Anchor every choice inside the user's named stack/constraints — do not bolt on extras.

Frame trade-ups: `Simplest: monolith / Trade-up A (only if N teams ship independently): split service X / Trade-up B (only if write throughput > Y): introduce queue`.

### 8. Anti-patterns to flag

While designing, watch out for these (full list in [reference/anti-patterns.md](../reference/anti-patterns.md)):

- Big Ball of Mud — no architecture defined.
- BDUF — overspecifying before any code is written.
- Patternitis — inserting GoF patterns "just in case".
- Over-engineering — heavy infra for a casual app.
- Microservices sharing one DB — autonomy gone.

## Output style

Concise. Bulleted. Ready for the user to copy into an ADR or design doc. If user wants narrative explanation, expand specific sections on request.
