import { AnimatedCard } from '@/components/ui/animated-card'
import { Button } from '@/components/ui/button'
import { CountUp } from '@/components/ui/count-up'
import { Icon } from '@/components/ui/icon'
import { Reveal } from '@/components/ui/reveal'
import { cn } from '@/lib/utils'

interface Industry {
  id: string
  title: string
  description: string
  slug: string
  icon: string
  stat?: { label: string; value: string; suffix: string }
}

interface IndustriesSectionProps {
  industries: Industry[]
  className?: string
}

export const IndustriesSection = ({ industries, className }: IndustriesSectionProps) => {
  return (
    <section className={cn('border-y border-border/60 bg-surface/40 py-24', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <Reveal delay={0}>
          <div className="mb-16 text-center">
            <h2 className="font-display text-3xl font-bold tracking-tight md:text-5xl">
              Industries We Serve
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-muted">
              Deep regional expertise across the sectors shaping Southern Africa's digital future.
            </p>
          </div>
        </Reveal>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {industries.map((industry, index) => (
            <Reveal key={industry.id} delay={index * 80}>
              <AnimatedCard variant="border-glow" className="group p-6">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-md bg-accent/10 text-accent">
                  <Icon name={industry.icon} size={22} />
                </div>
                <h3 className="text-xl font-semibold">{industry.title}</h3>
                <p className="mt-3 text-sm leading-relaxed text-muted">{industry.description}</p>
                {industry.stat && (
                  <div className="mt-6 flex items-baseline gap-2">
                    <CountUp
                      target={parseInt(industry.stat.value.replace(/,/g, ''), 10)}
                      suffix={industry.stat.suffix}
                      className="text-3xl font-bold text-primary tabular-nums"
                      duration={1400}
                    />
                    <span className="text-sm text-muted self-end pb-1">
                      {industry.stat.label}
                    </span>
                  </div>
                )}
                <Button
                  variant="ghost"
                  size="sm"
                  className="mt-6 gap-1 p-0 group-hover:text-primary"
                  href={industry.slug}
                >
                  Learn more <Icon name="arrow" size={16} className="arrow-slide" />
                </Button>
              </AnimatedCard>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  )
}