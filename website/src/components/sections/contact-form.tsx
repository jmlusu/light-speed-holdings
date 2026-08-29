'use client'

import * as React from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { InputLabel } from '@/components/ui/input-label'
import { Textarea } from '@/components/ui/textarea'

export const ContactForm = () => {
  const [status, setStatus] = React.useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [message, setMessage] = React.useState('')

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const data = new FormData(event.currentTarget)
    const payload = {
      name: String(data.get('name') ?? ''),
      email: String(data.get('email') ?? ''),
      company: String(data.get('company') ?? ''),
      message: String(data.get('message') ?? ''),
    }

    setStatus('loading')
    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      const body = await res.json()
      if (!res.ok) {
        setStatus('error')
        setMessage(body.error ?? 'Something went wrong. Please try again.')
        return
      }
      setStatus('success')
      setMessage(body.message ?? "Thanks — we'll get back to you shortly.")
    } catch {
      setStatus('error')
      setMessage('Something went wrong. Please try again.')
    }
  }

  if (status === 'success') {
    return (
      <div className="rounded-md border border-primary/40 bg-primary/10 p-8 text-center">
        <p className="text-lg font-semibold text-primary" role="status">
          {message}
        </p>
      </div>
    )
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-6" noValidate>
      <div className="grid gap-6 sm:grid-cols-2">
        <div>
          <InputLabel htmlFor="contact-name">Name</InputLabel>
          <Input id="contact-name" name="name" autoComplete="name" required />
        </div>
        <div>
          <InputLabel htmlFor="contact-email">Email</InputLabel>
          <Input
            id="contact-email"
            name="email"
            type="email"
            autoComplete="email"
            required
          />
        </div>
      </div>
      <div>
        <InputLabel htmlFor="contact-company">Company</InputLabel>
        <Input id="contact-company" name="company" autoComplete="organization" />
      </div>
      <div>
        <InputLabel htmlFor="contact-message">Message</InputLabel>
        <Textarea id="contact-message" name="message" rows={5} required />
      </div>
      {status === 'error' ? (
        <p className="text-sm text-accent" role="alert">
          {message}
        </p>
      ) : null}
      <div>
        <Button type="submit" size="lg" disabled={status === 'loading'}>
          {status === 'loading' ? 'Sending…' : 'Send Message'}
        </Button>
      </div>
    </form>
  )
}
