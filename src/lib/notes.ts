import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'

export interface Heading {
  id: string
  text: string
}

export interface NoteMeta {
  slug: string
  title: string
  summary: string
  /** ISO date; shown on the note's own page and in the feed, never in the lists. */
  date: string
  draft: boolean
  /** Reading time in whole minutes at 230 words a minute, never under one. */
  minutes: number
  /** A drawing from scripts/drawings and its caption, when the note has one. */
  drawing?: { name: string; caption: string }
}

export interface Note extends NoteMeta {
  content: string
  /** The second-level headings in order, with the ids the page gives them. */
  headings: Heading[]
}

const NOTES_DIR = path.join(process.cwd(), 'content/notes')
const WORDS_PER_MINUTE = 230

/** "What I ask for in the brief" becomes "what-i-ask-for-in-the-brief": a heading's id and the target in the contents. */
export function slugify(text: string): string {
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

export function readingMinutes(content: string): number {
  const words = content.split(/\s+/).filter(Boolean).length
  return Math.max(1, Math.round(words / WORDS_PER_MINUTE))
}

/** The "## " headings of the Markdown, for the contents list. */
export function headingsOf(content: string): Heading[] {
  const headings: Heading[] = []
  for (const line of content.split('\n')) {
    const match = /^##\s+(.+?)\s*$/.exec(line)
    if (match) headings.push({ id: slugify(match[1]), text: match[1] })
  }
  return headings
}

function read(slug: string): Note | null {
  const file = path.join(NOTES_DIR, `${slug}.mdx`)
  if (!fs.existsSync(file)) return null
  const { data, content } = matter(fs.readFileSync(file, 'utf8'))
  // YAML reads an unquoted 2026-10-20 as a Date; either form is accepted and kept as the ISO day.
  const date = data.date instanceof Date ? data.date.toISOString().slice(0, 10) : data.date
  if (typeof data.title !== 'string' || typeof data.summary !== 'string' || typeof date !== 'string') return null
  const drawing = typeof data.drawing === 'string' && typeof data.drawingCaption === 'string' ? { name: data.drawing, caption: data.drawingCaption } : undefined
  return { slug, title: data.title, summary: data.summary, date, draft: data.draft === true, minutes: readingMinutes(content), drawing, content, headings: headingsOf(content) }
}

/** Published notes, newest first, then by title. Drafts never leave the content folder. */
export function getPublishedNotes(): NoteMeta[] {
  if (!fs.existsSync(NOTES_DIR)) return []
  return fs
    .readdirSync(NOTES_DIR)
    .filter(f => f.endsWith('.mdx'))
    .map(f => read(f.replace(/\.mdx$/, '')))
    .filter((n): n is Note => n !== null && !n.draft)
    .sort((a, b) => (a.date === b.date ? a.title.localeCompare(b.title) : a.date < b.date ? 1 : -1))
    .map(({ content: _content, headings: _headings, ...meta }) => meta)
}

export function getNote(slug: string): Note | null {
  const note = read(slug)
  return note && !note.draft ? note : null
}

/** What to read after a note: the next ones in the list, going round to the start, never the note itself. */
export function getReadNext(slug: string, count = 2): NoteMeta[] {
  const notes = getPublishedNotes()
  const at = notes.findIndex(n => n.slug === slug)
  if (at < 0) return notes.slice(0, count)
  const next: NoteMeta[] = []
  for (let step = 1; step < notes.length && next.length < count; step++) next.push(notes[(at + step) % notes.length])
  return next
}
