/**
 * cn Utility — clsx + tailwind-merge
 *
 * Combines classnames conditionally and merges Tailwind classes
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
