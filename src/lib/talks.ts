export interface Talk {
  title: string
  /** Panel, keynote, fireside chat. */
  format: string
  event: string
  city: string
  /** ISO date of the session. */
  date: string
  /** The session page. */
  href?: string
  /** The recording, once the organiser has published it. */
  recording?: { href: string; label: string }
  /** A photograph of the session, shown on the Talks page; the file lives in public/talks at 2000 px wide. */
  photo?: { src: string; width: number; height: number; alt: string; caption: string }
}

/** Talks and panels, most recent first. Boardroom sessions are private and are not listed. */
export const TALKS: Talk[] = [
  {
    title: 'AI at scale: How MENA’s digital transformation is reshaping power, cooling, construction and design',
    format: 'Panel',
    event: 'DCD Connect MENA',
    city: 'Dubai',
    date: '2026-10-26',
    href: 'https://www.datacenterdynamics.com/en/dcdconnect-live/mena/2026/session-060faba0-1327-4e4a-a4a4-b186d04a792a/',
    recording: { href: 'https://vimeo.com/1239422288#t=1h32m30s', label: 'Watch the recording, DCD on Vimeo, from 1:32:30' },
    photo: {
      src: '/talks/dcd-connect-mena-2026.jpg',
      width: 2000,
      height: 1125,
      alt: 'The AI at scale panel on the main stage of DCD Connect MENA 2026 in Dubai, Abdelilah Sidqui second from the right',
      caption: 'DCD Connect MENA, Dubai, 26 October 2026. The AI at scale panel with Himmath Mohammed of Gulf Data Hub, Tom Bosmans of BAC, Yashnath Issur of Nxtra Africa and Gabriella Gillett-Perez of DCD.',
    },
  },
]

/** "26 Oct 2026", the short form used in the lists. */
export function shortDate(iso: string): string {
  const d = new Date(`${iso}T00:00:00Z`)
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })
}

/** Upcoming sessions soonest first and past sessions most recent first, as of a given day. */
export function splitByDate(talks: Talk[], now: Date): { upcoming: Talk[]; past: Talk[] } {
  const today = now.toISOString().slice(0, 10)
  return {
    upcoming: talks.filter(t => t.date >= today).sort((a, b) => a.date.localeCompare(b.date)),
    past: talks.filter(t => t.date < today).sort((a, b) => b.date.localeCompare(a.date)),
  }
}
