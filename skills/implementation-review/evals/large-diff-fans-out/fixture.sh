#!/usr/bin/env bash
set -euo pipefail
git init -q -b main .
git config user.email eval@example.com
git config user.name eval
cat > CLAUDE.md <<'EOF'
# Repo conventions
- Conventional Commits.
- Never add a Co-Authored-By trailer to commit messages.
EOF
mkdir -p src/cart src/api docs/plans
cat > src/cart/total.ts <<'EOF'
export type Line = { sku: string; price: number; qty: number };
export function total(lines: Line[]): number {
  return lines.reduce((s, l) => s + l.price * Math.max(0, l.qty), 0);
}
EOF
cat > src/api/routes.ts <<'EOF'
import { Router } from "./router";
export const routes = new Router();
routes.get("/cart", (req) => req.session.cart);
EOF
cat > docs/plans/0002-coupons.md <<'EOF'
# Implementation Plan: Coupon codes

- **Status**: in-progress

## Summary
A shopper can enter a coupon code at checkout and see the discounted total.

## Files Affected
| File | Role | Action |
|------|------|--------|
| `src/cart/coupon.ts` | coupon lookup and discount | New |
| `src/cart/total.ts` | total with an optional coupon | Mod |
| `src/api/routes.ts` | `POST /cart/coupon` | Mod |
| `src/cart/coupon.test.ts` | behavior tests | New |

## Implementation Phases
### Phase 1: Coupons
- **Done when**: AC-1 and AC-2 pass.
- [ ] **Coupon rules** in `src/cart/coupon.ts`.
- [ ] **Endpoint** `POST /cart/coupon` returns the new total, or 422 with the reason.

## Acceptance Criteria
- [ ] **AC-1** A valid code takes its percentage off the subtotal.
  - *a.* **Given** a $50 cart **When** the shopper applies WELCOME10 **Then** the total is $45
- [ ] **AC-2** An unusable code is refused with its reason and the total is unchanged.
  - *a.* **Given** a $150 cart **When** the shopper applies BIG20 (minimum $200) **Then** the API answers 422 `below-minimum`

## Edge Cases
| Case | Decision | Covered by |
|------|----------|-----------|
| code typed in lowercase or with spaces | handle | coupon test |
| expired code | handle | coupon test |
| two coupons on one cart | won't | one coupon per cart for now |
EOF
git add -A && git commit -qm "feat: initial shop"
# Staged change: 4 files, 74 changed lines, so over the small-diff limit.
cat > src/cart/coupon.ts <<'EOF'
export type Coupon = { code: string; percentOff: number; minSubtotal: number; expiresAt: string };

const COUPONS: Coupon[] = [
  { code: "WELCOME10", percentOff: 10, minSubtotal: 0, expiresAt: "2027-01-01" },
  { code: "BIG20", percentOff: 20, minSubtotal: 200, expiresAt: "2027-06-30" },
];

export class CouponError extends Error {
  constructor(public reason: "unknown" | "expired" | "below-minimum") {
    super(`coupon rejected: ${reason}`);
  }
}

export function findCoupon(code: string): Coupon | undefined {
  return COUPONS.find((c) => c.code === code.trim().toUpperCase());
}

export function applyCoupon(subtotal: number, code: string, today: Date = new Date()): number {
  const coupon = findCoupon(code);
  if (!coupon) throw new CouponError("unknown");
  if (new Date(coupon.expiresAt) < today) throw new CouponError("expired");
  if (subtotal < coupon.minSubtotal) throw new CouponError("below-minimum");
  const discount = (subtotal * coupon.percentOff) / 100;
  return Math.round((subtotal - discount) * 100) / 100;
}
EOF
cat > src/cart/total.ts <<'EOF'
import { applyCoupon } from "./coupon";

export type Line = { sku: string; price: number; qty: number };

export function subtotal(lines: Line[]): number {
  return lines.reduce((s, l) => s + l.price * Math.max(0, l.qty), 0);
}

export function total(lines: Line[], couponCode?: string): number {
  const sum = subtotal(lines);
  return couponCode ? applyCoupon(sum, couponCode) : sum;
}
EOF
cat > src/api/routes.ts <<'EOF'
import { Router } from "./router";
import { total } from "../cart/total";
import { CouponError } from "../cart/coupon";

export const routes = new Router();
routes.get("/cart", (req) => req.session.cart);
routes.post("/cart/coupon", (req, res) => {
  const code = String(req.body.code ?? "");
  try {
    const amount = total(req.session.cart.lines, code);
    req.session.cart.coupon = code;
    res.json({ total: amount });
  } catch (e) {
    if (e instanceof CouponError) {
      res.status(422).json({ error: e.reason });
      return;
    }
    throw e;
  }
});
EOF
cat > src/cart/coupon.test.ts <<'EOF'
import { describe, it, expect } from "vitest";
import { applyCoupon, CouponError } from "./coupon";

const TODAY = new Date("2026-11-01");

describe("applyCoupon", () => {
  it("takes 10% off a $50 cart with WELCOME10 (AC-1a)", () => {
    expect(applyCoupon(50, "WELCOME10", TODAY)).toBe(45);
  });
  it("accepts a lowercase code with spaces around it", () => {
    expect(applyCoupon(50, "  welcome10 ", TODAY)).toBe(45);
  });
  it("rejects an unknown code", () => {
    expect(() => applyCoupon(50, "NOPE", TODAY)).toThrow(CouponError);
  });
  it("rejects BIG20 on a $150 cart, below its $200 minimum", () => {
    expect(() => applyCoupon(150, "BIG20", TODAY)).toThrow(CouponError);
  });
  it("rejects an expired coupon", () => {
    expect(() => applyCoupon(50, "WELCOME10", new Date("2027-02-01"))).toThrow(CouponError);
  });
});
EOF
git add -A
