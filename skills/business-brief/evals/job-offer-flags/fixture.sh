#!/usr/bin/env bash
set -euo pipefail
mkdir -p research

cat > research/offer.md <<'EOF'
# Offer from Quillmetric (received 2026-10-24, answer due 2026-10-31)

- Role: Senior Full-Stack Engineer (TypeScript, React, Node). Remote, contractor via Deel,
  LATAM time zones OK.
- Base: USD 95,000 per year.
- Equity: 0.08% in stock options, 4-year vest, 1-year cliff, strike price at the last 409A.
- Start date: 2026-11-17.
EOF

cat > research/company-notes.md <<'EOF'
# Quillmetric, what I found (2026-10-20)

- Product: maintenance-request and work-order software for residential property managers.
  Residents report issues in a mobile app; managers dispatch vendors.
- Pricing page: $3 per unit per month, minimum 100 units. "Enterprise" tier for 5,000+ units
  says "contact sales".
- Homepage: "Trusted by 400+ property management companies. 160,000 units under management."
- Funding: $6M seed announced August 2024. No later round announced.
- Headcount: LinkedIn showed 61 employees in March 2026; it shows 52 today.
- March 2026, local tech news: "Quillmetric cut nine roles across sales and support to extend
  runway."
- Careers page: 3 open roles (this one, a Senior Account Executive, a Customer Success
  Manager).
EOF

cat > research/interview-notes.md <<'EOF'
# Hiring manager call, my notes (2026-10-15)

- Engineering team is 14 people.
- "Our biggest customer, Harbor Residential, is about 35% of ARR. They renew in March."
- "We want to hit profitability by Q3 2027."
- My team would own the resident mobile app and the vendor dispatch flow.
EOF
