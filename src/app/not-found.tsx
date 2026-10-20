import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = { title: 'Page not found', robots: { index: false } }

export default function NotFound() {
  return (
    <header className="page" style={{ paddingBottom: 96 }}>
      <p className="mono eyebrow">404</p>
      <h1 className="page-title">Page not found.</h1>
      <p className="lead muted">The address may have changed. The <Link href="/">home page</Link> and the <Link href="/about">About page</Link> carry everything on this site.</p>
    </header>
  )
}
