'use client'

import { useEffect } from 'react'

/** Marks the contents entry of the section on screen. Without JavaScript the contents are still a list of links. */
export default function TocHighlight({ ids }: { ids: string[] }) {
  const key = ids.join('|')
  useEffect(() => {
    const targets = key.split('|').map(id => document.getElementById(id)).filter((el): el is HTMLElement => el !== null)
    if (targets.length === 0) return
    const links = new Map(targets.map(el => [el.id, document.querySelector<HTMLAnchorElement>(`.toc a[href="#${el.id}"]`)]))
    let current = ''
    const onScroll = () => {
      const line = window.scrollY + 140
      let active = ''
      for (const el of targets) if (el.offsetTop <= line) active = el.id
      if (active === current) return
      links.get(current)?.removeAttribute('aria-current')
      links.get(active)?.setAttribute('aria-current', 'true')
      current = active
    }
    onScroll()
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [key])
  return null
}
