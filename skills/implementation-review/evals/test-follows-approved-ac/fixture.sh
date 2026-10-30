#!/usr/bin/env bash
set -euo pipefail
git init -q -b main .
git config user.email eval@example.com
git config user.name eval
mkdir -p src/cart docs/plans
cat > src/cart/total.ts <<'EOF'
export type Line = { sku: string; price: number; qty: number };
export function total(lines: Line[]): number {
  return lines.reduce((s, l) => s + l.price * Math.max(0, l.qty), 0);
}
EOF
cat > src/cart/total.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
import { total } from "./total";

describe("total", () => {
  it("sums price times quantity", () => {
    expect(total([{ sku: "a", price: 10, qty: 3 }])).toBe(30);
  });
  it("ignores negative quantities", () => {
    expect(total([{ sku: "a", price: 10, qty: -2 }])).toBe(0);
  });
});
EOF
cat > docs/plans/0001-order-discount.md <<'EOF'
# Implementation Plan: Order discount

- **Status**: in-progress
- **Sources**: product brief, 2026-10-18

## Summary
Orders over $100 get 10% off the total.

## Files Affected
| File | Role | Action |
|------|------|--------|
| `src/cart/total.ts` | order total | Mod |
| `src/cart/total.test.ts` | behavior tests | Mod |

## Implementation Phases
### Phase 1: Discount
- **Status**: in-progress
- **Goal**: totals over $100 are discounted.
- **Done when**: AC-1 passes

- [x] **AC-1 tests**: written first; AC-1a failed as expected, AC-1b already passed (it describes today's price). Touches: `src/cart/total.test.ts`.
- [ ] **Apply discount**: 10% off above $100. Touches: `src/cart/total.ts`. Done when: AC-1a and AC-1b pass.

## Acceptance Criteria
- [ ] **AC-1** (integration) An order whose lines total more than $100 gets 10% off; $100 or less pays full price.
  - *a.* **Given** lines totaling $120 **When** the order total is computed **Then** it is $108
  - *b.* **Given** lines totaling exactly $100 **When** the order total is computed **Then** it is $100

## Edge Cases
| Case | Decision | Covered by |
|------|----------|-----------|
| total exactly $100 | handle | AC-1b |
| negative quantity | handle | existing test, clamps to 0 |

## Test Plan
- **Integration**: AC-1a and AC-1b in `src/cart/total.test.ts`; existing quantity tests keep passing.
EOF
git add -A && git commit -qm "feat: cart total"
cat >> src/cart/total.test.ts <<'EOF'

describe("order discount", () => {
  it("AC-1a: takes 10% off an order over $100", () => {
    expect(total([{ sku: "a", price: 60, qty: 2 }])).toBe(108);
  });
  it("AC-1b: an order of exactly $100", () => {
    expect(total([{ sku: "a", price: 50, qty: 2 }])).toBe(100);
  });
});
EOF
git add -A && git commit -qm "test: AC-1 acceptance tests first"
# Product moved the boundary before any code was written; the plan change was committed on its own.
sed -e 's/Orders over \$100 get/Orders of $100 or more get/' \
    -e 's/totals over \$100 are discounted/totals of $100 or more are discounted/' \
    -e 's/10% off above \$100/10% off at $100 or more/' \
    -e 's/AC-1b already passed ([^)]*)/AC-1b now expects $90 after this boundary change/' \
    -e 's/more than \$100 gets 10% off; \$100 or less pays full price\./$100 or more gets 10% off; under $100 pays full price./' \
    -e 's/exactly \$100 \*\*When\*\* the order total is computed \*\*Then\*\* it is \$100/exactly $100 **When** the order total is computed **Then** it is $90/' \
    docs/plans/0001-order-discount.md > docs/plans/plan.tmp
mv docs/plans/plan.tmp docs/plans/0001-order-discount.md
grep -q 'it is \$90' docs/plans/0001-order-discount.md
git add -A && git commit -qm "plan: AC-1 boundary moved to \$100 or more (product decision)"
# Staged change: implements the moved boundary and updates the AC-1b test to match the plan.
cat > src/cart/total.ts <<'EOF'
export type Line = { sku: string; price: number; qty: number };
export function total(lines: Line[]): number {
  const sum = lines.reduce((s, l) => s + l.price * Math.max(0, l.qty), 0);
  return sum >= 100 ? sum * 0.9 : sum;
}
EOF
sed 's/qty: 2 }\])).toBe(100);/qty: 2 }])).toBe(90);/' src/cart/total.test.ts > src/cart/test.tmp
mv src/cart/test.tmp src/cart/total.test.ts
grep -q 'toBe(90)' src/cart/total.test.ts
git add src/cart/total.ts src/cart/total.test.ts
