import { get, put } from '@vercel/blob';

export const config = {
  runtime: 'edge'
};

const RESEND_API_KEY = process.env.RESEND_API_KEY;
const TURNSTILE_SECRET_KEY = process.env.TURNSTILE_SECRET_KEY;
const ENQUIRY_FROM_EMAIL = process.env.ENQUIRY_FROM_EMAIL ?? 'enquiries@lightspeedholdings.com';
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

  if (!RESEND_API_KEY || !ENQUIRY_TO_EMAIL) {
    return json({ error: { code: 'not_configured' } }, 500);
  }

  const referenceId = crypto.randomUUID();
  const sentAt = new Date().toISOString();

  const delivery = await sendEmail(fields);
  if (!delivery.ok) {
    return json({ error: { code: 'provider_unavailable' } }, 502);
  }

  const payloadRaw = JSON.stringify({
    form: fields.form ?? '',
    name: fields.name ?? '',
    email: fields.email ?? '',
    organization: fields.organization ?? '',
    enquiryType: fields.enquiryType ?? '',
    message: fields.message ?? '',
    phone: fields.phone ?? ''
  });
  const hashBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(payloadRaw));
  const payloadHash = Array.from(new Uint8Array(hashBuffer)).map((b) => b.toString(16).padStart(2, '0')).join('');

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

async function sendEmail(fields: EnquiryFields): Promise<DeliveryResult> {
  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY ?? ''}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: ENQUIRY_FROM_EMAIL,
        to: [ENQUIRY_TO_EMAIL ?? ''],
        replyTo: fields.email ?? '',
        subject: `Website enquiry (${fields.enquiryType}) — ${fields.organization}`,
        html: buildEmailHtml(fields)
      })
    });
    if (!response.ok) {
      return { ok: false };
    }
    const data = (await response.json()) as { id?: string };
    return { ok: true, id: data.id };
  } catch {
    return { ok: false };
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
