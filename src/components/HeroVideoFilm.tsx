import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  Maximize2,
  Sparkles,
  Radio,
  ShieldCheck,
  Cpu,
  Compass,
  Layers,
  Server,
  Terminal,
  Activity,
  ArrowRight
} from 'lucide-react';
import {
  StatusLedPip
} from './TactileHardwareElements';

interface HeroVideoFilmProps {
  theme?: 'light' | 'dark';
  onNavigate: (route: string) => void;
  onOpenContactModal: (intent?: string) => void;
}

export const HeroVideoFilm: React.FC<HeroVideoFilmProps> = ({
  theme = 'dark',
  onNavigate,
  onOpenContactModal
}) => {
  const isLight = theme === 'light';
  const [isPlaying, setIsPlaying] = useState(true);
  const [activeChapter, setActiveChapter] = useState<number>(0);
  const [progress, setProgress] = useState<number>(0);
  const [activeMode, setActiveMode] = useState<'cinematic' | 'telemetry' | 'datacenter'>('cinematic');
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const chapters = [
    {
      id: 0,
      title: '01. The Sovereign Imperative',
      subtitle: 'Escaping Extractive Cloud Dependency',
      timestamp: '00:00 - 00:15',
      caption: 'Why African institutions must own their foundational models, data sovereignty, and compute infrastructure rather than rent foreign chat wrappers.',
      badge: 'MALAWIAN SOVEREIGNTY',
      accent: '#f59e0b'
    },
    {
      id: 1,
      title: '02. The Pharos Doctrine',
      subtitle: 'Mathematical Rigor & Fiduciary Guidance',
      timestamp: '00:15 - 00:30',
      caption: 'Ancient African lighthouse engineering reimagined for modern algorithmic governance, steering boards safely through AI adoption.',
      badge: 'PHAROS BEACON',
      accent: '#d97706'
    },
    {
      id: 2,
      title: '03. Autonomous Swarm Fleet',
      subtitle: 'OpenCode-Native Agent Hierarchies',
      timestamp: '00:30 - 00:45',
      caption: 'Executives and specialists collaborating in real-time with Tier-1 to Tier-5 cryptographic Human-in-the-Loop approval gates.',
      badge: 'MULTI-AGENT SWARMS',
      accent: '#10b981'
    },
    {
      id: 3,
      title: '04. Real-World Economic Impact',
      subtitle: 'Sub-30s Mobile Money & Chichewa NLP',
      timestamp: '00:45 - 01:00',
      caption: 'Instantaneous financial transaction processing over Airtel/TNM and native indigenous language processing anchored in regional law.',
      badge: 'INSTITUTIONAL EXECUTION',
      accent: '#3b82f6'
    }
  ];
  useEffect(() => {
    if (!isPlaying) return;
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          setActiveChapter((c) => (c + 1) % chapters.length);
          return 0;
        }
        return prev + 1.25;
      });
    }, 100);
    return () => clearInterval(interval);
  }, [isPlaying, chapters.length]);

  // Ambient particle grid animation on canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = canvas.offsetWidth);
    let height = (canvas.height = canvas.offsetHeight);

    const particles: Array<{
      x: number;
      y: number;
      vx: number;
      vy: number;
      size: number;
      alpha: number;
      pulse: number;
    }> = [];

    for (let i = 0; i < 45; i++) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.6,
        vy: (Math.random() - 0.5) * 0.6,
        size: Math.random() * 2 + 1,
        alpha: Math.random() * 0.6 + 0.2,
        pulse: Math.random() * Math.PI * 2
      });
    }

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Draw subtle rotating Pharos Beacon light sweep across video stage
      const time = Date.now() * 0.0008;
      const originX = width * 0.5;
      const originY = height * 0.2;
      const sweepAngle = time % (Math.PI * 2);

      const grad = ctx.createRadialGradient(originX, originY, 10, originX, originY, width * 0.8);
      grad.addColorStop(0, isLight ? 'rgba(245, 158, 11, 0.18)' : 'rgba(251, 191, 36, 0.25)');
      grad.addColorStop(0.5, isLight ? 'rgba(245, 158, 11, 0.04)' : 'rgba(245, 158, 11, 0.08)');
      grad.addColorStop(1, 'transparent');

      ctx.save();
      ctx.beginPath();
      ctx.moveTo(originX, originY);
      ctx.arc(originX, originY, width, sweepAngle - 0.25, sweepAngle + 0.25);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();
      ctx.restore();

      // Draw subtle connective neural lines
      for (let i = 0; i < particles.length; i++) {
        const p1 = particles[i];
        p1.x += p1.vx;
        p1.y += p1.vy;
        p1.pulse += 0.02;

        if (p1.x < 0) p1.x = width;
        if (p1.x > width) p1.x = 0;
        if (p1.y < 0) p1.y = height;
        if (p1.y > height) p1.y = 0;

        for (let j = i + 1; j < particles.length; j++) {
          const p2 = particles[j];
          const dx = p1.x - p2.x;
          const dy = p1.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 110) {
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            const lineAlpha = (1 - dist / 110) * 0.15;
            ctx.strokeStyle = isLight
              ? `rgba(217, 119, 6, ${lineAlpha})`
              : `rgba(245, 158, 11, ${lineAlpha})`;
            ctx.lineWidth = 0.8;
            ctx.stroke();
          }
        }

        // Draw particle dot
        ctx.beginPath();
        const currentAlpha = p1.alpha * (0.6 + 0.4 * Math.sin(p1.pulse));
        ctx.arc(p1.x, p1.y, p1.size, 0, Math.PI * 2);
        ctx.fillStyle = isLight
          ? `rgba(217, 119, 6, ${currentAlpha})`
          : `rgba(251, 191, 36, ${currentAlpha})`;
        ctx.fill();
      }

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = canvas.offsetWidth;
      height = canvas.height = canvas.offsetHeight;
    };

    window.addEventListener('resize', handleResize);
    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
    };
  }, [isLight]);

  const currentChapterData = chapters[activeChapter];

  return (
    <div className={`rounded-3xl relative overflow-hidden transition-all text-left p-4 sm:p-7 ${
      isLight ? 'neu-card-light' : 'neu-card-dark'
    }`}>
      {/* Header bar of cinematic theater */}
      <div className={`relative z-10 flex flex-wrap items-center justify-between gap-3 pb-4 mb-5 border-b ${
        isLight ? 'border-slate-300/60' : 'border-slate-800/80'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-xl flex items-center justify-center shrink-0 ${
            isLight ? 'neu-inset-light text-amber-600' : 'neu-inset-dark text-amber-400'
          }`}>
            <Radio className="w-4 h-4 animate-pulse text-amber-500" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <StatusLedPip status="emerald" isLight={isLight} />
              <span className="text-[10px] sm:text-[11px] font-mono font-bold tracking-widest text-amber-500 uppercase">
                HERO CINEMATIC HOOK // WELCOMING FILM
              </span>
            </div>
            <p className={`text-xs font-mono ${isLight ? 'text-slate-600' : 'text-zinc-400'}`}>
              The Sovereign AI Narrative: From Lilongwe to the Continent
            </p>
          </div>
        </div>

        {/* Mode Switcher Buttons */}
        <div className="flex items-center gap-2">
          <div className={`flex items-center p-1 rounded-xl ${
            isLight ? 'neu-inset-light' : 'neu-inset-dark'
          }`}>
            <button
              onClick={() => setActiveMode('cinematic')}
              className={`px-3 py-1 rounded-lg text-[10px] font-mono font-bold uppercase transition-all cursor-pointer ${
                activeMode === 'cinematic'
                  ? (isLight ? 'bg-white text-amber-700 shadow-sm' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              Film View
            </button>
            <button
              onClick={() => setActiveMode('telemetry')}
              className={`px-3 py-1 rounded-lg text-[10px] font-mono font-bold uppercase transition-all cursor-pointer ${
                activeMode === 'telemetry'
                  ? (isLight ? 'bg-white text-amber-700 shadow-sm' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              Telemetry HUD
            </button>
            <button
              onClick={() => setActiveMode('datacenter')}
              className={`px-3 py-1 rounded-lg text-[10px] font-mono font-bold uppercase transition-all cursor-pointer ${
                activeMode === 'datacenter'
                  ? (isLight ? 'bg-white text-amber-700 shadow-sm' : 'bg-amber-500/20 text-amber-400 border border-amber-500/30')
                  : (isLight ? 'text-slate-600 hover:text-slate-900' : 'text-zinc-400 hover:text-white')
              }`}
            >
              Racks
            </button>
          </div>
        </div>
      </div>

      {/* Main Video/Film Viewport Display Container */}
      <div className={`relative rounded-2xl overflow-hidden aspect-video max-h-[480px] w-full mb-5 shadow-2xl flex flex-col justify-between ${
        isLight ? 'border border-slate-300/80 bg-slate-950' : 'border border-amber-500/20 bg-[#050811]'
      }`}>
        {/* Dynamic Procedural Simulation Backdrop */}
        <div className="absolute inset-0 overflow-hidden">
          <div
            className="absolute inset-0 transition-opacity duration-1000"
            style={{
              background: activeMode === 'datacenter'
                ? 'radial-gradient(circle at 50% 40%, #0f172a 0%, #020617 80%)'
                : activeMode === 'telemetry'
                  ? 'radial-gradient(circle at 60% 30%, #172554 0%, #020617 85%)'
                  : 'radial-gradient(circle at 50% 20%, #291804 0%, #050811 85%)'
            }}
          />
          {/* Subtle Cybernetic Grid Mesh */}
          <div
            className="absolute inset-0 opacity-20 pointer-events-none"
            style={{
              backgroundImage: 'linear-gradient(rgba(245, 158, 11, 0.2) 1px, transparent 1px), linear-gradient(90deg, rgba(245, 158, 11, 0.2) 1px, transparent 1px)',
              backgroundSize: '40px 40px'
            }}
          />
        </div>

        {/* Ambient Overlay Gradients */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/60 to-slate-950/30 z-0" />
        <div className="absolute inset-0 bg-amber-500/5 mix-blend-overlay z-0" />

        {/* Canvas Neural Particle Stream */}
        <canvas
          ref={canvasRef}
          className="absolute inset-0 w-full h-full pointer-events-none z-10 opacity-75"
        />

        {/* Top HUD Overlay Inside Video */}
        <div className="relative z-20 p-4 sm:p-6 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full text-[10px] font-mono font-bold bg-amber-500 text-slate-950 shadow-md">
              {currentChapterData.badge}
            </span>
            <span className="px-2.5 py-1 rounded-full text-[10px] font-mono bg-black/60 text-white/90 backdrop-blur-md border border-white/10 hidden sm:inline">
              4K CINEMATIC // SOVEREIGN ENGINE
            </span>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5 px-3 py-1 rounded-full text-[10px] font-mono bg-black/60 text-amber-400 backdrop-blur-md border border-amber-500/30">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping inline-block mr-1" />
              <span>LIVE TRANSMISSION</span>
            </div>
          </div>
        </div>

        {/* Central Overlay Cinematic Caption */}
        <div className="relative z-20 p-4 sm:p-8 max-w-2xl space-y-2 text-left">
          <div className="text-amber-400 font-mono text-xs uppercase font-bold tracking-wider">
            {currentChapterData.title} • {currentChapterData.subtitle}
          </div>
          <h2 className="text-xl sm:text-2xl md:text-3xl font-extrabold font-display text-white tracking-tight leading-tight">
            &ldquo;{currentChapterData.caption}&rdquo;
          </h2>
        </div>

        {/* Bottom Playback & Chapter Progress Bar */}
        <div className="relative z-20 p-4 sm:p-6 bg-gradient-to-t from-black via-black/80 to-transparent">
          {/* Progress bar line */}
          <div className="w-full bg-white/20 h-1.5 rounded-full overflow-hidden mb-3 relative">
            <div
              className="bg-amber-400 h-full rounded-full transition-all duration-100"
              style={{ width: `${progress}%` }}
            />
          </div>

          {/* Interactive Player Controls */}
          <div className="flex items-center justify-between gap-3 text-white">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="p-2.5 rounded-full bg-amber-500 hover:bg-amber-400 text-slate-950 transition-all active:scale-95 shadow-lg shadow-amber-500/30 cursor-pointer"
                title={isPlaying ? 'Pause Film' : 'Play Film'}
              >
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 fill-current ml-0.5" />}
              </button>

              <div className="text-xs font-mono text-white/80 hidden sm:block">
                <span>{currentChapterData.timestamp}</span>
              </div>
            </div>

            {/* Quick Action Button inside Video Screen */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => onOpenContactModal('Request Executive Film & Sovereign AI Deck')}
                className="px-4 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 backdrop-blur-md border border-white/20 text-xs font-mono font-bold text-white transition-all hover:border-amber-400 flex items-center gap-1.5 cursor-pointer"
              >
                <span>Request Full Deck</span>
                <ArrowRight className="w-3.5 h-3.5 text-amber-400" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* 4 Interactive Chapter Selector Tabs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {chapters.map((ch, idx) => {
          const isSelected = activeChapter === idx;
          return (
            <button
              key={ch.id}
              onClick={() => {
                setActiveChapter(idx);
                setProgress(0);
              }}
              className={`p-3.5 rounded-2xl text-left transition-all cursor-pointer flex flex-col justify-between relative ${
                isSelected
                  ? (isLight ? 'neu-pressed-light border-amber-500/40' : 'neu-pressed-dark border-amber-500/40')
                  : (isLight ? 'neu-convex-light hover:shadow-md' : 'neu-convex-dark hover:shadow-lg')
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <span className={`text-[10px] font-mono font-bold tracking-wider uppercase ${
                    isSelected ? 'text-amber-500' : (isLight ? 'text-slate-500' : 'text-zinc-500')
                  }`}>
                    CHAPTER [ 0{idx + 1} ]
                  </span>
                  {isSelected && (
                    <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
                  )}
                </div>
                <div className={`text-xs font-bold font-display line-clamp-1 ${
                  isSelected ? 'text-amber-600 dark:text-amber-400' : (isLight ? 'text-slate-900' : 'text-zinc-200')
                }`}>
                  {ch.title.split('. ')[1]}
                </div>
                <p className={`text-[11px] leading-snug line-clamp-2 mt-1 ${
                  isLight ? 'text-slate-600' : 'text-zinc-400'
                }`}>
                  {ch.subtitle}
                </p>
              </div>

              {isSelected && (
                <div className="w-full bg-amber-500/20 h-1 rounded-full overflow-hidden mt-2">
                  <div
                    className="bg-amber-500 h-full rounded-full transition-all duration-100"
                    style={{ width: `${progress}%` }}
                  />
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};
