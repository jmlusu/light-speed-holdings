import React from 'react';

export type Icon3DName =
  // 9 Canonical Reference Icons from image_89d7c5fd.png
  | 'pen'
  | 'edit'
  | 'finance'
  | 'coins'
  | 'revenue'
  | 'safe'
  | 'security'
  | 'vault'
  | 'folder'
  | 'documents'
  | 'records'
  | 'trash'
  | 'delete'
  | 'archive'
  | 'star'
  | 'favorite'
  | 'value'
  | 'rating'
  | 'chart'
  | 'analytics'
  | 'statistics'
  | 'dashboard'
  | 'home'
  | 'house'
  | 'building'
  | 'property'
  | 'notepad'
  | 'notebook'
  | 'tasks'
  | 'reports'
  // Extended Enterprise AI System Icons
  | 'intelligence'
  | 'brain'
  | 'orchestration'
  | 'workflow'
  | 'governance'
  | 'compliance'
  | 'memory'
  | 'database'
  | 'tools'
  | 'wrench'
  | 'settings'
  | 'administration'
  | 'users'
  | 'organizations'
  | 'human'
  | 'registration'
  | 'verification'
  | 'notifications'
  | 'activity'
  | 'search'
  | 'filtering'
  | 'support'
  | 'help'
  | 'approvals'
  | 'categories'
  | 'sectors'
  | 'location'
  | 'geography'
  | 'calendar'
  | 'history'
  | 'target'
  | 'mission'
  | 'lightning'
  | 'speed'
  | 'network'
  | 'connected'
  | 'compass'
  | 'direction'
  | 'microscope'
  | 'policy-shield'
  | 'system-map'
  | 'africa-map'
  | 'brand-emblem';

export type Icon3DSize = 'xs' | 'sm' | 'md' | 'lg' | 'hero' | number;

export interface Icon3DProps {
  name: Icon3DName;
  size?: Icon3DSize;
  className?: string;
  alt?: string;
  isInteractive?: boolean;
}

export const getPixelSize = (size: Icon3DSize = 'md'): number => {
  if (typeof size === 'number') return size;
  switch (size) {
    case 'xs':
      return 18;
    case 'sm':
      return 24;
    case 'md':
      return 48;
    case 'lg':
      return 64;
    case 'hero':
      return 96;
    default:
      return 48;
  }
};
