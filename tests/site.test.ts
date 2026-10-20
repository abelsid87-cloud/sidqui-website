import { describe, expect, it } from 'vitest'
import { getNote, getPublishedNotes } from '@/lib/notes'
import { BIO_LONG, BIO_SHORT, ROLES, SITE } from '@/lib/site'
import { TALKS, shortDate } from '@/lib/talks'

const words = (s: string) => s.trim().split(/\s+/).length

describe('the facts', () => {
  it('keeps the house style: no "we", no em-dashes, no praise adjectives', () => {
    const text = [SITE.definition, SITE.record, BIO_SHORT, ...BIO_LONG, ...ROLES.map(r => r.text)].join(' ')
    expect(text).not.toMatch(/—/)
    expect(text).not.toMatch(/\b(we|our)\b/i)
    expect(text).not.toMatch(/world-class|leading|trusted|passionate|seasoned|visionary/i)
  })
  it('keeps the biographies at the agreed lengths', () => {
    expect(words(BIO_SHORT)).toBeLessThanOrEqual(60)
    expect(words(BIO_LONG.join(' '))).toBeLessThanOrEqual(135)
  })
  it('uses the US spelling of data center only', () => {
    const text = [SITE.definition, SITE.record, BIO_SHORT, ...BIO_LONG, ...ROLES.map(r => r.text)].join(' ')
    expect(text).not.toMatch(/data centre/i)
  })
})

describe('talks', () => {
  it('lists the DCD panel with a short date', () => {
    expect(TALKS[0].event).toBe('DCD Connect MENA')
    expect(shortDate(TALKS[0].date)).toBe('26 Oct 2026')
  })
})

describe('notes', () => {
  it('publishes the three launch notes and nothing marked draft', () => {
    const notes = getPublishedNotes()
    expect(notes.map(n => n.slug).sort()).toEqual(['africa-brief-starts-with-the-utility', 'gulf-ai-hall-cooling', 'tier-iii-design-certificate'])
    for (const note of notes) expect(note.draft).toBe(false)
    expect(getNote('no-such-note')).toBeNull()
  })
  it('keeps the notes in the house style', () => {
    for (const meta of getPublishedNotes()) {
      const note = getNote(meta.slug)!
      expect(note.content).not.toMatch(/—/)
      expect(note.content).not.toMatch(/data centre/i)
      expect(note.content.split(/\s+/).length).toBeGreaterThan(600)
    }
  })
})
