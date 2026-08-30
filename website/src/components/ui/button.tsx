import * as React from 'react'
import Link from 'next/link'
import { cn } from '@/lib/utils'

type Variant = 'primary' | 'secondary' | 'ghost' | 'outline'
type Size = 'sm' | 'md' | 'lg'

interface BaseProps {
  variant?: Variant
  size?: Size
  className?: string
  children?: React.ReactNode
}

export interface ButtonLinkProps extends BaseProps {
  href: string
  onClick?: () => void
}

export interface ButtonNativeProps extends BaseProps, Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'type'> {
  type?: 'button' | 'submit' | 'reset'
  href?: never
}

export type ButtonProps = ButtonLinkProps | ButtonNativeProps

const baseClass =
  'inline-flex items-center justify-center rounded-md font-medium transition-colors ' +
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 ' +
  'disabled:pointer-events-none disabled:opacity-50'

const variantClass: Record<Variant, string> = {
  primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
  secondary: 'bg-card text-card-foreground border border-border hover:border-primary/60',
  ghost: 'text-foreground hover:bg-card',
  outline: 'border border-border text-foreground hover:border-primary/60',
}

const sizeClass: Record<Size, string> = {
  sm: 'h-9 px-3 text-sm',
  md: 'h-10 px-5 text-sm',
  lg: 'h-12 px-8 text-base',
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', children, ...props }, ref) => {
    const classes = cn(baseClass, variantClass[variant], sizeClass[size], className)

    if ('href' in props && props.href !== undefined) {
      const { href } = props
      return (
        <Link href={href} className={classes}>
          {children}
        </Link>
      )
    }

    const { type = 'button', ...buttonProps } = props as ButtonNativeProps
    return (
      <button ref={ref} type={type} className={classes} {...buttonProps}>
        {children}
      </button>
    )
  },
)

Button.displayName = 'Button'
