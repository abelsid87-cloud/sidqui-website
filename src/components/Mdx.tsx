import { isValidElement, type ComponentProps, type ReactNode } from 'react'
import { MDXRemote } from 'next-mdx-remote/rsc'
import { slugify } from '@/lib/notes'

function textOf(node: ReactNode): string {
  if (typeof node === 'string' || typeof node === 'number') return String(node)
  if (Array.isArray(node)) return node.map(textOf).join('')
  if (isValidElement<{ children?: ReactNode }>(node)) return textOf(node.props.children)
  return ''
}

/** A section heading carries an id and links to itself, so that a section can be cited by its address. */
function H2({ children }: ComponentProps<'h2'>) {
  const id = slugify(textOf(children))
  return (
    <h2 id={id}>
      <a className="anchor" href={`#${id}`}>{children}</a>
    </h2>
  )
}

/** A note's Markdown with the site's headings. */
export default function Mdx({ source }: { source: string }) {
  return <MDXRemote source={source} components={{ h2: H2 }} />
}
