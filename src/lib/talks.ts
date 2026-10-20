export interface Talk {
  title: string
  /** Panel, keynote, fireside chat. */
  format: string
  event: string
  city: string
  /** ISO date of the session. */
  date: string
  /** The session page or the recording. */
  href?: string
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
  },
]

/** "26 Oct 2026", the short form used in the lists. */
export function shortDate(iso: string): string {
  const d = new Date(`${iso}T00:00:00Z`)
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })
}
