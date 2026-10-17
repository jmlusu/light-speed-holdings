import React from 'react';
import { Link } from 'react-router-dom';

export interface RelatedLink {
  to: string;
  label: string;
}

interface RelatedLinksProps {
  theme: 'light' | 'dark';
  links: RelatedLink[];
}

/**
 * Shared related-content strip for interior pages. Keeps IA navigation
 * consistent (ADR-020 P3) without per-page ad-hoc Link markup.
 */
export const RelatedLinks: React.FC<RelatedLinksProps> = ({ theme, links }) => {
  if (!links.length) return null;
  const isLight = theme === 'light';

  return (
    <nav
      className="px-4 sm:px-8 max-w-7xl mx-auto w-full py-8"
      aria-label="Related sections"
    >
      <p
        className={`text-xs font-bold tracking-widest uppercase ${
          isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
        }`}
      >
        Related:{' '}
        {links.map((link, index) => (
          <React.Fragment key={link.to}>
            {index > 0 && <span aria-hidden="true"> · </span>}
            <Link to={link.to} className="text-ls-red hover:underline">
              {link.label}
            </Link>
          </React.Fragment>
        ))}
      </p>
    </nav>
  );
};

export default RelatedLinks;
