import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
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
    <section className={cn('bg-background py-24', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <div className="mb-16 text-center">
          <h2 className="text-3xl font-bold tracking-tight md:text-5xl">
            Our Latest Insights
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted">
            Perspectives on enterprise AI, governance, and transformation from our team.
          </p>
        </div>

        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          {insights.map((insight) => (
            <Card
              key={insight.id}
              className="group flex flex-col transition-colors hover:border-primary/40"
            >
              <div className="flex h-full flex-col p-6">
                <p className="text-sm text-muted">{insight.date}</p>
                <h3 className="mt-3 text-lg font-semibold leading-snug">{insight.title}</h3>
                <p className="mt-3 flex-1 text-sm leading-relaxed text-muted line-clamp-3">
                  {insight.excerpt}
                </p>
                <Button
                  variant="ghost"
                  size="sm"
                  className="mt-6 gap-1 self-start p-0 group-hover:text-primary"
                  href={insight.slug.replace('/insights/', '/insights/')}
                >
                  Read more <Icon name="arrow" size={16} />
                </Button>
              </div>
            </Card>
          ))}
        </div>

        <div className="mt-16 text-center">
          <Button variant="outline" href="/insights">
            View All Insights
          </Button>
        </div>
      </div>
    </section>
  )
}
