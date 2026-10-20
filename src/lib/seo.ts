import type { Metadata } from 'next'
import { SITE } from './site'

export const OG_IMAGE = { url: '/og.jpg', width: 1200, height: 630, alt: SITE.name }

/** Page metadata with its own canonical address and social card. */
export function pageMetadata({ title, description, path }: { title: string; description: string; path: string }): Metadata {
  const full = path === '/' ? SITE.name : `${title} · ${SITE.name}`
  return {
    title: path === '/' ? { absolute: SITE.name } : title,
    description,
    alternates: { canonical: path },
    openGraph: { type: 'website', siteName: SITE.name, title: full, description, url: path, images: [OG_IMAGE] },
    twitter: { card: 'summary_large_image', title: full, description },
  }
}
