import type { Metadata } from 'next'
import { PageShell } from '@/components/layout/page-shell'

export const metadata: Metadata = {
  title: 'Careers',
  description: 'Join LightSpeed Holdings and help build enterprise AI in production.',
}

export default function CareersPage() {
  return (
    <PageShell
      eyebrow="Careers"
      title="Come Build With Us"
      intro="We're hiring engineers, consultants, and operators who love taking AI from idea to production."
    >
      <div className="space-y-6 text-muted">
        <div className="rounded-md border border-border/60 p-6">
          <h2 className="font-semibold text-foreground">Open Roles</h2>
          <p className="mt-2">
            Role listings are coming soon. Introduce yourself via{' '}
            <a className="text-primary underline" href="mailto:hello@lightspeed-holdings.com">
              hello@lightspeed-holdings.com
            </a>{' '}
            and we&apos;ll keep you posted.
          </p>
        </div>
      </div>
    </PageShell>
  )
}
