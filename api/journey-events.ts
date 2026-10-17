export const config = {
  runtime: 'edge'
};

const WINDOW_MS = 60 * 60 * 1000; // 1 hour
const MAX_EVENTS_PER_IP = 200;

// Optional durable-store forward target (CEO dashboard ingest endpoint).
// When set, validated events are best-effort POSTed to the dashboard's
// FileStore-backed JourneyEventStore. Falls back to the in-memory buffer
// when unset or when the dashboard is unreachable.
const DASHBOARD_INGEST_URL = process.env.DASHBOARD_INGEST_URL ?? '';
const DASHBOARD_INGEST_TIMEOUT_MS = 2000;
// Optional shared-secret header for the dashboard ingest endpoint.
const DASHBOARD_INGEST_KEY = process.env.DASHBOARD_INGEST_KEY ?? '';

interface JourneyEvent {
  eventType: string;
  route: string;
  contentType?: string;
  solution?: string;
  sector?: string;
  cta?: string;
  journeyStage?: string;
  timestamp: string;
  sessionId?: string;
  metadata?: Record<string, unknown>;
}

const eventsBuffer = new Map<string, JourneyEvent[]>();
const ipRateLimit = new Map<string, number[]>();

function json(data: unknown, status: number): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' }
  });
}

function rateLimited(ip: string): boolean {
  const now = Date.now();
  const recent = (ipRateLimit.get(ip) ?? []).filter((t) => now - t < WINDOW_MS);
  if (recent.length >= MAX_EVENTS_PER_IP) {
    return true;
  }
  recent.push(now);
  ipRateLimit.set(ip, recent);
  return false;
}

function validateEvent(body: unknown): JourneyEvent | null {
  if (!body || typeof body !== 'object') return null;

  const event = body as Record<string, unknown>;

  // Required fields
  if (typeof event.eventType !== 'string' || !event.eventType.trim()) return null;
  if (typeof event.route !== 'string' || !event.route.trim()) return null;
  if (typeof event.timestamp !== 'string' || !event.timestamp.trim()) return null;

  // Validate eventType against allowed list
  const allowedEventTypes = [
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
    'cta_clicked'
  ];

  if (!allowedEventTypes.includes(event.eventType)) return null;

  // Validate journeyStage if present
  const allowedJourneyStages = [
    'awareness',
    'exploration',
    'consideration',
    'intent',
    'conversion'
  ];

  if (event.journeyStage && typeof event.journeyStage === 'string' && !allowedJourneyStages.includes(event.journeyStage)) {
    return null;
  }

  return {
    eventType: event.eventType,
    route: event.route,
    contentType: typeof event.contentType === 'string' ? event.contentType : undefined,
    solution: typeof event.solution === 'string' ? event.solution : undefined,
    sector: typeof event.sector === 'string' ? event.sector : undefined,
    cta: typeof event.cta === 'string' ? event.cta : undefined,
    journeyStage: typeof event.journeyStage === 'string' ? event.journeyStage : undefined,
    timestamp: event.timestamp,
    sessionId: typeof event.sessionId === 'string' ? event.sessionId : undefined,
    metadata: typeof event.metadata === 'object' && event.metadata !== null ? event.metadata as Record<string, unknown> : undefined
  };
}

// Best-effort forward of validated events to the durable dashboard store.
// Failures are non-fatal: the in-memory buffer still receives the events.
async function forwardToDashboard(events: JourneyEvent[]): Promise<boolean> {
  if (!DASHBOARD_INGEST_URL) return false;
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), DASHBOARD_INGEST_TIMEOUT_MS);
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (DASHBOARD_INGEST_KEY) {
      headers['X-API-Key'] = DASHBOARD_INGEST_KEY;
    }
    const resp = await fetch(DASHBOARD_INGEST_URL, {
      method: 'POST',
      headers,
      body: JSON.stringify(events),
      signal: controller.signal
    });
    clearTimeout(timer);
    return resp.ok;
  } catch {
    return false;
  }
}

export default async function handler(req: Request): Promise<Response> {
  if (req.method !== 'POST') {
    return json({ error: { code: 'method_not_allowed' } }, 405);
  }

  const ip = req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';

  if (rateLimited(ip)) {
    return json({ error: { code: 'rate_limited' } }, 429);
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return json({ error: { code: 'invalid_json' } }, 400);
  }

  // Support batch events
  const events = Array.isArray(body) ? body : [body];
  const validatedEvents: JourneyEvent[] = [];

  for (const event of events) {
    const validated = validateEvent(event);
    if (validated) {
      validatedEvents.push(validated);
    }
  }

  if (validatedEvents.length === 0) {
    return json({ error: { code: 'no_valid_events' } }, 400);
  }

  // Durable store: best-effort POST to CEO dashboard ingest endpoint.
  const durable = await forwardToDashboard(validatedEvents);

  // In-memory buffer as fallback / debugging aid (lost on cold start).
  const sessionKey = ip;
  const existing = eventsBuffer.get(sessionKey) ?? [];
  eventsBuffer.set(sessionKey, [...existing, ...validatedEvents].slice(-1000));

  // data_quality: none until the durable path is confirmed by a live ingest.
  console.log('[journey-events]', JSON.stringify({
    count: validatedEvents.length,
    ip,
    durable,
    dataQuality: durable ? 'file' : 'none',
    eventTypes: validatedEvents.map(e => e.eventType),
    routes: [...new Set(validatedEvents.map(e => e.route))]
  }));

  return json({
    status: 'recorded',
    count: validatedEvents.length,
    durable,
    dataQuality: durable ? 'file' : 'none',
    receivedAt: new Date().toISOString()
  }, 201);
}

// Helper to get events for debugging/admin (not for production use)
export async function getEvents(sessionKey?: string): Promise<JourneyEvent[]> {
  if (sessionKey) {
    return eventsBuffer.get(sessionKey) ?? [];
  }
  const all: JourneyEvent[] = [];
  for (const events of eventsBuffer.values()) {
    all.push(...events);
  }
  return all;
}
