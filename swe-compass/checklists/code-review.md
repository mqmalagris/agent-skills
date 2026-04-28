# Code Review Checklist

## Cohesion & responsibility

- [ ] Each class has a single reason to change (SRP)
- [ ] No God classes (`Manager`, `System`, `Helper` with 1000+ lines)
- [ ] No Feature Envy (method reading lots of getters of another class)
- [ ] Methods stay short (~ ≤ 20 lines unless justified)

## Coupling

- [ ] No `instanceof` chains — replaced by polymorphism
- [ ] No train wrecks (`a.getB().getC().do()`) — Demeter respected
- [ ] No hidden coupling via globals or shared mutable state
- [ ] Method parameters typed as interfaces (DIP) when likely to vary
- [ ] External APIs accessed only through Adapters

## Information hiding

- [ ] Unstable structures are `private`
- [ ] No public mutable collections leaking internals
- [ ] Getters/setters justified, not blanket-applied

## Naming

- [ ] Identifiers reflect current purpose (no stale names)
- [ ] Consistent casing across the file / module
- [ ] No comments propping up cryptic code (refactor instead)

## Tests

- [ ] New logic has unit tests
- [ ] Tests are FIRST-compliant (Fast, Independent, Repeatable, Self-checking, Timely)
- [ ] No `sleep`-based timing in tests
- [ ] Mocks bind to contracts, not implementation details
- [ ] No conditional logic inside test bodies
- [ ] Coverage on branch (C1), not just lines

## Patterns / smells

- [ ] No Patternitis (pattern injected without flexibility need)
- [ ] No primitive obsession (Money, Date, ZIP wrapped as domain types)
- [ ] No Singleton used as global mutable
- [ ] No subclass combinatorial explosion (`UDPLogBufferedZipChannel` style)

## Architecture / boundaries

- [ ] Layer rules respected (no UI calling DB directly)
- [ ] No microservices sharing a DB
- [ ] Async chosen where decoupling matters; sync where immediate response is required
- [ ] Cross-service contracts versioned

## Output format reminder

For each finding, write:

```
LOCATION: file:line
PROBLEM: <one short line>
WHY: <principle violated>
FIX: <concrete action>
SEVERITY: blocker | major | minor | nit
```
