import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import NoteRows from '@/components/NoteRows'
import TalkRows from '@/components/TalkRows'
import { getPublishedNotes } from '@/lib/notes'
import { pageMetadata } from '@/lib/seo'
import { CONTACT_TEXT, NOTES_INTRO, ROLES, SITE, TALKS_INTRO } from '@/lib/site'
import { TALKS } from '@/lib/talks'

export const metadata: Metadata = pageMetadata({ title: SITE.name, description: SITE.definition, path: '/' })

export default function HomePage() {
  const notes = getPublishedNotes().slice(0, 5)
  const talks = TALKS.slice(0, 3)
  return (
    <>
      <header className="hero">
        <div>
          <p className="mono eyebrow">{SITE.eyebrow}</p>
          <h1 className="hero-name">{SITE.name}</h1>
          <div className="hero-text">
            <p className="hero-definition">{SITE.definition}</p>
            <p className="hero-record">{SITE.record}</p>
          </div>
        </div>
        <div className="portrait">
          <Image src={SITE.portrait.src} alt={SITE.portrait.alt} width={400} height={500} sizes="200px" priority />
        </div>
      </header>

      <section className="section" aria-label="Roles">
        <div className="roles">
          {ROLES.map(role => (
            <div className="role" key={role.title}>
              <span className="mono eyebrow">{role.label}</span>
              <h2>{role.title}</h2>
              <p>{role.text}</p>
              {'link' in role && role.link && <a className="ext" href={role.link.href}>{role.link.label}</a>}
            </div>
          ))}
        </div>
      </section>

      {notes.length > 0 && (
        <section className="section" id="notes" aria-labelledby="notes-title">
          <div className="section-head">
            <h2 className="section-title" id="notes-title">Notes</h2>
            <div className="section-aside">
              <p className="section-intro">{NOTES_INTRO}</p>
              <Link className="ext" href="/notes">All notes</Link>
            </div>
          </div>
          <NoteRows notes={notes} />
        </section>
      )}

      <section className="section" id="talks" aria-labelledby="talks-title">
        <div className="section-head">
          <h2 className="section-title" id="talks-title">Talks</h2>
          <div className="section-aside">
            <p className="section-intro">{TALKS_INTRO}</p>
            <Link className="ext" href="/talks">All talks</Link>
          </div>
        </div>
        <TalkRows talks={talks} />
      </section>

      <section className="contact" id="contact" aria-labelledby="contact-title">
        <p className="mono eyebrow" id="contact-title">Contact</p>
        <a className="contact-email" href={`mailto:${SITE.email}`}>{SITE.email}</a>
        <p>{CONTACT_TEXT} <a href={SITE.linkedin}>LinkedIn</a> is for shorter messages.</p>
      </section>
    </>
  )
}
