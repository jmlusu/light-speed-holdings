import type { Metadata } from 'next'
import { PageShell } from '@/components/layout/page-shell'

export const metadata: Metadata = {
  title: 'Our Approach',
  description: 'How LightSpeed Holdings takes enterprise AI from strategy to production.',
}

export default function OurApproachPage() {
  return (
    <PageShell
      eyebrow="Our Approach"
      title="From Strategy to Production"
      intro="A deliberate, outcome-led method that moves AI from ambition to deployed reality."
    >
      <div className="space-y-6 text-muted">
        {[
          ['Discover', 'We align AI investment with business value, identifying high-impact use cases and measurable ROI.'],
          ['Design', 'We architect the data, governance, and operating model needed to succeed at scale.'],
          ['Build', 'Forward-deployed engineers build alongside your teams, from prototype to production.'],
          ['Run', 'We embed monitoring, risk controls, and continuous improvement so value keeps compounding.'],
        ].map(([step, copy]) => (
          <div key={step} className="flex gap-6 rounded-md border border-border/60 p-6">
            <span className="text-sm font-semibold uppercase tracking-widest text-primary">{step}</span>
            <p>{copy}</p>
          </div>
        ))}
      </div>
    </PageShell>
  )
}
