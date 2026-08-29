import Link from 'next/link'
import { Card } from '@/components/ui/card'
import { Icon } from '@/components/ui/icon'
import { industries } from '@/data/homepage-data'
import { PageShell } from '@/components/layout/page-shell'

export default function IndustriesPage() {
  return (
    <PageShell
      eyebrow="Industries"
      title="Industries We Serve"
      intro="Deep expertise and proven delivery across key enterprise sectors."
      className="max-w-none"
    >
      <div className="grid gap-6 md:grid-cols-3">
        {industries.map((industry) => (
          <Link key={industry.id} href={industry.slug} className="group">
            <Card className="h-full p-6 transition-colors hover:border-primary/40">
              <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-md bg-accent/10 text-accent">
                <Icon name={industry.icon} size={22} />
              </div>
              <h2 className="text-lg font-semibold group-hover:text-primary">
                {industry.title}
              </h2>
              <p className="mt-3 text-sm text-muted">{industry.description}</p>
            </Card>
          </Link>
        ))}
      </div>
    </PageShell>
  )
}
