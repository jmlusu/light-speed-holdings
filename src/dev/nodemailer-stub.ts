// Dev-only stand-in for nodemailer. vite.config.ts aliases `nodemailer` to this
// module in serve mode, so a local form submission runs the real handler
// (validation, rate limit, Turnstile siteverify) but records the message
// instead of opening an SMTP connection. Nothing here reaches the browser
// bundle: the alias only exists while serving, and no app module imports it.
//
// Lives under src/ rather than scripts/ because the alias target must survive
// .vercelignore (scripts/ is stripped from the upload, and the deploy guard
// treats every vite alias target as a build input).
import { appendFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const outDir = join(tmpdir(), 'lightspeed-dev-mail');
const outFile = join(outDir, 'messages.jsonl');

console.log('[dev-mail] nodemailer stub loaded (no SMTP connections will be made)');

export interface DevMailRecord {
  at: string;
  from: string;
  to: string;
  replyTo?: string;
  subject: string;
  html: string;
}

export function createTransport(): {
  sendMail: (message: {
    from?: string;
    to?: string;
    replyTo?: string;
    subject?: string;
    html?: string;
  }) => Promise<{ messageId: string }>;
  close: () => void;
} {
  return {
    async sendMail(message) {
      const record: DevMailRecord = {
        at: new Date().toISOString(),
        from: message.from ?? '',
        to: message.to ?? '',
        replyTo: message.replyTo,
        subject: message.subject ?? '',
        html: message.html ?? '',
      };
      mkdirSync(outDir, { recursive: true });
      appendFileSync(outFile, `${JSON.stringify(record)}\n`, 'utf8');
      console.log(`[dev-mail] recorded (not sent) -> ${outFile}`);
      return { messageId: `dev-${Date.now()}@localhost` };
    },
    close() {
      /* no socket to close */
    },
  };
}

export default { createTransport };
