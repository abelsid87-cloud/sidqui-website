import Link from 'next/link'
import type { NoteMeta } from '@/lib/notes'

/** The ruled list of notes: title, summary and reading time. Never a date: the rhythm of publishing is not on show. */
export default function NoteRows({ notes }: { notes: NoteMeta[] }) {
  return (
    <>
      {notes.map(note => (
        <Link className="row" href={`/notes/${note.slug}`} key={note.slug}>
          <div><h3>{note.title}</h3><p>{note.summary}</p></div>
          <span className="m">{note.minutes} min</span>
        </Link>
      ))}
    </>
  )
}
