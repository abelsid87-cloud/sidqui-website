import type { Metadata } from 'next'
import Link from 'next/link'
import { getPublishedNotes } from '@/lib/notes'
import { pageMetadata } from '@/lib/seo'

export const metadata: Metadata = pageMetadata({
  title: 'Notes',
  description: 'Short pieces by Abdelilah Sidqui on how data centers are planned, designed and delivered, drawn from his work in the Middle East and Africa.',
  path: '/notes',
})

export default function NotesPage() {
  const notes = getPublishedNotes()
  return (
    <>
      <header className="page">
        <p className="mono eyebrow">Notes</p>
        <h1 className="page-title">Notes</h1>
        <p className="lead muted">Short pieces on how data centers are planned, designed and delivered, drawn from my work in the Middle East and Africa.</p>
      </header>
      <section className="section" aria-label="All notes">
        {notes.length === 0 && <p className="muted">The first notes are in preparation.</p>}
        {notes.map(note => (
          <Link className="row" href={`/notes/${note.slug}`} key={note.slug}>
            <div><h3>{note.title}</h3><p>{note.summary}</p></div>
          </Link>
        ))}
      </section>
    </>
  )
}
