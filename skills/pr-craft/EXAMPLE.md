# Worked example

Context: marketing consent checkbox on a BigCommerce signup page was optional; needed to be required (compliance). Fixed across template + JS validator + lang files.

## Commit

```bash
git commit -F - <<'EOF'
fix(auth): enforce required marketing consent on signup

Marketing consent checkbox on the create-account form was purely
optional: no `required` attribute, not registered with the nod
validator, and the consent handler silently no-oped when unchecked.
Accounts could be created without consent — a compliance/regulatory
risk since the implicit audit trail is "account exists = box checked".

- Add native `required` to the checkbox (no-JS submit gate)
- Register a nod validator entry to block submit and show a themed
  inline error, clearing on tick
- Add `marketing_consent_required` to all validation message blocks

Refs task 29376269
EOF
```

## PR

```bash
gh pr create --base staging --head fix/marketing-consent-required-signup \
  --title "fix(auth): enforce required marketing consent on signup" \
  --body "$(cat <<'EOF'
## Problem

During QA, the marketing consent checkbox on the customer signup page could be bypassed — accounts created without checking it. Compliance/regulatory risk (FTC audit), since BigCommerce stores no separate consent flag and the implicit audit trail is *"account exists = box checked"* — only valid if enforcement is airtight.

## Root cause

The checkbox was purely optional across all three layers:
- **Template** — no `required` attribute, no `data-validation`; invisible to native HTML and the nod validator.
- **JS validator** (`registerCreateAccountValidator`) — checkbox never registered, so `areAll('valid')` ignored it.
- **Consent handler** (`handleMarketingEmailConsent`) — ran after validation passed; unchecked = silent early return, form submitted anyway.

## Fix

- Add native `required` to the checkbox — no-JS submit gate (airtight even if JS fails/disabled).
- Register a nod validator entry — blocks submit and shows a themed inline error, clearing on tick.
- Add `marketing_consent_required` to all three validation message blocks in `lang/en.json`.

Side benefit: required → consent handler always fires → every new account is subscribed, consistent with the audit-trail assumption.

## Test

1. `npm start`, open the signup page.
2. Submit with the box unchecked → blocked, inline error shown.
3. Tick the box → error clears, account creates.

## Out of scope (flag to compliance)

- Other lang files (`fr/pt/es/...`) fall back to the default EN string until translated.
- Accounts created during the bug window have no proof of consent.

Refs task 29376269
EOF
)"
```
