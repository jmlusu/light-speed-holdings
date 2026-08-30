import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { cn } from '@/lib/utils'

interface Service {
  id: string
  title: string
  description: string
  icon: string
  slug: string
}

interface ServicesSectionProps {
  services: Service[]
  className?: string
}

export const ServicesSection = ({ services, className }: ServicesSectionProps) => {
  return (
    <section className={cn('bg-background py-24', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold tracking-tight md:text-5xl">
            How We Help
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted">
            End-to-end AI services that turn ambition into production reality, delivering
            measurable business value.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
          {services.map((service) => (
            <Card
              key={service.id}
              className="group flex flex-col transition-colors hover:border-primary/40"
            >
              <div className="flex h-full flex-col p-6">
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-md bg-primary/10 text-primary">
                  <Icon name={service.icon} size={22} />
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
                  Learn more <Icon name="arrow" size={16} />
                </Button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
