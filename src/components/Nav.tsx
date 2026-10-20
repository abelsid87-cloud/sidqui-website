import Link from 'next/link'
import { SITE } from '@/lib/site'

/** The name on the left, four links on the right. Notes appears only when a note is published. */
export default function Nav({ showNotes }: { showNotes: boolean }) {
  return (
    <nav className="nav" aria-label="Site">
      <Link href="/" className="nav-name">{SITE.name}</Link>
      <div className="nav-links">
        <Link href="/about">About</Link>
        {showNotes && <Link href="/notes">Notes</Link>}
        <Link href="/#talks">Talks</Link>
        <Link href="/#contact">Contact</Link>
      </div>
    </nav>
  )
}
