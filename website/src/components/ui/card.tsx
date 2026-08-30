import * as React from 'react'
import { cn } from '@/lib/utils'

type CardProps = React.HTMLAttributes<HTMLDivElement> & {
  shadow?: 'sm' | 'md' | 'lg'
}

export const Card = ({ className, shadow = 'md', children, ...props }: CardProps) => {
  const shadowMap: Record<string, string> = {
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
  }

  return (
    <div
      className={cn('rounded-md border border-border bg-card', shadowMap[shadow], className)}
      {...props}
    >
      {children}
    </div>
  )
}
