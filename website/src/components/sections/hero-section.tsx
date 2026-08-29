import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

interface HeroProps {
  className?: string
}

export const Hero = ({ className }: HeroProps) => {
  return (
    <section className={cn('relative overflow-hidden bg-background', className)}>
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0"
        style={{
          background:
            'radial-gradient(60rem 40rem at 80% -10%, rgba(77,124,255,0.18), transparent 60%), radial-gradient(50rem 30rem at -10% 110%, rgba(255,107,107,0.12), transparent 60%)',
        }}
      />
      <div className="relative mx-auto max-w-7xl px-6 py-24 md:py-32">
        <div className="max-w-2xl">
          <p className="mb-6 text-sm font-medium uppercase tracking-widest text-muted">
            LightSpeed Holdings · In Production
          </p>
          <h1 className="text-4xl font-bold leading-tight tracking-tight md:text-6xl">
            Enterprise AI, Applied in Production.
          </h1>
          <p className="mt-6 text-lg text-muted md:text-xl">
            AI transformation, delivered for global enterprises. From strategy to deployment, we
            build it with you.
          </p>
          <div className="mt-10 flex flex-col gap-4 sm:flex-row">
            <Button size="lg" href="/get-in-touch">
              Ask what we can build for you
            </Button>
            <Button size="lg" variant="ghost" href="/our-approach">
              How we work
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}
