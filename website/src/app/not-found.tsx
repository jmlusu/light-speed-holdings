import { Button } from '@/components/ui/button'

export default function NotFound() {
  return (
    <div className="grid min-h-[60vh] place-items-center bg-background px-6 text-center">
      <div>
        <h1 className="text-6xl font-bold tracking-tight">404</h1>
        <p className="mt-4 text-lg text-muted">That page doesn&apos;t exist.</p>
        <div className="mt-8">
          <Button href="/">Back to home</Button>
        </div>
      </div>
    </div>
  )
}
