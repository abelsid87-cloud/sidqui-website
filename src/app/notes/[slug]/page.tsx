import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import Drawing from '@/components/Drawing'
import Mdx from '@/components/Mdx'
import NoteJsonLd from '@/components/NoteJsonLd'
import NoteRows from '@/components/NoteRows'
import Toc from '@/components/Toc'
import { getNote, getPublishedNotes, getReadNext } from '@/lib/notes'
import { pageMetadata } from '@/lib/seo'
import { SITE } from '@/lib/site'
import { shortDate } from '@/lib/talks'

// Only published notes have pages; any other address is the site's own not-found page.
export const dynamicParams = false

export function generateStaticParams() {
  return getPublishedNotes().map(n => ({ slug: n.slug }))
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params
  const note = getNote(slug)
  if (!note) return {}
  return pageMetadata({ title: note.title, description: note.summary, path: `/notes/${slug}`, image: `/og/${slug}.jpg`, published: note.date })
}

/**
 * Title and summary across the page, the drawing across the page, then the text beside a rail with the contents.
 * The text and the rail share a grid of their own: a sticky item in a grid is held by the grid container, not by
 * its cell, so "Read next" sits outside the grid or the rail would run on into it.
 */
export default async function NotePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const note = getNote(slug)
  if (!note) notFound()
  const url = `${SITE.url}/notes/${slug}`
  const share = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`
  const ask = `mailto:${SITE.email}?subject=${encodeURIComponent(note.title)}`
  const next = getReadNext(slug)
  return (
    <article>
      <div className="note">
      <header className="note-head">
        <p className="mono eyebrow"><Link href="/notes">Notes</Link></p>
        <h1 className="note-title">{note.title}</h1>
        <p className="lead muted">{note.summary}</p>
        <p className="mono muted note-meta">
          <span>{SITE.name}</span>
          <span>{shortDate(note.date)}</span>
          <span>{note.minutes} min read</span>
        </p>
      </header>

      {note.drawing && <Drawing name={note.drawing.name} caption={note.drawing.caption} />}

      <aside className="note-rail">
        <Toc headings={note.headings} />
        <div className="rail-block">
          <p className="mono muted">Share</p>
          <ul className="rail-links">
            <li><a href={share}>LinkedIn</a></li>
            <li><a href={ask}>Email</a></li>
          </ul>
        </div>
      </aside>

      <div className="note-body">
        <div className="prose"><Mdx source={note.content} /></div>
        <footer className="note-end">
          <p className="mono muted">{SITE.name} · {SITE.city} · {shortDate(note.date)}</p>
          <p className="muted">Questions and corrections are welcome at <a href={ask}>{SITE.email}</a>.</p>
        </footer>
      </div>
      </div>

      {next.length > 0 && (
        <section className="read-next" aria-labelledby="read-next-title">
          <div className="section-head">
            <h2 className="section-title" id="read-next-title">Read next</h2>
            <Link className="ext" href="/notes">All notes</Link>
          </div>
          <NoteRows notes={next} />
        </section>
      )}
      <NoteJsonLd note={note} />
    </article>
  )
}
