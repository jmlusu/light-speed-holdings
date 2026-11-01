import React from 'react';
import { ArrowRight } from 'lucide-react';
import { cn } from '@lightspeed/design-system/utils/cn';

export interface ArrowLinkProps {
  to: string | ((e: React.MouseEvent) => void);
  children: React.ReactNode;
  className?: string;
}

export const ArrowLink: React.FC<ArrowLinkProps> = ({ to, children, className }) => {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    if (typeof to === 'function') {
      to(e);
    } else {
      window.location.href = to;
    }
  };

  return (
    <a
      href="#"
      onClick={handleClick}
      className={cn(
        'flex items-center gap-1 text-ls-red transition-colors hover:underline',
        className
      )}
    >
      {children}
      <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
    </a>
  );
};