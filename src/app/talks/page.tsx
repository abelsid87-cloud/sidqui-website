import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import TalkRows from '@/components/TalkRows'
import { pageMetadata } from '@/lib/seo'
import { SITE, TALKS_DESCRIPTION, TALKS_INTRO } from '@/lib/site'
import { TALKS, splitByDate } from '@/lib/talks'

export const metadata: Metadata = pageMetadata({ title: 'Talks', description: TALKS_DESCRIPTION, path: '/talks' })

/** Upcoming sessions, past sessions, and how to invite him. The split is made when the site is built. */
export default function TalksPage() {
  const { upcoming, past } = splitByDate(TALKS, new Date())
  const latest = [...past, ...upcoming].find(t => t.photo)
  return (
    <>
      <header className="page">
        <p className="mono eyebrow">Talks</p>
        <h1 className="page-title">Talks</h1>
        <p className="lead muted">{TALKS_INTRO}</p>
      </header>
      {latest?.photo && (
        <figure className="talk-photo">
          <Image src={latest.photo.src} alt={latest.photo.alt} width={latest.photo.width} height={latest.photo.height} sizes="(max-width: 1200px) 100vw, 1136px" priority />
          <figcaption className="figcap">{latest.photo.caption}</figcaption>
        </figure>
      )}
      {upcoming.length > 0 && (
        <section className="section" aria-labelledby="upcoming-title">
          <h2 className="section-title sm" id="upcoming-title">Upcoming</h2>
          <TalkRows talks={upcoming} />
        </section>
      )}
      {past.length > 0 && (
        <section className="section" aria-labelledby="past-title">
          <h2 className="section-title sm" id="past-title">Past</h2>
          <TalkRows talks={past} />
        </section>
      )}
      {TALKS.length === 0 && (
        <section className="section"><p className="muted">No public sessions are scheduled.</p></section>
      )}
      <section className="section" aria-labelledby="invite-title">
        <h2 className="section-title sm" id="invite-title">Invitations</h2>
        <p className="reading invite">
          To invite me to speak, email <a href={`mailto:${SITE.email}`}>{SITE.email}</a> with the event, the date and the subject. The biographies and the headshot for a programme are on the <Link href="/about#organisers">About page</Link>.
        </p>
      </section>
    </>
  )
}
