import type { Metadata } from 'next'
import { PageShell } from '@/components/layout/page-shell'

export const metadata: Metadata = {
  title: 'About Us',
  description: 'LightSpeed Holdings — the AI Native Transformation Consultancy.',
}

export default function AboutPage() {
  return (
    <PageShell
      eyebrow="About Us"
      title="Who We Are"
      intro="LightSpeed Holdings is an AI native transformation consultancy. We work with global enterprises to turn AI ambition into production reality."
    >
      <div className="prose prose-invert max-w-none space-y-6 text-muted">
        <p>
          From strategy to deployment, we build it with you. Our forward-deployed engineers work
          alongside your teams, so the most strategic AI investments arrive far sooner.
        </p>
        <p>
          We combine proven accelerators with AI native engineering — covering strategy and
          roadmap, governance and risk, data and infrastructure, custom solutions, operating
          models, and AI agents and automation.
        </p>
      </div>
    </PageShell>
  )
}
