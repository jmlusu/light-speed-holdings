export const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export function requiredError(value: string, label: string): string {
  return value.trim() ? '' : `${label} is required.`;
}

export function emailError(value: string): string {
  const email = value.trim();
  if (!email) return '';
  return EMAIL_RE.test(email) ? '' : 'Enter a valid email address.';
}
