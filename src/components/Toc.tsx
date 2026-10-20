import type { Heading } from '@/lib/notes'
import TocHighlight from './TocHighlight'

/** The contents of a note: its section headings, the one on screen marked while reading. */
export default function Toc({ headings }: { headings: Heading[] }) {
  if (headings.length === 0) return null
  return (
    <nav className="toc" aria-labelledby="toc-title">
      <p className="mono muted" id="toc-title">In this note</p>
      <ol>
        {headings.map(h => (
          <li key={h.id}><a href={`#${h.id}`}>{h.text}</a></li>
        ))}
      </ol>
      <TocHighlight ids={headings.map(h => h.id)} />
    </nav>
  )
}
