"use client";

import dynamic from "next/dynamic";

const LightSpeedCore = dynamic(() => import("@/components/three/LightSpeedCore"), {
  ssr: false,
  loading: () => <div className="fixed inset-0 bg-zinc-950" />,
});

export default function Home() {
  return (
    <main className="relative min-h-[300vh] text-zinc-100 font-sans selection:bg-zinc-100 selection:text-zinc-950">
      {/* Fixed 3D Cinematic Canvas in Background */}
      <LightSpeedCore />

      {/* Fixed Glass Floating Navigation Pill */}
      <header className="fixed top-6 inset-x-0 z-50 flex justify-center px-4">
        <nav className="flex items-center gap-8 px-8 py-3 rounded-2xl bg-zinc-900/40 backdrop-blur-xl border border-zinc-700/40 shadow-2xl text-xs font-medium text-zinc-300">
          <span className="text-white font-bold tracking-widest uppercase">LIGHTSPEED</span>
          <a href="#hero" className="hover:text-white transition-colors">Overview</a>
          <a href="#features" className="hover:text-white transition-colors">Architecture</a>
          <a href="#contact" className="hover:text-white transition-colors font-mono text-[11px] text-zinc-400">+265 999 000 000</a>
        </nav>
      </header>

      {/* Large Backdrop Typography */}
      <div className="fixed top-1/4 left-1/2 -translate-x-1/2 -z-10 pointer-events-none select-none">
        <h1 className="text-[12vw] font-black uppercase text-zinc-800/20 tracking-tighter leading-none text-center">
          GLASSMORPHISM
        </h1>
      </div>

      {/* Section 1: Hero Viewport */}
      <section id="hero" className="min-h-screen flex flex-col justify-end p-8 lg:p-16 max-w-7xl mx-auto">
        <div className="max-w-2xl space-y-6 mb-12">
          <span className="text-xs font-mono uppercase tracking-[0.3em] text-zinc-400">
            [01] CINEMATIC EXECUTION
          </span>
          <h2 className="text-5xl lg:text-7xl font-light tracking-tight text-white leading-tight">
            Glassmorphism <br />
            <span className="font-bold text-zinc-400">In Motion.</span>
          </h2>
          <p className="text-sm lg:text-base text-zinc-400 font-light leading-relaxed">
            Scroll down to trigger real-time 3D camera vector displacement, geometry morphing, and interactive depth rendering.
          </p>
        </div>
      </section>

      {/* Section 2: Glassmorphism Cards Grid */}
      <section id="features" className="min-h-screen flex items-center justify-center p-6 lg:p-12 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">

          {/* Card 1 */}
          <div className="relative p-8 rounded-3xl bg-zinc-900/40 backdrop-blur-xl border border-zinc-700/50 shadow-2xl flex flex-col justify-between min-h-[320px] group hover:border-zinc-500 transition-all">
            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-white tracking-wide">Glass<br />Morphism</h3>
              <p className="text-xs text-zinc-400 font-light leading-relaxed">
                High-contrast dark frosted glass elements engineered with dynamic blur backdrops and chamfered edges.
              </p>
            </div>
            <div className="flex justify-between items-end pt-8 border-t border-zinc-800/80">
              <span className="text-2xl font-bold text-white">01</span>
              <span className="text-[11px] font-mono text-zinc-400">Phone No.<br /><strong className="text-zinc-200">+0976335-743</strong></span>
            </div>
          </div>

          {/* Card 2 */}
          <div className="relative p-8 rounded-3xl bg-zinc-900/40 backdrop-blur-xl border border-zinc-700/50 shadow-2xl flex flex-col justify-between min-h-[320px] group hover:border-zinc-500 transition-all">
            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-white tracking-wide">Glass<br />Morphism</h3>
              <p className="text-xs text-zinc-400 font-light leading-relaxed">
                Seamless scroll-driven camera translation passing through three-dimensional space with real-time vector math.
              </p>
            </div>
            <div className="flex justify-between items-end pt-8 border-t border-zinc-800/80">
              <span className="text-2xl font-bold text-white">02</span>
              <span className="text-[11px] font-mono text-zinc-400">Phone No.<br /><strong className="text-zinc-200">+0976335-743</strong></span>
            </div>
          </div>

          {/* Card 3 */}
          <div className="relative p-8 rounded-3xl bg-zinc-900/40 backdrop-blur-xl border border-zinc-700/50 shadow-2xl flex flex-col justify-between min-h-[320px] group hover:border-zinc-500 transition-all">
            <div className="space-y-4">
              <h3 className="text-2xl font-bold text-white tracking-wide">Glass<br />Morphism</h3>
              <p className="text-xs text-zinc-400 font-light leading-relaxed">
                Multi-agent enterprise workflows and local AI inference frameworks built for clean execution.
              </p>
            </div>
            <div className="flex justify-between items-end pt-8 border-t border-zinc-800/80">
              <span className="text-2xl font-bold text-white">03</span>
              <span className="text-[11px] font-mono text-zinc-400">Phone No.<br /><strong className="text-zinc-200">+0976335-743</strong></span>
            </div>
          </div>

        </div>
      </section>
    </main>
  );
}
