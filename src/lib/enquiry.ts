export const ENQUIRY_SLA_COPY =
  'We respond to qualified enquiries within two business days.';

export interface EnquiryFields {
  form: 'contact' | 'briefing';
  name: string;
  organization: string;
  email: string;
  enquiryType: string;
  message?: string;
  phone?: string;
  title?: string;
  timeline?: string;
}

export function newReferenceKey(): string {
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  const hex = Array.from(bytes, (byte) => byte.toString(16).padStart(2, '0')).join('');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}

export function enquiryPayload(
  fields: EnquiryFields,
  turnstileToken: string | null,
  honeypotValue = ''
): Record<string, string> {
  return {
    form: fields.form,
    name: fields.name,
    organization: fields.organization,
    email: fields.email,
    enquiryType: fields.enquiryType,
    message: fields.message ?? '',
    phone: fields.phone ?? '',
    title: fields.title ?? '',
    timeline: fields.timeline ?? '',
    hp_website: honeypotValue,
    turnstileToken: turnstileToken ?? '',
    idempotencyKey: newReferenceKey()
  };
}

export const ENQUIRY_GENERIC_ERROR =
  'We could not send that right now. Please try again.';

/**
 * The API answers with a stable error code and never with internal detail
 * (Turnstile rejection reasons name our own configuration and stay in the
 * server log). These strings turn each code into something a visitor can act
 * on, and into a signal that tells an operator which link failed.
 */
export const ENQUIRY_ERROR_COPY: Record<string, string> = {
  verification_required:
    'The security check has not finished yet. Please wait a moment and press send again.',
  verification_failed:
    'The security check was rejected. Refresh the page and try again.',
  rate_limited:
    'Too many attempts from this connection. Please try again later, or use WhatsApp.',
  validation_failed:
    'Some details are missing or invalid. Go back and check the fields marked required.',
  not_configured:
    'Our enquiry service is not available right now. Please use WhatsApp in the meantime.',
  provider_unavailable:
    'Our mail service is temporarily unavailable. Please try again, or use WhatsApp.',
};

export function enquiryErrorMessage(code?: string): string {
  if (!code) return ENQUIRY_GENERIC_ERROR;
  return ENQUIRY_ERROR_COPY[code] ?? ENQUIRY_GENERIC_ERROR;
}
