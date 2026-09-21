import React from 'react';
import {
  AreaChart as RechartsAreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { cn } from '@/lib/athena/utils';

interface AreaChartDataPoint {
  name: string;
  [key: string]: string | number;
}

interface AreaChartProps {
  data: AreaChartDataPoint[];
  keys: string[];
  colors: string[];
  height?: number;
  showGrid?: boolean;
  showXAxis?: boolean;
  showYAxis?: boolean;
  showTooltip?: boolean;
  className?: string;
  xKey?: string;
  stacked?: boolean;
  gradientOpacity?: [number, number];
}

export const AreaChart: React.FC<AreaChartProps> = ({
  data,
  keys,
  colors,
  height = 200,
  showGrid = false,
  showXAxis = true,
  showYAxis = false,
  showTooltip = true,
  className,
  xKey = 'name',
  stacked = false,
  gradientOpacity = [0.3, 0.05],
}) => {
  if (!data.length || !keys.length) {
    return (
      <div className={cn('h-[200px] flex items-center justify-center bg-ls-grey-light/50 rounded-xl border border-ls-grey-dark/30', className)}>
        <span className="font-body text-sm text-ls-grey-light-text">No data available</span>
      </div>
    );
  }

  const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: Array<{ value: number; name: string; color: string; payload: AreaChartDataPoint }>; label?: string }) => {
    if (!active || !payload || !payload.length) return null;

    return (
      <div className="bg-ls-white border border-ls-grey-dark/30 rounded-lg p-3 shadow-lg min-w-[160px]">
        <p className="font-display font-bold text-sm text-ls-navy mb-2">{label}</p>
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center gap-2 text-xs">
            <span
              className="w-2 h-2 rounded-full"
              style={{ backgroundColor: entry.color }}
            />
            <span className="font-body text-ls-grey-dark">{entry.name}:</span>
            <span className="font-display font-bold text-ls-navy">{entry.value.toLocaleString()}</span>
          </div>
        ))}
      </div>
    );
  };

  const CustomXAxis = ({ x, y, width, height, ticks }: { x: number; y: number; width: number; height: number; ticks: Array<{ value: string; coordinate: number }> }) => (
    <g transform={`translate(${x}, ${y})`}>
      {ticks.map((tick, index) => (
        <text
          key={index}
          x={tick.coordinate}
          y={height * 0.4}
          textAnchor="middle"
          fill="#9CA3AF"
          fontSize={11}
          fontFamily="Arial, sans-serif"
          fontWeight={500}
        >
          {tick.value}
        </text>
      ))}
    </g>
  );

  const CustomYAxis = ({ x, y, width, height, ticks }: { x: number; y: number; width: number; height: number; ticks: Array<{ value: string | number; coordinate: number }> }) => (
    <g transform={`translate(${x}, ${y})`}>
      {ticks.map((tick, index) => (
        <g key={index} transform={`translate(0, ${tick.coordinate})`}>
          {showGrid && (
            <line
              x1={0}
              x2={width}
              stroke="#E5E7EB"
              strokeDasharray="4 4"
            />
          )}
          <text
            x={-8}
            y={4}
            textAnchor="end"
            fill="#9CA3AF"
            fontSize={10}
            fontFamily="Arial, sans-serif"
          >
            {typeof tick.value === 'number' ? tick.value.toLocaleString() : tick.value}
          </text>
        </g>
      ))}
    </g>
  );

  return (
    <div className={cn('w-full', className)} style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsAreaChart
          data={data}
          margin={{ top: 8, right: 16, left: showYAxis ? 48 : 8, bottom: showXAxis ? 32 : 8 }}
        >
          <defs>
            {keys.map((key, index) => (
              <linearGradient
                key={key}
                id={`color-${key}`}
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop offset="0%" stopColor={colors[index % colors.length]} stopOpacity={gradientOpacity[0]} />
                <stop offset="100%" stopColor={colors[index % colors.length]} stopOpacity={gradientOpacity[1]} />
              </linearGradient>
            ))}
          </defs>

          {showGrid && (
            <CartesianGrid
              strokeDasharray="4 4"
              stroke="#E5E7EB"
              vertical={false}
              horizontal={true}
            />
          )}

          {showXAxis && <XAxis
            dataKey={xKey}
            tick={{ fill: '#9CA3AF', fontSize: 11, fontFamily: 'Arial, sans-serif', fontWeight: 500 }}
            axisLine={false}
            tickLine={false}
            dy={8}
            tickFormatter={(value) => value}
          />}

          {showYAxis && <YAxis
            tick={{ fill: '#9CA3AF', fontSize: 10, fontFamily: 'Arial, sans-serif' }}
            axisLine={false}
            tickLine={false}
            width={48}
            orientation="left"
            tickFormatter={(value) => value.toLocaleString()}
          />}

          {showTooltip && <Tooltip content={<CustomTooltip />} wrapperStyle={{ pointerEvents: 'none' }} />}

          {keys.map((key, index) => (
            <Area
              key={key}
              type="monotone"
              dataKey={key}
              stackId={stacked ? 'stack' : undefined}
              stroke={colors[index % colors.length]}
              strokeWidth={2}
              fillOpacity={1}
              fill={`url(#color-${key})`}
              isAnimationActive={true}
              animationDuration={800}
              animationEasing="ease"
            />
          ))}
        </RechartsAreaChart>
      </ResponsiveContainer>
    </div>
  );
};

