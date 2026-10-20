import type { Metadata } from 'next'
import NoteRows from '@/components/NoteRows'
import { getPublishedNotes } from '@/lib/notes'
import { pageMetadata } from '@/lib/seo'
import { NOTES_DESCRIPTION, NOTES_INTRO } from '@/lib/site'

export const metadata: Metadata = pageMetadata({ title: 'Notes', description: NOTES_DESCRIPTION, path: '/notes' })

export default function NotesPage() {
  const notes = getPublishedNotes()
  return (
    <>
      <header className="page">
        <p className="mono eyebrow">Notes</p>
        <h1 className="page-title">Notes</h1>
        <p className="lead muted">{NOTES_INTRO}</p>
      </header>
      <section className="section" aria-label="All notes">
        {notes.length === 0 ? <p className="muted">The first notes are in preparation.</p> : <NoteRows notes={notes} />}
        <p className="muted feed-line">New notes can be followed by <a href="/feed.xml">RSS</a>.</p>
      </section>
    </>
  )
}
