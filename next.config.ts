import type { NextConfig } from 'next'

// Everything is same-origin: fonts and images are self-hosted. Cloudflare Web Analytics is allowed so that the beacon
// can be switched on later with an environment variable (src/lib/analytics.ts) without a policy change.
const CSP =
  "default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self' https://cloudflareinsights.com https://static.cloudflareinsights.com; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests"

const config: NextConfig = {
  poweredByHeader: false,
  images: { formats: ['image/avif', 'image/webp'] },
  async headers() {
    const headers = [
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
    ]
    // Production only: in development the policy would block live reload and React's debugging eval.
    if (process.env.NODE_ENV === 'production') headers.push({ key: 'Content-Security-Policy', value: CSP })
    return [{ source: '/:path*', headers }]
  },
}

export default config
