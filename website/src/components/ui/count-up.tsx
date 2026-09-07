'use client'

import { useCountUp } from '@/hooks/use-count-up'

interface CountUpProps {
  target: number
  duration?: number
  suffix?: string
  prefix?: string
  className?: string
  startOnView?: boolean
  threshold?: number
}

export const CountUp = ({
  target,
  duration = 1200,
  suffix = '',
  prefix = '',
  className,
  startOnView = true,
  threshold = 0.5,
}: CountUpProps) => {
  const { ref, formatted } = useCountUp({
    target,
    duration,
    suffix,
    prefix,
    startOnView,
    threshold,
  })

  return <span ref={ref} className={className}>{formatted}</span>
}