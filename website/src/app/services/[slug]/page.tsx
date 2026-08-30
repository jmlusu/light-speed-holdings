import Link from 'next/link'
import { notFound } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { PageShell } from '@/components/layout/page-shell'
import { services } from '@/data/homepage-data'

export function generateStaticParams() {
  return services.map((service) => ({ slug: service.slug.replace('/services/', '') }))
}

interface Props {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params
  const service = services.find((s) => s.slug === `/services/${slug}`)
  return { title: service?.title, description: service?.description }
}

export default async function ServicePage({ params }: Props) {
  const { slug } = await params
  const service = services.find((s) => s.slug === `/services/${slug}`)

  if (!service) {
    notFound()
  }

  return (
    <PageShell
      eyebrow="Services"
      title={service.title}
      intro={service.description}
      className="max-w-none"
    >
      <div className="flex flex-col gap-6">
        <div className="flex h-14 w-14 items-center justify-center rounded-md bg-primary/10 text-primary">
          <Icon name={service.icon} size={28} />
        </div>
        <p className="max-w-2xl text-muted">
          This page is a foundation template. Detailed service copy, deliverables, and related
          case studies plug in here as the site is filled out.
        </p>
        <div>
          <Button href="/get-in-touch">
            Ask what we can build for you
          </Button>
        </div>
        <Link href="/" className="text-sm text-primary underline">
          ← Back to home
        </Link>
      </div>
    </PageShell>
  )
}
