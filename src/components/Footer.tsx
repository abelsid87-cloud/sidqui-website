import { SITE } from '@/lib/site'

export default function Footer() {
  return (
    <footer className="footer mono">
      <span>{SITE.name} · {SITE.city}</span>
      <span>{SITE.domain} · {new Date().getFullYear()}</span>
    </footer>
  )
}
