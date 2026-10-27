import { type Talk, shortDate } from '@/lib/talks'

/** The ruled list of talks; a row links to the session page, and names the recording when there is one. */
export default function TalkRows({ talks }: { talks: Talk[] }) {
  return (
    <>
      {talks.map(talk => (
        <div className="row" key={talk.title}>
          <div>
            <h3>{talk.href ? <a href={talk.href}>{talk.title}</a> : talk.title}</h3>
            <p>{talk.format}, {talk.event}, {talk.city}</p>
            {talk.recording && <p><a className="ext" href={talk.recording.href}>{talk.recording.label}</a></p>}
          </div>
          <span className="m">{shortDate(talk.date)}</span>
        </div>
      ))}
    </>
  )
}
