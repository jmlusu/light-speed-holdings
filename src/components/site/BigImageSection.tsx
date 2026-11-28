import React from 'react';

interface BigImageSectionProps {
  src: string;
  alt: string;
  caption?: string;
  theme: 'light' | 'dark';
  height?: string;
}

export const BigImageSection: React.FC<BigImageSectionProps> = ({
  src,
  alt,
  caption,
  theme,
  height = 'h-[48vh] sm:h-[56vh] lg:h-[64vh]',
}) => {
  const isLight = theme === 'light';
  return (
    <section
      className={`relative w-full overflow-hidden ${height}`}
      aria-label={alt}
    >
      <img
        src={src}
        alt={alt}
        loading="lazy"
        className="absolute inset-0 w-full h-full object-cover object-center"
      />
      <div
        className={`absolute inset-0 ${
          isLight
            ? 'bg-gradient-to-t from-[#F7F8F9]/70 via-transparent to-transparent'
            : 'bg-gradient-to-t from-[#0A0D14]/75 via-transparent to-transparent'
        }`}
        aria-hidden="true"
      />
      {caption && (
        <div className="absolute bottom-6 left-6 right-6 z-10 max-w-3xl">
          <p
            className={`text-sm sm:text-base font-medium ${
              isLight ? 'text-ls-navy' : 'text-white'
            }`}
          >
            {caption}
          </p>
        </div>
      )}
    </section>
  );
};

export default BigImageSection;
