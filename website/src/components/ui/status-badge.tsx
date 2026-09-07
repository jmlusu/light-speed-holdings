import { cn } from '@/lib/utils'
import * as React from 'react'

type Status = 'proven-in-house' | 'in-pilot' | 'fieldable-2026' | 'in-development'

const statusConfig: Record<Status, { label: string; color: string; bgColor: string }> = {
  'proven-in-house': {
    label: 'Proven in-house',
    color: 'text-sovereign',
    bgColor: 'bg-sovereign/10 border-sovereign/30',
  },
  'in-pilot': {
    label: 'In pilot',
    color: 'text-primary',
    bgColor: 'bg-primary/10 border-primary/30',
  },
  'fieldable-2026': {
    label: 'Fieldable in 2026',
    color: 'text-accent',
    bgColor: 'bg-accent/10 border-accent/30',
  },
  'in-development': {
    label: 'In active development',
    color: 'text-muted',
    bgColor: 'bg-muted/10 border-muted/30',
  },
}

interface StatusBadgeProps {
  status: Status
  className?: string
}

export const StatusBadge = ({ status, className }: StatusBadgeProps) => {
  const config = statusConfig[status]
  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
        config.color,
        config.bgColor,
        className
      )}
    >
      {config.label}
    </span>
  )
}