/**
 * Cloudflare Web Analytics, cookieless, runs only when NEXT_PUBLIC_CF_BEACON_TOKEN is set at build time (on Netlify:
 * Site configuration, Environment variables; the token is the "token" value in the snippet Cloudflare shows under
 * Web Analytics). Until then no script is loaded.
 */
export function getCloudflareToken(): string | null {
  const value = (process.env.NEXT_PUBLIC_CF_BEACON_TOKEN ?? '').trim()
  return /^[A-Za-z0-9]+$/.test(value) ? value : null
}
