'use client'

import { useState } from 'react'

/** Copies a biography to the clipboard for an organiser; falls back to the selected text where the API is absent. */
export default function CopyButton({ text, label }: { text: string; label: string }) {
  const [done, setDone] = useState(false)
  async function copy() {
    try {
      await navigator.clipboard.writeText(text)
      setDone(true)
      window.setTimeout(() => setDone(false), 2000)
    } catch {
      setDone(false)
    }
  }
  return (
    <button type="button" onClick={copy} className="copy" aria-live="polite">
      {done ? 'Copied' : label}
    </button>
  )
}
