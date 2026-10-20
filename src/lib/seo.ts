import type { Metadata } from 'next'
import { SITE } from './site'

export const OG_IMAGE = { url: '/og.jpg', width: 1200, height: 630, alt: SITE.name }

/** The feed, declared in every page's head so that a reader finds it from any address. */
export const FEED = { 'application/rss+xml': [{ url: `${SITE.url}/feed.xml`, title: `${SITE.name} · Notes` }] }

/** Page metadata with its own canonical address and social card; a note passes its own card and its date. */
export function pageMetadata({ title, description, path, image, published }: { title: string; description: string; path: string; image?: string; published?: string }): Metadata {
  const full = path === '/' ? SITE.name : `${title} · ${SITE.name}`
  const images = [image ? { url: image, width: 1200, height: 630, alt: title } : OG_IMAGE]
  const shared = { siteName: SITE.name, title: full, description, url: path, images }
  return {
    title: path === '/' ? { absolute: SITE.name } : title,
    description,
    alternates: { canonical: path, types: FEED },
    openGraph: published ? { ...shared, type: 'article', publishedTime: published, authors: [SITE.url] } : { ...shared, type: 'website' },
    twitter: { card: 'summary_large_image', title: full, description, images: images.map(i => i.url) },
  }
}
