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
  size = 36,
  className = '',
  theme = 'dark',
  instance = 'first',
}) => {
  const src = variant === 'icon' ? '/logo-icon.svg' : '/logo-full.svg';
  const isFirst = instance === 'first';

  return (
    <img
      src={src}
      alt={isFirst ? 'LightSpeed Holdings Limited' : ''}
      width={size}
      height={size}
      className={className}
      data-ls-image-type="brand-mark"
      data-ls-logo-instance={instance}
      aria-hidden={!isFirst ? 'true' : undefined}
      style={{ filter: theme === 'dark' ? 'none' : 'none' }}
    />
  );
};

export default Logo;