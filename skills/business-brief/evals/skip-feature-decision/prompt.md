---
description: "Guard: a feature decision inside a product the user already works on does not become a company business brief."
tags: [business-brief, guard]
max_turns: 6
timeout_seconds: 180
allowed_tools: [Read, Glob, Grep, Skill]
append_system_prompt: "The user answers in a later turn. Reply to the message as asked; do not search for files."
---

We sell coffee subscriptions on our Shopify store and I'm the dev on the team. Our PM wants a wishlist button on product pages. Is it worth building?
