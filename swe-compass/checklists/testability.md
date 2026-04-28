# Testability Checklist

Use to assess whether code under design or review can be tested cleanly.

## Unit-level testability

- [ ] Class can be instantiated without a database / network / filesystem
- [ ] Dependencies injected via constructor or method param (DIP)
- [ ] No reliance on a Singleton for state
- [ ] No static call to a real clock — time abstracted (`Clock`, `Instant.now()` injected)
- [ ] No reliance on `static` mutables that persist across tests

## Mocking seams

- [ ] External services accessible behind an interface (Adapter / Factory / Facade)
- [ ] No `final` / sealed classes in places where mocks are required
- [ ] No private static method holding behavior that needs to be stubbed

## FIRST compliance

- [ ] **Fast** — single test runs in milliseconds
- [ ] **Independent** — no shared mutable state across tests
- [ ] **Repeatable** — deterministic across machines and runs
- [ ] **Self-checking** — assertion result is binary; no manual log inspection
- [ ] **Timely** — tests written alongside or before production code

## Test smells (already in the suite)

- [ ] No `sleep` / wall-clock-sensitive waits
- [ ] No conditional logic (`if`, `for`, `while`) inside tests
- [ ] No giant fixture setups for tiny assertions
- [ ] No multiple unrelated asserts per test
- [ ] No `@Ignore` / skipped tests left undated

## Coverage

- [ ] Branch coverage (C1) measured, not just line (C0)
- [ ] Critical paths covered with an integration test, not just a unit test
- [ ] System tests reserved for top-of-pyramid critical user journeys (~10%)

## Untestable code = design smell

If a piece of code can't be tested cleanly, the answer is rarely "skip the test". The answer is to refactor for testability:

- Extract pure functions out of side-effecting methods
- Inject dependencies that were previously constructed inside the class
- Wrap external libraries behind your own interface
