import React from 'react';

interface LogoProps {
  variant?: 'icon' | 'full';
  size?: number;
  className?: string;
  theme?: 'light' | 'dark';
  showText?: boolean;
  instance?: 'first' | 'repeat';
}

const Logo: React.FC<LogoProps> = ({
  variant = 'full',
  size = 32,
  className = '',
  theme = 'dark',
  showText = false,
  instance = 'first',
}) => {
  const src = '/brand/logo/logo-favicon-transparent.png';
  const isFirst = instance === 'first';

  return (
    <div className={`inline-flex items-center gap-2.5 ${className}`}>
      <img
        src={src}
        alt={isFirst ? 'LightSpeed Holdings Limited™' : ''}
        width={size}
        height={size}
        className="object-contain shrink-0"
        data-ls-image-type="brand-mark"
        data-ls-logo-instance={instance}
        aria-hidden={!isFirst ? 'true' : undefined}
      />
      {showText && (
        <span className={`font-display font-black tracking-tight text-sm uppercase ${theme === 'light' ? 'text-[#070A40]' : 'text-white'}`}>
          LIGHTSPEED<span className="text-[#DC3641]"> HOLDINGS</span>
        </span>
      )}
    </div>
  );
};

export default Logo;
