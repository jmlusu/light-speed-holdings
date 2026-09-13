import React, { useState } from 'react';
import { 
  BookOpen, 
  Sparkles, 
  ShieldCheck, 
  Compass, 
  Landmark, 
  Cpu, 
  CheckCircle2, 
  ArrowRight, 
  Users, 
  MapPin, 
  Globe, 
  Award,
  Layers,
  HeartHandshake
} from 'lucide-react';
import { 
  StatusLedPip 
} from './TactileHardwareElements';

interface OurStoryOriginProps {
  theme?: 'light' | 'dark';
  onNavigate: (route: string) => void;
  onOpenContactModal: (intent?: string) => void;
}

export const OurStoryOrigin: React.FC<OurStoryOriginProps> = ({
  theme = 'dark',
  onNavigate,
  onOpenContactModal
}) => {
  const isLight = theme === 'light';
  const [activeStoryTab, setActiveStoryTab] = useState<'origin' | 'people' | 'values'>('origin');

  const coreValues = [
    {
      title: 'Technological Sovereignty',
      tagline: 'African Soil, African Law',
      description: 'We believe that the computing foundations of African commerce, governance, and finance must reside under local sovereign control—never vulnerable to foreign cloud sanctions or data extraction.',
      icon: ShieldCheck,
      color: 'amber'
    },
    {
      title: 'Fiduciary Mathematical Rigor',
      tagline: 'Auditability Over AI Hype',
      description: 'We construct deterministic, verifiable systems. Every agent task is cryptographically hashed, audited, and bound to real-world SLAs, ensuring zero unverified hallucinations.',
      icon: Landmark,
      color: 'cyan'
    },
    {
      title: 'Human-in-the-Loop Supremacy',
      tagline: 'Governed Autonomy',
      description: 'Artificial intelligence must serve human directors, ministries, and citizens. Our Tier-1 to Tier-5 cryptographic approval gates guarantee human veto authority on all high-stakes decisions.',
      icon: HeartHandshake,
      color: 'emerald'
    },
    {
      title: 'Indigenous Economic Grounding',
      tagline: 'Sub-30s Mobile Money & Chichewa NLP',
      description: 'True utility requires speaking the languages of our people (Chichewa, Tumbuka, Swahili) and settling across local financial rails (Airtel, TNM Mpamba, SADC RTGS).',
      icon: Cpu,
      color: 'purple'
    }
  ];

  const leadershipTeam = [
    {
      name: 'Jack Mlusu',
      role: 'Founder & Chief Executive Officer',
      location: 'Lilongwe, Malawi',
      bio: 'Visionary technologist and institutional architect driving sovereign AI infrastructure and mathematical agent hierarchies across the SADC region.',
      initials: 'JM',
      fingerprint: '0x9E7A...4F82',
      badge: 'Executive Command'
    },
    {
      name: 'Dr. Chifundo Banda',
      role: 'Chief AI Architect & Head of Research',
      location: 'Lilongwe Command Hub',
      bio: 'Pioneering mathematical multi-agent swarms, low-latency indigenous tokenizer development, and formal verification frameworks.',
      initials: 'CB',
      fingerprint: '0x3D11...B92C',
      badge: 'Engineering & R&D'
    },
    {
      name: 'SADC Sovereign Systems Group',
      role: 'Core Systems Engineering & Security Operations',
      location: 'Regional Datacenters (Lilongwe, Blantyre, Lusaka)',
      bio: '24/7 sovereign telemetry engineers, site reliability specialists, and cryptographic audit officers maintaining 99.98% uptime.',
      initials: 'SSG',
      fingerprint: '0xFA49...11DE',
      badge: 'SecOps & Reliability'
    }
  ];

  return (
    <div className={`rounded-3xl relative overflow-hidden transition-all text-left p-6 sm:p-10 ${
      isLight ? 'neu-card-light' : 'neu-card-dark'
    }`}>
      {/* Top Header Strip */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-2xl flex items-center justify-center shrink-0 ${
            isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
          }`}>
            <BookOpen className="w-5 h-5 text-amber-500" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <StatusLedPip status="emerald" isLight={isLight} />
              <span className="text-[11px] font-mono font-bold tracking-widest text-amber-500 uppercase">
                OUR ORIGIN // THE SOVEREIGN FOUNDATION STORY
              </span>
            </div>
            <span className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              Why We Started • The People Behind LightSpeed • Driving Values
            </span>
          </div>
        </div>

        {/* Tab Controls */}
        <div className="flex items-center gap-2">
          <div className={`flex items-center p-1 rounded-2xl ${
            isLight ? 'neu-inset-light' : 'neu-inset-dark'
          }`}>
            <button
              onClick={() => setActiveStoryTab('origin')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeStoryTab === 'origin'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              The Genesis
            </button>
            <button
              onClick={() => setActiveStoryTab('people')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeStoryTab === 'people'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              The Team &amp; Hubs
            </button>
            <button
              onClick={() => setActiveStoryTab('values')}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-bold transition-all cursor-pointer ${
                activeStoryTab === 'values'
                  ? (isLight ? 'neu-convex-light text-amber-700 shadow-sm' : 'neu-convex-dark text-amber-400')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              Guiding Values
            </button>
          </div>
        </div>
      </div>

      {/* Main Narrative Introduction */}
      <div className="relative z-10 max-w-4xl space-y-4 mb-10">
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-mono font-semibold ${
          isLight ? 'neu-pill-light text-amber-700' : 'neu-pill-dark text-amber-400'
        }`}>
          <Sparkles className="w-3.5 h-3.5 text-amber-500" />
          <span>Born in Lilongwe • Engineered for Africa</span>
        </div>

        <h2 className={`text-2xl sm:text-4xl lg:text-5xl font-extrabold font-display tracking-tight leading-tight ${
          isLight ? 'text-slate-900' : 'text-zinc-50'
        }`}>
          Building Africa&apos;s Sovereign Compute Engine—<span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-500 via-amber-400 to-amber-600">The Story of LightSpeed</span>
        </h2>

        <p className={`text-sm sm:text-base md:text-lg leading-relaxed font-sans ${
          isLight ? 'text-slate-700' : 'text-zinc-300'
        }`}>
          LightSpeed Holdings Limited was founded on a simple, non-negotiable principle: <strong className="text-amber-500 font-semibold">Africa cannot be a mere consumer of foreign algorithms.</strong> We construct the foundational infrastructure, agent swarms, and mathematical guardrails that allow African institutions to operate with absolute autonomy, high velocity, and zero data leakage.
        </p>
      </div>

      {/* Tab Content: Origin Story */}
      {activeStoryTab === 'origin' && (
        <div className="space-y-8 relative z-10 mb-10">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Left Narrative Text */}
            <div className="lg:col-span-7 space-y-4">
              <h3 className={`text-xl sm:text-2xl font-bold font-display ${
                isLight ? 'text-slate-900' : 'text-zinc-100'
              }`}>
                From Ephemeral AI Wrappers to Sovereign Institutional Infrastructure
              </h3>
              
              <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                In 2024, as the world was inundated by generic ChatGPT wrappers and foreign SaaS tools that charged high monthly fees while sending sensitive African state and corporate data to foreign datacenters, founder <strong>Jack Mlusu</strong> recognized a dangerous structural vulnerability.
              </p>

              <p className={`text-xs sm:text-sm leading-relaxed ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
                If African banks, utility providers, revenue authorities, and enterprises depended entirely on offshore APIs, our continental economy would remain perpetually beholden to foreign tech giants. LightSpeed Holdings was established in Lilongwe to reverse this paradigm: architecting self-hosted, OpenCode-native autonomous agent hierarchies and sovereign edge datacenters right here in Malawi and SADC.
              </p>

              <div className={`p-4 rounded-2xl flex items-center gap-3 border ${
                isLight ? 'bg-amber-500/5 border-amber-300 text-slate-800' : 'bg-amber-500/5 border-amber-500/20 text-zinc-200'
              }`}>
                <MapPin className="w-5 h-5 text-amber-500 shrink-0" />
                <div className="text-xs font-mono">
                  <span className="font-bold text-amber-500">HEADQUARTERS &amp; COMMAND:</span> Lilongwe HQ (13.9899° S, 33.7741° E) • Regional SADC Nodes in Blantyre, Lusaka, and Harare.
                </div>
              </div>
            </div>

            {/* Right Authentic Photography Card */}
            <div className={`lg:col-span-5 rounded-2xl overflow-hidden shadow-xl border ${
              isLight ? 'neu-convex-light border-slate-300' : 'neu-convex-dark border-amber-500/30'
            }`}>
              <div className="relative aspect-[4/3] overflow-hidden">
                <img 
                  src="/src/assets/images/lilongwe_command_center_1789250979827.jpg" 
                  alt="Lilongwe Sovereign Command Operations Center"
                  className="w-full h-full object-cover transform hover:scale-105 transition-transform duration-500"
                  referrerPolicy="no-referrer"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
                <div className="absolute bottom-3 left-3 right-3 text-white">
                  <span className="px-2.5 py-0.5 rounded-full text-[9px] font-mono font-bold bg-amber-500 text-slate-950 uppercase">
                    AUTHENTIC COMMAND FACILITY
                  </span>
                  <div className="text-xs font-bold font-display mt-1">
                    Lilongwe Sovereign AI Operations Command Hub
                  </div>
                </div>
              </div>
              <div className="p-4 text-xs font-mono text-zinc-400 space-y-1">
                <div className="flex justify-between">
                  <span className="text-amber-500">TELEMETRY:</span>
                  <span>48 Sovereign Agent Clusters Active</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-amber-500">LATENCY:</span>
                  <span>&lt;18ms Regional SADC Backbone</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab Content: People & Leadership */}
      {activeStoryTab === 'people' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 relative z-10 mb-10">
          {leadershipTeam.map((leader, idx) => (
            <div 
              key={idx}
              className={`rounded-2xl overflow-hidden transition-all flex flex-col justify-between ${
                isLight ? 'neu-convex-light' : 'neu-convex-dark'
              }`}
            >
              <div>
                <div className="relative aspect-[16/10] overflow-hidden bg-gradient-to-br from-slate-900 via-slate-950 to-amber-950/40 p-6 flex flex-col justify-between border-b border-amber-500/20">
                  <div className="flex items-center justify-between">
                    <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/40 flex items-center justify-center font-mono font-black text-lg text-amber-400 shadow-inner">
                      {leader.initials}
                    </div>
                    <span className="px-2.5 py-1 rounded-full text-[9px] font-mono font-bold bg-black/70 text-amber-400 backdrop-blur-md border border-amber-500/30">
                      {leader.badge}
                    </span>
                  </div>
                  <div>
                    <div className="text-[10px] font-mono text-zinc-400 flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block animate-pulse" />
                      <span>KEY: {leader.fingerprint}</span>
                    </div>
                  </div>
                </div>

                <div className="p-5 space-y-2">
                  <div className="flex items-center gap-1.5 text-[10px] font-mono text-amber-500 font-semibold">
                    <MapPin className="w-3 h-3" />
                    <span>{leader.location}</span>
                  </div>
                  <h3 className={`text-base font-bold font-display ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {leader.name}
                  </h3>
                  <div className="text-xs font-mono text-amber-600 dark:text-amber-400 font-medium">
                    {leader.role}
                  </div>
                  <p className={`text-xs leading-relaxed ${
                    isLight ? 'text-slate-600' : 'text-zinc-400'
                  }`}>
                    {leader.bio}
                  </p>
                </div>
              </div>

              <div className={`p-4 pt-3 border-t flex items-center justify-between text-xs font-mono ${
                isLight ? 'border-slate-300/60 text-slate-500' : 'border-slate-800/80 text-zinc-400'
              }`}>
                <span>Fiduciary Operator</span>
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Tab Content: Driving Core Values */}
      {activeStoryTab === 'values' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 relative z-10 mb-10">
          {coreValues.map((val, idx) => {
            const IconComp = val.icon;
            return (
              <div 
                key={idx}
                className={`p-6 rounded-2xl transition-all flex flex-col justify-between ${
                  isLight ? 'neu-convex-light' : 'neu-convex-dark'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <div className={`p-3 rounded-xl flex items-center justify-center ${
                      isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
                    }`}>
                      <IconComp className="w-5 h-5 text-amber-500" />
                    </div>
                    <span className="text-[10px] font-mono font-bold uppercase px-3 py-1 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20">
                      VALUE [ 0{idx + 1} ]
                    </span>
                  </div>

                  <h3 className={`text-base sm:text-lg font-bold font-display ${
                    isLight ? 'text-slate-900' : 'text-zinc-100'
                  }`}>
                    {val.title}
                  </h3>
                  <div className="text-xs font-mono font-semibold text-amber-600 dark:text-amber-400 mb-2">
                    {val.tagline}
                  </div>
                  <p className={`text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-slate-600' : 'text-zinc-400'
                  }`}>
                    {val.description}
                  </p>
                </div>

                <div className="pt-4 mt-4 border-t border-zinc-500/15 flex items-center justify-between text-[11px] font-mono text-emerald-500">
                  <span>Non-Negotiable Mandate</span>
                  <CheckCircle2 className="w-4 h-4" />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Action Buttons */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-4 pt-5 border-t ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={() => onOpenContactModal('Consult with Founder & Executive Team')}
            className="neu-btn-amber px-6 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 cursor-pointer"
          >
            <span>Engage Executive Leadership</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => onNavigate('about')}
            className={`px-5 py-3.5 rounded-2xl font-bold font-mono text-xs uppercase tracking-wider flex items-center gap-2 cursor-pointer ${
              isLight ? 'neu-btn-light text-slate-900' : 'neu-btn-dark text-zinc-200'
            }`}
          >
            <Users className="w-4 h-4 text-amber-500" />
            <span>Read Institutional Charter</span>
          </button>
        </div>

        <button
          onClick={() => onNavigate('pharos')}
          className="text-xs font-mono font-bold text-amber-500 hover:text-amber-400 transition-colors py-2 px-3 flex items-center gap-1.5 cursor-pointer"
        >
          <span>Explore The Pharos Treatises</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
};
