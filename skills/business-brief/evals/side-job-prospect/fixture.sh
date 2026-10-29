#!/usr/bin/env bash
set -euo pipefail
mkdir -p research

cat > research/client-email.md <<'EOF'
From: Dana Ortiz, Head of E-commerce, Kettlebird Coffee
Date: 2026-10-21
Subject: Site performance help before Black Friday

Hi,

A friend passed along your name. Our Shopify Plus store got slow after we added the coffee
quiz and a new reviews widget in August. Mobile conversion went from 2.1% to 1.6% since then;
desktop is flat at 3.0%. About 70% of our sessions are mobile.

Black Friday through Cyber Monday is our biggest stretch of the year, roughly 15% of Q4
revenue, so I'd love the top issues fixed before Nov 20.

Could you send a proposal for a performance audit plus fixes? Budget is flexible, but our CFO
signs off on anything over $5k and I need to justify it.

Thanks,
Dana
EOF

cat > research/site-notes.md <<'EOF'
# Kettlebird site, what I saw (2026-10-22)

- Tagline: "Fresh-roasted specialty coffee, delivered every 2 or 4 weeks."
- Subscription: $19 per 12 oz bag, ships every 2 or 4 weeks. One-time purchase: $22 per bag.
  Free shipping over $35.
- Homepage banner: "Join 18,000 subscribers."
- Also sells brewing gear (grinders, kettles) and gift subscriptions.
- About page: founded 2017 in Portland, Oregon. Roasts in-house.
- Careers page: "Retention Marketing Manager" and "Warehouse Associate (seasonal)". No
  engineering roles.
- Page source loads from cdn.shopify.com (Shopify Plus, per Dana's email).
EOF

cat > research/reviews.md <<'EOF'
# Trustpilot, read 2026-10-22

4.3 stars from about 2,100 reviews.

Common praise: freshness, roast date printed on every bag, friendly support.

Common complaints:
- "Pausing or skipping a delivery takes forever on my phone."
- "Site is slow on mobile."
- "Late deliveries around the holidays."
- A handful: "charged after I cancelled."
EOF

cat > research/news.md <<'EOF'
# News and company signals

- 2023-03, local business journal: Kettlebird raised a $4M seed round "to expand wholesale and
  its subscription program". No later round found.
- LinkedIn company page: "51-200 employees"; 38 people list it as their current employer.
- 2025-11, podcast interview with the founder: "subscriptions are about two thirds of our
  online sales."
EOF
