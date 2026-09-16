import { get, put } from '@vercel/blob';
import { createHash } from 'node:crypto';
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
const AUDIT_PATH = 'audit/enquiry.jsonl';
const IDEM_PATH = (key: string) => `audit/idem/${key}.json`;

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const WINDOW_MS = 12 * 60 * 60 * 1000;
const MAX_DELIVERIES_PER_IP = 5;

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
  idempotencyKey?: string;
}

export default async function handler(req: Request): Promise<Response> {
  if (req.method !== 'POST') {
    return json({ error: { code: 'method_not_allowed' } }, 405);
  }

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
    const verified = await verifyTurnstile(fields.turnstileToken, ip);
    if (!verified) {
      return json({ error: { code: 'verification_failed' } }, 403);
    }
  }

  if (fields.idempotencyKey) {
    const existing = await readIdem(fields.idempotencyKey);
    if (existing) {
      return json({ error: { code: 'duplicate', referenceId: existing.referenceId } }, 409);
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

  const payloadHash = createHash('sha256')
    .update(
      JSON.stringify({
        form: fields.form ?? '',
        name: fields.name ?? '',
        email: fields.email ?? '',
        organization: fields.organization ?? '',
        enquiryType: fields.enquiryType ?? '',
        message: fields.message ?? '',
        phone: fields.phone ?? ''
      })
    )
    .digest('hex');

  try {
    await appendLine(
      AUDIT_PATH,
      JSON.stringify({
        referenceId,
        sentAt,
        payloadHash,
        form: fields.form ?? 'contact',
        providerId: delivery.id ?? null,
        status: 'sent'
      })
    );
  } catch {
    return json({ error: { code: 'audit_failed' } }, 502);
  }

  if (fields.idempotencyKey) {
    await writeIdem(fields.idempotencyKey, { referenceId, sentAt });
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
    'turnstileToken',
    'idempotencyKey'
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

async function verifyTurnstile(token: string, ip: string): Promise<boolean> {
  try {
    const response = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ secret: TURNSTILE_SECRET_KEY ?? '', response: token, remoteip: ip })
    });
    const data = (await response.json()) as { success?: boolean };
    return data.success === true;
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

async function appendLine(path: string, line: string): Promise<void> {
  let existing = '';
  try {
    const blobObject = await get(path, { access: 'private', useCache: false });
    if (blobObject?.statusCode === 200) {
      existing = await new Response(blobObject.stream).text();
    }
  } catch {
    // first write
  }
  await put(path, `${existing}${line}\n`, {
    access: 'private',
    addRandomSuffix: false,
    allowOverwrite: true
  });
}

interface IdemRecord {
  referenceId: string;
  sentAt: string;
}

async function readIdem(key: string): Promise<IdemRecord | null> {
  try {
    const blobObject = await get(IDEM_PATH(key), { access: 'private', useCache: false });
    if (!blobObject || blobObject.statusCode !== 200) return null;
    return JSON.parse(await new Response(blobObject.stream).text()) as IdemRecord;
  } catch {
    return null;
  }
}

async function writeIdem(key: string, record: IdemRecord): Promise<void> {
  await put(IDEM_PATH(key), JSON.stringify(record), {
    access: 'private',
    addRandomSuffix: false,
    allowOverwrite: true
  });
}
