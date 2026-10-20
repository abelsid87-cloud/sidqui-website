import type { Note } from '@/lib/notes'
import { SITE } from '@/lib/site'

/** Article data for search engines: the note, its date, its card and its author. */
export default function NoteJsonLd({ note }: { note: Note }) {
  const url = `${SITE.url}/notes/${note.slug}`
  const person = { '@type': 'Person', name: SITE.name, url: SITE.url }
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: note.title,
    description: note.summary,
    datePublished: note.date,
    dateModified: note.date,
    url,
    mainEntityOfPage: url,
    image: `${SITE.url}/og/${note.slug}.jpg`,
    author: person,
    publisher: person,
    inLanguage: 'en-GB',
    timeRequired: `PT${note.minutes}M`,
  }
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
}
