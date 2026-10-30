---
name: testing-philosophy
description: "Defines what a good test is: behavior over implementation details, the Testing Trophy with a hard floor on end-to-end coverage for user-facing features, acceptance tests written as Given/When/Then examples, and the integrity rules for tests an agent writes or changes. Stack-agnostic, any language (TS/JS, Rust, Go, Elixir, Python, ...) and any layer (frontend, backend, CLI, library). REQUIRED BACKGROUND for skills that plan or review tests (implementation-review, blueprint, review-pass, dev-flow). Use when proposing, writing, or reviewing automated tests or acceptance criteria, or when the user asks whether tests are good, what to test, why a test is brittle, whether e2e is needed, how to write Given/When/Then scenarios, or whether BDD tooling like Cucumber or Gherkin is worth it."
---

# Testing philosophy

The shared definition of "good test" that every skill in this set which proposes or reviews tests leans on. It distils Kent Dodds' testing writing and generalizes it past his JS/React context to any language and any layer, then adds what the ATDD/BDD literature and recent studies of coding agents agree on for acceptance tests.

## The one principle

> **The more your tests resemble the way your software is used, the more confidence they can give you.** (Kent C. Dodds)

Every rule below is a corollary. The principle is already language- and layer-agnostic; "the way your software is used" just resolves to a different surface in each context. When a testing decision is unclear, return to this sentence.

## Pillar 1: Behavior over implementation details

An **implementation detail** is anything *"users of your code will not typically use, see, or even know about."* A test bound to one fails in both directions at once:

- **False negative on refactor**: you change internals without changing behavior, and the test breaks anyway. It cries wolf.
- **False positive on breakage**: you break the actual behavior, and the test stays green because it was watching the mechanism, not the result.

Dodds' framing: a test that drives your code differently from how real users drive it becomes *a third user you never wanted*, now you keep the end user, the calling developer, **and** the test happy.

**"User" generalizes by layer.** Assert only on what *that* user can observe; drive the code only through the surface *that* user touches:

| Layer | The user | Assert on (observable) | Do NOT touch (implementation) |
|---|---|---|---|
| Library / module | the calling developer | return values, thrown errors, public types, emitted events | private fields/methods, internal helpers, internal data-structure choices |
| Backend / API | the HTTP/RPC client | status codes, response bodies, headers, state visible *through* the API, domain events | ORM internals, service method names, query shapes, internal DTOs |
| Frontend / UI | the person clicking | rendered text, roles, what appears/disappears after an interaction | component state vars, hook internals, CSS class names, child-component names |
| CLI | the person at the prompt | stdout/stderr, exit code, files written | internal flag parsing, function call order |

**Concrete tells of an implementation-detail test** (stack-independent, flag any of these):

- Asserts on private fields, unexported functions, internal state, or internal data-structure shape.
- Asserts a particular internal function/method *was called*, spy / mock-call-count assertions on a collaborator **you own**.
- Mocks a collaborator you own, rather than mocking only at a true external boundary (network, disk, clock, OS process, third-party service).
- Its name describes a mechanism (`calls set_index with 0`) instead of a behavior (`shows the first slide on load`).

**The acid test:** *"If I refactor the internals but keep the public contract identical, does this test break?"* If yes, it tests the wrong thing. Pair it with: *"Does this assert what a real user observes?"* If no, same problem.

## Pillar 2: The Testing Trophy, and the e2e floor

Four layers, bottom to top. Height is **confidence**; height is also **cost/time**. Testing is "return on investment where return is confidence and investment is time."

| Layer | What it is | Mock how much |
|---|---|---|
| **Static** | types + lint, correctness for free (`tsc`, `cargo check`, `go vet`, Dialyzer) | n/a |
| **Unit** | one piece in isolation | dependencies mocked |
| **Integration** | several units working together, **the default tier** | mock only external boundaries |
| **E2E** | the whole assembled system | "as little as possible" |

"Write tests. Not too many. **Mostly integration**" puts most effort in the middle, because that is the best confidence-per-effort and most regressions live *between* units, not inside them.

**The correction that matters: "mostly integration" is not "skip e2e."** Two opposite violations, and most reviews only catch the first:

1. **Too much e2e**: every scenario duplicated as a slow, flaky full-stack test that could be an integration test. Flag it; push it down the trophy.
2. **No e2e at all for the critical path**: every layer tested in isolation, but nothing proves they connect. The quieter, more common gap. Flag it just as hard.

