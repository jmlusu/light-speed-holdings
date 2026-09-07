import { cn } from '@/lib/utils'
import * as React from 'react'

interface AnimatedCardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'border-glow'
}

export const AnimatedCard = React.forwardRef<HTMLDivElement, AnimatedCardProps>(
  ({ className, variant = 'default', children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'animated-card rounded-md border border-border bg-surface',
          variant === 'border-glow' && 'border-primary/20',
          className
        )}
        {...props}
      >
        {children}
      </div>
    )
  }
)

AnimatedCard.displayName = 'AnimatedCard'