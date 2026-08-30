import type { Metadata } from 'next'
import { PageShell } from '@/components/layout/page-shell'

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description: 'How LightSpeed Holdings handles your data.',
}

export default function PrivacyPolicyPage() {
  return (
    <PageShell
      eyebrow="Legal"
      title="Privacy Policy"
      intro="This notice explains how LightSpeed Holdings collects, uses, and protects personal information."
    >
      <div className="space-y-6 text-sm leading-relaxed text-muted">
        <p>
          <strong className="text-foreground">Information we collect.</strong> We collect the
          details you provide through our contact and newsletter forms — typically name, email
          address, company, and message.
        </p>
        <p>
          <strong className="text-foreground">How we use it.</strong> We use your information to
          respond to enquiries, keep you informed about relevant updates, and improve our
          services. We will never sell your personal data.
        </p>
        <p>
          <strong className="text-foreground">Your rights.</strong> You can unsubscribe from
          communications at any time, and request access to, correction of, or deletion of your
          data by contacting hello@lightspeed-holdings.com.
        </p>
        <p>
          <strong className="text-foreground">Cookies.</strong> We use minimal analytics to
          understand site usage. You can disable cookies in your browser at any time.
        </p>
      </div>
    </PageShell>
  )
}
