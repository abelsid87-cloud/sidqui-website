import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'

export interface NoteMeta {
  slug: string
  title: string
  summary: string
  /** ISO date; shown on the note's own page, never in the lists. */
  date: string
  draft: boolean
  /** A drawing from scripts/drawings and its caption, when the note has one. */
  drawing?: { name: string; caption: string }
}

export interface Note extends NoteMeta {
  content: string
}

const NOTES_DIR = path.join(process.cwd(), 'content/notes')

function read(slug: string): Note | null {
  const file = path.join(NOTES_DIR, `${slug}.mdx`)
  if (!fs.existsSync(file)) return null
  const { data, content } = matter(fs.readFileSync(file, 'utf8'))
  // YAML reads an unquoted 2026-10-20 as a Date; either form is accepted and kept as the ISO day.
  const date = data.date instanceof Date ? data.date.toISOString().slice(0, 10) : data.date
  if (typeof data.title !== 'string' || typeof data.summary !== 'string' || typeof date !== 'string') return null
  const drawing = typeof data.drawing === 'string' && typeof data.drawingCaption === 'string' ? { name: data.drawing, caption: data.drawingCaption } : undefined
  return { slug, title: data.title, summary: data.summary, date, draft: data.draft === true, drawing, content }
}

/** Published notes, newest first. Drafts never leave the content folder. */
export function getPublishedNotes(): NoteMeta[] {
  if (!fs.existsSync(NOTES_DIR)) return []
  return fs
    .readdirSync(NOTES_DIR)
    .filter(f => f.endsWith('.mdx'))
    .map(f => read(f.replace(/\.mdx$/, '')))
    .filter((n): n is Note => n !== null && !n.draft)
    .sort((a, b) => (a.date < b.date ? 1 : -1))
    .map(({ content: _content, ...meta }) => meta)
}

export function getNote(slug: string): Note | null {
  const note = read(slug)
  return note && !note.draft ? note : null
}
