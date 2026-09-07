'use client'

import { cn } from '@/lib/utils'
import { useReveal } from '@/hooks/use-reveal'
import * as React from 'react'

interface RevealProps {
  children: React.ReactNode
  className?: string
  delay?: number
  asChild?: boolean
}

export const Reveal = ({
  children,
  className,
  delay = 0,
  asChild = false,
}: RevealProps) => {
  const { ref, isVisible } = useReveal()

  const child = React.Children.only(children) as React.ReactElement

  if (asChild) {
    return React.cloneElement(child, {
      ref,
      className: cn(
        child.props.className,
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6',
        'transition-all duration-[600ms] ease-[cubic-bezier(0.16,1,0.3,1)]',
        delay > 0 && `transition-delay-[${delay}ms]`,
        className
      ),
    })
  }

  return (
    <div
      ref={ref}
      className={cn(
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6',
        'transition-all duration-[600ms] ease-[cubic-bezier(0.16,1,0.3,1)]',
        delay > 0 && `transition-delay-[${delay}ms]`,
        className
      )}
    >
      {children}
    </div>
  )
}