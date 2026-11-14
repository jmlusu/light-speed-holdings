import React from 'react';

import { SectionHeading } from './site/SectionHeading';

interface CarouselItem {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  category: string;
  readTime?: string;
  image?: string;
  badge?: string;
  linkText?: string;
  onClick?: () => void;
}

interface ContentCarouselProps {
  theme: 'light' | 'dark';
  title: string;
  subtitle: string;
  lead?: string;
  items: CarouselItem[];
  onItemClick?: (item: CarouselItem) => void;
}

export const ContentCarousel: React.FC<ContentCarouselProps> = ({
  theme,
  title,
  subtitle,
  lead,
  items,
  onItemClick,
}) => {
  const isLight = theme === 'light';
  return (
    <section className={`py-[100px] px-6 lg:px-12 relative overflow-hidden transition-colors ${
      isLight ? 'bg-ls-grey-light text-ls-navy' : 'bg-[#1A1D21] text-white'
    }`}>
      <div className="max-w-7xl mx-auto w-full">
        <SectionHeading
          theme={theme}
          eyebrow={subtitle}
          title={title}
          lead={lead}
        />

        {/* Grid Container */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {items.map((item) => (
            <div
              key={item.id}
              onClick={() => onItemClick && onItemClick(item)}
              className="rounded-2xl overflow-hidden flex flex-col justify-between transition-all duration-300 group cursor-pointer shadow-none bg-transparent border-none"
            >
              {item.image && (
                <div className="h-40 overflow-hidden relative">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                  />
                  <div className={`absolute inset-0 bg-gradient-to-t ${isLight ? 'from-ls-white' : 'from-[#070A40]/90'} to-transparent`} />
                </div>
              )}
              <div className="p-6 flex-1 flex flex-col">
                {/* Category & Badge */}
                <div className="flex items-center justify-between text-xs mb-3">
                  <span className={`font-semibold uppercase tracking-wider text-[11px] ${isLight ? 'text-ls-navy' : 'text-[#00BFFF]'}`}>
                    {item.category}
                  </span>
                  {item.badge && (
                    <span className="px-2.5 py-1 rounded font-medium text-[11px] bg-[#DC3641]/10 text-[#DC3641] border-none">
                      {item.badge}
                    </span>
                  )}
                  {item.readTime && <span className={`${isLight ? 'text-ls-grey-dark' : 'text-[#9CA3AF]'} text-xs`}>{item.readTime}</span>}
                </div>

                <h3 className={`text-xl font-bold transition-colors mb-2 ${isLight ? 'text-ls-navy group-hover:text-[#DC3641]' : 'text-white group-hover:text-[#00BFFF]'}`}>
                  {item.title}
                </h3>

                <p className={`text-xs font-medium mb-3 ${isLight ? 'text-ls-grey-dark' : 'text-[#9CA3AF]'}`}>
                  {item.subtitle}
                </p>

                <p className={`text-sm leading-relaxed line-clamp-3 mb-6 ${isLight ? 'text-ls-grey-dark' : 'text-[#9CA3AF]'}`}>
                  {item.description}
                </p>

                <div className={`mt-auto pt-4 flex items-center justify-between text-xs font-semibold group-hover:translate-x-1 transition-transform ${isLight ? 'text-ls-navy' : 'text-[#00BFFF]'}`}>
                  <span>{item.linkText || 'Explore Detail'}</span>
                  <span>→</span>
                </div>
              </div>
            </div>
          ))}
        </div>

      </div>
    </section>
  );
};
