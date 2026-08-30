import type { Metadata } from 'next'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { insights } from '@/data/homepage-data'
import { PageShell } from '@/components/layout/page-shell'

export function generateStaticParams() {
  return insights.map((insight) => ({ slug: insight.slug.replace('/insights/', '') }))
}

interface Props {
  params: Promise<{ slug: string }>
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params
  const insight = insights.find((i) => i.slug === `/insights/${slug}`)
  return { title: insight?.title ?? 'Insight' }
}

export default async function InsightPage({ params }: Props) {
  const { slug } = await params
  const insight = insights.find((i) => i.slug === `/insights/${slug}`)

  if (!insight) {
    notFound()
  }

  return (
    <PageShell eyebrow={insight.date} title={insight.title}>
      <p className="text-lg leading-relaxed text-muted">{insight.excerpt}</p>
      <div className="mt-8">
        <Link href="/insights" className="text-sm text-primary underline">
          ← All insights
        </Link>
      </div>
    </PageShell>
  )
}
