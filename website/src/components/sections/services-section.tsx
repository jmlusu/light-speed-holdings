import { AnimatedCard } from '@/components/ui/animated-card'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { Reveal } from '@/components/ui/reveal'
import { StatusBadge } from '@/components/ui/status-badge'
import { cn } from '@/lib/utils'

interface Service {
  id: string
  title: string
  description: string
  icon: string
  slug: string
  status: 'proven-in-house' | 'in-pilot' | 'fieldable-2026' | 'in-development'
}

interface ServicesSectionProps {
  services: Service[]
  className?: string
}

export const ServicesSection = ({ services, className }: ServicesSectionProps) => {
  return (
    <section className={cn('bg-bg py-24', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <Reveal delay={0}>
          <div className="mb-16 text-center">
            <h2 className="font-display text-3xl font-bold tracking-tight md:text-5xl">
              How We Help
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-muted">
              Three offer lines plus our proven agentic platform — all built on the same governed,
              offline-first architecture.
            </p>
          </div>
        </Reveal>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {services.map((service, index) => (
            <Reveal key={service.id} delay={index * 80}>
              <AnimatedCard variant="border-glow" className="group flex flex-col p-6">
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div className="flex h-11 w-11 items-center justify-center rounded-md bg-primary/10 text-primary shrink-0">
                    <Icon name={service.icon} size={22} />
                  </div>
                  <StatusBadge status={service.status} />
                </div>
                <h3 className="text-xl font-semibold">{service.title}</h3>
                <p className="mt-3 flex-1 text-sm leading-relaxed text-muted">
                  {service.description}
                </p>
                <Button
                  variant="ghost"
                  size="sm"
                  className="mt-6 self-start gap-1 p-0 group-hover:text-primary"
                  href={service.slug}
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