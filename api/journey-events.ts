export const config = {
  runtime: 'edge'
};

const WINDOW_MS = 60 * 60 * 1000; // 1 hour
const MAX_EVENTS_PER_IP = 200;

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

  // Store in buffer (in production, this would go to a proper analytics store)
  const sessionKey = ip; // In production, use sessionId if available
  const existing = eventsBuffer.get(sessionKey) ?? [];
  eventsBuffer.set(sessionKey, [...existing, ...validatedEvents].slice(-1000)); // Keep last 1000 per session
  
  // Log for debugging (in production, send to analytics pipeline)
  console.log('[journey-events]', JSON.stringify({
    count: validatedEvents.length,
    ip,
    eventTypes: validatedEvents.map(e => e.eventType),
    routes: [...new Set(validatedEvents.map(e => e.route))]
  }));

  return json({ 
    status: 'recorded', 
    count: validatedEvents.length,
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