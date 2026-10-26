import { describe, it, expect } from 'vitest';
import { ENQUIRY_ERROR_COPY, ENQUIRY_GENERIC_ERROR, enquiryErrorMessage } from '../lib/enquiry';

/**
 * The API answers with a stable code and keeps the Turnstile rejection reason
 * in the server log. These tests pin the visitor-facing half of that contract:
 * every code the handler can return has copy a visitor can act on, and no
 * internal reason leaks into it.
 */

/** Codes api/enquiry.ts can return to the browser. */
const HANDLER_CODES = [
  'validation_failed',
  'rate_limited',
  'verification_required',
  'verification_failed',
  'not_configured',
  'provider_unavailable',
] as const;

describe('enquiryErrorMessage', () => {
  it('has actionable copy for every code the handler returns', () => {
    for (const code of HANDLER_CODES) {
      expect(ENQUIRY_ERROR_COPY[code], `missing copy for ${code}`).toBeTruthy();
    }
  });

  it('returns the mapped copy for a known code', () => {
    expect(enquiryErrorMessage('verification_failed')).toBe(
      ENQUIRY_ERROR_COPY.verification_failed,
    );
  });

  it('falls back to the generic message for unknown or missing codes', () => {
    expect(enquiryErrorMessage('invalid_json')).toBe(ENQUIRY_GENERIC_ERROR);
    expect(enquiryErrorMessage('something_new')).toBe(ENQUIRY_GENERIC_ERROR);
    expect(enquiryErrorMessage(undefined)).toBe(ENQUIRY_GENERIC_ERROR);
  });

  it('never exposes the Turnstile rejection reason', () => {
    for (const [code, message] of Object.entries(ENQUIRY_ERROR_COPY)) {
      expect(message, `copy for ${code} leaks internals`).not.toMatch(
        /invalid-input|verify_failed|turnstile|secret/i,
      );
    }
  });
});
