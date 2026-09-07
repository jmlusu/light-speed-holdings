import { cn } from '@/lib/utils'
import * as React from 'react'

interface MarqueeProps {
  children: React.ReactNode
  className?: string
  speed?: number
  paused?: boolean
}

export const Marquee = ({
  children,
  className,
  speed = 30,
  paused = false,
}: MarqueeProps) => {
  const contentRef = React.useRef<HTMLDivElement>(null)

  return (
    <div
      className={cn('overflow-hidden', className)}
      onMouseEnter={() => (paused ? null : contentRef.current?.style.setProperty('animation-play-state', 'paused'))}
      onMouseLeave={() => (paused ? null : contentRef.current?.style.setProperty('animation-play-state', 'running'))}
    >
      <div
        ref={contentRef}
        className="marquee-track"
        style={{ animationDuration: `${speed}s` }}
      >
        {children}
        {children}
      </div>
    </div>
  )
}