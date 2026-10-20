/**
 * Every fact the site states about Abdelilah Sidqui, in one place. The pages read from here, so a change is made
 * once. Nothing here is invented: each line is on ubik.ae, in the UBIK company profile, or was given by him.
 */
export const SITE = {
  name: 'Abdelilah Sidqui',
  domain: 'sidqui.com',
  url: 'https://sidqui.com',
  email: 'abdelilah@sidqui.com',
  linkedin: 'https://www.linkedin.com/in/abdelilah-sidqui-8856132/',
  city: 'Dubai',
  eyebrow: 'Dubai · Data center infrastructure',
  /** The one-sentence definition, also the page description for search engines. */
  definition: 'Electrical engineer, Managing Partner of the data center engineering consultancy UBIK, and Board Director of African Digital Infrastructure Investments.',
  record: 'More than twenty years in critical infrastructure and technology programmes across the Middle East and Africa. I spent eleven of them at EMC and then Dell Technologies in Dubai, and co-founded UBIK in 2019. I work in Arabic, French and English.',
  portrait: { src: '/people/abdelilah-sidqui.jpg', width: 1122, height: 1402, alt: 'Abdelilah Sidqui' },
} as const

export const ROLES = [
  {
    label: 'Now',
    title: 'Managing Partner, UBIK',
    text: 'UBIK is independent and works for owners, developers, operators, investors and contractors, from feasibility to operational readiness. I lead its advisory and engineering design work.',
    link: { href: 'https://ubik.ae', label: 'ubik.ae' },
  },
  {
    label: 'Board',
    title: 'Board Director, ADII',
    text: 'African Digital Infrastructure Investments, which invests in data centers, cloud and AI infrastructure across Africa.',
    link: { href: 'https://adii.africa', label: 'adii.africa' },
  },
  {
    label: 'Before',
    title: 'EMC, then Dell Technologies',
    text: 'I ran data center, cloud migration and IT transformation programmes for government and enterprise clients across the Middle East and Africa. I also led the region’s advanced software and data protection practice.',
  },
] as const

/** Third person, for organisers and nomination committees to copy unchanged. */
export const BIO_SHORT =
  'Abdelilah Sidqui is Co-founder and Managing Partner of UBIK, an independent data center engineering consultancy established in Dubai in 2019. He is also a Board Director of African Digital Infrastructure Investments. Before UBIK, he spent eleven years at EMC and then Dell Technologies, running data center and IT transformation programmes across the Middle East and Africa.'

export const BIO_LONG = [
  'Abdelilah Sidqui is Co-founder and Managing Partner of UBIK, an independent data center engineering consultancy established in Dubai in 2019. He leads the firm’s advisory and engineering design work. He is a Board Director of African Digital Infrastructure Investments (ADII).',
  'He has worked in critical infrastructure and technology for more than twenty years. At EMC and then Dell Technologies in Dubai, he spent eleven years running data center, cloud migration and IT transformation programmes for government and enterprise clients. He also led the advanced software and data protection practice for the Middle East and Africa.',
  'He holds a Master of Engineering in Electrical Engineering from ENSEM Casablanca, completed Executing Complex Programs at Stanford University School of Engineering, and is an MSP Practitioner. He works in Arabic, French and English.',
]

export const EDUCATION = [
  'Master of Engineering in Electrical Engineering, ENSEM Casablanca',
  'Executing Complex Programs, Stanford University School of Engineering',
  'MSP Practitioner',
]

export const LANGUAGES = ['Arabic', 'French', 'English']

export const HEADSHOTS = [
  { href: '/downloads/abdelilah-sidqui-headshot-800.jpg', label: '800 px, for programmes and web' },
  { href: '/downloads/abdelilah-sidqui-headshot-full.jpg', label: 'Full size, for print' },
]
