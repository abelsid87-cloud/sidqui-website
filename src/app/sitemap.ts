import type { MetadataRoute } from 'next'
import { getPublishedNotes } from '@/lib/notes'
import { SITE } from '@/lib/site'

export default function sitemap(): MetadataRoute.Sitemap {
  const notes = getPublishedNotes()
  const built = new Date()
  const pages: MetadataRoute.Sitemap = [
    { url: `${SITE.url}/`, lastModified: built, changeFrequency: 'monthly', priority: 1 },
    { url: `${SITE.url}/about`, lastModified: built, changeFrequency: 'monthly', priority: 0.8 },
    { url: `${SITE.url}/talks`, lastModified: built, changeFrequency: 'monthly', priority: 0.7 },
    { url: `${SITE.url}/contact`, lastModified: built, changeFrequency: 'yearly', priority: 0.5 },
  ]
  if (notes.length > 0) pages.push({ url: `${SITE.url}/notes`, lastModified: new Date(notes[0].date), changeFrequency: 'monthly', priority: 0.7 })
  for (const note of notes) pages.push({ url: `${SITE.url}/notes/${note.slug}`, lastModified: new Date(note.date), changeFrequency: 'yearly', priority: 0.6 })
  return pages
}
