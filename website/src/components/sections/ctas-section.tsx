import { Card } from '@/components/ui/card'
import { Icon } from '@/components/ui/icon'
import { cn } from '@/lib/utils'

interface Partner {
  id: string
  name: string
  logo: string
  url: string
}

interface CaseStudy {
  id: string
  title: string
  client: string
  outcome: string
  slug: string
}

interface CtasSectionProps {
  partners: Partner[]
  caseStudies: CaseStudy[]
  className?: string
}

export const CtasSection = ({ partners, caseStudies, className }: CtasSectionProps) => {
  return (
    <section className={cn('bg-background py-24', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <div className="grid gap-16 md:grid-cols-2">
          <div>
            <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
              Value We&apos;ve Delivered
            </h2>
            <p className="mt-4 text-muted">
              We work with global enterprises to turn AI ambition into production reality.
            </p>
            <div className="mt-8 grid gap-4">
              {caseStudies.map((study) => (
                <Card key={study.id} className="p-5">
                  <p className="text-sm font-semibold text-primary">{study.outcome}</p>
                  <p className="mt-1 text-sm text-muted">
                    {study.title} · {study.client}
                  </p>
                </Card>
              ))}
            </div>
          </div>

          <div>
            <h2 className="text-3xl font-bold tracking-tight md:text-4xl">
              Our Partners
            </h2>
            <p className="mt-4 text-muted">
              We deploy AI-native solutions with best-in-class infrastructure and technology
              partners.
            </p>
            <div className="mt-8 grid grid-cols-2 gap-4">
              {partners.map((partner) => (
                <a
                  key={partner.id}
                  href={partner.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 rounded-md border border-border p-4 text-foreground transition-colors hover:border-primary/50"
                >
                  <Icon name={partner.logo} size={24} className="text-primary" />
                  <span className="font-medium">{partner.name}</span>
                </a>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
