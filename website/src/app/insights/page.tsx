import type { Metadata } from 'next'
import Link from 'next/link'
import { insights } from '@/data/homepage-data'
import { PageShell } from '@/components/layout/page-shell'

export const metadata: Metadata = {
  title: 'Insights',
  description: 'Perspectives on enterprise AI, governance, and transformation from LightSpeed Holdings.',
}

export default function InsightsPage() {
  return (
    <PageShell
      eyebrow="Community"
      title="Insights"
      intro="What we're learning about AI in production — from strategy to governance to delivery."
      className="max-w-none"
    >
      <div className="grid gap-6 md:grid-cols-2">
        {insights.map((insight) => (
          <Link
            key={insight.id}
            href={insight.slug}
            className="group rounded-md border border-border/60 p-6 transition-colors hover:border-primary/40"
          >
            <p className="text-sm text-muted">{insight.date}</p>
            <h2 className="mt-3 text-lg font-semibold leading-snug group-hover:text-primary">
              {insight.title}
            </h2>
            <p className="mt-3 text-sm text-muted line-clamp-3">{insight.excerpt}</p>
          </Link>
        ))}
      </div>
    </PageShell>
  )
}
