import React from 'react';
import { Link } from 'react-router-dom';
import { CategoryChip } from './CategoryChip';

/**
 * ArticleCard — Pharos teaser card.
 *
 * Mirrors the `ArticleCard` record exported by `src/data/homeCopy.ts`
 * (`title` / `excerpt` / `category` / `slug` / `readTime`) so the homepage copy
 * stays the single source of truth. Colours come from the brand palette in
 * `brand/tokens/brand-tokens.json` only.
 */
export interface ArticleCardProps {
  title: string;
  excerpt: string;
  category: string;
  slug: string;
  readTime: string;
  imageUrl?: string;
  theme: 'light' | 'dark';
}

export const ArticleCard: React.FC<ArticleCardProps> = ({
  title,
  excerpt,
  category,
  slug,
  readTime,
  imageUrl,
  theme,
}) => {
  const isLight = theme === 'light';

  return (
    <article
      className={`flex h-full flex-col overflow-hidden rounded-2xl border transition-shadow hover:shadow-lg ${
        isLight
          ? 'bg-ls-white border-ls-grey-dark/20'
          : 'bg-ls-navy/80 border-ls-white/15'
      }`}
    >
      {imageUrl && (
        <img src={imageUrl} alt="" className="h-48 w-full object-cover" />
      )}

      <div className="flex flex-1 flex-col gap-3 p-5">
        <CategoryChip category={category} theme={theme} />

        <h3
          className={`font-display font-bold text-lg leading-snug tracking-tight line-clamp-2 ${
            isLight ? 'text-ls-navy' : 'text-ls-white'
          }`}
        >
          {title}
        </h3>

        <p
          className={`text-sm leading-relaxed line-clamp-3 ${
            isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
          }`}
        >
          {excerpt}
        </p>

        <div className="mt-auto flex items-center justify-between gap-3 pt-2">
          <span
            className={`text-[11px] font-bold uppercase tracking-widest ${
              isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
            }`}
          >
            {readTime}
          </span>
          <Link
            to={`/insights/${slug}`}
            className="text-[11px] font-bold uppercase tracking-widest text-ls-red transition-colors hover:text-ls-red/80"
          >
            Read article
          </Link>
        </div>
      </div>
    </article>
  );
};
