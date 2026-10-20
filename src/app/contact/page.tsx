import type { Metadata } from 'next'
import Link from 'next/link'
import { pageMetadata } from '@/lib/seo'
import { CONTACT_TEXT, LANGUAGES, SITE } from '@/lib/site'

export const metadata: Metadata = pageMetadata({ title: 'Contact', description: `How to reach ${SITE.name}: email, LinkedIn, and where organisers find the biographies and the headshot.`, path: '/contact' })

export default function ContactPage() {
  return (
    <>
      <header className="page">
        <p className="mono eyebrow">Contact</p>
        <h1 className="page-title">Contact</h1>
        <a className="contact-email" href={`mailto:${SITE.email}`}>{SITE.email}</a>
        <p className="lead muted">{CONTACT_TEXT} <a href={SITE.linkedin}>LinkedIn</a> is for shorter messages.</p>
      </header>
      <section className="section" aria-labelledby="details-title">
        <h2 className="section-title sm" id="details-title">Details</h2>
        <ul className="facts">
          <li><span>Email</span><span><a href={`mailto:${SITE.email}`}>{SITE.email}</a></span></li>
          <li><span>LinkedIn</span><span><a href={SITE.linkedin} rel="me">LinkedIn profile</a></span></li>
          <li><span>Based in</span><span>{SITE.city}, United Arab Emirates. Gulf Standard Time, UTC+4.</span></li>
          <li><span>Languages</span><span>{LANGUAGES.join(', ')}.</span></li>
          <li><span>Organisers</span><span>The biographies and the headshot are on the <Link href="/about#organisers">About page</Link>.</span></li>
          <li><span>The firm</span><span>For UBIK, <a href="https://ubik.ae">ubik.ae</a>.</span></li>
        </ul>
      </section>
    </>
  )
}
