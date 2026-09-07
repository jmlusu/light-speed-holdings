import './globals.css'
import type { Metadata } from 'next'
import { Inter, Sora } from 'next/font/google'
import { Header } from '@/components/sections/header'
import { Footer } from '@/components/sections/footer-section'

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

const sora = Sora({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-sora',
  weight: ['400', '600', '700'],
})

export const metadata: Metadata = {
  title: {
    default: 'LightSpeed Holdings — The AI-Native Company Builder for Southern Africa',
    template: '%s | LightSpeed Holdings',
  },
  description:
    'We architect sovereign, governed AI systems that run offline-first and comply from day one. Agentic AI company building, brand systems, WhatsApp assistants, and NGO M&E — piloted in Malawi, architected for SADC.',
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${sora.variable}`}>
      <body className="min-h-screen bg-bg text-text">
        <a href="#main-content" className="skip-link">
          Skip to main content
        </a>
        <Header />
        <main id="main-content">{children}</main>
        <Footer />
      </body>
    </html>
  )
}
