#!/usr/bin/env bash
# code-craft active-mode hook
# Reads PostToolUse JSON payload from stdin. If the edited file matches a
# code-craft language/framework, emits a system reminder pointing Claude to the
# relevant rule files. Exits silently if disabled or no match.

set -e

flag_file="${HOME}/.claude/code-craft.active"
[ -f "$flag_file" ] || exit 0

payload="$(cat)"
[ -z "$payload" ] && exit 0

# Extract file_path with sed (no jq dependency)
file_path="$(printf '%s' "$payload" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
[ -z "$file_path" ] && exit 0

# Normalize separators for matching
path="$(printf '%s' "$file_path" | tr '\\' '/')"
ext="${path##*.}"
ext="$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')"

refs=()

case "$ext" in
  ts|tsx|js|jsx|mjs|cjs) refs+=("languages/ts.md") ;;
  rs)                    refs+=("languages/rust.md") ;;
  css|scss|sass)         refs+=("languages/css-sass.md") ;;
  svelte)                refs+=("frameworks/svelte.md") ;;
  astro)                 refs+=("frameworks/astro.md") ;;
  tf|tfvars|hcl)         refs+=("frameworks/terraform.md") ;;
  dart)                  refs+=("languages/dart.md") ;;
  go)                    refs+=("languages/go.md") ;;
  py|pyi)                refs+=("languages/python.md") ;;
esac

# Flutter — .dart files in a Flutter project (pubspec mentions flutter, or path hint)
if [ "$ext" = "dart" ] && echo "$path" | grep -Eq '(/lib/|/test/|widget|flutter|pubspec\.ya?ml)'; then
  refs+=("frameworks/flutter.md")
fi

# React for .tsx/.jsx
case "$ext" in
  tsx|jsx) refs+=("frameworks/react.md") ;;
esac

# Next.js — App Router conventions
if echo "$path" | grep -Eq '/app/.+/(page|layout|loading|error|route|template|not-found|default)\.(tsx?|jsx?)$'; then
  refs+=("frameworks/nextjs.md")
fi

# React Native + Expo
if echo "$path" | grep -Eq '(/expo[-/]|react-native|/eas\.json|/app\.config\.|/(metro|babel)\.config\.(js|ts)$)'; then
  refs+=("frameworks/react-native-expo.md")
fi

# Cloudflare Workers
if echo "$path" | grep -Eq '(wrangler\.(toml|jsonc?)$|/workers?/|/_worker\.(js|ts)$)'; then
  refs+=("frameworks/cloudflare-workers.md")
fi

# Hono
if echo "$path" | grep -Eq '(hono|/api/.*\.(ts|js)$)'; then
  case "$ext" in
    ts|tsx|js) refs+=("frameworks/hono.md") ;;
  esac
fi

# AWS Lambda + SAM — overrides others when clearly Lambda
if echo "$path" | grep -Eq '(template\.ya?ml$|samconfig\.toml$|/lambda(s)?/|handler\.(ts|js)$)'; then
  refs=("frameworks/aws-lambda-sam.md")
fi

# Drizzle
if echo "$path" | grep -Eq '(drizzle\.config\.|/db/schema|/db/migrations|/drizzle/)'; then
  refs+=("frameworks/drizzle.md")
fi

# Supabase
if echo "$path" | grep -Eq '(supabase[/-]|/supabase/migrations/|@supabase)'; then
  refs+=("frameworks/supabase.md")
fi

# Tailwind — any CSS or tailwind config
if [ "$ext" = "css" ] || echo "$path" | grep -Eq 'tailwind\.config\.'; then
  refs+=("languages/tailwind.md")
fi

# No covered file type
[ ${#refs[@]} -eq 0 ] && exit 0

# Dedupe
unique_refs=()
declare -A seen
for r in "${refs[@]}"; do
  if [ -z "${seen[$r]:-}" ]; then
    unique_refs+=("$r")
    seen[$r]=1
  fi
done

# Build the reminder as one string with real newlines, then JSON-escape.
# Use a literal placeholder for ${CLAUDE_PLUGIN_ROOT} so it survives the shell.
reminder="[code-craft active] Just edited ${file_path}. Apply rules from:"
for r in "${unique_refs[@]}"; do
  reminder="${reminder}
  - \${CLAUDE_PLUGIN_ROOT}/${r}"
done
reminder="${reminder}
Flag any violations from your edit inline. If clean, no need to mention."

# JSON-escape: backslash, double-quote, then convert newlines to literal \n
escaped=$(printf '%s' "$reminder" \
  | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' \
  | awk '{printf "%s%s", (NR>1 ? "\\n" : ""), $0}')

printf '{"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"%s"}}\n' "$escaped"
exit 0
