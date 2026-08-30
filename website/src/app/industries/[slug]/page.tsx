import Link from 'next/link'
import { notFound } from 'next/navigation'
import { PageShell } from '@/components/layout/page-shell'
import { industries } from '@/data/homepage-data'

export function generateStaticParams() {
  return industries.map((industry) => ({ slug: industry.slug.replace('/industries/', '') }))
}

interface Props {
  params: Promise<{ slug: string }>
}

export default async function IndustryPage({ params }: Props) {
  const { slug } = await params
  const industry = industries.find((i) => i.slug === `/industries/${slug}`)

  if (!industry) {
    notFound()
  }

  return (
    <PageShell eyebrow="Industries" title={industry.title}>
      <p className="text-lg leading-relaxed text-muted">{industry.description}</p>
      <div className="mt-8">
        <Link href="/industries" className="text-sm text-primary underline">
          ← All industries
        </Link>
      </div>
    </PageShell>
  )
}
