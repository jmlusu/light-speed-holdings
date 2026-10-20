import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Brain, ShieldCheck, TrendingUp } from 'lucide-react';
import { HAOMTGV_LAYERS } from './layers';

const CYAN = '#22D3EE';
const RED = '#FF2D55';

const SLAB_STEP = 105;
const PARALLELOGRAM = 'polygon(12% 0%, 100% 0%, 88% 100%, 0% 100%)';

const FEATURES = [
  { Icon: Brain, label: 'Human authority' },
  { Icon: ShieldCheck, label: 'Governance woven in' },
  { Icon: TrendingUp, label: 'Measured value' },
];

export interface HaomtgvBlueprintHeroProps {
  backgroundImage?: string;
}

/**
 * HAOMTGV hero, built from brand/H.A.O.M.T.G.V. CSS Blueprint.md.
 * Blueprint palette values are intentionally local: they differ from the
 * brand tokens (navy #070A40 / cyan #00BFFF / red #E63946).
 */
export const HaomtgvBlueprintHero: React.FC<HaomtgvBlueprintHeroProps> = ({
  backgroundImage,
}) => {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const [imageFailed, setImageFailed] = useState(false);
  const showImage = Boolean(backgroundImage) && !imageFailed;

  return (
    <section className="ls-hero-motion relative overflow-hidden border-b border-white/10 bg-[#050B1A] text-slate-100 lg:flex lg:min-h-screen lg:items-center">
      {/* Background: gradient stand-in, scrims, and an optional swappable photo */}
      <div aria-hidden="true" className="pointer-events-none absolute inset-0 z-0">
        <div
          className="absolute inset-0"
          style={{
            background:
              'radial-gradient(ellipse 120% 90% at 70% 15%, #16234A 0%, #0A1330 42%, #050B1A 100%)',
          }}
        />
        {showImage ? (
          <img
            src={backgroundImage}
            alt=""
            onError={() => setImageFailed(true)}
            className="absolute inset-0 h-full w-full object-cover"
          />
        ) : null}
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(to left, rgba(5,11,26,0.88) 0%, rgba(5,11,26,0.55) 45%, rgba(5,11,26,0) 75%)',
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(to bottom, rgba(5,11,26,0.7) 0%, rgba(5,11,26,0) 25%)',
          }}
        />
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(to right, rgba(5,11,26,0.65) 0%, rgba(5,11,26,0) 55%)',
          }}
        />
      </div>

      <div className="relative z-20 mx-auto w-full max-w-7xl px-6 py-16 sm:px-10 lg:px-16 lg:py-12">
        <div className="relative grid gap-x-8 gap-y-12 lg:grid-cols-[1.1fr_0.8fr_1.1fr] lg:items-center">
          {/* Connectors: slab stack → layer badges (desktop only) */}
          <div aria-hidden="true" className="pointer-events-none absolute inset-0 hidden lg:block">
            {HAOMTGV_LAYERS.map((layer, i) => {
              const isGov = layer.letter === 'G';
              return (
                <span
                  key={layer.id}
                  className="absolute h-px w-10"
                  style={{
                    top: i * SLAB_STEP + 24,
                    left: 'calc(50% + 150px)',
                    backgroundColor: isGov
                      ? 'rgba(255,45,85,0.6)'
                      : 'rgba(34,211,238,0.6)',
                    transformOrigin: 'left',
                    animation: 'ls-hero-draw 0.5s ease-out backwards',
                    animationDelay: `${i * 80 + 300}ms`,
                  }}
                >
                  <span
                    className="absolute right-0 top-1/2 h-1.5 w-1.5 -translate-y-1/2 rounded-full"
                    style={{
                      backgroundColor: isGov ? RED : CYAN,
                      boxShadow: `0 0 8px ${isGov ? 'rgba(255,45,85,0.8)' : 'rgba(34,211,238,0.8)'}`,
                    }}
                  />
                </span>
              );
            })}
          </div>

          {/* Left: headline */}
          <div className="max-w-xl">
            <p
              className="text-sm tracking-[0.3em] text-slate-300"
              style={{ animation: 'ls-hero-slide 0.6s ease-out backwards' }}
            >
              OPERATING FRAMEWORK
            </p>
            <h1
              id="haomtgv-title"
              className="mt-4 font-display text-5xl font-extrabold tracking-tight sm:text-6xl lg:text-6xl xl:text-7xl"
              style={{
                animation: 'ls-hero-drop-text 0.7s ease-out backwards',
                animationDelay: '60ms',
              }}
            >
              H.A.O.M.T.G.V.
            </h1>
            <p
              className="mt-4 text-2xl font-bold sm:text-3xl lg:text-4xl"
              style={{
                color: CYAN,
                textShadow: '0 0 24px rgba(34,211,238,0.35)',
                animation: 'ls-hero-slide 0.7s ease-out backwards',
                animationDelay: '120ms',
              }}
            >
              Human at the Core.
            </p>
            <p
              className="mt-6 max-w-md text-base text-slate-300 lg:text-lg"
              style={{
                animation: 'ls-hero-slide 0.7s ease-out backwards',
                animationDelay: '180ms',
              }}
            >
              A control model for agentic companies:{' '}
              <strong className="font-semibold text-white">
                human authority runs through every layer
              </strong>
              , governance is woven in, and value is the only score that counts.
            </p>

            <ul
              className="mt-10 flex flex-wrap gap-8"
              style={{
                animation: 'ls-hero-slide 0.7s ease-out backwards',
                animationDelay: '240ms',
              }}
            >
              {FEATURES.map(({ Icon, label }, i) => (
                <li
                  key={label}
                  className={`flex items-center gap-3 ${
                    i > 0 ? 'border-l border-white/20 pl-8' : ''
                  }`}
                >
                  <Icon
                    aria-hidden="true"
                    className="h-5 w-5"
                    style={{ color: CYAN, filter: 'drop-shadow(0 0 6px rgba(34,211,238,0.8))' }}
                  />
                  <span className="text-sm text-slate-200">{label}</span>
                </li>
              ))}
            </ul>

            <Link
              to="/ai-company-builder/#governance"
              className="mt-10 inline-flex items-center gap-2 rounded-full bg-[#FF2D55] px-6 py-3 text-sm font-bold tracking-wide text-white transition-all hover:brightness-110 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-cyan-300"
              style={{
                animation: 'ls-hero-slide 0.7s ease-out backwards',
                animationDelay: '300ms',
              }}
            >
              Explore the Framework
              <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
          </div>

          {/* Center: the slab stack */}
          <div className="relative flex justify-center">
            <div className="relative mx-auto aspect-video w-full max-w-[560px] overflow-hidden lg:aspect-auto lg:h-[720px] lg:max-w-none">
              <div className="absolute inset-0 origin-center scale-[0.26] sm:scale-[0.4] md:scale-[0.42] lg:scale-100">
                <div
                  aria-hidden="true"
                  className="absolute left-1/2 top-1/2 h-[520px] w-[380px] -translate-x-1/2 -translate-y-1/2 rounded-full blur-3xl"
                  style={{
                    background:
                      'radial-gradient(ellipse at center, rgba(34,211,238,0.25), transparent 70%)',
                    animation: 'ls-hero-float 9s ease-in-out infinite',
                  }}
                />
                <div
                  aria-hidden="true"
                  className="absolute left-1/2 top-[88%] h-[120px] w-[320px] -translate-x-1/2 rounded-full blur-2xl"
                  style={{
                    background:
                      'radial-gradient(ellipse at center, rgba(255,45,85,0.45), transparent 70%)',
                    animation: 'ls-hero-breathe 4s ease-in-out infinite',
                  }}
                />

                {/* Vertical beam */}
                <div
                  aria-hidden="true"
                  className="absolute left-1/2 top-0 h-full w-[2px] -translate-x-1/2 bg-gradient-to-b from-[#22D3EE] to-transparent blur-[1px]"
                  style={{ animation: 'ls-hero-breathe 3s ease-in-out infinite' }}
                />

                {HAOMTGV_LAYERS.map((layer, i) => {
                  const isGov = layer.letter === 'G';
                  const isActive = activeIndex === i;
                  const glowColor = isGov
                    ? 'rgba(255,45,85,0.6)'
                    : 'rgba(34,211,238,0.55)';
                  return (
                    <div
                      key={layer.id}
                      className="absolute left-1/2 -ml-[150px] w-[300px]"
                      style={{ top: i * SLAB_STEP, perspective: 1200 }}
                    >
                      <div
                        className="relative h-24 transition-[transform,opacity] duration-300 ease-out"
                        style={{
                          transformStyle: 'preserve-3d',
                          transform: isActive
                            ? 'rotateX(62deg) translateY(-10px) scale(1.03)'
                            : 'rotateX(62deg)',
                          opacity: activeIndex !== null && !isActive ? 0.7 : 1,
                          animation: 'ls-hero-drop 0.6s cubic-bezier(0.2,0.8,0.2,1) backwards',
                          animationDelay: `${i * 80}ms`,
                          zIndex: isActive ? 40 : undefined,
                        }}
                      >
                        {/* Slab face */}
                        <div
                          className="absolute inset-0"
                          style={{
                            clipPath: PARALLELOGRAM,
                            background: isGov
                              ? 'linear-gradient(135deg, rgba(255,120,140,0.42), rgba(190,18,60,0.34))'
                              : 'linear-gradient(135deg, rgba(103,232,249,0.35), rgba(37,99,235,0.28))',
                            backdropFilter: 'blur(12px)',
                            WebkitBackdropFilter: 'blur(12px)',
                            boxShadow: isGov
                              ? 'inset 0 0 0 1px rgba(255,150,170,0.7), inset 0 0 20px rgba(255,120,140,0.3)'
                              : 'inset 0 0 0 1px rgba(125,211,252,0.6), inset 0 0 20px rgba(125,211,252,0.3)',
                            filter: `drop-shadow(0 0 ${isActive ? 26 : 18}px ${glowColor})`,
                            transition: 'filter 300ms ease-out',
                          }}
                        >
                          <div
                            aria-hidden="true"
                            className="absolute inset-0"
                            style={{
                              background:
                                'linear-gradient(115deg, transparent 35%, rgba(255,255,255,0.18) 50%, transparent 65%)',
                            }}
                          />
                        </div>

                        {/* Slab thickness */}
                        <div
                          aria-hidden="true"
                          className="absolute inset-x-0 top-full h-[14px]"
                          style={{
                            transform: 'rotateX(-90deg)',
                            transformOrigin: 'top',
                            background: isGov
                              ? 'linear-gradient(to bottom, rgba(190,18,60,0.85), rgba(60,8,26,0.9))'
                              : 'linear-gradient(to bottom, rgba(37,99,235,0.7), rgba(8,30,90,0.9))',
                            clipPath: PARALLELOGRAM,
                          }}
                        />

                        {/* Upright content, counter-rotated against the slab tilt */}
                        <div
                          className="absolute inset-0 flex items-center"
                          style={{ transform: 'rotateX(-62deg)' }}
                        >
                          <span
                            className="ml-4 text-3xl font-bold"
                            style={{
                              color: isGov ? '#FFB3C1' : '#A5F3FC',
                              textShadow: isGov
                                ? '0 0 12px rgba(255,45,85,0.8)'
                                : '0 0 12px rgba(34,211,238,0.8)',
                            }}
                          >
                            {layer.letter}
                          </span>
                          <layer.Icon
                            aria-hidden="true"
                            className="ml-auto mr-6 h-6 w-6"
                            style={{
                              color: isGov ? RED : CYAN,
                              filter: `drop-shadow(0 0 6px ${isGov ? 'rgba(255,45,85,0.8)' : 'rgba(34,211,238,0.8)'})`,
                            }}
                          />
                        </div>
                      </div>
                    </div>
                  );
                })}

                {/* Base ring */}
                <div
                  aria-hidden="true"
                  className="absolute left-1/2 top-[92%] h-[2px] w-[260px] -translate-x-1/2 bg-gradient-to-r from-transparent via-[#22D3EE] to-transparent"
                  style={{
                    boxShadow:
                      '0 0 40px rgba(34,211,238,0.6), 0 0 80px rgba(255,45,85,0.35)',
                  }}
                />
              </div>
            </div>

          </div>

          {/* Right: interactive layer list */}
          <div
            className="relative"
            onMouseLeave={() => setActiveIndex(null)}
          >
            <div className="relative lg:h-[720px]">
              {HAOMTGV_LAYERS.map((layer, i) => {
                const isActive = activeIndex === i;
                return (
                  <div
                    key={layer.id}
                    tabIndex={0}
                    onMouseEnter={() => setActiveIndex(i)}
                    onFocus={() => setActiveIndex(i)}
                    onBlur={() => setActiveIndex(null)}
                    className="mb-5 grid grid-cols-[48px_40px_1fr] items-start gap-x-4 rounded-lg outline-none focus-visible:ring-2 focus-visible:ring-cyan-300/70 lg:absolute lg:mb-0"
                    style={{
                      top: i * SLAB_STEP,
                      transform: isActive ? 'translateX(6px)' : 'translateX(0)',
                      transition: 'transform 200ms ease-out',
                      animation: 'ls-hero-slide 0.5s ease-out backwards',
                      animationDelay: `${i * 80 + 120}ms`,
                    }}
                  >
                    <span
                      className="flex h-10 w-12 items-center justify-center rounded-md border text-sm font-bold transition-colors"
                      style={{
                        borderColor: isActive
                          ? 'rgba(34,211,238,0.7)'
                          : 'rgba(125,211,252,0.35)',
                        color: isActive ? '#E0FBFF' : '#A5F3FC',
                        background: 'rgba(5,11,26,0.55)',
                        boxShadow: isActive
                          ? '0 0 14px rgba(34,211,238,0.5), inset 0 0 10px rgba(34,211,238,0.25)'
                          : 'none',
                      }}
                    >
                      {layer.letter}
                    </span>
                    <layer.Icon
                      aria-hidden="true"
                      className="mt-2 h-5 w-5"
                      style={{
                        color: CYAN,
                        filter: 'drop-shadow(0 0 6px rgba(34,211,238,0.8))',
                      }}
                    />
                    <div>
                      <h2
                        className={`text-sm font-bold transition-colors ${
                          isActive ? 'text-white' : 'text-slate-200'
                        }`}
                      >
                        {layer.title}
                      </h2>
                      <p className="mt-1 text-sm leading-relaxed text-slate-400">
                        {layer.heroDescription}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        <p className="mt-12 text-xs tracking-[0.35em] text-slate-400 lg:absolute lg:right-16 lg:top-12 lg:mt-0">
          ASPIRE. ACT. ACHIEVE.
        </p>
      </div>
    </section>
  );
};
