import { AnimatedCard } from '@/components/ui/animated-card'
import { CountUp } from '@/components/ui/count-up'
import { Icon } from '@/components/ui/icon'
import { Marquee } from '@/components/ui/marquee'
import { Reveal } from '@/components/ui/reveal'
import { StatusBadge } from '@/components/ui/status-badge'
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
  industry: string
  status: 'proven-in-house' | 'in-pilot' | 'fieldable-2026' | 'in-development'
  description: string
  slug: string
}

interface ProofSectionProps {
  partners: Partner[]
  caseStudies: CaseStudy[]
  className?: string
}

export const ProofSection = ({ partners, caseStudies, className }: ProofSectionProps) => {
  const proofStats = [
    { label: 'Agents in production', value: '144', suffix: '' },
    { label: 'Countries in SADC', value: '4', suffix: '' },
    { label: 'Institutional partners', value: '8', suffix: '' },
    { label: 'Malawian ML engineers', value: '50', suffix: '+' },
  ]

  return (
    <section className={cn('bg-bg py-24', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <Reveal delay={0}>
          <div className="mb-16 text-center">
            <h2 className="font-display text-3xl font-bold tracking-tight md:text-5xl">
              Proof — Not Promises
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-muted">
              Everything here is real: our 144-agent platform, government pilots, and the SME
              running on our stack. No fabricated case studies.
            </p>
          </div>
        </Reveal>

        {/* Stats strip */}
        <Reveal delay={100}>
          <div className="mb-16 grid grid-cols-2 gap-8 md:grid-cols-4">
            {proofStats.map((stat, index) => (
              <div key={stat.label} className="text-center">
                <CountUp
                  target={parseInt(stat.value.replace(/,/g, ''), 10)}
                  suffix={stat.suffix}
                  className="text-4xl font-bold text-primary tabular-nums"
                  duration={1600}
                />
                <p className="mt-1 text-sm text-muted">{stat.label}</p>
              </div>
            ))}
          </div>
        </Reveal>

        {/* Pilot showcase */}
        <Reveal delay={200}>
          <div className="mb-16">
            <h3 className="text-2xl font-semibold mb-8">Current Engagements</h3>
            <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
              {caseStudies.map((study, index) => (
                <Reveal key={study.id} delay={index * 80}>
                  <AnimatedCard variant="border-glow" className="p-6">
                    <div className="flex items-start justify-between gap-4 mb-3">
                      <span className="text-sm font-semibold text-primary">{study.industry}</span>
                      <StatusBadge status={study.status} />
                    </div>
                    <h4 className="text-lg font-semibold">{study.title}</h4>
                    <p className="mt-1 text-sm text-muted">{study.client}</p>
                    <p className="mt-3 text-sm leading-relaxed text-muted">{study.description}</p>
                  </AnimatedCard>
                </Reveal>
              ))}
            </div>
          </div>
        </Reveal>

        {/* Partner marquee */}
        <Reveal delay={300}>
          <div className="border-t border-border/60 pt-16">
            <h3 className="text-sm font-medium uppercase tracking-widest text-muted mb-8">
              Ecosystem & Institutional Partners
            </h3>
            <Marquee speed={40} className="py-4">
              {partners.map((partner) => (
                <a
                  key={partner.id}
                  href={partner.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-3 px-6 py-3 min-w-[180px] rounded-md border border-border/60 bg-surface/50 transition-colors hover:border-primary/50 hover:bg-surface"
                >
                  <div className="w-8 h-8 flex items-center justify-center text-primary">
                    <Icon name={partner.logo} size={24} />
                  </div>
                  <span className="font-medium text-sm">{partner.name}</span>
                </a>
              ))}
            </Marquee>
          </div>
        </Reveal>
      </div>
    </section>
  )
}