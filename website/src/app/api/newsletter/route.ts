import { NextResponse } from 'next/server'

export const runtime = 'nodejs'

export async function POST(request: Request) {
  try {
    const { email } = (await request.json()) as { email?: string }

    if (!email || typeof email !== 'string' || !email.includes('@')) {
      return NextResponse.json({ error: 'A valid email address is required.' }, { status: 400 })
    }

    // Foundation hook: connect to Mailchimp/SendGrid/Supabase here.
    // For now, confirm receipt so the form flow works end-to-end.
    return NextResponse.json({
      ok: true,
      message: "You're subscribed — thanks!",
      email: email.toLowerCase().trim(),
    })
  } catch {
    return NextResponse.json({ error: 'Invalid request.' }, { status: 400 })
  }
}
