# Brag Doc — Filled Example

> Illustrative only — invented content to show the *shape and bar*, not a real record.
> Notice every "shipped" line answers "so what?" with an outcome and carries ownership, status and refs; every number says how it was measured; honest limits are stated plainly.

## March 2026
_Client order platform (Node + SQS), refunds app · drafted from git + PRs + tickets on 1 Apr 2026_

**Shipped + impact**
↳ Rebuilt the client's order-import pipeline (Node + SQS): cut the nightly batch from ~3h to 22min (CloudWatch job duration, median of 7 nights before vs 7 after, production), so support stopped fielding "where's my order" tickets the next morning (~15/wk gone) `[ESTIMADO]`. `mine · prod 18 Mar · refs: #412, #418, ADR-0007`
↳ Shipped the self-serve refund flow the client asked for in Q4: live for all 3 of their brands, ~200 refunds/wk handled without an agent (refunds table, weeks 2 to 4 after launch). `with the frontend dev (UI was theirs) · prod 9 Mar · refs: #401, REF-88`
↳ Migrated 2 Angular apps off a deprecated auth lib before its EOL: no user-facing change, but removed a "won't pass their security review" blocker to the contract renewal. `mine · staging, prod after the client's freeze · refs: #420, #421`

**Caught**
↳ The coding agent's retry wrapper swallowed the SQS visibility-timeout error, so failed batches looked successful. Unit tests passed (they mocked the queue). I caught it reading the diff against the dead-letter queue, which stayed empty during a forced failure. refs: #418 review note

**Challenges & how I tackled them**
↳ Import pipeline failures were silent: added structured logging + a dead-letter queue first, *then* optimized, so I was tuning against real failure data instead of guesses.
↳ Client kept expanding refund scope mid-sprint → wrote a one-page "what's in / what's out" and got sign-off before coding; scope creep stopped.

**Would be much better if…**
↳ We had a staging env that mirrored the client's data volume: I found the batch bottleneck only in prod. A seeded staging DB would've caught it a week earlier.

**Focus next month**
↳ Instrument the refund flow (I shipped it but have no dashboard on it: can't yet prove the agent-time saved).
↳ Pair with the junior on the auth migration pattern so the next app doesn't wait on me.

**Story seeds**
↳ [agent-wrong] Agent's retry wrapper hid failed batches; tests mocked the queue; caught by forcing a failure and checking the DLQ · refs: #418
↳ [pushback] Client wanted refunds for every order state; showed 2 states had no reversible payment yet and proposed shipping the other 4 first; client agreed · refs: REF-88 thread
↳ [decision] Logging + DLQ before optimizing, instead of profiling first · refs: ADR-0007
