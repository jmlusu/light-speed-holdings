export const config = {
  runtime: 'edge'
};

export default function handler(): Response {
  return new Response('edge-ok', {
    status: 200,
    headers: { 'Content-Type': 'text/plain' }
  });
}
