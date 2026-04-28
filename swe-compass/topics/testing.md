# Raw — Testing

## 1. Concepts

### Testing Pyramid
- **Definition**: tests organized in three granularity layers — base of unit (~70%), middle of integration (~20%), top of system (~10%).
- **Solves**: balances effort; avoids overload of slow, flaky UI-level tests.

### Unit Tests
- **Definition**: programs that instantiate, call, and verify isolated parts of code (typically classes).
- **Solves**: catches bugs early; safety net against regressions.

### FIRST Principles
- **Definition**: tests must be Fast, Independent, Repeatable (deterministic), Self-checking, Timely (written early).
- **Solves**: stops the test suite from being abandoned due to slowness, mutual dependencies, or unclear results.

### Test-Driven Development (TDD)
- **Definition**: red → green → refactor. Write failing test first, then code that passes, then improve.
- **Solves**: guarantees tests get written, raises testability of code, encourages clean interfaces.

### Mocks / Stubs
- **Definition**: stand-in objects (e.g., Mockito) emulating external systems without real access.
- **Solves**: isolates tests from slow / flaky deps (DBs, network, remote APIs).

### Test Coverage
- **Definition**: % of code executed by tests. C0 = command/line coverage. C1 = branch coverage.
- **Solves**: visualizes blind spots; reveals unprotected code regions.

### Testability
- **Definition**: how easily parts of the system can be put under test.
- **Solves**: surfaces critical design problems; forces separation of business rules from UI.

### Integration Tests
- **Definition**: validate interactions across multiple real classes connected to real dependencies (real DB, etc.).
- **Solves**: validate persistent, real communication between subsystems.

### System Tests
- **Definition**: end-to-end from the user's perspective (e.g., Selenium clicking through the browser).
- **Solves**: validate the full integration from UI to network in real flow.

## 2. When to Use

- **Unit Tests** — building model logic; reproducing reported bugs as a test; debugging instead of `println`.
- **Mocks** — when scope crosses outside the language / in-memory boundary (disk, web servers, real time/async).
- **TDD** — predictable input/output; aiming for sustained 90%+ coverage.
- **System Tests** — critical end-user paths (final purchase click); strict minority of total tests.

## 3. When NOT to Use

- **Mocks** — when they make tests fragile by coupling to internal implementation details rather than the interface contract; not workable on classic Java `final`/static methods.
- **Late unit tests** — never start testing after the whole system is built; will be rushed, low quality, or dropped under time pressure.
- **Mass system tests** — don't replace logic checks with end-to-end (Selenium); any layout change yields false positives.
- **Blind 100% coverage** — avoid forcing 100% on getters/setters or non-essential async modules; pure waste.

## 4. Smells

- **Flaky test** — passes/fails randomly. Caused by concurrency or `sleep`-based timing.
- **Obscure test** — impossible to read intent. Sign: huge fixture setup, or one test attacking multiple unrelated functions.
- **Conditional logic in tests** — `if` branches and loops inside tests. Sign: hides paths that don't run; invalidates the test.
- **Multiple unrelated asserts** — one assert fails and aborts the whole test, masking subsequent errors.

## 5. Operational Checklist

- [ ] Balance volume per the pyramid distribution (70/20/10).
- [ ] Use the AAA structure: Arrange (fixture) → Act (call SUT) → Assert.
- [ ] Keep local runs in milliseconds (Fast).
- [ ] Replace flaky networking/IO with Mocks where possible.
- [ ] Replace `println` debugging with formal unit tests for routine bug fixes.
- [ ] Configure branch coverage (C1), stricter than line coverage (C0).
- [ ] Start TDD in red; force pragmatic interfaces before successful implementation.
- [ ] Pull domain logic out of UI components → improves testability.

## 6. Examples

- **Simple JUnit unit test** — Arrange object, call method, assert result.
- **Isolated test with Mockito mock** — stub external dependency, assert behavior of unit under test.

## 7. Trade-offs

- **Unit vs System Tests** — Unit pinpoints failing file, scales infinitely, runs instantly, but doesn't catch UI transitions. System tests reflect the user's real journey, but run for minutes, are fragile to UI changes, and slow root-cause discovery.
- **Mock vs Real DB (integration)** — Mock gives stable, fast tests but couples to internal call shape. Real DB validates true integration but slows tests and adds infra dependencies.
- **C0 vs C1 coverage** — C0 verifies command execution but a single `if` only proves the truthy branch. C1 forces branch coverage; stricter and harder to maximize.

## 8. Cross-references

- **DevOps** — modern pipelines run a CI server reading from Git, invoking the full pyramid before code reaches review/Production.
- **Design Principles (SOLID)** — DIP and decoupled cohesive code yield natural testability; high coupling (globals) breaks FIRST's deterministic property in parallel runs.
- **Refactoring** — without unit tests as safety net, refactoring becomes impractical; risk of regression on stable algorithms.
