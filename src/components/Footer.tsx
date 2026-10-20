import Link from 'next/link'
import { SITE } from '@/lib/site'

export default function Footer({ showNotes }: { showNotes: boolean }) {
  return (
    <footer className="footer">
      <div className="footer-row">
        <span className="mono">{SITE.name} · {SITE.city}</span>
        <nav className="footer-links" aria-label="Footer">
          <Link href="/about">About</Link>
          {showNotes && <Link href="/notes">Notes</Link>}
          <Link href="/talks">Talks</Link>
          <Link href="/contact">Contact</Link>
          <a href={SITE.linkedin} rel="me">LinkedIn</a>
          {showNotes && <a href="/feed.xml">RSS</a>}
        </nav>
      </div>
      <div className="footer-row mono muted">
        <span>{SITE.domain} · {new Date().getFullYear()}</span>
        <span>Text and drawings by the author.</span>
      </div>
    </footer>
  )
}
