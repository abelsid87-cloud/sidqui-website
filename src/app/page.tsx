import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import { getPublishedNotes } from '@/lib/notes'
import { pageMetadata } from '@/lib/seo'
import { ROLES, SITE } from '@/lib/site'
import { TALKS, shortDate } from '@/lib/talks'

export const metadata: Metadata = pageMetadata({ title: SITE.name, description: SITE.definition, path: '/' })

export default function HomePage() {
  const notes = getPublishedNotes().slice(0, 5)
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
            <p className="section-intro">Short pieces on how data centers are planned, designed and delivered, drawn from my work in the Middle East and Africa.</p>
          </div>
          {notes.map(note => (
            <Link className="row" href={`/notes/${note.slug}`} key={note.slug}>
              <div><h3>{note.title}</h3><p>{note.summary}</p></div>
            </Link>
          ))}
        </section>
      )}

      <section className="section" id="talks" aria-labelledby="talks-title">
        <div className="section-head">
          <h2 className="section-title" id="talks-title">Talks</h2>
          <p className="section-intro">Talks and panels, most recent first. Biographies for organisers are on the <Link href="/about">About page</Link>.</p>
        </div>
        {TALKS.map(talk =>
          talk.href ? (
            <a className="row" href={talk.href} key={talk.title}>
              <div><h3>{talk.title}</h3><p>{talk.format}, {talk.event}, {talk.city}</p></div>
              <span className="m">{shortDate(talk.date)}</span>
            </a>
          ) : (
            <div className="row" key={talk.title}>
              <div><h3>{talk.title}</h3><p>{talk.format}, {talk.event}, {talk.city}</p></div>
              <span className="m">{shortDate(talk.date)}</span>
            </div>
          ),
        )}
      </section>

      <section className="contact" id="contact" aria-labelledby="contact-title">
        <p className="mono eyebrow" id="contact-title">Contact</p>
        <a className="contact-email" href={`mailto:${SITE.email}`}>{SITE.email}</a>
        <p>Email me about board and advisory roles, speaking invitations, press questions or a data center project. <a href={SITE.linkedin}>LinkedIn</a> is for shorter messages.</p>
      </section>
    </>
  )
}
