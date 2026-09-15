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
    hp_website: honeypotValue,
    turnstileToken: turnstileToken ?? '',
    idempotencyKey: newReferenceKey()
  };
}

export const ENQUIRY_GENERIC_ERROR =
  'We could not send that right now. Please try again.';
