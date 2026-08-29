import type { Metadata } from 'next'
import { PageShell } from '@/components/layout/page-shell'
import { ContactForm } from '@/components/sections/contact-form'

export const metadata: Metadata = {
  title: 'Get In Touch',
  description: 'Tell us what you want to build. We\'ll respond with a plan.',
}

export default function GetInTouchPage() {
  return (
    <PageShell
      eyebrow="Get In Touch"
      title="What can we build for you?"
      intro="Tell us about your AI ambition and the outcome you need. We'll respond with a practical path to production."
    >
      <ContactForm />
    </PageShell>
  )
}
