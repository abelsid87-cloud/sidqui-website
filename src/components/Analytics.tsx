import { getCloudflareToken } from '@/lib/analytics'

export default function Analytics() {
  const token = getCloudflareToken()
  if (!token) return null
  return <script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon={JSON.stringify({ token })} />
}
