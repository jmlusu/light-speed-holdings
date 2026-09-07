import type { SVGProps } from 'react'

const paths: Record<string, React.ReactNode> = {
  // Service icons
  'agentic-building': (
    <>
      <rect x="4" y="4" width="6" height="6" rx="1" />
      <rect x="14" y="4" width="6" height="6" rx="1" />
      <rect x="4" y="14" width="6" height="6" rx="1" />
      <rect x="14" y="14" width="6" height="6" rx="1" />
      <path d="M10 10h4M10 14h4" strokeWidth={1.2} />
    </>
  ),
  'offer-a': (
    <>
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <path d="M9 12h6M12 9v6" strokeWidth={1.5} />
    </>
  ),
  'offer-b': (
    <>
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      <path d="M14 10h-4M12 8v4" strokeWidth={1.5} />
    </>
  ),
  'offer-c': (
    <>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <path d="M16 13H8M16 17H8M10 9H8" strokeWidth={1.5} />
    </>
  ),
  governance: (
    <>
      <path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7l8-4z" />
      <path d="M9 12l2 2 4-4" />
    </>
  ),

  // Industry icons
  agriculture: (
    <>
      <path d="M12 2v20M17 5v14M7 5v14M12 2a10 10 0 0 0-10 10c0 5.5 10 13 10 13s10-7.5 10-13a10 10 0 0 0-10-10z" />
    </>
  ),
  health: (
    <>
      <path d="M12 2v20M5 12h14M12 5l-5 5M12 5l5 5" strokeWidth={1.5} />
    </>
  ),
  financial: (
    <>
      <path d="M3 21h18" />
      <path d="M5 21V10M10 21V4M15 21v-7M19 21V7" />
    </>
  ),
  sme: (
    <>
      <rect x="2" y="7" width="8" height="12" rx="1" />
      <rect x="14" y="7" width="8" height="12" rx="1" />
      <path d="M6 11h4M6 15h4M18 11h4M18 15h4" strokeWidth={1.5} />
    </>
  ),
  government: (
    <>
      <path d="M12 2l8 5v10c0 4-3 7-8 8-5-1-8-4-8-9V7l8-5z" />
      <path d="M9 12l2 2 4-4" />
    </>
  ),

  // Common
  mail: (
    <>
      <rect x="3" y="5" width="18" height="14" rx="2" />
      <path d="M3 7l9 6 9-6" />
    </>
  ),
  pin: (
    <>
      <path d="M12 21s-7-6.1-7-11a7 7 0 0114 0c0 4.9-7 11-7 11z" />
      <circle cx="12" cy="10" r="2.5" />
    </>
  ),
  linkedin: (
    <>
      <rect x="3" y="3" width="18" height="18" rx="2" />
      <path d="M8 11v6M8 8v.01M12 17v-4a2.5 2.5 0 015 0v4M8 11h4" />
    </>
  ),
  youtube: (
    <>
      <rect x="2" y="6" width="20" height="12" rx="3" />
      <path d="M10 9.5v5l4.5-2.5-4.5-2.5z" />
    </>
  ),
  arrow: (
    <>
      <path d="M5 12h14M13 6l6 6-6 6" />
    </>
  ),
  // Legacy partners (for reference)
  aws: (
    <>
      <path d="M12 2l2.6 5.4L20 6.2l-1.6 5.6 4 3.9-5.4 2.1-1 5.6L12 21l-4 2.4-.9-5.6-5.4-2.1 4-3.9L4 6.2l5.4 1.2L12 2z" />
    </>
  ),
  microsoft: (
    <>
      <rect x="4" y="4" width="7.5" height="7.5" />
      <rect x="12.5" y="4" width="7.5" height="7.5" />
      <rect x="4" y="12.5" width="7.5" height="7.5" />
      <rect x="12.5" y="12.5" width="7.5" height="7.5" />
    </>
  ),
  nvidia: (
    <>
      <path d="M12 2C7 4 4 8 4 13c0 1 0 2 .2 3" />
      <path d="M12 2c3 1.5 5 4 5.5 7" />
      <path d="M4.2 13C5 17 8 20 12 22c2-1 3.5-2.5 4.5-4.5" />
    </>
  ),
  openai: (
    <>
      <path d="M12 3a4 4 0 014 4 4 4 0 01-4 4 4 4 0 01-4-4 4 4 0 014-4z" />
      <path d="M8.5 13.5a4.2 4.2 0 11-1.8-8" />
    </>
  ),
}

export interface IconProps extends SVGProps<SVGSVGElement> {
  name: keyof typeof paths | string
  size?: number
}

export const Icon = ({ name, size = 24, className, ...props }: IconProps) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.8}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
    className={className}
    {...props}
  >
    {paths[name] ?? paths.arrow}
  </svg>
)
