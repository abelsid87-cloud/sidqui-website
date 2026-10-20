import { type Talk, shortDate } from '@/lib/talks'

/** The ruled list of talks; a row links to the session page or the recording when there is one. */
export default function TalkRows({ talks }: { talks: Talk[] }) {
  return (
    <>
      {talks.map(talk => {
        const body = (
          <>
            <div><h3>{talk.title}</h3><p>{talk.format}, {talk.event}, {talk.city}</p></div>
            <span className="m">{shortDate(talk.date)}</span>
          </>
        )
        return talk.href ? <a className="row" href={talk.href} key={talk.title}>{body}</a> : <div className="row" key={talk.title}>{body}</div>
      })}
    </>
  )
}
