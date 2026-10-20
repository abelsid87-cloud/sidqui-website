import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = { title: 'Page not found', robots: { index: false } }

export default function NotFound() {
  return (
    <header className="page page-end">
      <p className="mono eyebrow">404</p>
      <h1 className="page-title">Page not found.</h1>
      <p className="lead muted">
        The address may have changed. Everything on this site is on the <Link href="/">home page</Link>, <Link href="/about">About</Link>, <Link href="/notes">Notes</Link>, <Link href="/talks">Talks</Link> and <Link href="/contact">Contact</Link>.
      </p>
    </header>
  )
}
