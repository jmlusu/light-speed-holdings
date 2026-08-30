import type { SVGProps } from 'react'

const paths: Record<string, React.ReactNode> = {
  strategy: (
    <>
      <path d="M3 3v18h18" />
      <path d="M7 15l4-6 4 3 5-8" />
      <circle cx="7" cy="15" r="1" />
      <circle cx="11" cy="9" r="1" />
      <circle cx="15" cy="12" r="1" />
      <circle cx="20" cy="4" r="1" />
    </>
  ),
  governance: (
    <>
      <path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7l8-4z" />
      <path d="M9 12l2 2 4-4" />
    </>
  ),
  data: (
    <>
      <ellipse cx="12" cy="5" rx="8" ry="3" />
      <path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5" />
      <path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" />
    </>
  ),
  custom: (
    <>
      <path d="M12 2l3 6 6 .9-4.5 4 1.1 6.1L12 16l-5.7 3L7.5 13 3 8.9 9 8l3-6z" />
    </>
  ),
  operating: (
    <>
      <circle cx="12" cy="12" r="3" />
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1" />
    </>
  ),
  agents: (
    <>
      <rect x="4" y="4" width="6" height="6" rx="1" />
      <rect x="14" y="4" width="6" height="6" rx="1" />
      <rect x="4" y="14" width="6" height="6" rx="1" />
      <rect x="14" y="14" width="6" height="6" rx="1" />
    </>
  ),
  toolkit: (
    <>
      <path d="M14.7 6.3a4 4 0 00-5.4 5.4L3 18v3h3l6.3-6.3a4 4 0 005.4-5.4L15 12l-3-3 2.7-2.7z" />
    </>
  ),
  financial: (
    <>
      <path d="M3 21h18" />
      <path d="M5 21V10M10 21V4M15 21v-7M19 21V7" />
    </>
  ),
  energy: (
    <>
      <path d="M13 2L4 14h6l-1 8 9-12h-6l1-8z" />
    </>
  ),
  retail: (
    <>
      <path d="M3 9l1.5 12h15L21 9H3z" />
      <path d="M8 9V6a4 4 0 018 0v3" />
    </>
  ),
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
