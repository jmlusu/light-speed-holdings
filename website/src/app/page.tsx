import { Hero } from '@/components/sections/hero-section'
import { ServicesSection } from '@/components/sections/services-section'
import { IndustriesSection } from '@/components/sections/industries-section'
import { CtasSection } from '@/components/sections/ctas-section'
import { InsightsSection } from '@/components/sections/insights-section'
import { services, industries, partners, caseStudies, insights } from '@/data/homepage-data'

export default function HomePage() {
  return (
    <>
      <Hero />
      <ServicesSection services={services} />
      <IndustriesSection industries={industries} />
      <CtasSection partners={partners} caseStudies={caseStudies} />
      <InsightsSection insights={insights} />
    </>
  )
}
