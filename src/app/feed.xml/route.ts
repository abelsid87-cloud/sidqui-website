import { getPublishedNotes } from '@/lib/notes'
import { NOTES_DESCRIPTION, SITE } from '@/lib/site'

export const dynamic = 'force-static'

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const rfc822 = (iso: string) => new Date(`${iso}T00:00:00Z`).toUTCString()

/** RSS 2.0 of the published notes, newest first. */
export function feedXml(): string {
  const notes = getPublishedNotes()
  const items = notes
    .map(n => {
      const url = `${SITE.url}/notes/${n.slug}`
      return `<item><title>${esc(n.title)}</title><link>${url}</link><guid isPermaLink="true">${url}</guid><pubDate>${rfc822(n.date)}</pubDate><description>${esc(n.summary)}</description></item>`
    })
    .join('')
  const updated = notes[0] ? rfc822(notes[0].date) : new Date().toUTCString()
  return (
    `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>` +
    `<title>${esc(SITE.name)} · Notes</title><link>${SITE.url}/notes</link>` +
    `<atom:link href="${SITE.url}/feed.xml" rel="self" type="application/rss+xml"/>` +
    `<description>${esc(NOTES_DESCRIPTION)}</description><language>en-gb</language><lastBuildDate>${updated}</lastBuildDate>` +
    `${items}</channel></rss>`
  )
}

export function GET() {
  return new Response(feedXml(), { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } })
}
