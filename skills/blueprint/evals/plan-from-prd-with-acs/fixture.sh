#!/usr/bin/env bash
set -euo pipefail
mkdir -p src/cart src/api src/db
cat > src/cart/total.ts <<'EOF'
export type Line = { sku: string; price: number; qty: number };
export function total(lines: Line[]): number {
  return lines.reduce((s, l) => s + l.price * l.qty, 0);
}
EOF
cat > src/api/routes.ts <<'EOF'
import { Router } from "./router";
export const routes = new Router();
routes.get("/cart", (req) => req.session.cart);
EOF
cat > src/db/schema.ts <<'EOF'
// Postgres schema (see docs/adr/0001)
export const tables = { users: "users", carts: "carts" };
EOF
mkdir -p docs/adr
cat > docs/adr/0001-postgres-for-all-persistence.md <<'EOF'
# ADR 0001: Postgres for all persistence

- **Status**: accepted
- **Date**: 2026-03-02

## Decision
All durable application state lives in the existing Postgres database. No new datastores (Redis, DynamoDB, document stores) without a superseding ADR.

## Consequences
New features add tables or columns in `src/db/schema.ts`, migrated with the existing migration tool.
EOF
mkdir -p docs/intent
cat > docs/intent/0001-saved-carts.md <<'EOF'
# Design Notes: Saved carts

- **Status**: settled
- **Date**: 2026-09-20
- **Slug**: saved-carts

## Resolved decisions
- Who can save: signed-in shoppers only: guests have no account page to restore from.
- Limit: at most 5 saved carts per shopper: keeps the account page scannable.
- Restore semantics: restoring replaces the active cart after a confirm prompt: merging caused duplicate-line confusion in user tests.
- Prices: a restored saved cart reprices every line at current prices: stale prices are a support burden.

## Open questions
- OPEN: should saved carts expire?: product owner to decide.

## Edge cases
- Restoring a saved cart that contains a discontinued SKU: handle. Drop the line and show a notice.
- Saving when already at 5 saved carts: handle. Block with a message naming the limit.
- Two tabs restoring different saved carts at once: defer. Single-session feature for now.
- Guest tries to save: won't. The save control is not rendered for guests.

## Glossary
Saved cart: a named snapshot of cart lines a signed-in shopper keeps on their account. (aliases: wishlist cart; canonical: saved cart)
Active cart: the one cart the shopper is currently checking out with.
Restore: replace the active cart with a saved cart's lines, repriced.
EOF
mkdir -p docs/prds
cat > docs/prds/0001-saved-carts.md <<'EOF'
# PRD: Saved carts

- **Status**: approved
- **Sources**: docs/intent/0001-saved-carts.md, docs/adr/0001-postgres-for-all-persistence.md

## Problem Statement
Signed-in shoppers lose carts they build for later; support gets requests to "get my cart back".

## Glossary
- **Saved cart**: a named snapshot of cart lines a signed-in shopper keeps on their account.
- **Active cart**: the cart currently being checked out.
- **Restore**: replace the active cart with a saved cart's lines, repriced at current prices.

## Solution
A "Save cart" action on the cart page and a "Saved carts" list on the account page with Restore and Delete. Stored in a new `saved_carts` table in Postgres.

## User Stories
1. As a signed-in shopper, I save my active cart under a name.
2. As a signed-in shopper, I restore a saved cart, replacing my active cart after confirming.
3. As a signed-in shopper, I delete a saved cart.

## Acceptance Examples

### Story 1: save the active cart
- **AC-1** A signed-in shopper can save the active cart under a name, up to 5 saved carts.
  - *a.* **Given** a shopper with 2 saved carts and an active cart of 3 lines **When** they save it as "Weekly" **Then** "Weekly" appears in their saved carts with those 3 lines
  - *b.* **Given** a shopper with 5 saved carts **When** they try to save the active cart **Then** the save is refused with a message naming the 5-cart limit

### Story 2: restore a saved cart
- **AC-2** Restoring replaces the active cart after the shopper confirms, repriced at current prices.
  - *a.* **Given** an active cart of 2 lines and a saved cart "Weekly" with 3 lines **When** the shopper restores "Weekly" and confirms **Then** the active cart holds exactly the 3 "Weekly" lines at today's prices
  - *b.* **Given** the same carts **When** the shopper cancels the confirm prompt **Then** the active cart still holds its 2 lines
- **AC-3** A discontinued SKU is dropped on restore, with a notice.
  - *a.* **Given** "Weekly" holds a line for a discontinued SKU **When** the shopper restores it **Then** that line is absent from the active cart and a notice names the dropped item

### Story 3: delete a saved cart
- **AC-4** A shopper can delete a saved cart.
  - *a.* **Given** saved carts "Weekly" and "Party" **When** the shopper deletes "Party" **Then** only "Weekly" remains

## Implementation Decisions
- Max 5 saved carts per shopper, enforced server-side.
- Restore reprices every line; discontinued SKUs are dropped with a notice.

## Edge cases (from design notes)
- Discontinued SKU on restore: handle.
- Saving at the 5-cart limit: handle.
- Two tabs restoring at once: defer.
- Guest save: won't.

## Out of Scope
Sharing saved carts; expiry (open question).
EOF
