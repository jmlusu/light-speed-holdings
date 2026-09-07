'use client'

import { useEffect, useRef, useState } from 'react'

export function useScrolled(threshold = 100) {
  const [isScrolled, setIsScrolled] = useState(false)
  const rafRef = useRef<number | null>(null)

  useEffect(() => {
    const onScroll = () => {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current)
      }
      rafRef.current = requestAnimationFrame(() => {
        setIsScrolled(window.scrollY > threshold)
      })
    }

    window.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      window.removeEventListener('scroll', onScroll)
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current)
      }
    }
  }, [threshold])

  return isScrolled
}