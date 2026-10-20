import type { Metadata, Viewport } from 'next'
import localFont from 'next/font/local'
import './globals.css'
import Nav from '@/components/Nav'
import Footer from '@/components/Footer'
import JsonLd from '@/components/JsonLd'
import Analytics from '@/components/Analytics'
import { getPublishedNotes } from '@/lib/notes'
import { OG_IMAGE } from '@/lib/seo'
import { SITE } from '@/lib/site'

// Self-hosted, licences alongside in public/fonts. Only the display face is preloaded: the name is the largest paint.
const schibsted = localFont({ src: '../../public/fonts/schibsted-grotesk-latin-variable.woff2', weight: '400 900', display: 'swap', variable: '--font-schibsted' })
const inter = localFont({ src: '../../public/fonts/inter-latin-variable.woff2', weight: '100 900', display: 'swap', preload: false, variable: '--font-inter' })
const jetbrains = localFont({ src: '../../public/fonts/jetbrains-mono-latin-variable.woff2', weight: '400 700', display: 'swap', preload: false, variable: '--font-jetbrains' })

export const viewport: Viewport = { themeColor: '#F2EFE9' }

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title: { default: SITE.name, template: `%s · ${SITE.name}` },
  description: SITE.definition,
  openGraph: { type: 'website', siteName: SITE.name, title: SITE.name, description: SITE.definition, url: '/', images: [OG_IMAGE] },
  twitter: { card: 'summary_large_image' },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const showNotes = getPublishedNotes().length > 0
  return (
    <html lang="en-GB" className={`${schibsted.variable} ${inter.variable} ${jetbrains.variable}`}>
      <body>
        <div className="wrap">
          <Nav showNotes={showNotes} />
          <main id="main">{children}</main>
          <Footer />
        </div>
        <JsonLd />
        <Analytics />
      </body>
    </html>
  )
}
