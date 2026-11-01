import React from 'react';
import { StatBlock } from './StatBlock';

export interface BandStat {
  value: string | number;
  label: string;
}

interface AfricaStatBandProps {
  heading: string;
  body: string;
  stats: BandStat[];
  className?: string;
}

/** Africa outline — single stroked path (no fill) so it reads as a line drawing. */
const AFRICA_PATH =
  'M41 14 Q60 4 83 8 Q97 18 105 30 Q120 24 133 28 L140 32 Q146 50 151 65 Q160 76 168 85 ' +
  'Q180 86 188 87 Q180 102 172 117 Q164 126 158 135 Q157 140 157 144 Q159 157 160 169 ' +
  'Q152 178 146 184 Q142 194 140 203 Q138 210 136 215 Q120 226 108 229 Q105 228 104 227 ' +
  'Q98 210 94 193 Q91 170 90 150 Q88 146 87 141 Q82 131 80 122 Q80 116 81 111 Q72 107 65 103 ' +
  'Q60 105 56 106 Q50 107 46 107 Q33 103 22 97 Q16 88 12 78 Q14 72 15 68 Q13 64 13 59 ' +
  'Q22 44 32 30 Q36 21 41 14 Z';

const MADAGASCAR_PATH =
  'M176 160 Q184 156 185 166 Q187 178 183 190 Q180 202 175 196 Q171 186 172 178 Q171 166 176 160 Z';

/**
 * Dark band closing the page: outlined Africa, positioning statement, and the
 * operating-model figures (passed in from the metrics registry by the page).
 */
export const AfricaStatBand: React.FC<AfricaStatBandProps> = ({ heading, body, stats, className }) => (
  <section className={`bg-ls-navy ${className ?? ''}`}>
    <div className="mx-auto grid w-full max-w-7xl grid-cols-1 items-center gap-10 px-4 py-14 sm:px-8 sm:py-16 lg:grid-cols-12 lg:gap-8 lg:px-10">
      <div className="order-1 lg:col-span-3">
        <svg
          viewBox="0 0 200 240"
          role="img"
          aria-label="Outline map of Africa with Malawi marked"
          className="mx-auto h-40 w-auto text-ls-cyan/60 sm:h-48 lg:mx-0"
        >
          <path d={AFRICA_PATH} fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
          <path d={MADAGASCAR_PATH} fill="none" stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
          <circle cx="145" cy="164" r="6" fill="none" stroke="currentColor" strokeWidth="1" opacity="0.55" />
          <circle cx="145" cy="164" r="2.4" fill="currentColor" />
        </svg>
      </div>

      <div className="order-2 lg:col-span-5">
        <h2 className="font-display text-xl font-bold leading-snug tracking-tight text-ls-cyan sm:text-2xl">
          {heading}
        </h2>
        <p className="mt-3 max-w-md text-[13px] leading-relaxed text-ls-white/70">{body}</p>
      </div>

      <div className="order-3 grid grid-cols-3 gap-6 border-t border-ls-white/10 pt-8 lg:col-span-4 lg:gap-0 lg:border-t-0 lg:pt-0">
        {stats.map((stat, index) => (
          <div
            key={stat.label}
            className={index > 0 ? 'lg:border-l lg:border-ls-white/15 lg:pl-8' : 'lg:pr-4'}
          >
            <StatBlock value={stat.value} label={stat.label} mode="dark" />
          </div>
        ))}
      </div>
    </div>
  </section>
);

export default AfricaStatBand;
