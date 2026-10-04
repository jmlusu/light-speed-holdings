export const config = {
  runtime: 'nodejs'
};

export function GET(): Response {
  return new Response('pong', {
    status: 200,
    headers: { 'Content-Type': 'text/plain' }
  });
}