// Mountain-style layered area chart specifically for ATS score distribution
export const MountainAreaChart: React.FC<{
  data: Array<{ range: string; count: number }>;
  height?: number;
  className?: string;
  colors?: string[];
}> = ({ data, height = 240, className, colors = ['#FF6B35', '#E63946', '#00BFFF'] }) => {
  if (!data.length) {
    return (
      <div className={cn('h-[240px] flex items-center justify-center bg-ls-grey-light/50 rounded-xl border border-ls-grey-dark/30', className)}>
        <span className="font-body text-sm text-ls-grey-light-text">No ATS score data</span>
      </div>
    );
  }

  // Create layered data for mountain effect
  const maxCount = Math.max(...data.map(d => d.count));
  const layers = 3;

  const layeredData = data.map((point, i) => ({
    name: point.range,
    base: point.count,
    layer1: point.count * 0.8,
    layer2: point.count * 0.5,
    layer3: point.count * 0.2,
  }));

  return (
    <div className={cn('w-full', className)} style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsAreaChart data={layeredData} margin={{ top: 8, right: 16, left: 8, bottom: 32 }}>
          <defs>
            {colors.map((color, index) => (
              <linearGradient
                key={color}
                id={`mountain-${index}`}
                x1="0"
                y1="0"
                x2="0"
                y2="1"
              >
                <stop offset="0%" stopColor={color} stopOpacity={0.4 - index * 0.1} />
                <stop offset="100%" stopColor={color} stopOpacity={0.05} />
              </linearGradient>
            ))}
          </defs>

          <CartesianGrid strokeDasharray="4 4" stroke="#E5E7EB" vertical={false} horizontal={true} />

          <XAxis
            dataKey="name"
            tick={{ fill: '#9CA3AF', fontSize: 11, fontFamily: 'Arial, sans-serif', fontWeight: 500 }}
            axisLine={false}
            tickLine={false}
            dy={8}
          />

          <YAxis
            tick={{ fill: '#9CA3AF', fontSize: 10, fontFamily: 'Arial, sans-serif' }}
            axisLine={false}
            tickLine={false}
            width={40}
            orientation="left"
            tickFormatter={(value) => value >= 1000 ? `${(value/1000).toFixed(1)}k` : value}
            domain={[0, 'dataMax + 10%']}
          />

          <Tooltip
            content={({ active, payload, label }) => {
              if (!active || !payload) return null;
              return (
                <div className="bg-ls-white border border-ls-grey-dark/30 rounded-lg p-3 shadow-lg">
                  <p className="font-display font-bold text-sm text-ls-navy mb-2">ATS Range: {label}</p>
                  {payload.map((entry, index) => (
                    <div key={index} className="flex items-center gap-2 text-xs">
                      <span className="w-2 h-2 rounded-full" style={{ backgroundColor: colors[index % colors.length] }} />
                      <span className="font-body text-ls-grey-dark">Layer {index + 1}:</span>
                      <span className="font-display font-bold text-ls-navy">{Math.round(typeof entry.value === 'number' ? entry.value : 0).toLocaleString()}</span>
                    </div>
                  ))}
                </div>
              );
            }}
            wrapperStyle={{ pointerEvents: 'none' }}
          />

          {/* Draw layers from back to front for mountain effect */}
          {['layer3', 'layer2', 'layer1', 'base'].map((key, index) => (
            <Area
              key={key}
              type="monotone"
              dataKey={key}
              stroke={colors[Math.min(index, colors.length - 1)]}
              strokeWidth={index === 3 ? 2 : 1}
              fillOpacity={1}
              fill={`url(#mountain-${Math.min(index, colors.length - 1)})`}
              isAnimationActive={true}
              animationDuration={1000}
              animationEasing="ease"
            />
          ))}
        </RechartsAreaChart>
      </ResponsiveContainer>
    </div>
  );
};

// Circular gauge chart for ATS score
export const CircularGaugeChart: React.FC<{
  value: number;
  size?: number;
  strokeWidth?: number;
  colors?: string[];
  showValue?: boolean;
  className?: string;
}> = ({ value, size = 120, strokeWidth = 12, colors = ['#FF6B35', '#E63946'], showValue = true, className }) => {
  const clampedValue = Math.max(0, Math.min(100, value));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - clampedValue / 100);

  const gradientId = `gauge-gradient-${Math.random().toString(36).slice(2)}`;

  return (
    <div className={cn('relative inline-flex', className)} style={{ width: size, height: size }}>
      <svg width={size} height={size} className="transform -rotate-90">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor={colors[0]} />
            <stop offset="100%" stopColor={colors[1]} />
          </linearGradient>
        </defs>

        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#E5E7EB"
          strokeWidth={strokeWidth}
          fill="none"
        />

        {/* Progress */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={`url(#${gradientId})`}
          strokeWidth={strokeWidth}
          fill="none"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className="transition-all duration-1000 ease-out"
          style={{ filter: 'drop-shadow(0 4px 8px rgba(230, 57, 70, 0.3))' }}
        />
      </svg>

      {showValue && (
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className="font-display font-black text-ls-navy" style={{ fontSize: size * 0.28 }}>
            {Math.round(clampedValue)}
          </span>
          <span className="font-body text-xs font-medium text-ls-grey-dark">
            ATS Score
          </span>
        </div>
      )}
    </div>
  );
};
