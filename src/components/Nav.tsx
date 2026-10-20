'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { SITE } from '@/lib/site'

const LINKS = [
  { href: '/about', label: 'About' },
  { href: '/notes', label: 'Notes' },
  { href: '/talks', label: 'Talks' },
  { href: '/contact', label: 'Contact' },
]

/** The name on the left, the pages on the right, the current one marked. Notes appears only when a note is published. */
export default function Nav({ showNotes }: { showNotes: boolean }) {
  const pathname = usePathname()
  return (
    <nav className="nav" aria-label="Site">
      <Link href="/" className="nav-name" aria-current={pathname === '/' ? 'page' : undefined}>{SITE.name}</Link>
      <div className="nav-links">
        {LINKS.filter(l => showNotes || l.href !== '/notes').map(l => {
          const current = pathname === l.href || pathname.startsWith(`${l.href}/`)
          return <Link key={l.href} href={l.href} aria-current={current ? 'page' : undefined}>{l.label}</Link>
        })}
      </div>
    </nav>
  )
}
