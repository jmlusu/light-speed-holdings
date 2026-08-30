import { cn } from '@/lib/utils'

interface PageShellProps {
  eyebrow?: string
  title: string
  intro?: string
  children?: React.ReactNode
  className?: string
}

export const PageShell = ({ eyebrow, title, intro, children, className }: PageShellProps) => (
  <div className="bg-background">
    <div className="mx-auto max-w-3xl px-6 py-20 md:py-24">
      {eyebrow ? (
        <p className="mb-4 text-sm font-medium uppercase tracking-widest text-muted">{eyebrow}</p>
      ) : null}
      <h1 className="text-4xl font-bold tracking-tight md:text-5xl">{title}</h1>
      {intro ? <p className="mt-5 text-lg leading-relaxed text-muted">{intro}</p> : null}
      <div className={cn('mt-10', className)}>{children}</div>
    </div>
  </div>
)
