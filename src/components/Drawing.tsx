import fs from 'fs'
import path from 'path'

/**
 * A drawing from scripts/drawings, inlined so that it uses the page's fonts and draws itself in. The caption's
 * first sentence is set as a mono label naming the figure; the rest follows in sentence case.
 */
export default function Drawing({ name, caption }: { name: string; caption: string }) {
  const file = path.join(process.cwd(), 'public/drawings', `${name}.svg`)
  if (!fs.existsSync(file)) return null
  const svg = fs.readFileSync(file, 'utf8')
  const match = /^(.+?\.)\s+(\S[\s\S]*)$/.exec(caption.trim())
  const label = match ? match[1] : null
  const text = match ? match[2] : caption.trim()
  return (
    <figure className="plate">
      <div className="drawing" dangerouslySetInnerHTML={{ __html: svg }} />
      <figcaption className="figcap">
        {label && <span className="mono lab">{label}</span>}
        <span>{text}</span>
      </figcaption>
    </figure>
  )
}
