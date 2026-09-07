import { AnimatedCard } from '@/components/ui/animated-card'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { Reveal } from '@/components/ui/reveal'
import { cn } from '@/lib/utils'

interface Insight {
  id: string
  title: string
  excerpt: string
  date: string
  slug: string
}

interface InsightsSectionProps {
  insights: Insight[]
  className?: string
}

export const InsightsSection = ({ insights, className }: InsightsSectionProps) => {
  return (
    <section className={cn('bg-bg py-24', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <Reveal delay={0}>
          <div className="mb-16 text-center">
            <h2 className="font-display text-3xl font-bold tracking-tight md:text-5xl">
              Pharos — Thought Leadership
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-muted">
              The CEO's long-form intellectual program: white papers, the monthly Malawi Agentic AI
              Monitor, and regional governance frameworks.
            </p>
          </div>
        </Reveal>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          {insights.map((insight, index) => (
            <Reveal key={insight.id} delay={index * 80}>
              <AnimatedCard variant="border-glow" className="group flex flex-col p-6">
                <p className="text-sm text-muted">{insight.date}</p>
                <h3 className="mt-3 text-lg font-semibold leading-snug">{insight.title}</h3>
                <p className="mt-3 flex-1 text-sm leading-relaxed text-muted line-clamp-3">
                  {insight.excerpt}
                </p>
                <Button
                  variant="ghost"
                  size="sm"
                  className="mt-6 gap-1 self-start p-0 group-hover:text-primary"
                  href={insight.slug}
                >
                  Read more <Icon name="arrow" size={16} className="arrow-slide" />
                </Button>
              </AnimatedCard>
            </Reveal>
          ))}
        </div>

        <Reveal delay={300}>
          <div className="mt-16 text-center">
            <Button variant="outline" href="/proof#insights">
              View All Pharos Publications
            </Button>
          </div>
        </Reveal>
      </div>
    </section>
  )
}