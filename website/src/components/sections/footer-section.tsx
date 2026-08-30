import Link from 'next/link'
import { Icon } from '@/components/ui/icon'
import { NewsletterForm } from '@/components/sections/newsletter-form'
import { cn } from '@/lib/utils'

interface FooterProps {
  className?: string
}

const serviceLinks = [
  { label: 'AI Strategy & Roadmap', href: '/ai-strategy-roadmap' },
  { label: 'AI Governance & Risk Management', href: '/ai-governance-risk-management' },
  { label: 'AI-Ready Data & Infrastructure', href: '/ai-ready-data-infrastructure' },
  { label: 'Custom AI Solutions & AI-Native Engineering', href: '/custom-ai-solutions' },
  { label: 'AI Operating Model Design', href: '/ai-operating-model-design' },
  { label: 'AI Agents & Automation', href: '/ai-agents-automation' },
  { label: 'Deliberate AI Toolkit', href: '/deliberate-ai-toolkit' },
]

const companyLinks = [
  { label: 'About Us', href: '/about-us' },
  { label: 'Our Approach', href: '/our-approach' },
  { label: 'Careers', href: '/careers' },
  { label: 'Customers', href: '/customers' },
  { label: 'Get In Touch', href: '/get-in-touch' },
]

const industryLinks = [
  { label: 'Financial Services', href: '/financial-services' },
  { label: 'Energy & Utilities', href: '/energy-and-utilities' },
  { label: 'Retail', href: '/retail' },
]

export const Footer = ({ className }: FooterProps) => {
  return (
    <footer className={cn('border-t border-border/60 bg-card/40 py-16', className)}>
      <div className="mx-auto max-w-7xl px-6">
        <div className="grid gap-12 lg:grid-cols-4">
          <div>
            <Link href="/" className="text-lg font-bold tracking-tight">
              LightSpeed<span className="text-primary"> Holdings</span>
            </Link>
            <p className="mt-4 text-sm leading-relaxed text-muted">
              The AI Native Transformation Consultancy. Enterprise AI, applied in production.
            </p>
            <div className="mt-6 flex gap-4 text-muted">
              <a
                href="https://www.linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="LinkedIn"
                className="transition-colors hover:text-primary"
              >
                <Icon name="linkedin" size={20} />
              </a>
              <a
                href="https://www.youtube.com"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="YouTube"
                className="transition-colors hover:text-primary"
              >
                <Icon name="youtube" size={20} />
              </a>
            </div>
          </div>

          <div>
            <h4 className="mb-4 font-semibold">Services</h4>
            <ul className="space-y-2.5 text-sm text-muted">
              {serviceLinks.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="transition-colors hover:text-foreground">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="mb-4 font-semibold">Company</h4>
            <ul className="space-y-2.5 text-sm text-muted">
              {companyLinks.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="transition-colors hover:text-foreground">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
            <h4 className="mb-4 mt-8 font-semibold">Industries</h4>
            <ul className="space-y-2.5 text-sm text-muted">
              {industryLinks.map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="transition-colors hover:text-foreground">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="mb-4 font-semibold">Stay In The Loop</h4>
            <p className="mb-4 text-sm text-muted">
              The Prompt — we&apos;ll email you with relevant information and updates.
            </p>
            <NewsletterForm />
            <div className="mt-8 space-y-3 text-sm text-muted">
              <p className="flex items-center gap-2">
                <Icon name="mail" size={16} /> hello@lightspeed-holdings.com
              </p>
              <p className="flex items-center gap-2">
                <Icon name="pin" size={16} /> London, United Kingdom
              </p>
            </div>
          </div>
        </div>

        <div className="mt-12 flex flex-col justify-between gap-4 border-t border-border/60 pt-8 text-sm text-muted md:flex-row">
          <p>© {new Date().getFullYear()} LightSpeed Holdings. All rights reserved.</p>
          <div className="flex gap-6">
            <Link href="/privacy-policy" className="transition-colors hover:text-foreground">
              Privacy Policy
            </Link>
            <Link href="/faq" className="transition-colors hover:text-foreground">
              FAQs
            </Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
