# code-craft

Language-specific code best practices and idioms for [Claude Code](https://claude.com/claude-code). Complementary to [`swe-compass`](../swe-compass), which covers stack-agnostic architecture and design — `code-craft` is tactical and per-language.

## What it does

Two modes:

| Mode | Trigger | Output |
|---|---|---|
| **reader** | "TS best practices for error handling", "is `forwardRef` still needed?", "/code-craft ts" | rule + reason + wrong/right example for the matching topic |
| **reviewer** | "review this Hono route", paste of code with no other framing | flat list of `location → rule → fix`, grouped by severity |

## Coverage

| Language / framework | Rules | File |
|---|---:|---|
| TypeScript | ~50 | [`languages/ts.md`](languages/ts.md) |
| Rust | ~65 | [`languages/rust.md`](languages/rust.md) |
| CSS / SASS | ~65 | [`languages/css-sass.md`](languages/css-sass.md) |
| React (19) | ~50 | [`frameworks/react.md`](frameworks/react.md) |
| Next.js (14 / 15) | ~40 | [`frameworks/nextjs.md`](frameworks/nextjs.md) |
| React Native + Expo (SDK 53/54+) | ~80 | [`frameworks/react-native-expo.md`](frameworks/react-native-expo.md) |
| Hono (4.x) | ~55 | [`frameworks/hono.md`](frameworks/hono.md) |
| Cloudflare Workers | ~75 | [`frameworks/cloudflare-workers.md`](frameworks/cloudflare-workers.md) |
| Astro (4 / 5 / 6) | ~80 | [`frameworks/astro.md`](frameworks/astro.md) |
| Svelte 5 | ~65 | [`frameworks/svelte.md`](frameworks/svelte.md) |
| Drizzle ORM (Postgres / MySQL / SQLite / D1) | ~60 | [`frameworks/drizzle.md`](frameworks/drizzle.md) |

Every rule has: short name, one-sentence rule, one-line reason, 3–10 line wrong-vs-right example. Source citations only on debated rules (enums vs unions, `@extend`, `forwardRef` migration, BEM alternatives, etc.).

## When to defer to swe-compass

| Goes to `swe-compass` | Goes to `code-craft` |
|---|---|
| Architecture, system design | Inside-the-file decisions |
| SOLID, GoF patterns, MVC, microservices | Idiomatic syntax, std-lib helpers |
| Refactoring strategy across modules | Anti-patterns within one file |
| TDD, CI/CD, DevOps | Per-language conventions |
| Stack selection | Framework-specific APIs |

## Install

```text
/plugin marketplace add mqmalagris/claude-skills
/plugin install code-craft@claude-skills
/reload-plugins
```

## Trigger examples

```text
/code-craft what's the modern Rust error-handling pattern?
/code-craft review this TypeScript:  <paste>
TS best practices for async cancellation
is using `forwardRef` still needed in React 19?
review this Hono route for idioms: <paste>
how should I handle theming in CSS — variables or SCSS?
```

## Adding a language or framework

1. Drop a file in `languages/<lang>.md` or `frameworks/<framework>.md`.
2. Group rules under three buckets — **A** tactical, **B** modern idioms, **D** anti-patterns.
3. Each rule:
   - Short name (1–6 words)
   - One-sentence **Rule.**
   - One-line **Reason.**
   - ≤ 10-line wrong + right code example
   - Source citation if there is genuine debate
4. Update the **Coverage** table above.
5. Aim for 30–80 rules per file. Quality over quantity.

## License

MIT
