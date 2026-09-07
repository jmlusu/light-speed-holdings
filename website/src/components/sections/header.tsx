'use client'

import * as React from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { useScrolled } from '@/hooks/use-scrolled'

const navLinks = [
  { label: 'Method', href: '/method' },
  { label: 'Services', href: '/services' },
  { label: 'Industries', href: '/industries' },
  { label: 'Proof', href: '/proof' },
]

export const Header = () => {
  const [open, setOpen] = React.useState(false)
  const isScrolled = useScrolled(100)

  return (
    <header
      className={`sticky top-0 z-50 border-b border-border/60 transition-all duration-300 ${
        isScrolled ? 'bg-bg/95 backdrop-blur' : 'bg-transparent'
      }`}
    >
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-lg font-bold tracking-tight">
          LightSpeed<span className="text-primary"> Holdings</span>
        </Link>

        <div className="hidden items-center gap-7 lg:flex">
          {navLinks.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className="text-sm text-muted transition-colors hover:text-foreground"
            >
              {item.label}
            </Link>
          ))}
          <Button size="sm" href="/get-in-touch">
            Get In Touch
          </Button>
        </div>

        <button
          type="button"
          className="lg:hidden"
          aria-expanded={open}
          aria-label="Toggle navigation menu"
          onClick={() => setOpen((v) => !v)}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width={24}
            height={24}
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
            strokeLinecap="round"
          >
            {open ? <path d="M6 6l12 12M18 6L6 18" /> : <path d="M4 7h16M4 12h16M4 17h16" />}
          </svg>
        </button>
      </nav>

      {open && (
        <div className="border-t border-border/60 bg-bg lg:hidden">
          <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 py-6">
            {navLinks.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="text-muted transition-colors hover:text-foreground"
              >
                {item.label}
              </Link>
            ))}
            <Button href="/get-in-touch" onClick={() => setOpen(false)}>
              Get In Touch
            </Button>
          </div>
        </div>
      )}
    </header>
  )
}