import type { Metadata } from 'next'
import Image from 'next/image'
import CopyButton from '@/components/CopyButton'
import { pageMetadata } from '@/lib/seo'
import { BIO_LONG, BIO_SHORT, EDUCATION, HEADSHOTS, LANGUAGES, SITE } from '@/lib/site'

export const metadata: Metadata = pageMetadata({ title: 'About', description: BIO_SHORT, path: '/about' })

/** The long biography, the facts an organiser or a committee asks for, and the kit to copy from. */
export default function AboutPage() {
  return (
    <>
      <header className="page about-head">
        <div>
          <p className="mono eyebrow">About</p>
          <h1 className="page-title">{SITE.name}</h1>
          <div className="reading about-bio">
            {BIO_LONG.map(paragraph => <p key={paragraph.slice(0, 24)}>{paragraph}</p>)}
          </div>
        </div>
        <div className="portrait">
          <Image src={SITE.portrait.src} alt={SITE.portrait.alt} width={400} height={500} sizes="200px" priority />
        </div>
      </header>

      <section className="section" aria-labelledby="facts-title">
        <h2 className="section-title sm" id="facts-title">Record</h2>
        <ul className="facts">
          <li><span>Now</span><span>Co-founder and Managing Partner, UBIK, Dubai, since 2019. Independent data center engineering consultancy for owners, developers, operators, investors and contractors.</span></li>
          <li><span>Board</span><span>Board Director, African Digital Infrastructure Investments (ADII).</span></li>
          <li><span>Before</span><span>Eleven years at EMC and then Dell Technologies in Dubai: data center, cloud migration and IT transformation programmes for government and enterprise clients across the Middle East and Africa; led the region&rsquo;s advanced software and data protection practice.</span></li>
          <li><span>Education</span><span>{EDUCATION.join('. ')}.</span></li>
          <li><span>Languages</span><span>{LANGUAGES.join(', ')}.</span></li>
          <li><span>Based in</span><span>{SITE.city}.</span></li>
        </ul>
      </section>

      <section className="section" id="organisers" aria-labelledby="kit-title">
        <div className="section-head">
          <h2 className="section-title sm" id="kit-title">For organisers</h2>
          <p className="section-intro">Two biographies in the third person and the headshot, to use unchanged in a programme, a nomination or a press piece.</p>
        </div>
        <div className="kit">
          <div>
            <h3>Short biography</h3>
            <p>{BIO_SHORT}</p>
            <CopyButton text={BIO_SHORT} label="Copy the short biography" />
          </div>
          <div>
            <h3>Long biography</h3>
            {BIO_LONG.map(paragraph => <p key={paragraph.slice(0, 24)}>{paragraph}</p>)}
            <CopyButton text={BIO_LONG.join('\n\n')} label="Copy the long biography" />
          </div>
          <div>
            <h3>Headshot</h3>
            <p>Photograph, 2026. Please use it uncropped and without a filter.</p>
            <ul className="downloads">
              {HEADSHOTS.map(file => (
                <li key={file.href}><a href={file.href} download>{file.label}</a></li>
              ))}
            </ul>
          </div>
        </div>
      </section>
    </>
  )
}
