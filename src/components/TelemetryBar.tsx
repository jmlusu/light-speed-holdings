import React, { useEffect, useState } from 'react';

interface TelemetryBarProps {
  className?: string;
  variant?: 'top-ticker' | 'section-footer' | 'inline';
  customNode?: string;
}

export const TelemetryBar: React.FC<TelemetryBarProps> = ({
  className = '',
  variant = 'top-ticker',
  customNode = 'ACTIVE // LILONGWE-CORE'
}) => {
  const [timeString, setTimeString] = useState<string>('');
  const [latency, setLatency] = useState<number>(12);

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const year = now.getUTCFullYear();
      const month = String(now.getUTCMonth() + 1).padStart(2, '0');
      const day = String(now.getUTCDate()).padStart(2, '0');
      const hours = String(now.getUTCHours()).padStart(2, '0');
      const mins = String(now.getUTCMinutes()).padStart(2, '0');
      const secs = String(now.getUTCSeconds()).padStart(2, '0');
      setTimeString(`${year}.${month}.${day} — ${hours}:${mins}:${secs} UTC`);
    };

    updateTime();
    const timer = setInterval(updateTime, 1000);
    const latencyTimer = setInterval(() => {
      setLatency(11 + Math.floor(Math.random() * 3));
    }, 4000);

    return () => {
      clearInterval(timer);
      clearInterval(latencyTimer);
    };
  }, []);

  return (
    <div
      className={`w-full bg-[#0a0f14] border-b border-[#1e2d3d] text-[10px] font-mono text-[#5a6a78] select-none py-1.5 px-4 sm:px-6 lg:px-8 flex flex-wrap items-center justify-between gap-y-1 gap-x-4 ${className}`}
      data-telemetry-layer
    >
      {/* Left indicators */}
      <div className="flex items-center gap-3 sm:gap-5 flex-wrap">
        <div className="flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 bg-[#4ecdc4] block" />
          <span className="text-[#a0aab4]">SYS:</span>
          <span className="text-[#4ecdc4] font-bold">ONLINE</span>
        </div>

        <div className="hidden xs:flex items-center gap-1.5">
          <span className="text-[#5a6a78]">LAT:</span>
          <span className="text-[#f0f0f0] font-bold">{latency}ms</span>
        </div>

        <div className="hidden md:flex items-center gap-1.5">
          <span className="text-[#5a6a78]">NODE:</span>
          <span className="text-[#2a6b7c] font-bold">{customNode}</span>
        </div>

        <div className="hidden lg:flex items-center gap-1.5">
          <span className="text-[#5a6a78]">SYNC:</span>
          <span className="text-[#4ecdc4]">98.7%</span>
        </div>

        <div className="hidden xl:flex items-center gap-1.5">
          <span className="text-[#5a6a78]">UPTIME:</span>
          <span className="text-[#a0aab4]">14d 07h 22m</span>
        </div>
      </div>

      {/* Center Mini Sparkline (Sharp 1px bars) */}
      <div className="hidden sm:flex items-center gap-1">
        <span className="text-[9px] uppercase tracking-wider text-[#5a6a78] mr-1.5">TELEMETRY</span>
        <div className="flex items-end gap-[2px] h-3">
          {[4, 7, 5, 9, 6, 11, 8, 12, 7, 10, 8, 11, 9, 12, 10].map((h, i) => (
            <div
              key={i}
              style={{ height: `${h}px` }}
              className={`w-[2px] ${i >= 12 ? 'bg-[#4ecdc4]' : i >= 8 ? 'bg-[#2a6b7c]' : 'bg-[#1e2d3d]'}`}
            />
          ))}
        </div>
      </div>

      {/* Right Live UTC Clock */}
      <div className="flex items-center gap-2 ml-auto sm:ml-0">
        <span className="w-1.5 h-1.5 bg-[#c9a96e] block" />
        <span className="text-[#f0f0f0] font-medium tracking-wider">
          {timeString || '2026.11.04 — 12:55:20 UTC'}
        </span>
      </div>
    </div>
  );
};

export default TelemetryBar;
