'use client'

import { useEffect, useRef, useState } from 'react'

interface UseCountUpOptions {
  target: number
  duration?: number
  suffix?: string
  prefix?: string
  startOnView?: boolean
  threshold?: number
}

export function useCountUp({
  target,
  duration = 1200,
  suffix = '',
  prefix = '',
  startOnView = true,
  threshold = 0.5,
}: UseCountUpOptions) {
  const [count, setCount] = useState(0)
  const [hasStarted, setHasStarted] = useState(!startOnView)
  const elementRef = useRef<HTMLElement | null>(null)
  const animationRef = useRef<number | null>(null)

  useEffect(() => {
    if (startOnView && !hasStarted) {
      const element = elementRef.current
      if (!element) return

      const prefersReducedMotion = window.matchMedia(
        '(prefers-reduced-motion: reduce)'
      ).matches

      if (prefersReducedMotion) {
        setCount(target)
        setHasStarted(true)
        return
      }

      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setHasStarted(true)
            observer.unobserve(element)
          }
        },
        { threshold }
      )

      observer.observe(element)

      return () => {
        observer.disconnect()
      }
    }
  }, [startOnView, hasStarted, threshold])

  useEffect(() => {
    if (!hasStarted) return

    const prefersReducedMotion = window.matchMedia(
      '(prefers-reduced-motion: reduce)'
    ).matches

    if (prefersReducedMotion) {
      setCount(target)
      return
    }

    const startTime = performance.now()
    const startValue = 0

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)

      const easedProgress = 1 - Math.pow(1 - progress, 3)
      const currentValue = Math.floor(startValue + (target - startValue) * easedProgress)

      setCount(currentValue)

      if (progress < 1) {
        animationRef.current = requestAnimationFrame(animate)
      } else {
        setCount(target)
      }
    }

    animationRef.current = requestAnimationFrame(animate)

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [hasStarted, target, duration])

  return {
    ref: elementRef,
    count,
    formatted: `${prefix}${count.toLocaleString()}${suffix}`,
  }
}