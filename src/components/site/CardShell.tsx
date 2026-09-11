import React from 'react';

interface CardShellProps {
  children: React.ReactNode;
  className?: string;
  screw?: boolean;
}

/**
 * Card shell shared by interior pages. Optional `screw` renders the hardware
 * corner fasteners used on chassis cards. Shell keeps borders/radii/theme
 * consistent; content owns spacing and typography.
 */
export const CardShell: React.FC<CardShellProps> = ({ children, className, screw = false }) => (
  <div className={`relative rounded-3xl p-6 sm:p-8 ${className ?? ''}`}>
    {screw && (
      <>
        <div className="absolute top-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
        <div className="absolute top-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
        <div className="absolute bottom-3 left-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
        <div className="absolute bottom-3 right-3 w-2 h-2 rounded-full hardware-screw" aria-hidden="true" />
      </>
    )}
    {children}
  </div>
);

export default CardShell;
