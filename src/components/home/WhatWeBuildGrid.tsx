import React from 'react';
import { Link } from 'react-router-dom';
import { SectionHeading } from '../site/SectionHeading';
import { ArrowRight } from 'lucide-react';
import { Icon3D, Icon3DName } from '../common';

interface CapabilityArea {
  id: string;
  title: string;
  problem: string;
  explanation: string;
  icon3d: Icon3DName;
  badge: string;
}

const CAPABILITIES: CapabilityArea[] = [
  {
    id: 'company-building',
    title: 'AI-Native Company Building',
    problem: 'Traditional ventures suffer from heavy overhead, slow hiring cycles, and fragmented early operations.',
    explanation: 'We design and scale new companies from the ground up where AI agents execute core workflows under human executive direction.',
    icon3d: 'home',
    badge: 'Venture Studio',
  },
  {
    id: 'workflow-automation',
    title: 'Intelligent Workflow Automation',
    problem: 'Enterprise processes get bogged down in repetitive manual handoffs and legacy spreadsheets.',
    explanation: 'We collapse multi-step processes into automated, deterministic agentic execution paths with verified SLA turnarounds.',
    icon3d: 'lightning',
    badge: 'Automation',
  },
  {
    id: 'agentic-systems',
    title: 'Agentic Systems & Orchestration',
    problem: 'Single-bot solutions fail on complex multi-role operations requiring decomposition.',
    explanation: 'We orchestrate multi-agent networks where specialized roles collaborate on shared task graphs with state lock-step.',
    icon3d: 'orchestration',
    badge: 'Orchestration',
  },
  {
    id: 'enterprise-integration',
    title: 'Enterprise AI Integration',
    problem: 'Siloed LLM prototypes cannot safely read from or write to core enterprise databases.',
    explanation: 'We embed AI capability directly into existing ERP, CRM, and internal software stacks via secure API tool sandboxes.',
    icon3d: 'network',
    badge: 'Enterprise Stack',
  },
  {
    id: 'organizational-memory',
    title: 'Organizational Memory Systems',
    problem: 'Institutional knowledge is lost when team members rotate or leave the organization.',
    explanation: 'We deploy persistent vector memory and structured knowledge stores so agents recall enterprise context automatically.',
    icon3d: 'memory',
    badge: 'Knowledge Engine',
  },
  {
    id: 'ai-governance',
    title: 'AI Governance Infrastructure',
    problem: 'Uncontrolled AI deployment exposes companies to hallucination, data leakage, and compliance risk.',
    explanation: 'We enforce 5-tier human approval matrices, risk-classified permission gates, and append-only cryptographic audit trails.',
    icon3d: 'security',
    badge: 'Governance',
  },
];

interface WhatWeBuildGridProps {
  theme?: 'light' | 'dark';
}

export const WhatWeBuildGrid: React.FC<WhatWeBuildGridProps> = ({ theme = 'dark' }) => {
  const isLight = theme === 'light';

  return (
    <section id="what-we-build" className={`py-24 px-6 lg:px-12 relative overflow-hidden transition-colors duration-300 ${
      isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-[#0A0D14] text-white'
    }`}>
      {/* Background Architectural Modular Agent Image */}
      <div className="absolute inset-0 pointer-events-none select-none overflow-hidden z-0">
        <img
          src="/assets/images/modular_agent_architecture_1793818142394.avif"
          alt="Modular Agent Architecture Visual"
          className="w-full h-full object-cover object-center transition-all duration-700 opacity-65 dark:opacity-75 filter saturate-110 brightness-100"
          loading="lazy"
        />
        {/* Clear Atmospheric Scrim Overlay for optimal contrast & typography clarity */}
        <div
          className={`absolute inset-0 transition-colors duration-500 ${
            isLight
              ? 'bg-gradient-to-b from-[#F2F2F2]/70 via-[#F2F2F2]/45 to-[#F2F2F2]/75'
              : 'bg-gradient-to-b from-[#0A0D14]/75 via-[#0A0D14]/50 to-[#0A0D14]/80'
          }`}
        />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        <SectionHeading
          theme={theme}
          eyebrow="PRACTICE AREAS"
          title="What We Build"
          lead="LightSpeed engineers production-grade AI-native capabilities. Each practice area solves a fundamental enterprise operational bottleneck."
        />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-16">
          {CAPABILITIES.map((cap) => {
            return (
              <div
                key={cap.id}
                className={`p-8 rounded-2xl border transition-all duration-300 flex flex-col justify-between text-left backdrop-blur-xl ${
                  isLight
                    ? 'bg-white/85 border-slate-200/90 shadow-lg hover:border-ls-navy/40 hover:shadow-xl'
                    : 'bg-[#0A0D14]/75 border-white/10 shadow-xl hover:border-ls-cyan/40 hover:shadow-2xl'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <span className={`text-[10px] font-mono font-bold uppercase tracking-wider px-2.5 py-1 rounded-md ${
                      isLight ? 'bg-ls-navy/10 text-ls-navy' : 'bg-ls-cyan/10 text-ls-cyan'
                    }`}>
                      {cap.badge}
                    </span>
                    <div className="flex items-center shrink-0">
                      <Icon3D name={cap.icon3d} size="md" isInteractive />
                    </div>
                  </div>

                  <h3 className={`text-xl font-bold font-display mb-3 ${isLight ? 'text-ls-navy' : 'text-white'}`}>
                    {cap.title}
                  </h3>

                  <div className={`mb-4 p-3 rounded-xl text-xs ${isLight ? 'bg-ls-red/5 text-ls-red border border-ls-red/10' : 'bg-ls-red/10 text-red-300 border border-ls-red/20'}`}>
                    <strong>Problem Addressed:</strong> {cap.problem}
                  </div>

                  <p className={`text-xs leading-relaxed ${isLight ? 'text-slate-600' : 'text-slate-300'}`}>
                    {cap.explanation}
                  </p>
                </div>

                <div className="mt-8 pt-4 border-t border-slate-200/20">
                  <Link
                    to="/what-we-do"
                    className="inline-flex items-center gap-2 text-xs font-bold font-mono text-ls-red hover:text-ls-cyan transition-colors"
                  >
                    <span>EXPLORE CAPABILITY</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default WhatWeBuildGrid;
