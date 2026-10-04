/**
 * Journey instrumentation client — CUSTOMER_JOURNEY_CONVERSION_ARCHITECTURE §39/§40.
 *
 * Posts whitelisted events to `/api/journey-events` (the edge endpoint's
 * allow-lists are mirrored here so junk never consumes the IP rate budget).
 * Batched with a short timer; flushed via sendBeacon on page hide; every
 * failure path is silent — analytics must never break the journey.
 */

export const JOURNEY_EVENT_TYPES = [
  'page_view',
  'solution_view',
  'sector_view',
  'proof_view',
  'insight_view',
  'ask_started',
  'ask_completed',
  'newsletter_started',
  'newsletter_completed',
  'contact_started',
  'contact_completed',
  'cta_clicked',
] as const;
export type JourneyEventType = (typeof JOURNEY_EVENT_TYPES)[number];

export const JOURNEY_STAGES = [
  'awareness',
  'exploration',
  'consideration',
  'intent',
  'conversion',
] as const;
export type JourneyStage = (typeof JOURNEY_STAGES)[number];

export interface JourneyEvent {
  eventType: JourneyEventType;
  route: string;
  contentType?: string;
  solution?: string;
  sector?: string;
  cta?: string;
  journeyStage?: JourneyStage;
  timestamp: string;
  sessionId: string;
  metadata?: Record<string, unknown>;
}

export type JourneyEventInput = Omit<JourneyEvent, 'route' | 'timestamp' | 'sessionId'> & {
  route?: string;
};

const ENDPOINT = '/api/journey-events';
const FLUSH_INTERVAL_MS = 5000;
const FLUSH_BATCH_SIZE = 10;

const queue: JourneyEvent[] = [];
let flushTimer: ReturnType<typeof setTimeout> | null = null;
let sessionId: string | null = null;
let listenersBound = false;

function getSessionId(): string {
  if (sessionId) return sessionId;
  try {
    const stored = sessionStorage.getItem('ls_journey_session');
    if (stored) {
      sessionId = stored;
      return stored;
    }
    const fresh =
      typeof crypto !== 'undefined' && 'randomUUID' in crypto
        ? crypto.randomUUID()
        : `s-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
    sessionStorage.setItem('ls_journey_session', fresh);
    sessionId = fresh;
    return fresh;
  } catch {
    return (sessionId = 'anon');
  }
}

function flush(mode: 'timer' | 'beacon'): void {
  if (queue.length === 0) return;
  const batch = queue.splice(0, queue.length);
  if (flushTimer) {
    clearTimeout(flushTimer);
    flushTimer = null;
  }
  try {
    const payload = JSON.stringify(batch);
    if (mode === 'beacon' && typeof navigator.sendBeacon === 'function') {
      navigator.sendBeacon(ENDPOINT, new Blob([payload], { type: 'application/json' }));
      return;
    }
    void fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: payload,
      keepalive: true,
    }).catch(() => undefined);
  } catch {
    /* fail-silent: drop the batch */
  }
}

function scheduleFlush(): void {
  if (flushTimer) return;
  flushTimer = setTimeout(() => {
    flushTimer = null;
    flush('timer');
  }, FLUSH_INTERVAL_MS);
}

function bindUnloadFlush(): void {
  if (listenersBound || typeof window === 'undefined') return;
  listenersBound = true;
  window.addEventListener('pagehide', () => flush('beacon'));
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') flush('beacon');
  });
}

/** Track one event. Never throws; silently drops invalid types/stages. */
export function trackJourneyEvent(input: JourneyEventInput): void {
  if (typeof window === 'undefined') return;
  try {
    if (!JOURNEY_EVENT_TYPES.includes(input.eventType)) return;
    if (input.journeyStage && !JOURNEY_STAGES.includes(input.journeyStage)) return;
    const { route, ...rest } = input;
    queue.push({
      ...rest,
      route: route ?? window.location.pathname,
      timestamp: new Date().toISOString(),
      sessionId: getSessionId(),
    });
    if (queue.length >= FLUSH_BATCH_SIZE) flush('timer');
    else scheduleFlush();
    bindUnloadFlush();
  } catch {
    /* fail-silent */
  }
}

/** React convenience wrapper — stable `track` for effects and handlers. */
export function useJourneyEvents(): { track: typeof trackJourneyEvent } {
  return { track: trackJourneyEvent };
}

/** Journey stage implied by a route (§ the five-stage journey model). */
export function stageForRoute(pathname: string): JourneyStage {
  if (pathname === '/') return 'awareness';
  if (['/what-we-do', '/ai-company-builder', '/solutions', '/sectors', '/about'].includes(pathname)) {
    return 'exploration';
  }
  if (['/proof', '/insights', '/ask'].includes(pathname) || pathname.startsWith('/insights/')) {
    return 'consideration';
  }
  if (['/contact', '/legal/privacy', '/legal/terms'].includes(pathname)) return 'conversion';
  return 'awareness';
}
