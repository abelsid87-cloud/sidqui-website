import { describe, expect, it } from 'vitest'
import { feedXml } from '@/app/feed.xml/route'
import { getNote, getPublishedNotes, getReadNext, headingsOf, readingMinutes, slugify } from '@/lib/notes'
import { BIO_LONG, BIO_SHORT, CONTACT_TEXT, NOTES_INTRO, ROLES, SITE, TALKS_INTRO } from '@/lib/site'
import { TALKS, shortDate, splitByDate } from '@/lib/talks'

const words = (s: string) => s.trim().split(/\s+/).length
const STANDING = [SITE.definition, SITE.record, BIO_SHORT, ...BIO_LONG, ...ROLES.map(r => r.text), NOTES_INTRO, TALKS_INTRO, CONTACT_TEXT].join(' ')

describe('the facts', () => {
  it('keeps the house style: no "we", no em-dashes, no praise adjectives', () => {
    expect(STANDING).not.toMatch(/—/)
    expect(STANDING).not.toMatch(/\b(we|our)\b/i)
    expect(STANDING).not.toMatch(/world-class|leading|trusted|passionate|seasoned|visionary/i)
  })
  it('keeps the biographies at the agreed lengths', () => {
    expect(words(BIO_SHORT)).toBeLessThanOrEqual(60)
    expect(words(BIO_LONG.join(' '))).toBeLessThanOrEqual(135)
  })
  it('uses the US spelling of data center only', () => {
    expect(STANDING).not.toMatch(/data centre/i)
  })
})

describe('talks', () => {
  it('lists the DCD panel with a short date', () => {
    expect(TALKS[0].event).toBe('DCD Connect MENA')
    expect(shortDate(TALKS[0].date)).toBe('26 Oct 2026')
  })
  it('splits upcoming from past on the day of the build', () => {
    const before = splitByDate(TALKS, new Date('2026-10-01T00:00:00Z'))
    const after = splitByDate(TALKS, new Date('2026-11-01T00:00:00Z'))
    expect(before.upcoming.map(t => t.date)).toEqual(['2026-10-26'])
    expect(before.past).toEqual([])
    expect(after.past.map(t => t.date)).toEqual(['2026-10-26'])
    expect(after.upcoming).toEqual([])
  })
})

describe('notes', () => {
  it('publishes the three launch notes and nothing marked draft', () => {
    const notes = getPublishedNotes()
    expect(notes.map(n => n.slug).sort()).toEqual(['africa-brief-starts-with-the-utility', 'gulf-ai-hall-cooling', 'tier-iii-design-certificate'])
    for (const note of notes) expect(note.draft).toBe(false)
    expect(getNote('no-such-note')).toBeNull()
  })
  it('keeps the notes in the house style, each with a drawing', () => {
    for (const meta of getPublishedNotes()) {
      const note = getNote(meta.slug)!
      expect(note.content).not.toMatch(/—/)
      expect(note.content).not.toMatch(/data centre/i)
      expect(note.content.split(/\s+/).length).toBeGreaterThan(600)
      expect(note.drawing?.name).toBeTruthy()
      expect(note.drawing?.caption).toMatch(/^Figure 0\d\. /)
    }
  })
  it('gives a reading time and addressable headings', () => {
    expect(readingMinutes('one two three')).toBe(1)
    expect(readingMinutes(Array(690).fill('word').join(' '))).toBe(3)
    expect(slugify('What I ask for in the brief')).toBe('what-i-ask-for-in-the-brief')
    expect(slugify('Phases follow the signed capacity')).toBe('phases-follow-the-signed-capacity')
    expect(headingsOf('# Title\n\n## First section\ntext\n## Second, with a comma\n')).toEqual([
      { id: 'first-section', text: 'First section' },
      { id: 'second-with-a-comma', text: 'Second, with a comma' },
    ])
    for (const meta of getPublishedNotes()) {
      const note = getNote(meta.slug)!
      expect(note.minutes).toBeGreaterThanOrEqual(3)
      expect(note.headings.length).toBeGreaterThanOrEqual(3)
      expect(new Set(note.headings.map(h => h.id)).size).toBe(note.headings.length)
    }
  })
  it('recommends the other notes after each one, never the note itself', () => {
    for (const note of getPublishedNotes()) {
      const next = getReadNext(note.slug)
      expect(next.length).toBe(2)
      expect(next.map(n => n.slug)).not.toContain(note.slug)
    }
  })
})

describe('the feed', () => {
  it('lists every published note with its address and date', () => {
    const xml = feedXml()
    expect(xml).toMatch(/^<\?xml version="1.0" encoding="UTF-8"\?><rss version="2.0"/)
    for (const note of getPublishedNotes()) {
      expect(xml).toContain(`<link>${SITE.url}/notes/${note.slug}</link>`)
      expect(xml).toContain('<pubDate>Tue, 20 Oct 2026 00:00:00 GMT</pubDate>')
    }
    expect(xml).not.toMatch(/[^&]&[^a]/)
  })
})
