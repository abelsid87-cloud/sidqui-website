import { EDUCATION, SITE } from '@/lib/site'

/** Person data for search engines: name, roles, affiliations and the addresses that are his. */
export default function JsonLd() {
  const schema = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: SITE.name,
    url: SITE.url,
    image: `${SITE.url}${SITE.portrait.src}`,
    jobTitle: 'Managing Partner',
    description: SITE.definition,
    worksFor: { '@type': 'Organization', name: 'UBIK', legalName: 'UBIK FZ LLC', url: 'https://ubik.ae' },
    affiliation: { '@type': 'Organization', name: 'African Digital Infrastructure Investments', url: 'https://adii.africa' },
    alumniOf: [
      { '@type': 'CollegeOrUniversity', name: 'ENSEM Casablanca' },
      { '@type': 'CollegeOrUniversity', name: 'Stanford University School of Engineering' },
    ],
    hasCredential: EDUCATION.map(name => ({ '@type': 'EducationalOccupationalCredential', name })),
    knowsLanguage: ['ar', 'fr', 'en'],
    address: { '@type': 'PostalAddress', addressLocality: 'Dubai', addressCountry: 'AE' },
    email: `mailto:${SITE.email}`,
    sameAs: [SITE.linkedin, 'https://ubik.ae'],
  }
  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
}
