# sidqui.com

The personal site of Abdelilah Sidqui. Next.js, static, self-hosted fonts, no analytics unless switched on, deployed on Netlify behind Cloudflare DNS.

## Working on it

```bash
pnpm install
pnpm dev          # http://localhost:3002
pnpm test
pnpm typecheck
pnpm build
```

## Adding a note

Create `content/notes/<slug>.mdx` with this front matter and the text in Markdown below it:

```
---
title: A Tier III design certificate is not a Tier III facility
summary: Uptime Institute certifies the design, the constructed facility and its operation separately.
date: 2026-11-03
draft: false
---
```

A note with `draft: true` is not built, not listed and not in the sitemap. The Notes section and the Notes link appear only when at least one note is published; the home page never shows dates, so an irregular rhythm is invisible.

## Adding a talk

Add an entry to `src/lib/talks.ts`: title, format, event, city, ISO date and, when there is one, the link to the session or recording. Most recent first.

## Facts

Every fact about Abdelilah Sidqui is in `src/lib/site.ts`: roles, bios, education, languages, contact. The pages read from it, so a change is made once.

## Images

`pnpm images` regenerates the social card, the icons and the headshot downloads from `public/people/abdelilah-sidqui.jpg` with Pillow and the static fonts in `scripts/fonts`.
