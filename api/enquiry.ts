import nodemailer from 'nodemailer';

export const config = {
  runtime: 'nodejs'
};

const SMTP_HOST = process.env.SMTP_HOST;
const SMTP_PORT = Number(process.env.SMTP_PORT ?? (Number(process.env.SMTP_SECURE) ? 465 : 587));
const SMTP_SECURE = (process.env.SMTP_SECURE ?? '').toLowerCase() === 'true';
const SMTP_USER = process.env.SMTP_USER;
const SMTP_PASS = process.env.SMTP_PASS;
const TURNSTILE_SECRET_KEY = process.env.TURNSTILE_SECRET_KEY;
const ENQUIRY_FROM_EMAIL = process.env.ENQUIRY_FROM_EMAIL ?? SMTP_USER;
const ENQUIRY_TO_EMAIL = process.env.ENQUIRY_TO_EMAIL;

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const WINDOW_MS = 12 * 60 * 60 * 1000;
const MAX_DELIVERIES_PER_IP = 5;
const EXPECTED_ACTIONS = new Set(['contact', 'briefing']);
const ALLOWED_HOSTNAMES = (process.env.TURNSTILE_HOSTNAMES ?? '')
  .split(',')
  .map((h) => h.trim())
  .filter(Boolean);

const deliveries = new Map<string, number[]>();

interface EnquiryFields {
  form?: string;
  name?: string;
  organization?: string;
  email?: string;
  enquiryType?: string;
  message?: string;
  phone?: string;
  turnstileToken?: string;
}

export async function POST(req: Request): Promise<Response> {
  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return json({ error: { code: 'invalid_json' } }, 400);
  }

  if (typeof body.hp_website === 'string' && body.hp_website.length > 0) {
    return json({ status: 'skipped' }, 200);
  }

  const fields = pickStrings(body);
  const invalid = validate(fields);
  if (invalid) {
    return json({ error: { code: 'validation_failed', fields: invalid } }, 400);
  }

  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
  if (rateLimited(ip)) {
    return json({ error: { code: 'rate_limited' } }, 429);
  }

  if (TURNSTILE_SECRET_KEY) {
    if (!fields.turnstileToken) {
      return json({ error: { code: 'verification_required' } }, 403);
    }
    const action = fields.form ?? '';
    if (!EXPECTED_ACTIONS.has(action)) {
      return json({ error: { code: 'verification_failed' } }, 403);
    }
    const verified = await verifyTurnstile(fields.turnstileToken, ip, action);
    if (!verified) {
      return json({ error: { code: 'verification_failed' } }, 403);
    }
  }

  if (!SMTP_HOST || !SMTP_USER || !SMTP_PASS || !ENQUIRY_TO_EMAIL) {
    return json({ error: { code: 'not_configured' } }, 500);
  }

  const referenceId = crypto.randomUUID();
  const sentAt = new Date().toISOString();

  const delivery = await sendEmail(fields, ENQUIRY_FROM_EMAIL ?? '', ENQUIRY_TO_EMAIL ?? '');
  if (!delivery.ok) {
    return json({ error: { code: 'provider_unavailable' } }, 502);
  }

  return json({ status: 'recorded', referenceId, sentAt }, 201);
}

function json(data: unknown, status: number): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}

function pickStrings(body: Record<string, unknown>): EnquiryFields {
  const keys = [
    'form',
    'name',
    'organization',
    'email',
    'enquiryType',
    'message',
    'phone',
    'turnstileToken'
  ] as const;
  const out: EnquiryFields = {};
  for (const key of keys) {
    const value = body[key];
    if (typeof value === 'string') {
      out[key] = value;
    }
  }
  return out;
}

function validate(fields: EnquiryFields): string[] | null {
  const errors: string[] = [];
  if (!fields.name?.trim()) errors.push('name');
  if (!fields.email?.trim() || !EMAIL_RE.test(fields.email)) errors.push('email');
  if (!fields.organization?.trim()) errors.push('organization');
  if (!fields.enquiryType?.trim()) errors.push('enquiryType');
  return errors.length ? errors : null;
}

function rateLimited(ip: string): boolean {
  const now = Date.now();
  const recent = (deliveries.get(ip) ?? []).filter((t) => now - t < WINDOW_MS);
  if (recent.length >= MAX_DELIVERIES_PER_IP) {
    return true;
  }
  recent.push(now);
  deliveries.set(ip, recent);
  return false;
}

async function verifyTurnstile(token: string, ip: string, expectedAction: string): Promise<boolean> {
  if (typeof token !== 'string' || token.length === 0 || token.length > 2048) {
    return false;
  }
  try {
    const response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ secret: TURNSTILE_SECRET_KEY ?? '', response: token, remoteip: ip })
    });
    if (!response.ok) return false;
    const data = (await response.json()) as {
      success?: boolean;
      action?: string;
      hostname?: string;
    };
    if (data.success !== true) return false;
    if (data.action !== expectedAction) return false;
    if (ALLOWED_HOSTNAMES.length > 0 && !ALLOWED_HOSTNAMES.includes(data.hostname ?? '')) return false;
    return true;
  } catch {
    return false;
  }
}

interface DeliveryResult {
  ok: boolean;
  id?: string;
}

async function sendEmail(fields: EnquiryFields, from: string, to: string): Promise<DeliveryResult> {
  const transporter = nodemailer.createTransport({
    host: SMTP_HOST,
    port: SMTP_PORT,
    secure: SMTP_SECURE,
    auth: { user: SMTP_USER ?? '', pass: SMTP_PASS ?? '' }
  });
  try {
    const info = await transporter.sendMail({
      from,
      to,
      replyTo: fields.email ?? '',
      subject: `Website enquiry (${fields.enquiryType}) — ${fields.organization}`,
      html: buildEmailHtml(fields)
    });
    return { ok: true, id: info.messageId };
  } catch {
    return { ok: false };
  } finally {
    transporter.close();
  }
}

function buildEmailHtml(fields: EnquiryFields): string {
  const escape = (value: string | undefined) =>
    (value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const rows = [
    ['Form', escape(fields.form)],
    ['Name', escape(fields.name)],
    ['Organization', escape(fields.organization)],
    ['Work email', escape(fields.email)],
    ['Enquiry type', escape(fields.enquiryType)],
    ['Phone', escape(fields.phone)],
    ['Message', escape(fields.message)]
  ];
  const body = rows
    .map(([label, value]) => `<tr><th align="left">${label}</th><td>${value}</td></tr>`)
    .join('');
  return `<table>${body}</table>`;
}
