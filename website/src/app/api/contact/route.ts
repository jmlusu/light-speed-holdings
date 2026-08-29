import { NextResponse } from 'next/server'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as Record<string, unknown>

    const name = typeof body.name === 'string' ? body.name.trim() : ''
    const email = typeof body.email === 'string' ? body.email.trim() : ''
    const company = typeof body.company === 'string' ? body.company.trim() : ''
    const message = typeof body.message === 'string' ? body.message.trim() : ''

    if (!name || !email || !email.includes('@')) {
      return NextResponse.json(
        { error: 'Name and a valid email address are required.' },
        { status: 400 },
      )
    }
    if (!message) {
      return NextResponse.json({ error: 'Please include a short message.' }, { status: 400 })
    }

    // Foundation hook: forward to CRM/email (HubSpot, SendGrid, Supabase) here.
    return NextResponse.json({
      ok: true,
      message: "Thanks — we'll get back to you shortly.",
      received: { name, email, company, message },
    })
  } catch {
    return NextResponse.json({ error: 'Invalid request.' }, { status: 400 })
  }
}