**The e2e necessity rule** (this skill's own floor, not a rule Dodds sets): *every user-facing feature needs at least one end-to-end (or highest-practical) test that exercises its critical happy path through the real, assembled system*, one or two paths, not one per scenario. E2e proves the wiring; integration proves the behavior; unit proves the tricky pure logic; static proves the shapes. Unit + integration coverage with no wiring proof for a user-facing feature **is a gap**.

**E2e does not require a browser, it generalizes by surface and by stack:**

| Surface | What "e2e" means | Typical tooling |
|---|---|---|
| Frontend app | browser-driven: load then act then see the result | Playwright, Cypress |
| Backend service | hit the running service over its real protocol against a real (test) DB; assert response + persisted state | Go `net/http/httptest`, Rust `reqwest` + spawned server, Elixir Phoenix `ConnCase` / `Phoenix.LiveViewTest`, supertest |
| CLI | invoke the built binary as a subprocess; assert stdout / exit code / files written | Rust `assert_cmd`, Go `os/exec` in `_test.go`, shell harness |
| Library | consume the published public API exactly as a downstream user would, nothing internal stubbed | Rust `tests/` integration dir, Go external `_test` package, Elixir ExUnit against the public module, Vitest against the built entrypoint |

Runners by stack are just the mechanism: `cargo test` / `cargo nextest` (Rust), `go test` (Go), `mix test` / ExUnit (Elixir), Vitest / Jest / Playwright (TS/JS), pytest (Python). The tier matters, not the runner.

## Acceptance tests and Given/When/Then

An **acceptance example** is one concrete case of a business rule that the people who own the feature agreed on: the rule ("a transfer can't take an account below zero") plus two or three examples that pin it down. An **acceptance test** asserts one such example through the highest practical boundary. The dev-flow chain carries these as numbered `AC-n` rules from the PRD to the plan to the test names, so a reviewer can trace every agreed example to the test that proves it.

**Given/When/Then is a structure, not a tier or a tool.** It is Arrange/Act/Assert with business words, and it works at any tier. Where an acceptance test lands follows Pillar 2: a rule is usually proven at integration, through the API or service layer just under the UI, and only the critical happy path goes through the full e2e surface. The tier is chosen per example, not per rule: a rule's happy-path example may be the feature's critical path and run e2e while its counter-examples stay at integration. Writing an example as Given/When/Then does not make it a browser test.

- **Given** is the context the example needs, stated as state ("checking holds $50"), not as the steps to reach it.
- **When** is one event: the actor's action.
- **Then** is what that actor can observe (Pillar 1's "assert on" column), never internal state.

**A good scenario is Pillar 1 applied to the spec.** A click-by-click scenario is the spec-level twin of an implementation-detail test: it changes whenever the UI changes, even when the rule did not. So:

- Declarative: say what happens in the domain ("the customer transfers $80 to savings"), not how the UI is driven ("clicks Transfer, types 80 into the amount field").
- One rule per scenario. A scenario that checks two rules can fail for two reasons and names neither.
- Business language: the PRD's Glossary terms, verbatim.
- Real-looking data and about five steps (Seb Rose's BRIEF heuristic). A long scenario is usually a script, not a specification.
- Named for the rule it proves, not the mechanism behind it.

**The scenario acid test:** *"If the UI changed but the rule didn't, would this scenario's wording change?"* If yes, it sits at the wrong level. It is Pillar 1's refactor question asked one level up.

Examples are the key cases, not an exhaustive list: two or three per rule, enough to pin its edges (one case where it applies, one where it doesn't, a boundary if it has one). More than that on one rule usually means it is two rules. The edge-case ledger and implementation-review's missing-scenarios checklist cover the remaining cases at integration level.

**Tooling: plain test code by default.** Gherkin runners (Cucumber, Reqnroll, pytest-bdd, playwright-bdd) exist so that non-developers can read and help write the specs. When nobody outside engineering reads the feature files, the extra layer costs glue code, duplicated steps and specs that drift from the code, and buys nothing. So keep Given/When/Then as structure inside ordinary tests: a test name that states the rule, and Given/When/Then as comments or helper names. Use a Gherkin runner only when a non-developer actually reads or co-writes the specs (often on client work) or the repo already uses one. An ADR or an existing repo convention overrides this default either way.

## Tests written by agents

In this workflow a coding agent writes most tests, and that changes what a green run proves.

- **An agent-written test is a weaker oracle than a human-approved one.** The agent that wrote the code also chose what to check, so its tests tend to confirm the code they sit next to. The strong oracle is the set of acceptance examples a human approved. Treat agent-proposed examples as proposals until a human has read them.
- **Coverage and mutation scores are not proof here.** They show that a suite exercises the code on the assumption that the code is right. When the open question is whether the code is right, they say little.
- **Ask for the unhappy inputs by name.** Generated suites lean to the happy path. Null, empty, zero, negative and error inputs are the ones to request explicitly.

**Test integrity.** When a test fails there are two honest moves: fix the code, or change the test because the agreed behavior really changed. An agent that is stuck sometimes takes a third move and shifts the test instead. Studies of coding agents and practitioner reports document agents editing tests, skipping or deleting failing ones, and special-casing code to pass them, and read-only test files alone do not stop the special-casing kind. The tells:

- deleting or skipping a test, or marking it expected-to-fail (a test renamed or moved so that it still runs, assertions intact, is not a deletion; one moved out of the runner's reach is)
- fewer or looser assertions than before: a widened tolerance, a catch-all matcher, a dropped assertion
- an edited expected value
- production code that detects a test environment and behaves differently, hard-codes the value a test expects instead of computing it (a constant return, a branch on the test's exact inputs), or overrides equality or comparison so an assertion cannot fail

**Nothing the agent writes settles a tell.** A plan edit, a commit message, a PR body and a code comment can all be written by the same agent that moved the test, and commit order proves nothing about who approved what. So every tell goes to a human. What makes that cheap is a pointer: report the tell together with whatever reason exists (the acceptance example that changed, the user's message, the commit) so the human can confirm it in one look. A tell with no reason anywhere is a defect, however green the run.

`implementation-review` applies this list to every diff that touches a test. An agent that believes an acceptance test is wrong should stop and ask, not edit it.

## How skills use this

**When proposing tests** (planning, ATDD): write tests behavior-first against the public surface; default to integration; reserve unit tests for pure functions with tricky logic; and **include at least one e2e/full-stack happy-path test for any user-facing feature.** Turn each agreed acceptance example into one test at the tier it names, with its id in the test name (or its docstring or description, where the language's names can't hold `AC-1a`), and write it before the code it gates. Examples of the new behavior should fail first; a counter-example that describes today's behavior may already pass, and should stay as written rather than be bent until it fails. Never aim at a coverage number, coverage is a side effect of testing the right behaviors.

**When reviewing tests:** run both acid-test questions on every test; flag the implementation-detail tells above; check **both** e2e directions, overuse *and* the missing-critical-path gap; and run the test-integrity list on any diff that touches a test.

## Anti-patterns

- Treating "mostly integration" as license to ship a user-facing feature with zero e2e coverage.
- Asserting on mock call counts / spies for collaborators you own, then calling it a behavior test.
- Test or scenario names that describe the mechanism (`calls X`) rather than the outcome the user observes.
- Snapshot tests that get rubber-stamped on update, they assert "it changed," not "it is correct."
- Chasing a coverage percentage instead of covering the behaviors that matter.
- Assuming e2e means a browser: for a backend or CLI the e2e is a subprocess/HTTP test, and skipping it "because there is no UI" is the gap, not an excuse.
- Imperative, UI-scripted scenarios ("clicks", "types into the field") that change whenever the UI does.
- One scenario that checks several rules.
- Pushing every acceptance example to browser e2e. The floor is one or two critical paths; the rest of the examples belong at integration.
- Getting to green by deleting, skipping or loosening a test, or editing its expected value, without a human confirming it.
- Treating agent-written tests or agent-written Gherkin as self-validating.
- Adding a Gherkin runner when no non-developer reads the specs.

## Source

Kent C. Dodds: [Testing Implementation Details](https://kentcdodds.com/blog/testing-implementation-details), [The Testing Trophy and Testing Classifications](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications), [Write tests. Not too many. Mostly integration.](https://kentcdodds.com/blog/write-tests). Generalized here to any language and layer.

Acceptance tests and agents: Martin Fowler, [Given When Then](https://martinfowler.com/bliki/GivenWhenThen.html); Cucumber, [Writing better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/) and Seb Rose, [Keep your scenarios BRIEF](https://cucumber.io/blog/bdd/keep-your-scenarios-brief/); Matt Wynne, [Introducing Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/); Aslak Hellesøy on when not to use Cucumber, [InfoQ, 2018](https://www.infoq.com/news/2018/04/cucumber-bdd-ten-years/); Zhong, Raghunathan and Carlini, [ImpossibleBench](https://arxiv.org/abs/2510.20270) (agents gaming tests); Kent Beck, [Augmented coding: beyond the vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes); Zhao, Zhou and Cohen, [coverage and mutation scores of LLM-generated suites](https://doi.org/10.1145/3832093).
