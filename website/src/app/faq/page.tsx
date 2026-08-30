import type { Metadata } from 'next'
import { PageShell } from '@/components/layout/page-shell'

export const metadata: Metadata = {
  title: 'FAQs',
  description: 'Frequently asked questions about LightSpeed Holdings and how we work.',
}

const faqs = [
  [
    'How do we start?',
    'A discovery workshop aligned to a high-value use case, with a prioritised roadmap and ROI frame within weeks.',
  ],
  [
    'Do you build, or just advise?',
    'Both. We deliver production systems end-to-end with forward-deployed engineers who build alongside your teams.',
  ],
  [
    'Which industries do you serve?',
    'Financial services, energy and utilities, retail, and more — we anchor on business outcomes, not tech for its own sake.',
  ],
  [
    'How do you handle governance and risk?',
    'Responsible AI frameworks and controls are a core service: ethical use, regulatory compliance (incl. EU AI Act), and risk mitigation.',
  ],
]

export default function FaqPage() {
  return (
    <PageShell
      eyebrow="FAQs"
      title="Frequently Asked Questions"
      intro="Quick answers to the questions we hear most often."
    >
      <div className="space-y-6">
        {faqs.map(([question, answer]) => (
          <div key={question} className="rounded-md border border-border/60 p-6">
            <h2 className="font-semibold text-foreground">{question}</h2>
            <p className="mt-2 text-muted">{answer}</p>
          </div>
        ))}
      </div>
    </PageShell>
  )
}
