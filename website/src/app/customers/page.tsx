import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { caseStudies } from '@/data/homepage-data'
import { PageShell } from '@/components/layout/page-shell'

export default function CustomersPage() {
  return (
    <PageShell
      eyebrow="Community"
      title="Our Customers"
      intro="How we've helped sovereign wealth funds, private equity firms, and legal practices deliver measurable outcomes."
      className="max-w-none"
    >
      <div className="grid gap-6 md:grid-cols-3">
        {caseStudies.map((study) => (
          <Link key={study.id} href={study.slug} className="group">
            <Card className="h-full p-6 transition-colors hover:border-primary/40">
              <p className="text-xs font-semibold uppercase tracking-widest text-primary">
                {study.client}
              </p>
              <h2 className="mt-3 text-lg font-semibold leading-snug">{study.title}</h2>
              <p className="mt-3 text-sm text-muted">{study.outcome}</p>
            </Card>
          </Link>
        ))}
      </div>
    </PageShell>
  )
}
