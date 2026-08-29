import Link from 'next/link'
import { caseStudies } from '@/data/homepage-data'
import { PageShell } from '@/components/layout/page-shell'

export function generateStaticParams() {
  return caseStudies.map((study) => ({ slug: study.slug.replace('/customers/', '') }))
}

interface Props {
  params: Promise<{ slug: string }>
}

export default async function CaseStudyPage({ params }: Props) {
  const { slug } = await params
  const study = caseStudies.find((s) => s.slug === `/customers/${slug}`)

  if (!study) {
    return (
      <PageShell eyebrow="Customers" title="Case study not found">
        <Link href="/customers" className="text-primary underline">
          ← All customers
        </Link>
      </PageShell>
    )
  }

  return (
    <PageShell eyebrow={study.client} title={study.title}>
      <p className="text-lg font-semibold text-primary">{study.outcome}</p>
      <div className="mt-8">
        <Link href="/customers" className="text-sm text-primary underline">
          ← All customers
        </Link>
      </div>
    </PageShell>
  )
}
