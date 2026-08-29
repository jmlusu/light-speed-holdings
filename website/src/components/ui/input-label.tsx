import { cn } from '@/lib/utils'

export interface InputLabelProps {
  htmlFor: string
  className?: string
  children: React.ReactNode
}

export const InputLabel = ({ htmlFor, className, children }: InputLabelProps) => (
  <label htmlFor={htmlFor} className={cn('block text-sm font-medium text-foreground mb-2', className)}>
    {children}
  </label>
)
