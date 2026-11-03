import { CategoryChip } from './CategoryChip';
import { CtaBand } from '../components/site/CtaBand';

/**
 * ArticleCard - A card displaying an article with title, description, and CTA.
 * Uses library tokens and components only.
 */
export interface ArticleCardProps {
  title: string;
  description: string;
  category: string;
  ctaText: string;
  ctaUrl: string;
  imageUrl?: string;
  theme: 'light' | 'dark';
  onRequestBriefing?: (summary?: string) => void;
}

export const ArticleCard: React.FC<ArticleCardProps> = ({
  title,
  description,
  category,
  ctaText,
  ctaUrl,
  imageUrl,
  theme,
}) => {
  return (
    <article className="bg-ls-white rounded-lg overflow-hidden shadow-sm border-y border-ls-navy/10 hover:shadow-md transition-shadow duration-200 max-w-sm mx-auto">
      {imageUrl && <img src={imageUrl} alt={title} className="w-full h-48 object-cover" />}
      <div className="p-5">
        <h3 className="text-ls-heading-lg font-semibold text-ls-navy mb-2 line-clamp-2">{title}</h3>
        <p className="text-ls-body-sm text-ls-teal line-clamp-3">{description}</p>
        <CategoryChip category={category} theme={theme} />
        <CtaBand
          theme={theme}
          text={ctaText}
          ctaTo={ctaUrl}
        />
      </div>
    </article>
  );
};