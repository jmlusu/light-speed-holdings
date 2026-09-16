export const config = {
  runtime: 'nodejs'
};

export default function handler(): Response {
  return new Response('pong', {
    status: 200,
    headers: { 'Content-Type': 'text/plain' }
  });
}
