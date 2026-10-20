import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { MDXRemote } from 'next-mdx-remote/rsc'
import Drawing from '@/components/Drawing'
import { getNote, getPublishedNotes } from '@/lib/notes'
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
  return pageMetadata({ title: note.title, description: note.summary, path: `/notes/${slug}` })
}

export default async function NotePage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const note = getNote(slug)
  if (!note) notFound()
  return (
    <article className="page note">
      <p className="mono eyebrow"><Link href="/notes" style={{ textDecoration: 'none' }}>Notes</Link></p>
      <h1 className="page-title">{note.title}</h1>
      <p className="lead muted">{note.summary}</p>
      <p className="mono muted note-date">{SITE.name} · {shortDate(note.date)}</p>
      {note.drawing && <Drawing name={note.drawing.name} caption={note.drawing.caption} />}
      <div className="prose">
        <MDXRemote source={note.content} />
      </div>
    </article>
  )
}
