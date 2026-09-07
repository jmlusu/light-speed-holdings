'use client'

import { Button } from '@/components/ui/button'
import { Icon } from '@/components/ui/icon'
import { cn } from '@/lib/utils'
import * as React from 'react'

interface HeroProps {
  className?: string
}

const nodes = [
  { id: 'malawi', label: 'Malawi', x: 35, y: 55, type: 'geo' },
  { id: 'zambia', label: 'Zambia', x: 20, y: 40, type: 'geo' },
  { id: 'zimbabwe', label: 'Zimbabwe', x: 50, y: 30, type: 'geo' },
  { id: 'sa', label: 'South Africa', x: 65, y: 65, type: 'geo' },
  { id: 'gov', label: 'Government', x: 25, y: 70, type: 'inst' },
  { id: 'enterprise', label: 'Enterprise', x: 55, y: 85, type: 'inst' },
  { id: 'donor', label: 'Donors', x: 80, y: 45, type: 'inst' },
  { id: 'sme', label: 'SMEs', x: 75, y: 80, type: 'inst' },
]

const arcs = [
  { from: 'malawi', to: 'gov', governed: true },
  { from: 'malawi', to: 'zambia', governed: true },
  { from: 'zambia', to: 'zimbabwe', governed: false },
  { from: 'zimbabwe', to: 'sa', governed: true },
  { from: 'gov', to: 'enterprise', governed: true },
  { from: 'donor', to: 'sme', governed: false },
  { from: 'enterprise', to: 'sme', governed: true },
]

export const Hero = ({ className }: HeroProps) => {
  return (
    <section className={cn('relative overflow-hidden bg-bg', className)}>
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 animate-constellation"
        style={{
          background:
            'radial-gradient(60rem 40rem at 80% -10%, rgba(77,124,255,0.12), transparent 60%), radial-gradient(50rem 30rem at -10% 110%, rgba(255,107,107,0.08), transparent 60%)',
        }}
      />
      
      {/* Constellation motif */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0"
        style={{ opacity: 0.6 }}
      >
        <svg viewBox="0 0 100 100" className="w-full h-full" preserveAspectRatio="none">
          <defs>
            <linearGradient id="governedArc" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#35D6A5" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#4D7CFF" stopOpacity="0.4" />
            </linearGradient>
            <linearGradient id="activeArc" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#4D7CFF" stopOpacity="0.4" />
              <stop offset="100%" stopColor="#FF6B6B" stopOpacity="0.2" />
            </linearGradient>
          </defs>
          
          {/* Arcs */}
          {arcs.map((arc, i) => {
            const from = nodes.find(n => n.id === arc.from)!
            const to = nodes.find(n => n.id === arc.to)!
            const cx = (from.x + to.x) / 2
            const cy = (from.y + to.y) / 2
            const dx = to.x - from.x
            const dy = to.y - from.y
            const dist = Math.sqrt(dx * dx + dy * dy)
            const angle = Math.atan2(dy, dx)
            const cpX = cx - dist * 0.3 * Math.sin(angle)
            const cpY = cy + dist * 0.3 * Math.cos(angle)
            
            return (
              <path
                key={i}
                d={`M${from.x} ${from.y} Q${cpX} ${cpY} ${to.x} ${to.y}`}
                stroke={arc.governed ? 'url(#governedArc)' : 'url(#activeArc)'}
                strokeWidth={arc.governed ? 1.5 : 1}
                fill="none"
                strokeDasharray={arc.governed ? '0' : '4,4'}
                strokeLinecap="round"
                className="transition-opacity duration-300"
              />
            )
          })}
          
          {/* Nodes */}
          {nodes.map((node) => (
            <g key={node.id}>
              <circle
                cx={node.x}
                cy={node.y}
                r={node.type === 'geo' ? 3.5 : 2.5}
                fill={node.type === 'geo' ? '#4D7CFF' : '#FF6B6B'}
                className="transition-all duration-300"
              />
              <text
                x={node.x}
                y={node.y - 6}
                textAnchor="middle"
                fontSize="4"
                fill="#E8EAF2"
                fontFamily="system-ui, sans-serif"
                opacity="0.7"
                className="pointer-events-none"
              >
                {node.label}
              </text>
            </g>
          ))}
          
          {/* HITL center ring */}
          <circle
            cx={50}
            cy={50}
            r={12}
            stroke="#35D6A5"
            strokeWidth={1.5}
            fill="none"
            strokeDasharray="8,4"
            className="animate-hitl-pulse"
            opacity="0.5"
          />
          <circle
            cx={50}
            cy={50}
            r={8}
            stroke="#35D6A5"
            strokeWidth={1}
            fill="none"
            className="animate-hitl-pulse"
            style={{ animationDelay: '0.5s' }}
            opacity="0.3"
          />
        </svg>
      </div>

      <div className="relative mx-auto max-w-7xl px-6 py-24 md:py-32">
        <div className="max-w-2xl hero-cascade">
          <p className="text-sm font-medium uppercase tracking-widest text-muted">
            LightSpeed Holdings · Lilongwe, Malawi
          </p>
          <h1 className="font-display text-4xl font-bold leading-tight tracking-tight md:text-6xl lg:text-7xl">
            The AI-native company builder for Southern Africa.
          </h1>
          <p className="mt-6 text-lg text-muted md:text-xl max-w-xl">
            We architect sovereign, governed AI systems that run offline-first and comply from day one.
            From agentic orchestration platforms to mobile-first field systems — piloted in Malawi,
            architected for SADC.
          </p>
          <div className="mt-10 flex flex-col gap-4 sm:flex-row">
            <Button size="lg" href="/get-in-touch">
              Book a Discovery Call <Icon name="arrow" size={18} className="arrow-slide" />
            </Button>
            <Button size="lg" variant="ghost" href="/method">
              See How We Build <Icon name="arrow" size={18} className="arrow-slide" />
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}