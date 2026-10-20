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

## Pages

Home, About (biographies, record, the organisers' kit), Notes and each note, Talks (upcoming and past, split when the site is built), Contact, the 404 page, `/sitemap.xml`, `/robots.txt` and `/feed.xml` (RSS of the notes). The navigation marks the current page.

## Adding a note

Create `content/notes/<slug>.mdx` with this front matter and the text in Markdown below it:

```
---
title: A Tier III design certificate is not a Tier III facility
summary: Uptime Institute certifies the design, the constructed facility and its operation separately.
date: 2026-11-03
draft: false
drawing: three-certificates
drawingCaption: "Figure 02. The three Tier certifications on the life of a facility. Typical sequence, no project."
---
```

A note with `draft: true` is not built, not listed, not in the sitemap and not in the feed. The Notes section and the Notes link appear only when at least one note is published; the lists never show dates, so an irregular rhythm is invisible. The note's page shows the date, the reading time, the contents (from the `##` headings, each with its own address), the drawing across the page, and two notes to read next.

`drawing` names an SVG in `public/drawings`, built by a script in `scripts/drawings` (run it with plain `python` from that folder; the build fails rather than truncate a label). `drawingCaption` starts with the figure label as its first sentence.

After adding a note, run `pnpm images` so that it gets its own social card in `public/og`.

## Adding a talk

Add an entry to `src/lib/talks.ts`: title, format, event, city, ISO date and, when there is one, the link to the session or recording.

## Facts

Every fact about Abdelilah Sidqui is in `src/lib/site.ts`: roles, bios, education, languages, contact, and the standing texts of the sections. The pages read from it, so a change is made once.

## Images

`pnpm images` regenerates the social card, a card per published note, the icons and the headshot downloads from `public/people/abdelilah-sidqui.jpg` with Pillow and the static fonts in `scripts/fonts`.
