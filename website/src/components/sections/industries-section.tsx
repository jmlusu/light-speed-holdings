import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { cn } from '@/lib/utils'

interface Industry {
  id: string
  title: string
  description: string
  slug: string
  icon: string
}

interface IndustriesSectionProps {
  industries: Industry[]
  className?: string
}

export const IndustriesSection = ({ industries, className }: IndustriesSectionProps) => {
  return (
    <section className={cn('border-y border-border/60 bg-card/40 py-24', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold tracking-tight md:text-5xl">
            Industries We Serve
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted">
            Deep expertise and proven delivery across key enterprise sectors.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          {industries.map((industry) => (
            <Card
              key={industry.id}
              className="group p-6 transition-colors hover:border-primary/40"
            >
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-md bg-accent/10 text-accent">
                <Icon name={industry.icon} size={22} />
              </div>
              <h3 className="text-xl font-semibold">{industry.title}</h3>
              <p className="mt-3 text-sm leading-relaxed text-muted">{industry.description}</p>
              <Button
                variant="ghost"
                size="sm"
                className="mt-6 gap-1 p-0 group-hover:text-primary"
                href={industry.slug}
              >
                Learn more <Icon name="arrow" size={16} />
              </Button>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
